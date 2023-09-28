import json
import multiprocessing
import time
from typing import List, Dict
from utils.logger import Logger
import nmap

from config import COMMON_PORTS


class NetworkScanner:
    """
    Сlass for performing network scans using nmap.
    """

    def __init__(self, target_subnets: List[str]):
        self.target_subnets = target_subnets
        self.results_queue = multiprocessing.Queue()
        with open(COMMON_PORTS) as f:
            self.ports = json.load(f)
        self.top_ports = 300
        self.logger = Logger(__name__).get_logger()

    def extract_port_info(self, scanned_host: str, protocol_type: str, port_number: int, scan_data: Dict) -> Dict:
        """
        Extracts information for a scanned port.

        Args:
            scanned_host (str): IP address of the scanned host.
            protocol_type (str): Protocol type, e.g., 'tcp'.
            port_number (int): Port number being scanned.
            scan_data (dict): Scan data returned from nmap scan.

        Returns:
            dict: A dictionary containing port information.
        """
        self.logger.info(f"Extracting port info for {scanned_host}, {protocol_type}, {port_number}")
        protocol_data = scan_data[protocol_type][port_number]
        port_info = {'host': scanned_host, 'protocol': protocol_type, 'port': port_number}
        if protocol_data['state'] != 'open':
            return None
        for key in ['name', 'product', 'version', 'script']:
            if key in protocol_data:
                port_info[key] = protocol_data[key]

        return port_info

    def scan_range(self, subnet_address: str, start_port: int, end_port: int):
        """
        Scans a range of ports on a subnet.

        Args:
            subnet_address (str): The address of the subnet to be scanned.
            start_port (int): The starting port number.
            end_port (int): The ending port number.
        """
        self.logger.info(f"Scanning range {start_port}-{end_port} on subnet {subnet_address}")
        port_scanner = nmap.PortScanner()
        ports_enumeration = ",".join(self.ports[start_port:end_port + 1])
        port_scanner.scan(hosts=subnet_address, arguments='-sV -T4 -sT --script=discovery -p' + ports_enumeration)

        for scanned_host in port_scanner.all_hosts():
            for protocol_type in port_scanner[scanned_host].all_protocols():
                if protocol_type != "tcp":
                    continue

                for port_number in port_scanner[scanned_host][protocol_type].keys():
                    port_info = self.extract_port_info(scanned_host, protocol_type, port_number,
                                                       port_scanner[scanned_host])
                    if port_info:
                        self.results_queue.put(port_info)

    def _create_processes(self, subnet_address: str, cpu_count: int, port_range: int, last_port: int) -> List:
        """
        Creates and starts a list of processes to scan a subnet.

        Args:
            subnet_address (str): The address of the subnet to be scanned.
            cpu_count (int): Number of CPU cores available.
            port_range (int): Range of ports to be scanned per process.
            last_port (int): The last port in the range to be scanned.

        Returns:
            list: List of created and started multiprocessing.Process objects.
        """
        processes = []
        for i in range(cpu_count):
            start_port = i * port_range
            end_port = (i + 1) * port_range if i < cpu_count - 1 else last_port
            p = multiprocessing.Process(target=self.scan_range, args=(subnet_address, start_port, end_port))
            processes.append(p)
            p.start()
        return processes

    def _yield_results(self, processes: List) -> Dict:
        """
        Yields results from the results_queue as they become available.

        Args:
            processes (list): List of multiprocessing.Process objects.

        Yields:
            dict: Port information dictionary from the results_queue.
        """
        while processes:
            while not self.results_queue.empty():
                yield self.results_queue.get()

            for p in processes[:]:
                if not p.is_alive():
                    processes.remove(p)
                    while not self.results_queue.empty():
                        yield self.results_queue.get()

            time.sleep(1)

    def execute_scan(self) -> Dict:
        """
        Executes the scanning, evently distributing the ports to be scanned among CPU cores.

        Yields:
            dict: Port information dictionary from the results_queue.
        """
        cpu_count = multiprocessing.cpu_count()
        port_range = self.top_ports // cpu_count

        self.logger.info(f"Starting the scanning process with {cpu_count} processes...")

        for subnet_address in self.target_subnets:
            processes = self._create_processes(subnet_address, cpu_count, port_range, self.top_ports)
            yield from self._yield_results(processes)

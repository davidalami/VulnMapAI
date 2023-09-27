import nmap
import multiprocessing
import time
from config import COMMON_PORTS
import json


class NetworkScanner:
    def __init__(self, target_subnets):
        self.target_subnets = target_subnets
        self.results_queue = multiprocessing.Queue()
        with open(COMMON_PORTS) as f:
            self.ports = json.load(f)
        self.top_ports = 300

    def extract_port_info(self, scanned_host, protocol_type, port_number, scan_data):
        protocol_data = scan_data[protocol_type][port_number]
        port_info = {'host': scanned_host, 'protocol': protocol_type, 'port': port_number}
        if protocol_data['state'] != 'open':
            return None
        for key in ['name', 'product', 'version', 'script']:
            if key in protocol_data:
                port_info[key] = protocol_data[key]

        return port_info

    def scan_range(self, subnet_address, start_port, end_port):
        port_scanner = nmap.PortScanner()
        ports_enumeration = ",".join(self.ports[start_port:end_port+1])
        port_scanner.scan(hosts=subnet_address, arguments='-sV -T4 -sT --script=discovery -p'+ports_enumeration)

        for scanned_host in port_scanner.all_hosts():
            for protocol_type in port_scanner[scanned_host].all_protocols():
                if protocol_type != "tcp":
                    continue

                for port_number in port_scanner[scanned_host][protocol_type].keys():
                    port_info = self.extract_port_info(scanned_host, protocol_type, port_number, port_scanner[scanned_host])
                    if port_info:
                        self.results_queue.put(port_info)

    def _create_processes(self, subnet_address, cpu_count, port_range, last_port):
        processes = []
        for i in range(cpu_count):
            start_port = i * port_range
            end_port = (i + 1) * port_range if i < cpu_count - 1 else last_port
            p = multiprocessing.Process(target=self.scan_range, args=(subnet_address, start_port, end_port))
            processes.append(p)
            p.start()
        return processes

    def _yield_results(self, processes):
        while processes:
            while not self.results_queue.empty():
                yield self.results_queue.get()

            for p in processes[:]:
                if not p.is_alive():
                    processes.remove(p)
                    while not self.results_queue.empty():
                        yield self.results_queue.get()

            time.sleep(1)

    def execute_scan(self):
        cpu_count = multiprocessing.cpu_count()
        port_range = self.top_ports // cpu_count

        print(f"Starting the scanning process with {cpu_count} processes...")

        for subnet_address in self.target_subnets:
            processes = self._create_processes(subnet_address, cpu_count, port_range, self.top_ports)
            yield from self._yield_results(processes)

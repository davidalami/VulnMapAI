import nmap
import time
import json

class NetworkScanner:
    def __init__(self, target_subnets, logging_filename):
        self.target_subnets = target_subnets
        self.logging_filename = logging_filename
        self.port_scanner = nmap.PortScanner()

    def extract_port_info(self, scanned_host, protocol_type, port_number):
        """Extract relevant port information from a scanned host."""
        port_info = {
            'host': scanned_host,
            'protocol': protocol_type,
            'port': port_number,
        }

        protocol_data = self.port_scanner[scanned_host][protocol_type][port_number]
        print(protocol_data)

        if 'name' in protocol_data:
            port_info['service'] = protocol_data['name']

        if 'state' in protocol_data:
            port_info['state'] = protocol_data['state']

        if 'product' in protocol_data:
            port_info['product'] = protocol_data['product']
        if 'version' in protocol_data:
            port_info['version'] = protocol_data['version']

        if 'script' in protocol_data:
            port_info['discovery_output'] = protocol_data['script']

        return port_info

    def perform_scan_on_subnet(self, subnet_address):
        """Scan a given subnet and return results."""
        self.port_scanner.scan(hosts=subnet_address, ports='1-65535', arguments='-sV -T4 -sT  --script=discovery')
        scan_results = []

        for scanned_host in self.port_scanner.all_hosts():
            for protocol_type in self.port_scanner[scanned_host].all_protocols():
                if protocol_type not in ["tcp", "udp"]:
                    continue

                sorted_ports = sorted(self.port_scanner[scanned_host][protocol_type].keys())

                for port_number in sorted_ports:
                    port_info = self.extract_port_info(scanned_host, protocol_type, port_number)
                    scan_results.append(port_info)

        return scan_results

    def record_scan_results_to_file(self, scan_results):
        with open(self.logging_filename, "a") as log_file:
            for result_entry in scan_results:
                log_file.write(json.dumps(result_entry))
                log_file.write("\n")

    def execute_scan_and_log(self):
        print("Starting the scanning process...")
        for subnet_address in self.target_subnets:
            scan_results = self.perform_scan_on_subnet(subnet_address)
            self.record_scan_results_to_file(scan_results)
            time.sleep(1)

# Usage
target_subnets = ['metasploitable']
logging_filename = "detailed_scan_log.log"
network_scanner_instance = NetworkScanner(target_subnets, logging_filename)
network_scanner_instance.execute_scan_and_log()

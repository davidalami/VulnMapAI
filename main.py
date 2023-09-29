import argparse
from orchestration.pentest import PenetrationTester


def main(targets, top_ports):
    pentester = PenetrationTester(targets, top_ports)
    pentester.scan_and_report()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run penetration tests on the given target subnets.')

    # Targets Argument
    parser.add_argument('targets', nargs='+', help='List of target subnets.')

    # Top Ports Argument
    parser.add_argument('-p', '--top_ports', type=int, default=300, help='Number of most common ports to scan.')

    # Parse the arguments
    args = parser.parse_args()

    # Validate top_ports
    if args.top_ports < 1:
        parser.error("top_ports must be a positive integer.")

    # Maximum limit of top_ports
    if args.top_ports > 8367:
        parser.error("top_ports must be less than or equal to 8367.")

    # Run the main function with parsed arguments
    main(args.targets, args.top_ports)

import argparse

from orchestration.pentest import PenetrationTester
from webapp.app import app


def main(targets, top_ports, authorized_modules):
    pentester = PenetrationTester(targets, top_ports, authorized_modules)
    pentester.scan_and_report()
    app.run(debug=False, host='0.0.0.0', port=1337)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run penetration tests on the given target subnets.')

    # Targets Argument
    parser.add_argument('targets', nargs='+', help='List of target subnets.')

    # Top Ports Argument
    parser.add_argument('-p', '--top_ports', type=int, default=300, help='Number of most common ports to scan.')

    # Active exploitation is opt-in: each flag authorizes one Metasploit module path to actually run.
    # Without any, the tool only ranks and reports candidate exploits and never launches one.
    parser.add_argument('--authorize-module', action='append', dest='authorized_modules', metavar='MODULE_PATH',
                        help='Authorize a Metasploit module path for active exploitation (repeatable).')

    # Parse the arguments
    args = parser.parse_args()

    # Validate top_ports
    if args.top_ports < 1:
        parser.error("top_ports must be a positive integer.")

    # Maximum limit of top_ports
    if args.top_ports > 8367:
        parser.error("top_ports must be less than or equal to 8367.")

    # Run the main function with parsed arguments
    main(args.targets, args.top_ports, args.authorized_modules)

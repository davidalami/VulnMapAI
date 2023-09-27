import argparse
from orchestration.pentest import PenetrationTester


def main(targets):
    pentester = PenetrationTester(targets)
    pentester.scan_and_report()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run penetration tests on the given target subnets.')
    parser.add_argument('targets', nargs='+', help='List of target subnets')
    args = parser.parse_args()
    
    main(args.targets)

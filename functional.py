

import argparse
from utils.session import Session

from mainpage_nav1 import MainPage_Navigation1
from mainpage_nav2 import MainPage_Navigation2
from mainpage_nav3 import MainPage_Navigation3


# Create the parser
parser = argparse.ArgumentParser(
    description="Example script with arguments.")

# Add arguments
parser.add_argument("--url", type=str, required=True,
                    help="Endpoint URL to test")
parser.add_argument("--headless", action="store_true",
                    help="Run in headless mode")

# Parse the arguments
args = parser.parse_args()

# Use the arguments
print("Endpoint:", args.url)
print("Headless:", args.headless)

with Session(domain=args.url, headless=args.headless) as sn:
    MainPage_Navigation1(**sn.confs).close()
    MainPage_Navigation2(**sn.confs).close()
    MainPage_Navigation3(**sn.confs).close()
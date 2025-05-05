

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

    _page = sn.new_page(
        permissions=["geolocation"],
        geolocation={
            "latitude": 52.52,
            "longitude": 13.4050
        },
        locale="en-US",
        record_video_dir=str(sn.confs['run']),
        record_video_size={"width": 1280, "height": 720}
    )

    MainPage_Navigation1(_page, **sn.confs).close()
    MainPage_Navigation2(_page, **sn.confs).close()
    MainPage_Navigation3(_page, **sn.confs).close()

    _page.close()
    video_path = _page.video.path()
    print(f"Video saved at: {video_path}")

    _page = sn.new_page(
        permissions=["geolocation"],
        geolocation={
            "latitude": 52.52,
            "longitude": 13.4050
        },
        locale="en-US",
        record_video_dir=str(sn.confs['run']),
        record_video_size={"width": 1280, "height": 720}
    )

    MainPage_Navigation1(_page, **sn.confs).close()
    MainPage_Navigation2(_page, **sn.confs).close()
    MainPage_Navigation3(_page, **sn.confs).close()

    _page.close()
    video_path = _page.video.path()
    print(f"Video saved at: {video_path}")

    _page = sn.new_page(
        permissions=["geolocation"],
        geolocation={
            "latitude": 52.52,
            "longitude": 13.4050
        },
        locale="en-US",
        record_video_dir=str(sn.confs['run']),
        record_video_size={"width": 1280, "height": 720}
    )

    MainPage_Navigation1(_page, **sn.confs).close()
    MainPage_Navigation2(_page, **sn.confs).close()
    MainPage_Navigation3(_page, **sn.confs).close()

    _page.close()
    video_path = _page.video.path()
    print(f"Video saved at: {video_path}")

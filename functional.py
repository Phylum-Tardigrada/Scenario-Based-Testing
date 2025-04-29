import time
from datetime import datetime
from utils.scenario import Base


# Navigation based on Dropdown
class MainPage_Navigation(Base):
    """Demonstrating Navigations from Main Page to Sub Pages"""

    # Check Main Page without Login
    def task_1(self, _page, url) -> dict:
        """ Check if only Search & Submit page Navigation is shown, if not logged in """

        self._info("Checking No Login - Navigation Menu Options")
        _page.goto(f"{url}/")

        # Click to open the dropdown
        _page.get_by_role("button", name="Navigate").click()

        # Wait for the listbox or menu to appear
        _page.get_by_role("menu").wait_for()

        # Get all options by role
        # or "menuitem", depending on markup
        options = _page.get_by_role("menuitem").all()
        option_texts = [opt.inner_text() for opt in options]

        self._chk(act=option_texts, ref=['Home', 'Search & Submit'])

        self._info("Checking Page navigation for each of the options")

        self._dbg("Home Page Navigation")
        _page.goto(f"{url}/")
        _page.get_by_role("menuitem", name="Home").click()
        _page.wait_for_url("**/")

        self._chk(act=_page.url, ref=url)

        self._dbg("Search Page Navigation")
        _page.goto(f"{url}/")
        _page.get_by_role("menuitem", name="Search & Submit").click()
        _page.wait_for_url("**/search")

        self._chk(act=_page.url, ref=f"{url}/search")

        img = f"{int(datetime.now().timestamp())}.png"
        _page.screenshot(path=img)
        self._pin(loc=img)

        time.sleep(3)


# Example
if __name__ == "__main__":

    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(
        description="Example script with arguments.")

    # Add arguments
    parser.add_argument("--url", type=str, required=True, help="URL to open")
    parser.add_argument("--headless", action="store_true",
                        help="Run in headless mode")

    # Parse the arguments
    args = parser.parse_args()

    # Use the arguments
    print("URL:", args.url)
    print("Headless:", args.headless)

    MainPage_Navigation(url=args.url, headless=args.headless).close()

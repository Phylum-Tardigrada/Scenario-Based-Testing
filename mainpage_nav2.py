import time
from datetime import datetime
from utils.scenario import Scenario


# Navigation based on Dropdown
class MainPage_Navigation2(Scenario):
    """Demonstrating Navigations from Main Page to Sub Pages"""

    # Check Main Page without Login
    def task_1(self, _page, domain) -> dict:
        """ Check if only Search & Submit page Navigation is shown, if not logged in """

        self._info("Checking No Login - Navigation Menu Options")
        _page.goto(f"{domain}/")

        # Click to open the dropdown
        _page.get_by_role("button", name="Navigate").click()

        # Wait for the listbox or menu to appear
        _page.get_by_role("menu").wait_for()

        # Get all options by role menuitem, depending on markup
        options = _page.get_by_role("menuitem").all()
        option_texts = [opt.inner_text() for opt in options]

        # Check if only ['Home', 'Search & Submit'] is present in the dropdown options when not logged in
        self._chk(act=option_texts, ref=['Home', 'Search & Submit'])

        time.sleep(2)

    # Check if Home page is navigated correctly
    def task_2(self, _page, domain):
        """ Check if Home page is navigated correctly """

        self._info("Checking Home Page Navigation")
        _page.goto(f"{domain}/")

        # Click to open the dropdown
        _page.get_by_role("button", name="Navigate").click()

        # Wait for the listbox or menu to appear
        _page.get_by_role("menu").wait_for()

        # Click on the "Home" option
        _page.get_by_role("menuitem", name="Home").click()

        # Wait for the navigation to complete
        # or until a specific element is visible on the new page
        _page.wait_for_url("**/")

        # Check if the navigation is successful
        self._chk(act=_page.url.replace(domain, '**'), ref='**')

        time.sleep(3)
        # Take a screenshot and pin it for reference
        img = f"{int(datetime.now().timestamp())}.png"
        _page.screenshot(path=img)
        self._pin(loc=img)

    # Check if Search & Submit page is navigated correctly
    def task_3(self, _page, domain):
        """ Check if Search & Submit page is navigated correctly """

        self._info("Search Page Navigation")
        _page.goto(f"{domain}/")

        # Click to open the dropdown
        _page.get_by_role("button", name="Navigate").click()

        # Wait for the listbox or menu to appear
        _page.get_by_role("menu").wait_for()

        # Click on the "Search & Submit" option
        _page.get_by_role("menuitem", name="Search & Submit").click()

        # wait for navigation to complete
        # or until a specific element is visible on the new page
        _page.wait_for_url("**/search")

        # Check if the navigation is successful
        self._chk(act=_page.url.replace(domain, '**'), ref="**/search")

        time.sleep(3)
        # Take a screenshot and pin it for reference
        img = f"{int(datetime.now().timestamp())}.png"
        _page.screenshot(path=img)
        self._pin(loc=img)

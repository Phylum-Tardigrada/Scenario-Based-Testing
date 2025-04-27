
from utils.scenario import Base

# Scenario 1 Heading
class Derived(Base):
    """Scenario 1 Docstring"""

    # Task 1 Heading
    def task_1(self) -> dict:
        """ Task 1 Docstring """
        self._dbg("Running Task 1")
        self._info("Running Task 1")
        self._warn("Running Task 1")
        self._err("Running Task 1")

    # Task 2 Heading
    def task_2(self) -> dict:
        """ Task 2 Docstring """
        self._dbg("Running Task 2")
        self._info("Running Task 2")
        self._warn("Running Task 2")
        self._err("Running Task 2")

    # Task 3 Heading
    def task_3(self) -> dict:
        """ Task 3 Docstring """
        self._dbg("Running Task 3")
        self._info("Running Task 3")
        self._warn("Running Task 3")
        self._err("Running Task 3")

    # Task 10 Heading
    def task_10(self) -> dict:
        """ Task 10 Docstring """
        self._dbg("Running Task 10")
        self._info("Running Task 10")
        self._warn("Running Task 10")
        self._err("Running Task 10")

# Example
if __name__ == "__main__":

    Derived().close()
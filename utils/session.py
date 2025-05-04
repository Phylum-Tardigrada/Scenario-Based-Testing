import os
from datetime import datetime
from pathlib import Path


class Session:

    def __init__(self, **confs):
        self.confs = confs

    def __enter__(self):

        self.confs['run'] = str(int(datetime.now().timestamp()))
        os.makedirs(Path(self.confs['run']).absolute(), exist_ok=True)
        return self  # return resource object

    def __exit__(self, exc_type, exc_value, traceback):

        # Handle any exceptions here
        return True  # Suppress exception

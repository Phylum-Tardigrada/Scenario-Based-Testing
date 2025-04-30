import re
import inspect
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)]


class Base:

    __vars = {}
    __tasks = []
    __lines = {}

    def __init__(self, **confs):

        self.__vars = confs

        # Get all methods of this instance
        methods = inspect.getmembers(self, predicate=inspect.ismethod)

        # Filter methods that match a regex pattern
        pattern = re.compile(r'^task_\d+$')  # e.g., task_1, task_2, etc.
        matched_methods = [(name, method)
                           for name, method in methods if pattern.match(name)]

        # Sort by method name (you can customize this sorting logic)
        matched_methods.sort(key=lambda x: natural_sort_key(x[0]))
        class_st_ts = datetime.now().isoformat()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=confs['headless'])
            page = browser.new_page()
            page.wait_for_timeout(10000)

            # Call each method in order
            for name, method in matched_methods:

                kwargs = list(inspect.signature(method).parameters.keys())
                params = {key: self.__vars[key]
                          for key in self.__vars if key in kwargs}

                self.__tasks.append(
                    {
                        'typ': 'task',
                        'obj': method.__name__,
                        'desc': inspect.getcomments(method)[1:].strip(),
                        'doc': inspect.getdoc(method),
                        'src': inspect.getsource(method),
                        'inp': params,
                    }
                )

                try:
                    returns = {}
                    self.__lines = {}
                    func_st_ts = datetime.now().isoformat()
                    returns = method(_page=page, **params)
                    if returns:
                        self.__vars.update(returns)
                    func_nd_ts = datetime.now().isoformat()
                    self.__tasks[-1].update(
                        {
                            'out': returns,
                            'vars': self.__vars,
                            'st_ts': func_st_ts,
                            'nd_ts': func_nd_ts,
                            'lines': self.__lines
                        }
                    )
                except Exception as err:
                    self.__tasks[-1].update(
                        {
                            'err': err,
                            'vars': self.__vars,
                            'st_ts': func_st_ts,
                            'nd_ts': func_nd_ts,
                            'lines': self.__lines
                        }
                    )

            class_nd_ts = datetime.now().isoformat()
            self.__scenario = {
                'typ': 'scenario',
                'obj': self.__class__.__name__,
                'desc': inspect.getcomments(self.__class__)[1:].strip(),
                'doc': inspect.getdoc(self.__class__),
                'st_ts': class_st_ts,
                'nd_ts': class_nd_ts,
                'tasks': self.__tasks
            }

            browser.close()

    def _dbg(self, msg):

        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'log',
            'ts': datetime.now().isoformat(),
            'lvl': 'DBG',
            'msg': msg
        }

    def _info(self, msg):

        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'log',
            'ts': datetime.now().isoformat(),
            'lvl': 'INFO',
            'msg': msg
        }

    def _warn(self, msg):

        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'log',
            'ts': datetime.now().isoformat(),
            'lvl': 'WARNING',
            'msg': msg
        }

    def _err(self, msg):

        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'log',
            'ts': datetime.now().isoformat(),
            'lvl': 'ERR',
            'msg': msg
        }

    def _critical(self, msg):

        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'log',
            'ts': datetime.now().isoformat(),
            'lvl': 'CRITICAL',
            'msg': msg
        }

    def _chk(self, act, ref):

        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        chk_act = [type(act).__name__, act]
        chk_ref = [type(ref).__name__, ref]
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'chk',
            'ts': datetime.now().isoformat(),
            'act': chk_act,
            'ref': chk_ref,
            'rslt': bool(chk_act == chk_ref)}

    def _pin(self, loc: Path):

        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        url = loc
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'pin',
            'ts': datetime.now().isoformat(),
            'path': loc,
            'url': url,
        }

    def close(self):

        import json
        print(self.__scenario)
        with open(f'{self.__class__.__name__}.json', 'w') as file:
            json.dump(self.__scenario, file, indent=2)

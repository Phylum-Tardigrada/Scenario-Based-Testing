import re
import inspect
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)]


class Scenario:

    __vars = {}
    __tasks = []
    __lines = {}

    def __init__(self, _page, **confs):

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
        print("", class_st_ts, f"\033[1;37m{self.__class__.__name__}\033[0m")
        _page.wait_for_timeout(10000)

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
                print(" ", func_st_ts, f"\033[1;37m{self.__tasks[-1]['desc']}\033[0m")
                returns = method(_page, **params)
                if returns:
                    self.__vars.update(returns)
                func_nd_ts = datetime.now().isoformat()
                self.__tasks[-1].update(
                    {
                        'out': returns,
                        # 'vars': self.__vars,
                        'st_ts': func_st_ts,
                        'nd_ts': func_nd_ts,
                        'lines': self.__lines
                    }
                )
            except Exception as err:
                self.__tasks[-1].update(
                    {
                        'err': err,
                        # 'vars': self.__vars,
                        'st_ts': func_st_ts,
                        'nd_ts': func_nd_ts,
                        'lines': self.__lines
                    }
                )

        class_nd_ts = datetime.now().isoformat()
        self.__scenario = {
            'run': confs.get('run', None),
            'typ': 'scenario',
            'obj': self.__class__.__name__,
            'desc': inspect.getcomments(self.__class__)[1:].strip(),
            'doc': inspect.getdoc(self.__class__),
            'st_ts': class_st_ts,
            'nd_ts': class_nd_ts,
            'tasks': self.__tasks,
            'vars': self.__vars
        }

    def _dbg(self, msg):

        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        now = datetime.now().isoformat()
        print("  ", now, f"\033[37m{msg}\033[0m")
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'log',
            'ts': now,
            'lvl': 'DBG',
            'msg': msg
        }

    def _info(self, msg):

        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        now = datetime.now().isoformat()
        print("  ", now, f"\033[38;5;111m{msg}\033[0m")
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'log',
            'ts': now,
            'lvl': 'INFO',
            'msg': msg
        }

    def _warn(self, msg):

        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        now = datetime.now().isoformat()
        print("  ", now, f"\033[33m{msg}\033[0m")
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'log',
            'ts': now,
            'lvl': 'WARNING',
            'msg': msg
        }

    def _err(self, msg):

        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        now = datetime.now().isoformat()
        print("  ", now, f"\033[1;31m{msg}\033[0m")
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'log',
            'ts': now,
            'lvl': 'ERR',
            'msg': msg
        }

    def _critical(self, msg):

        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        now = datetime.now().isoformat()
        print("  ", now, f"\033[31m{msg}\033[0m")
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'log',
            'ts': now,
            'lvl': 'CRITICAL',
            'msg': msg
        }

    def _chk(self, act, ref):

        tick = "\033[1;92mPASS\033[0m"
        cross = "\033[1;31mFAIL\033[0m"
        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        chk_act = [act, type(act).__name__]
        chk_ref = [ref, type(ref).__name__]
        now = datetime.now().isoformat()
        print(
            "  ", now, f"\033[3m{chk_act} == {chk_ref}\033[0m {tick if bool(chk_act == chk_ref) else cross}")
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'chk',
            'ts': now,
            'act': chk_act,
            'ref': chk_ref,
            'rslt': bool(chk_act == chk_ref)}

    def _pin(self, loc: Path):

        source_lines, caller_from = inspect.getsourcelines(
            inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        url = loc
        now = datetime.now().isoformat()
        self.__lines[
            (called_from-caller_from) + 1
        ] = {
            'typ': 'pin',
            'ts': now,
            'path': loc,
            'url': url,
        }

    def close(self):

        import json
        tmp_dir = self.__vars.get('run', None)
        if tmp_dir:
            fname = f"{tmp_dir}/{self.__class__.__name__}.json"
        else:
            fname = f"{self.__class__.__name__}.json"
        print(f"\033[1;37m writing {fname}...\033[0m")
        with open(fname, 'w') as file:
            json.dump(self.__scenario, file, indent=2)

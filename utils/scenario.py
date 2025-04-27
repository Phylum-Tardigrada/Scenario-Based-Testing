import re
import inspect
from datetime import datetime

import pandas as pd

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)]

class Base:

    __vars = {}
    __out = []

    def __init__(self):
        # Get all methods of this instance
        methods = inspect.getmembers(self, predicate=inspect.ismethod)

        # Filter methods that match a regex pattern
        pattern = re.compile(r'^task_\d+$')  # e.g., task_1, task_2, etc.
        matched_methods = [(name, method) for name, method in methods if pattern.match(name)]

        # Sort by method name (you can customize this sorting logic)
        matched_methods.sort(key=lambda x: natural_sort_key(x[0]))
        class_st_dt = self.__vars
        class_st_ts = datetime.now().isoformat()

        # Call each method in order
        for name, method in matched_methods:
            self.__run = f"{self.__class__.__name__}/{method.__name__}"
            func_st_ts = datetime.now().isoformat()
            kwargs = list(inspect.signature(method).parameters.keys())
            params = {key: self.__vars[key] for key in self.__vars if key in kwargs}
            try:
                returns = {}
                returns = method(**params)
                if returns:
                    self.__vars.update(returns)
            except Exception as err:
                self._critical(err)
            
            func_nd_ts = datetime.now().isoformat()

            self.__out.append(
                {
                # 'task': int(name.split('_')[-1]),
                'typ': 'span',
                'loc.typ': 'method',
                'loc.run': self.__run,
                'loc.obj': method.__name__,
                'loc.desc': inspect.getcomments(method)[1:].strip(),
                'loc.doc': inspect.getdoc(method),
                'loc.src': inspect.getsource(method),
                'loc.inp': params,
                'loc.out': returns,
                'loc.vars': self.__vars,
                'span.st': func_st_ts,
                'span.nd': func_nd_ts
                }
            )

        class_nd_ts = datetime.now().isoformat()
        class_nd_dt = self.__vars
        self.__out.append(
            {
                # 'task': 0,
                'typ': 'span',
                'loc.typ': 'class',
                'loc.run': f"{self.__class__.__name__}/",
                'loc.obj': self.__class__.__name__,
                'loc.desc': inspect.getcomments(self.__class__)[1:].strip(),
                'loc.doc': inspect.getdoc(self.__class__),
                'loc.src': inspect.getsource(self.__class__),
                'loc.inp': class_st_dt,
                'loc.out': class_nd_dt,
                'span.st': class_st_ts,
                'span.nd': class_nd_ts
            }
        )

    def _log(self, lvl, msg, lno=None):

        self.__out.append(
            {
                'line': None,
                'typ': 'log',
                'loc.typ': 'method',
                'loc.run': self.__run,
                'log.ts': datetime.now().isoformat(),
                'log.lvl': lvl,
                'log.lno': lno,
                'log.msg': msg
            }
        )
        print(f"[{datetime.now().isoformat()}]: {msg}")

    def _dbg(self, msg):

        # caller = inspect.currentframe().f_back.f_code.co_name
        # called = inspect.currentframe().f_code.co_name

        source_lines, caller_from = inspect.getsourcelines(inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        self._log('DEBUG', msg, (called_from-caller_from)+1)

    def _info(self, msg):

        source_lines, caller_from = inspect.getsourcelines(inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        self._log('INFO', msg, (called_from-caller_from)+1)

    def _warn(self, msg):

        source_lines, caller_from = inspect.getsourcelines(inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        self._log('WARNING', msg, (called_from-caller_from)+1)

    def _err(self, msg):

        source_lines, caller_from = inspect.getsourcelines(inspect.currentframe().f_back.f_code)
        called_from = inspect.currentframe().f_back.f_lineno
        self._log('ERROR', msg, (called_from-caller_from)+1)

    def _critical(self, msg):

        self._log('CRITICAL', msg)

    def close(self):

        df = pd.DataFrame(self.__out, columns=[
            # 'task',
            'loc.typ', 'loc.obj', 'loc.src', 
            'loc.run', 'loc.desc', 'loc.doc', 
            'typ', 
                'span.st', 
                    'loc.inp', 
                        'log.ts', 'log.lvl', 'log.lno','log.msg', 
                    'loc.out', 
                'span.nd', 
            'loc.vars'])
        df.sort_values(by=[
            # 'task', 
            'loc.run', 
            'span.st', 'log.ts', 'span.nd']).to_excel(f"{self.__class__.__name__}.xlsx")
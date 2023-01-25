from IPython import display
from typing import Any
import re, warnings

class Template:
    
    def __init__(self, text: str, *param: Any):
        self.text = text
        self.params = param
        self.varpattern = re.compile("\\\\(?:\\\\|([\\*@])([\\w]+);)")
        self._paramsnum = len(self.params)
        self._varsnum = len(self.varpattern.findall(self.text))
        if self._paramsnum < self._varsnum:
            raise IndexError(f"The number of parameters does not match that of variables - need {self._varsnum-self._paramsnum} more variable{'s' if self._varsnum-self._paramsnum>1 else ''}")
        elif self._paramsnum > self._varsnum:
            warnings.warn(f"This template needs only {self._varsnum} parameter{'s' if self._varsnum>1 else ''}, got {self._paramsnum} parameter{'s' if self._paramsnum>1 else ''} instead", UserWarning)
    
    def VarList(self) -> list:
        return self.varpattern.findall(self.text)

def DisplayMd(text: str):
    display.display_markdown(text, raw=True)
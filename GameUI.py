from IPython import display
from typing import Any, Optional
import re

class Template:
    
    def __init__(self, text: str, *param: Any):
        self.text = text
        self.params = param
        self._varpattern = re.compile("\\\\(?:\\\\|[\\w]+;)")
        self._vars = self._varpattern.findall(self.text)
        while "\\\\" in self._vars:
            self._vars.remove("\\\\")
        self._paramsnum = len(self.params)
        self._varsnum = len(self._vars)
        if self._paramsnum < self._varsnum:
            raise IndexError(f"The number of parameters does not match that of variables - need {self._varsnum-self._paramsnum} more variable{'s' if self._varsnum-self._paramsnum>1 else ''}")
        elif self._paramsnum > self._varsnum:
            raise IndexError(f"This template needs only {self._varsnum} parameter{'s' if self._varsnum>1 else ''}, got {self._paramsnum} parameter{'s' if self._paramsnum>1 else ''} instead")
    
    def Render(self, order: Optional[list[int]] = None) -> str:
        """
        Render the template into formatted text by replacing variables with given parameters.
        """
        pairs = {idx0: idx1 for idx0, idx1 in zip(self._vars, self.params)}
        
        def CurrentVar(match: re.Match) -> str:
            return pairs[match.group()]
        
        if order is None:
            return re.sub("\\\\[\\w]+;", CurrentVar, self.text).replace("\\\\", "\\")
        else:
            pairs = {idx0: idx1 for idx0, idx1 in zip(self._vars, [self.params[i] for i in order])}
            return re.sub("\\\\[\\w]+;", CurrentVar, self.text).replace("\\\\", "\\")

def DisplayMd(obj: str | Template):
    if isinstance(obj, str):
        display.display_markdown(obj, raw=True)
    elif isinstance(obj, Template):
        display.display_markdown(obj.Render(), raw=True)

def DisplayHTML(obj: str | Template):
    if isinstance(obj, str):
        display.display_html(obj, raw=True)
    elif isinstance(obj, Template):
        display.display_html(obj.Render(), raw=True)
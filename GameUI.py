from IPython import display
from typing import Optional
import random
    
# Constances
CONDENSED_MENU = 0
MUTABLE_MENU = 1

class EngineError:
    pass

class CoreRenderer:

    def DisplayMd(self, text: str):
        display.display_markdown(text, raw=True)

    def DisplayHTML(self, text: str):
        display.display_html(text, raw=True)

class DisplayBlock:
    
    def __init__(self):
        self.Elements = {}
        # {
        #   "example": "Pekora was here", 0
        #   |       |  |               |  |
        #   +---+---+  +-------+-------+  +-- Display order
        #       |              |
        #       |              +------------- Content
        #       |
        #       +---------------------------- Element name
        # }
        self.mutable = True
        self._DisplayBlockID = random.randint(0, 0xffffffff)
    
    def ModifyElement(self, element: str, text: str, display_order: int):
        if element in self.Elements.keys():
            self.Elements[element][0] = text
            self.Elements[element][1] = display_order
    
    def ModifyDisplayOrder(self, element: str, num: int):
        if element in self.Elements.keys() or self.mutable:
            self.Elements[element][1] = num
    
    def NewElement(self, element: str, text: str, display_order: int):
        if self.mutable:
            self.Elements[element] = [text, display_order]
    
    def RemoveElement(self, element: str):
        self.Elements.pop(element)
    
    def PopElement(self, element: str) -> tuple:
        return (element, self.Elements.pop(element))

    def DisplayOrder(self) -> set[int]:
        return set([i[1] for i in self.Elements.values()])

class Menu(DisplayBlock):
    
    def __init__(self, type_: int):
        super().__init__()
        match type_:
            case 0:
                self.mutable = False
                self.Elements["header"] = ["# Your Game", 0]
                self.Elements["commands"] = [
                    "New game &#x2014; `Player.NewGame()`\n"
                    "\n"
                    "Load game &#x2014; `Player.Load()`",
                    1
                ]
                self.Elements["footer"] = [
                    "----\n"
                    "Created by me",
                    2
                ]
            case 1:
                self.Elements["header"] = ["# Your Game", 0]
                self.Elements["commands"] = [
                    "New game &#x2014; `Player.NewGame()`\n"
                    "\n"
                    "Load game &#x2014; `Player.Load()`",
                    1
                ]
                self.Elements["footer"] = [
                    "----\n"
                    "Created by me",
                    2
                ]

class Renderer(CoreRenderer):

    # Error codes
    class ErrorCode:
        Index = 0x22
        EmptyString = 0x23
    
    def __init__(self):
        self.RendererID = random.randint(0, 0xffff)

    def ShowError(self, errcode: int, sender: str = "Engine", message: str = "No message set"):
        self.DisplayMd(
            "### **<div style=\"background: red; color: white;\">Error!</div>**\n"
            f"{message}"
            "\n"
            "\n"
            "|Error code|Caught by|\n"
            "|:-|:-|\n"
            f"|`{errcode}`|{sender}|\n"
            "\n"
            "----"
        )
    
    def SetMenu(self, extra_elements: Optional[dict[str, str]] = None, menutype: int = 0):
        self.Menu = Menu(menutype)
        if extra_elements is not None:
            for k, v in zip(extra_elements.keys(), extra_elements.values()):
                if not self.Menu.mutable:
                    self.ShowError(self.ErrorCode.Index, message=f"The `CONDENSED_MENU` type menu is not mutable")
                elif k not in self.Menu.Elements.keys():
                    if v[0] == "":
                        self.ShowError(self.ErrorCode.EmptyString, message=f"Element \"{k}\" is empty")
                    elif v[1] < 0:
                        self.ShowError(self.ErrorCode.Index, message=f"Element \"{k}\"'s display order cannot be a negative number")
                    else:
                        self.Menu.NewElement(k, v[0], v[1])
                else:
                    self.Menu.ModifyElement(k, v[0], v[1])
    
    def DisplayMenu(self):
        for i0 in self.Menu.DisplayOrder():
            for i1 in self.Menu.Elements.values():
                if i1[1] == i0:
                    self.DisplayMd(i1[0])
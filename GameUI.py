from IPython import display
import re
import random

class CoreRenderer:

    def DisplayMd(self, text: str):
        display.display_markdown(text, raw=True)

    def DisplayHTML(self, text: str):
        display.display_html(text, raw=True)

class Renderer(CoreRenderer):
    
    def __init__(self):
        self.RendererID = random.randint(0, 0xffff)
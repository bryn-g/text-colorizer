# text-colorizer
Some classes to easily colorize terminal text.

Example usage:
```Python
import text_colorizer

# add your own custom colors
class TextColorSet(text_colorizer.TermTextColorizer):
    def __init__(self):
        super().__init__()
        self.add_iro("orange", "172")
        self.add_iro("gold", "220")
        self.add_iro("green", "112")
        self.add_iro("purple", "140")
        self.add_iro("gray", "246")
        self.add_iro("plum", "96")
        self.add_iro("darkcyan", "38")
        self.add_iro("bg_green", "112", True)
        self.add_iro("bg_plum", "96", True)
        self.add_iro("bg_gray", "246", True)
```
```Python
term = TextColorSet()

print(f"{term.orange('This is some orange text.')}")
```

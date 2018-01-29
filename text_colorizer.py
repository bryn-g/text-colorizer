import os
import sys
import re
import click

# iro is japanese romanji for color - saves text colors
class IroList:
    def __init__(self):
        self._iro_list = {}
        self._set_iro = ""

    @property
    def iro_list(self):
        return self._iro_list

    @property
    def set_iro(self):
        return self._set_iro

    @set_iro.setter
    def set_iro(self, name):
        if name in self._iro_list:
            self._set_iro = name

    def remove_iro(self, name):
        if name in self._iro_list:
            del self._iro_list[name]

    def iro(self, text, name=""):
        if name is "":
            name = self._set_iro

        if name in self._iro_list:
            pre_code, post_code = self._iro_list[name]

            return f"{pre_code}{text}{post_code}"

        return text

class TermTextColorizer(IroList):
    # format: "\033[{text_code};5;{256_code}m{text}\033[0m"

    TERM_TEXT_PRE_CODE = "\033[38;5;"
    TERM_BACKGROUND_PRE_CODE = "\033[48;5;"
    TERM_POST_CODE = "\033[0m"

    # 0-255 (bg=True|False)
    @classmethod
    #term_color_text
    def code(cls, text, term_code, bg=False):
        if int(term_code) >=0 and int(term_code) < 256:
            text_code = cls.TERM_TEXT_PRE_CODE
            if bg:
                text_code = cls.TERM_BACKGROUND_PRE_CODE

            return f"{text_code}{term_code}m{text}{cls.TERM_POST_CODE}"
        else:
            return text

    @classmethod
    def print_term_color_table(cls, bg=False):
        print(f"\nterminal color table {'(background)' if bg else ''} - codes\n")
        pad_to = 19
        row_string = ""
        for i in range(256):
            row_string += f" {cls.code(str(i), str(i), bg)} "

            if i % 16 == 0 and i != 0:
                print(f"{row_string}")
                row_string = ""
        print(f"{row_string}")

    def add_iro(self, name, code, bg=False):
        if int(code) >=0 and int(code) < 256:
            text_code = self.TERM_TEXT_PRE_CODE
            if bg:
                text_code = self.TERM_BACKGROUND_PRE_CODE

            pre = f"{text_code}{code}m"
            self._iro_list[name] = [pre, self.TERM_POST_CODE]
            if name in self._iro_list:
                if self._set_iro is "":
                    self._set_iro = name
                return True

        return False

class ANSITextColorizer(IroList):
    # format: "\x1b[{code}m{text}\x1b[0m"

    ANSI_TEXT_PRE_CODE = "\x1b["
    ANSI_TEXT_POST_CODE = "\x1b[0m"
    ANSI_CODE_PATTERN = re.compile('^[0-8](;3[0-8])?(;4[0-8])?$')

    # 0-8;30-38;40-48
    @classmethod
    def code(cls, text, ansi_code):
        if self.ANSI_CODE_PATTERN.match(code):
            return f"{cls.ANSI_TEXT_PRE_CODE}{ansi_code}m{text}{cls.ANSI_TEXT_POST_CODE}"
        else:
            return text

    @staticmethod
    def is_ansi_supported():
        if ((os.getenv("CLICOLOR", '0') != '0' and sys.stdout.isatty()) or
            os.getenv("CLICOLOR_FORCE", '0') != '0'):
            return True

        return False

    @classmethod
    def print_ansi_color_tables(cls):
        print("\nansi color tables - codes\n")
        for text_code in range(8):
            #print(f"text style: {text_code}")
            for foreground_code in range(30, 38):
                color_code_string = ""
                for background_code in range(40, 48):
                    color_sequence = f"{text_code};{foreground_code};{background_code}"
                    color_code_string += f"{cls.ANSI_TEXT_PRE_CODE}{color_sequence}m {color_sequence} {cls.ANSI_TEXT_POST_CODE}"

                print(f"{color_code_string}")

    def add_iro(self, name, code):
        if self.ANSI_CODE_PATTERN.match(code):
            pre = f"{self.ANSI_TEXT_PRE_CODE}{code}m"
            self._iro_list[name] = [pre, self.ANSI_TEXT_POST_CODE]
            if name in self._iro_list:
                if self._set_iro is "":
                    self._set_iro = name
                return True

        return False

@click.command()
@click.option(
    '--text', '-txt',
    help='example colorizer text'
)
@click.option(
    '--tables', '-t', is_flag=True,
    help='print ansi color tables'
)
def main(text, tables):
    """
    A simple script to colorize text using ansi or terminal color codes.
    """

    ansi_colorizer = ANSITextColorizer()
    term_colorizer = TermTextColorizer()

    if not ansi_colorizer.is_ansi_supported():
        print(f"* ansi colors not supported.")

    if tables:
        ansi_colorizer.print_ansi_color_tables()
        term_colorizer.print_term_color_table()
        # term background colors
        term_colorizer.print_term_color_table(True)
        exit()

    if text != None:
        # examples
        # ansi colorizer

        print(f"text: {text}")

        print("\nansi colorizer examples\n")
        ansi_colorizer.add_iro("pinkbg", "7;35;47")
        ansi_colorizer.add_iro("pink", "1;35")

        print(f"ansi_colorizer.iro(text, 'pinkbg'): {ansi_colorizer.iro(text, 'pinkbg')}")

        ansi_colorizer.set_iro = "pink"
        print(f"ansi_colorizer.set_iro: {ansi_colorizer.set_iro}")
        print(f"ansi_colorizer.iro(text): {ansi_colorizer.iro(text)}")

        print(f"ansi iro list: {ansi_colorizer.iro_list}")

        # term colorizer
        print("\nterm colorizer examples\n")

        term_colorizer.add_iro("orange", "172")
        term_colorizer.add_iro("redbg", "197", True)

        print(f"term_colorizer.iro(text, 'orange'): {term_colorizer.iro(text, 'orange')}")
        print(f"term_colorizer.iro(text, 'redbg'): {term_colorizer.iro(text, 'redbg')}")

        term_colorizer.set_iro = "orange"
        print(f"term_colorizer.set_iro: {term_colorizer.set_iro}")
        print(f"term_colorizer.iro(text): {term_colorizer.iro(text)}")

        print(f"term iro list: {term_colorizer.iro_list}")

if __name__ == "__main__":
    main()

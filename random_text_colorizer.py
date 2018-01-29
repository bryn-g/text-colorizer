import random
import click
import colorama
from colorama import Fore, Back, Style

class RandomTextColorizer(object):
    FORE_COLOR_LIST = (Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE)
    BACK_COLOR_LIST = (Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE)
    STYLE_LIST = (Style.DIM, Style.NORMAL, Style.BRIGHT)

    def __init__(self, text=""):
        self._original_text = text
        self._colorized_text = ""

    @property
    def original_text(self):
        return self._original_text

    @property
    def colorized_text(self):
        return self._colorized_text

    @classmethod
    def get_random_fore_style(cls):
        text_color = random.choice(cls.FORE_COLOR_LIST)
        while text_color == Fore.BLACK:
            text_color = random.choice(cls.FORE_COLOR_LIST)

        style = random.choice(cls.STYLE_LIST)
        # dont set dim text
        while style == Style.DIM:
            style = random.choice(cls.STYLE_LIST)

        return f"{text_color}{style}"

    @classmethod
    def get_random_back_style(cls):
        text_color = random.choice(cls.FORE_COLOR_LIST)
        fore_index = cls.FORE_COLOR_LIST.index(text_color)

        back_color = random.choice(cls.BACK_COLOR_LIST)
        back_index = cls.BACK_COLOR_LIST.index(back_color)
        # dont set back color and fore color to be the same
        while back_index == fore_index:
            back_color = random.choice(cls.BACK_COLOR_LIST)
            back_index = cls.BACK_COLOR_LIST.index(back_color)

        style = random.choice(cls.STYLE_LIST)

        return f"{back_color}{text_color}{style}"

    def randomly_colorize(self, back, words):
        colorized_value = ""
        char_index = 0
        for char in self._original_text:
            if words:
                if char.isspace() or char_index == 0:
                    if back:
                        colorized_value += self.get_random_back_style()
                    else:
                        colorized_value += self.get_random_fore_style()
            else:
                if back:
                    colorized_value += self.get_random_back_style()
                else:
                    colorized_value += self.get_random_fore_style()

            colorized_value += char
            char_index += 1

        self._colorized_text = colorized_value

def get_random_case(value):
    upper = random.choice([True, False])
    if upper:
        return value.upper()

    return value

@click.command()
@click.argument('text')
@click.option(
    '--back', '-b', is_flag=True,
    help='include back colors'
)
@click.option(
    '--words', '-w', is_flag=True,
    help='color words instead of letters'
)
@click.option(
    '--case', '-c', is_flag=True,
    help='randomize case of letters'
)
def main(text, back, words, case):
    """
    A simple script to randomly colorize text.
    """
    colorama.init(autoreset=True)

    if case:
        temp_text = ""
        for char in text:
            temp_text += get_random_case(char)
        text = temp_text

    colorizer = RandomTextColorizer(text)
    colorizer.randomly_colorize(back, words)
    print(f"{colorizer.colorized_text}")

if __name__ == "__main__":
    main()

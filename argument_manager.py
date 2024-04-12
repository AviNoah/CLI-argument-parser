import re
from typing import List


class argumentManager:
    def __init__(self, desc: str) -> None:
        self.desc: str = desc
        self.arguments: List[argument] = list()

    def add_argument(self, symbol: str, long_name: str, help: str, default: str):

        for arg in self.arguments:
            if arg.symbol == symbol or arg.long_name == long_name:
                raise ValueError(
                    "Symbol or long name already exists with-in this context, please select another"
                )

        self.arguments.append(argument(symbol, long_name, help, default))

    def parse_args(self, string_input: str) -> dict:
        # Return a dictionary where the key is the long_name of an argument and then its value.
        values = {arg.long_name: arg.parse_arg(string_input) for arg in self.arguments}
        return dict(values)

    def print_help(self):
        print(self.desc)

        for arg in self.arguments:
            arg.print_help()


class argument:
    def __init__(self, symbol: str, long_name: str, help: str, default: str) -> None:
        self.symbol: str = symbol
        self.long_name: str = long_name
        self.help: str = help
        self.default: str = str(default)  # Default value if argument not parsed
        self.__post_init__()

    def __post_init__(self):
        if not self.symbol.startswith("-"):
            raise ValueError("Symbol must start with '-'")

        if not self.long_name.startswith("--"):
            raise ValueError("Long name must start with '--'")

    def print_help(self):
        print(
            f"{self.symbol} / {self.long_name} - default: {self.default} - {self.help}"
        )

    def parse_arg(self, string_input: str) -> str:
        # Return the argument value extracted from the string input or default if not found
        pattern = (
            f"(?:{self.symbol}|{self.long_name})"
            + r'\s+(?:"([^"]*)"|([^\s-]+)(?=\s*-|$))'
        )

        match = re.search(pattern, string_input)
        if match is None:
            return self.default

        # Fetch result, first capture group is "", second is without ""
        value = match.group(1)
        if value is None:
            value = match.group(2)

        value = value.strip()

        if value:
            return value

        return self.default


def main():
    mgr: argumentManager = argumentManager("Directory and lang selector")
    mgr.add_argument("-d", "--file-path", "directory path", r"C:/")
    mgr.add_argument("-l", "--language", "Pick a language code", "en")
    mgr.add_argument(
        "-p", "--pepper", "pepper and salt!", "Salt"
    )  # Edge case for --file-path
    mgr.print_help()
    inp = r'-d "C:\ss" -l jp'

    args = mgr.parse_args(inp)
    print(args)

    while True:
        inp = input("Something and then do -d for directory: ")
        args = mgr.parse_args(inp)
        print(args)


if __name__ == "__main__":
    main()

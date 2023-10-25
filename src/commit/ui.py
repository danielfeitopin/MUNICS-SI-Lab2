class UI:

    __COLOR_LIGHT_RED = '\033[1;31m'
    __COLOR_LIGHT_GREEN = '\033[1;32m'
    __COLOR_YELLOW = '\033[0;33m'
    __COLOR_CYAN = '\033[1;36m'
    __COLOR_MAGENTA = '\033[1;35m'

    __TEXT_RESET = '\033[0m'
    __TEXT_BOLD = '\033[1m'
    __TEXT_FAINT = '\033[2m'
    __TEXT_UNDERLINE = "\033[4m"
    __TEXT_BLINK = "\033[5m"

    @classmethod
    def header(cls, m: str) -> str:
        return cls.__COLOR_YELLOW + cls.__TEXT_BOLD + m + cls.__TEXT_RESET

    @classmethod
    def cyan(cls, m: str) -> str:
        return cls.__COLOR_CYAN + m + cls.__TEXT_RESET

    @classmethod
    def magenta(cls, m: str) -> str:
        return cls.__COLOR_MAGENTA + m + cls.__TEXT_RESET

    @classmethod
    def set_bold(cls):
        print(cls.__TEXT_BOLD, end='')

    @classmethod
    def set_faint(cls):
        print(cls.__TEXT_FAINT, end='')

    @classmethod
    def reset_style(cls):
        print(cls.__TEXT_RESET, end='')

    @classmethod
    def success(cls, m: str) -> str:
        return cls.__COLOR_LIGHT_GREEN + m + cls.__TEXT_RESET

    @classmethod
    def error(cls, m: str) -> str:
        return cls.__COLOR_LIGHT_RED + m + cls.__TEXT_RESET

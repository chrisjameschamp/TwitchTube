import colorama
import logging
import logging.handlers
import re

class ColorCodes:
    white = colorama.Fore.WHITE + colorama.Style.NORMAL
    grey = colorama.Fore.WHITE + colorama.Style.DIM
    green = colorama.Fore.GREEN + colorama.Style.BRIGHT
    yellow = colorama.Fore.YELLOW + colorama.Style.NORMAL
    red = colorama.Fore.RED + colorama.Style.NORMAL
    bold_red = colorama.Fore.RED + colorama.Style.BRIGHT
    blue = colorama.Fore.BLUE + colorama.Style.NORMAL
    light_blue = colorama.Fore.LIGHTBLUE_EX + colorama.Style.NORMAL
    purple = colorama.Fore.MAGENTA + colorama.Style.NORMAL
    reset = colorama.Fore.RESET + colorama.Style.RESET_ALL


class ColorizedArgsFormatter(logging.Formatter):
    arg_colors = [ColorCodes.purple, ColorCodes.light_blue]
    level_fields = ["levelname", "levelno"]
    level_to_color = {
        logging.DEBUG: ColorCodes.white,
        logging.INFO: ColorCodes.green,
        logging.WARNING: ColorCodes.yellow,
        logging.ERROR: ColorCodes.red,
        logging.CRITICAL: ColorCodes.bold_red,
    }
    level_names = {
        logging.DEBUG: "DBUG",
        logging.INFO: "INFO",
        logging.WARNING: "WARN",
        logging.ERROR: "ERRR",
        logging.CRITICAL: "CRIT"
    }

    def __init__(self, fmt: str, datefmt=None):
        super().__init__()
        colorama.init()
        self.level_to_formatter = {}

        def add_color_format(level: int):
            color = ColorizedArgsFormatter.level_to_color[level]
            _format = fmt
            _format = _format.replace("%(asctime)s", ColorCodes.grey + "%(asctime)s" + ColorCodes.reset)
            for fld in ColorizedArgsFormatter.level_fields:
                search = "(%\(" + fld + "\).*?s)"
                _format = re.sub(search, f"{color}\\1{ColorCodes.reset}", _format)
            if datefmt:
                formatter = logging.Formatter(_format, datefmt=datefmt)
            else:
                formatter = logging.Formatter(_format)
            self.level_to_formatter[level] = formatter

        add_color_format(logging.DEBUG)
        add_color_format(logging.INFO)
        add_color_format(logging.WARNING)
        add_color_format(logging.ERROR)
        add_color_format(logging.CRITICAL)

    @staticmethod
    def rewrite_record(record: logging.LogRecord):
        if not BraceFormatStyleFormatter.is_brace_format_style(record):
            return

        msg = record.msg
        msg = msg.replace("{", "_{{")
        msg = msg.replace("}", "_}}")
        placeholder_count = 0
        # add ANSI escape code for next alternating color before each formatting parameter
        # and reset color after it.
        while True:
            if "_{{" not in msg:
                break
            color_index = placeholder_count % len(ColorizedArgsFormatter.arg_colors)
            color = ColorizedArgsFormatter.arg_colors[color_index]
            msg = msg.replace("_{{", color + "{", 1)
            msg = msg.replace("_}}", "}" + ColorCodes.reset, 1)
            placeholder_count += 1

        record.msg = msg.format(*record.args)
        record.args = []

    def format(self, record):
        orig_msg = record.msg
        orig_args = record.args
        record.levelname = self.level_names.get(record.levelno, record.levelname)
        formatter = self.level_to_formatter.get(record.levelno)
        self.rewrite_record(record)
        formatted = formatter.format(record)
        record.msg = orig_msg
        record.args = orig_args
        return formatted


class BraceFormatStyleFormatter(logging.Formatter):
    def __init__(self, fmt: str):
        super().__init__()
        self.formatter = logging.Formatter(fmt)

    @staticmethod
    def is_brace_format_style(record: logging.LogRecord):
        if len(record.args) == 0:
            return False

        msg = record.msg
        if '%' in msg:
            return False

        count_of_start_param = msg.count("{")
        count_of_end_param = msg.count("}")

        if count_of_start_param != count_of_end_param:
            return False

        if count_of_start_param != len(record.args):
            return False

        return True

    @staticmethod
    def rewrite_record(record: logging.LogRecord):
        if not BraceFormatStyleFormatter.is_brace_format_style(record):
            return

        record.msg = record.msg.format(*record.args)
        record.args = []

    def format(self, record):
        orig_msg = record.msg
        orig_args = record.args
        self.rewrite_record(record)
        formatted = self.formatter.format(record)
        
        # restore log record to original state for other handlers
        record.msg = orig_msg
        record.args = orig_args
        return formatted
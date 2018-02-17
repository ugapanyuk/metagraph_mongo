# -*- coding: utf-8 -*-

class DataHelper():
    """
    Вспомогательный класс
    """

    indent = "|  "

    @staticmethod
    def PrintWithLevel(string_to_print: str, level: int):
        indent_str = ""
        if level > 1:
            indent_str = DataHelper.indent * (level-1)
        if level > 0:
            indent_str = indent_str + "|->"
        print(indent_str + string_to_print)
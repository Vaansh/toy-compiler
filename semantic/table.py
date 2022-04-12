#! /usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, Union

from semantic.record import Record, VarRecord


class SymbolTable:
    def __init__(self, name: str, level: int, link: Optional["SymbolTable"]) -> None:
        self.name = None
        self.list = []
        self.size = 0
        self.level = 0
        self.link = None
        self.offset = 0

        if name:
            self.name = name

        if level and link:
            self.list = []
            self.level = level
            self.link = link

    def check_records(self, lookup: Union[VarRecord, str]) -> Record:
        return_value = Record()
        found = False
        for r in self.list:
            if lookup == r.name:
                return_value = r
                found = True
        if not found:
            if self.link:
                return_value = self.link.check_records(lookup)

        return return_value

    def __repr__(self):
        return self.__str__()

    def __str__(self, indentation: Optional[int] = None) -> str:
        res, indent = "", ""
        indent += (
            (("|" + "  ") * self.level)
            if not indentation
            else (self._str_helper(indentation, self.level))
        )
        res += (
            "\n"
            + indent
            + ("  " * indentation if indentation else "")
            + ("=" * 120)
            + "\n"
        )
        res += (
            indent
            + ("  " * indentation if indentation else "")
            + "|  table:  "
            + self.name
            + "  |  scope offset: "
            + str(self.offset)
            + "\n"
        )
        res += indent + ("  " * indentation if indentation else "") + ("=" * 120) + "\n"

        for record in self.list:
            res += (
                indent
                + ("  " * indentation if indentation else "")
                + str(record)
                + "\n"
            )

        res += indent + ("  " * indentation if indentation else "") + ("=" * 120)
        return res

    def _str_helper(self, indentation: int, level: int) -> str:
        res = "|  " + ("  " * indentation if indentation else "")
        for i in range(level - 1):
            res += "|" + ("  " * i)
        return res

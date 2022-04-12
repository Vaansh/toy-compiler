#! /usr/bin/python
# -*- coding: utf-8 -*-

from typing import List, Union

from lexer.util import *


class Reader:
    def __init__(self, source_code: List[str]) -> None:
        """Method constructor.

        Args:
            source_code (List[str]): source code split into lines.
        """
        self.source_code = source_code
        self.line_number, self.curr_index, self.index = 0, 0, 0

    def next_character(self) -> Union[int, str]:
        """Function that moves current index to next character.

        Returns:
            Union[int, str]: returns next character. 0 if end of file.
        """
        next_character = 0

        if self.end_of_file():
            return 0

        if self.curr_index < len(self.source_code[self.line_number]):
            next_character = self.source_code[self.line_number][self.curr_index]
            self.index = self.curr_index
            self.curr_index += 1

        elif self.line_number < len(self.source_code):
            next_character, self.curr_index = "\n", 0
            self.index = self.curr_index
            self.line_number += 1

        return next_character

    def backup_character(self) -> None:
        """Function that moves current index to previoud character."""
        if len(self.source_code) == 0 or (
            self.line_number <= 0 and self.curr_index <= 0
        ):
            return

        if self.curr_index > 0:
            self.curr_index -= 1

        elif self.line_number > 0:
            self.line_number -= 1
            self.curr_index = (
                0
                if self.source_code[self.line_number] == 0
                else int(len(self.source_code[self.line_number]))
            )

        self.index = self.curr_index

    def scan_id(self) -> str:
        """Scans ID. Form: id ::= letter alphanum*

        Returns:
            str: scanned ID.
        """
        res_id = ""
        c = self.next_character()

        if is_letter(c):
            res_id += c
            c = self.next_character()
            while is_alphanum(c):
                res_id += c
                c = self.next_character()
            if c and c != 0:
                self.backup_character()

        return res_id

    def scan_integer(self) -> str:
        """Scans integer. Form: integer ::= nonzero digit* | 0

        Returns:
            str: scanned integer.
        """
        res_integer = ""
        c = self.next_character()

        if c == "0":
            res_integer = c
        else:
            while is_digit(c):
                res_integer += c
                c = self.next_character()
            if c and c != 0:
                self.backup_character()

        return res_integer

    def scan_fraction(self) -> str:
        """Scans fraction. Form: fraction ::= .digit* nonzero | .0

        Returns:
            str: scanned fraction.
        """
        res_fraction = ""
        c = self.next_character()

        if c == ".":
            res_fraction += c
            c = self.next_character()
            if c == "0":
                res_fraction += c
                c = self.next_character()
                if not is_digit(c):
                    if c and c != 0:
                        self.backup_character()
                elif is_digit(c):
                    self.backup_character()
                    res_fraction += self.scan_fraction_aux()
            elif is_nonzero(c):
                self.backup_character()
                res_fraction += self.scan_fraction_aux()
            else:
                [self.backup_character() for _ in range(2)]
                res_fraction = res_fraction[-1]

        return res_fraction

    def scan_fraction_aux(self) -> str:
        """Scans fraction_aux. Form: fraction_aux ::= digit* nonzero

        Returns:
            str: scanned fraction_aux.
        """
        res_fraction_aux = ""

        c = self.next_character()
        while is_digit(c):
            res_fraction_aux += c
            c = self.next_character()

        if c and c != 0:
            self.backup_character()

        if not is_nonzero(res_fraction_aux[-1]):
            while len(res_fraction_aux) != 0 and not is_nonzero(res_fraction_aux[-1]):
                res_fraction_aux = res_fraction_aux[:-1]
                self.backup_character()

        return res_fraction_aux

    def scan_float_aux(self) -> str:
        """Scans scan_float_aux. Form: scan_float_aux ::= e [+|-] integer

        Returns:
            str: scanned scan_float_aux.
        """
        res_scan_float_aux, sign_flag = "", False
        c = self.next_character()

        if c == "e":
            res_scan_float_aux += c
            c = self.next_character()

            if c in ["+", "-"]:
                res_scan_float_aux += c
                c = self.next_character()
                sign_flag = True

            integer = ""
            if is_digit(c):
                if c and c != 0:
                    self.backup_character()
                integer = self.scan_integer()
            if len(integer) == 0:
                [self.backup_character() for _ in range(2)]
                res_scan_float_aux = res_scan_float_aux[:-1]
                if sign_flag:
                    self.backup_character()
                    res_scan_float_aux = res_scan_float_aux[:-1]
            else:
                res_scan_float_aux += integer

        return res_scan_float_aux

    def end_of_file(self) -> bool:
        """Function that returns true if end of file has been reached.

        Returns:
            bool: returns whether end of file has been reached.
        """
        return len(self.source_code) == 0 or (
            self.curr_index >= len(self.source_code[self.line_number])
            and self.line_number + 1 >= len(self.source_code)
        )

    def coordinates(self) -> List[int]:
        """Function to make the reader return current pointer coordinates.

        Returns:
            List[int]: current coordinates.
        """
        return [self.line_number, self.index]

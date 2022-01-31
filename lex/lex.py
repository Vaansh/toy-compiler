from lex.token import Token
from typing import List, Tuple, Union

from lex.reader import Reader
from lex.regex import *


class Lexer:
    RESERVED = [
        "if",
        "public",
        "read",
        "then",
        "private",
        "write",
        "else",
        "return",
        "integer",
        "var",
        "self",
        "float",
        "struct",
        "inherits",
        "void",
        "while",
        "let",
        "func",
        "impl",
    ]
    LEXEME_MAP = {
        ".": "dot",
        "+": "plus",
        "*": "mult",
        ";": "semi",
        ",": "comma",
        "!": "not",
        "(": "openpr",
        ")": "closepr",
        "{": "opencpr",
        "}": "closecpr",
        "[": "openspr",
        "]": "closespr",
        "&": "and",
        "|": "or",
    }

    def __init__(self, source_code: List[str]) -> None:
        """Method constructor.

        Args:
            source_code (List[str]): source code split into lines.
        """
        self.reader = Reader(source_code)

    def next_token(self) -> Union[None, Token]:
        """Method to get next token.

        Returns:
            Union[None, Token]: created token.
        """
        token, lexeme = None, ""
        c = self.next_character()

        while is_space(c):
            c = self.next_character()

        coordinates = self.get_location()
        if c == 0:
            return self.create_token("eof", lexeme, coordinates)

        if is_letter(c):
            token = self.handle_id(coordinates)
        elif c == "0":
            token = self.handle_invalid_float(coordinates, lexeme, c)
        elif is_digit(c):
            token = self.handle_digit(coordinates)
        else:
            token_kind = self.LEXEME_MAP.get(c, "UNMAPPED")
            # use lexeme map if a key-value pair exists.
            if token_kind != "UNMAPPED":
                return self.create_token(token_kind, c, coordinates)

            if c == "=":
                c, token = self.handle_unmapped(
                    "=", "eq", "==", "assgn", "=", coordinates
                )
            elif c == ">":
                c, token = self.handle_unmapped(
                    "=", "greateq", ">=", "gt", ">", coordinates
                )
            elif c == "-":
                c, token = self.handle_unmapped(
                    ">", "arrow", "->", "minus", "-", coordinates
                )
            elif c == ":":
                c, token = self.handle_unmapped(
                    ":", "sro", "::", "colon", ":", coordinates
                )
            elif c == "<":
                token = self.handle_less_than(coordinates)
            elif c == "/":
                token = self.handle_comment_or_div(coordinates)
            elif c == "_":
                lexeme = c
                c = self.next_character()
                if not is_space(c):
                    while not is_space(c):
                        lexeme += c
                        c = self.next_character()
                token = self.create_token(
                    "invalidchar" if len(lexeme) == 1 else "invalidid",
                    lexeme,
                    coordinates,
                )
                self.backup_character()
            else:
                token = self.create_token("invalidchar", c, coordinates)

        return token

    def handle_id(self, coordinates: List[int]) -> Token:
        """Function to handle id token.

        Args:
            coordinates (List[int]): coordinates of token.

        Returns:
            Token: created token.
        """
        self.backup_character()
        lexeme = self.reader.scan_id()
        tokenType = lexeme if lexeme in self.RESERVED else "NOT_RESERVED"

        token = self.create_token(
            "id" if tokenType == "NOT_RESERVED" else tokenType,
            lexeme,
            coordinates,
        )

        return token

    def handle_invalid_float(
        self, coordinates: List[int], lexeme: str, c: str
    ) -> Token:
        """Function to handle invalidfloat token.

        Args:
            coordinates (List[int]): coordinates of token.
            lexeme (str): value of token.

        Returns:
            Token: created token.
        """
        lexeme += c
        c = self.next_character()

        if is_space(c):
            return self.handle_digit(coordinates, zero_err_case=True)

        while not is_space(c):
            lexeme += c
            c = self.next_character()
            if c not in self.LEXEME_MAP.keys():
                [self.backup_character() for _ in range(2)]
                return self.create_token("int", "0", coordinates)
        token = self.create_token("invalidfloat", lexeme, coordinates)

        return token

    def handle_digit(
        self, coordinates: List[int], zero_err_case: bool = False
    ) -> Token:
        """Function to handle digit token.

        Args:
            coordinates (List[int]): coordinates of token.
            zero_err_case (bool): flag to handle zero error case. Defaults to False.

        Returns:
            Token: created token.
        """
        if zero_err_case:
            return self.create_token("int", "0", coordinates)

        self.backup_character()
        lexeme = self.reader.scan_integer()
        c = self.next_character()

        if c == ".":
            self.backup_character()
            res_fraction = self.reader.scan_fraction()
            if len(res_fraction) != 0:
                lexeme += res_fraction
                c = self.next_character()
                if c == "e":
                    self.backup_character()
                    res_fraction = self.reader.scan_float_aux()
                    if len(res_fraction) != 0:
                        lexeme += res_fraction
                else:
                    self.backup_character()

                if lexeme[-1] == ".":
                    self.backup_character()
                    return self.create_token("int", lexeme[:-1], coordinates)

                token = self.create_token("float", lexeme, coordinates)
            else:
                token = self.create_token("int", lexeme, coordinates)
        else:
            self.backup_character()
            token = self.create_token("int", lexeme, coordinates)

        return token

    def handle_unmapped(
        self,
        next_character: str,
        next_token_kind: str,
        next_lexeme: str,
        token_kind: str,
        lexeme: str,
        coordinates: List[int],
    ) -> Tuple[str, Token]:
        """Function to handle unmapped token.

        Args:
            next_character (str): next character read by the reader.
            next_token_kind (str): next token kind.
            next_lexeme (str): next token value.
            token_kind (str): type of token.
            lexeme (str): value of token.
            coordinates (List[int]): coordinates of token.

        Returns:
            Tuple[str, Token]: current character and created token.
        """
        c = self.next_character()
        if c == next_character:
            token = self.create_token(next_token_kind, next_lexeme, coordinates)
        else:
            self.backup_character(c)
            token = self.create_token(token_kind, lexeme, coordinates)

        return c, token

    def handle_less_than(self, coordinates: List[int]) -> Token:
        """Function to handle tokens created when less than character is rader.

        Args:
            coordinates (List[int]): coordinates of token.

        Returns:
            Token: created token.
        """
        c = self.next_character()

        if c == ">":
            token = self.create_token("neq", "<>", coordinates)
        elif c == "=":
            token = self.create_token("lesseq", "<=", coordinates)
        else:
            self.backup_character(c)
            token = self.create_token("lt", "<", coordinates)

        return token

    def handle_comment_or_div(self, coordinates: List[int]) -> Token:
        """Function to handle tokens created when slash character is rader.

        Args:
            coordinates (List[int]): coordinates of token.

        Returns:
            Token: created token.
        """
        c = self.next_character()
        comment_res = ""
        if c == "/":
            c = self.next_character()
            while c != "\n" and c != 0:
                comment_res += c
                c = self.next_character()
            token = self.create_token("inlinecmt", comment_res, coordinates)
        elif c == "*":
            while True:
                c = self.next_character()
                while c != "*" and c != 0:
                    comment_res += c
                    c = self.next_character()
                if c == "*":
                    c = self.next_character()
                    if c != "/":
                        comment_res += "*"
                        self.backup_character()
                    else:
                        token = self.create_token(
                            "blockcmt",
                            comment_res.encode("unicode_escape"),
                            coordinates,
                        )
                        break
                elif c == 0:
                    token = self.create_token(
                        "unclosedcmt",
                        "Unclosed multi-line comment",
                        coordinates,
                    )
                    break
        else:
            self.backup_character()
            token = self.create_token("div", "/", coordinates)

        return token

    def next_character(self) -> Union[int, str]:
        """Wrapper function to make the reader read next character.

        Returns:
            Union[int, str]: next character.
        """
        return self.reader.next_character()

    def backup_character(self, c: str = None) -> None:
        """Wrapper function to make the reader back up a character.

        Args:
            c (str, optional): next character. Defaults to None.
        """
        if c and c != 0:
            self.reader.backup_character()
        else:
            self.reader.backup_character()

    def get_location(self) -> List[int]:
        """Wrapper function to make the reader return current pointer coordinates.

        Returns:
            List[int]: current coordinates.
        """
        return self.reader.coordinates()

    def create_token(
        self, token_kind: str, lexeme: str, coordinates: List[int]
    ) -> Token:
        """Function that returns a new token.

        Args:
            token_kind (str): type of token to be created.
            lexeme (str): value of token to be created.
            coordinates (List[int]): coordinates of token to be created.

        Returns:
            Token: token to create.
        """
        return Token(token_kind, lexeme, coordinates[0], coordinates[1])

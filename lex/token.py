class Token:
    ERROR_KINDS = ["invalidchar", "invalidid", "invalidfloat", "unclosedcmt"]

    def __init__(
        self, token_kind: str, lexeme: str, src_row: int, src_column: int
    ) -> None:
        """Method constructor.

        Args:
            token_kind (str): type of token.
            lexeme (str): value of token.
            src_row (int): line number.
            src_column (int): line index.
        """
        self.token_kind = token_kind.lower()
        self.lexeme = lexeme
        self.src_row = src_row + 1
        self.src_column = src_column + 1

    def __repr__(self) -> str:
        """String value.

        Returns:
            str: string value of token.
        """
        return self.__str__()

    def __str__(self) -> str:
        """String value.

        Returns:
            str: token information.
        """
        return "[{}, {}, {}, {}]".format(
            self.token_kind, self.lexeme, self.src_row, self.src_column
        )

    def is_error(self) -> bool:
        """Determines if token is an error.

        Returns:
            bool: boolean value of error.
        """
        return self.token_kind in self.ERROR_KINDS

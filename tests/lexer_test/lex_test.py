#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

from lexer.lex import Lexer

test_src_paths = [
    test_src_path
    for test_src_path in os.listdir("tests/lexer_test/cases/")
    if test_src_path != ".DS_Store"
]


def lexer_test() -> None:
    """Main test function."""
    print("List of files found:", test_src_paths)
    for t in test_src_paths:
        if t.endswith(".src"):
            lex_driver(file_path(t), output_path(t), error_path(t), False)
        else:
            print("\nSkipping file ({}) because it doesn't end with .src".format(t))
            continue


def file_path(t: str) -> str:
    """Returns file path."""
    return "tests/lexer_test/cases/" + t


def output_path(t: str) -> str:
    """Returns output path."""
    return "tests/lexer_test/results/" + t.split(".")[0] + ".outlextokens"


def error_path(t: str) -> str:
    """Returns error path."""
    return "tests/lexer_test/errors/" + t.split(".")[0] + ".outlexerrors"


def lex_driver(
    file_path: str, output_path: str, error_path: str, debug: bool = True
) -> None:
    """Driver function that writes/logs the results in the respective files.

    Args:
        file_path (str): path of source code file.
        output_path (str): path of output token file.
        error_path (str): path of invalid tokens file.
        debug (bool, optional): Prints token to console when program is run. Defaults to True.
    """
    file, output_file, error_file = (
        open(file_path),
        open(output_path, "w"),
        open(error_path, "w"),
    )

    source_code = file.readlines()

    if len(source_code) == 0:
        error_msg = "\nEmpty file, no such file at: {}".format(file_path)
        print(error_msg)
        error_file.write(error_msg[1:])
        print("Error log stored at: {}".format(error_path))
        return
    else:
        source_code[-1] += "\n"

    print("\nTokenizing source code file at: {}".format(file_path))
    lex = Lexer(source_code)
    token = lex.next_token()

    output_file, error_file = open(output_path, "a"), open(error_path, "a")
    while token.token_kind != "eof":
        if debug:
            print(token)

        if token.is_error():
            error_file.write(token.__repr__() + "\n")
        else:
            output_file.write(token.__repr__() + "\n")

        token = lex.next_token()

    print("Output tokens generated and stored at: {}".format(output_path))
    print("Invalid tokens and error logs stored at: {}".format(error_path))

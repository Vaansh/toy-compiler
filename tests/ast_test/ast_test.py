#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
from parser.parser import Parser

test_src_paths = [
    test_src_path
    for test_src_path in os.listdir("tests/ast_test/cases/")
    if test_src_path != ".DS_Store"
]


def ast_test() -> None:
    """Main test function."""
    print("List of files found:", test_src_paths)
    for t in test_src_paths:
        if t.endswith(".src"):
            ast_driver(
                file_path(t),
                output_path(t),
                error_path(t),
                tree_output_path(t),
                lex_output_path(t),
                lex_err_path(t),
            )
        else:
            print("\nSkipping file ({}) because it doesn't end with .src".format(t))
            continue


def file_path(t: str) -> str:
    """Returns file path."""
    return "tests/ast_test/cases/" + t


def tree_output_path(t: str) -> str:
    """Returns output path."""
    return "tests/ast_test/results/" + t.split(".")[0] + ".outast"


def output_path(t: str) -> str:
    """Returns output path."""
    return "tests/ast_test/results/" + t.split(".")[0] + ".outderivation"


def error_path(t: str) -> str:
    """Returns error path."""
    return "tests/ast_test/errors/" + t.split(".")[0] + ".outsyntaxerrors"


def lex_output_path(t: str) -> str:
    """Returns output path."""
    return "tests/ast_test/results/" + t.split(".")[0] + ".outlextokens"


def lex_err_path(t: str) -> str:
    """Returns error path."""
    return "tests/ast_test/errors/" + t.split(".")[0] + ".outlexerrors"


def ast_driver(
    file_path: str,
    output_path: str,
    error_path: str,
    tree_output_path: str,
    lex_output_path: str,
    lex_err_path: str,
) -> None:
    """Driver function that writes/logs the results in the respective files.

    Args:
        file_path (str): path of source code file.
    """
    p = Parser(
        file_path,
        output_path,
        error_path,
        lex_output_path,
        lex_err_path,
        tree_output_path,
        debug=False,
    ).parse()
    print("\nGenerating AST for source code file at: {0}".format(file_path))
    print("Output tokens generated and stored at: {0}".format(lex_output_path))
    print("Invalid tokens and error logs stored at: {0}".format(lex_err_path))
    print("Derivation for the file stored at: {0}".format(output_path + " "))
    print("Syntax errors for the file stored at: {0}".format(error_path))
    print("AST Tree for the file stored at: {0}".format(tree_output_path + " "))

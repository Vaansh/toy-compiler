#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
from parser.parser import Parser

test_src_paths = [
    test_src_path
    for test_src_path in os.listdir("tests/semantic_test/cases/")
    if test_src_path != ".DS_Store"
]


def semantic_test() -> None:
    """Main test function."""
    print("List of files found:", test_src_paths)
    for t in test_src_paths:
        if t.endswith(".src"):
            sem_driver(
                file_path(t),
                output_path(t),
                error_path(t),
                lex_output_path(t),
                lex_err_path(t),
                sem_err_path(t),
                tree_output_path(t),
                sym_tab_output_path(t),
            )
        else:
            print("\nSkipping file ({}) because it doesn't end with .src".format(t))
            continue


def file_path(t: str) -> str:
    """Returns file path."""
    return "tests/semantic_test/cases/" + t


def tree_output_path(t: str) -> str:
    """Returns output path."""
    return "tests/semantic_test/results/" + t.split(".")[0] + ".outast"


def sym_tab_output_path(t: str) -> str:
    """Returns output path."""
    return "tests/semantic_test/results/" + t.split(".")[0] + ".outsymboltable"


def output_path(t: str) -> str:
    """Returns output path."""
    return "tests/semantic_test/results/" + t.split(".")[0] + ".outderivation"


def error_path(t: str) -> str:
    """Returns error path."""
    return "tests/semantic_test/errors/" + t.split(".")[0] + ".outsyntaxerrors"


def lex_output_path(t: str) -> str:
    """Returns output path."""
    return "tests/semantic_test/results/" + t.split(".")[0] + ".outlextokens"


def lex_err_path(t: str) -> str:
    """Returns error path."""
    return "tests/semantic_test/errors/" + t.split(".")[0] + ".outlexerrors"


def sem_err_path(t: str) -> str:
    """Returns error path."""
    return "tests/semantic_test/errors/" + t.split(".")[0] + ".outsemanticerrors"


def sem_driver(
    file_path: str,
    output_path: str,
    error_path: str,
    lex_output_path: str,
    lex_err_path: str,
    sem_err_path: str,
    tree_output_path: str,
    sym_tab_output_path: str,
) -> None:
    """Driver function that writes/logs the results in the respective files.

    Args:
        file_path (str): path of source code file.
    """
    Parser(
        file_path,
        output_path,
        error_path,
        lex_output_path,
        lex_err_path,
        tree_output_path,
        sem_err_path=sem_err_path,
        sem=sym_tab_output_path,
        debug=False,
        sem_test=True,
    ).parse()
    print(
        "\nGenerating symbol table and performing type checks for source code file at: {0}".format(
            file_path
        )
    )
    print("Output tokens generated and stored at: {0}".format(lex_output_path))
    print("Invalid tokens and error logs stored at: {0}".format(lex_err_path))
    print("Derivation for the file stored at: {0}".format(output_path + " "))
    print("Syntax errors for the file stored at: {0}".format(error_path))
    print("AST Tree for the file stored at: {0}".format(tree_output_path + " "))
    print("Symbol Table for the file stored at: {0}".format(sym_tab_output_path + " "))
    print(
        "Semantic Errors/Warning for the file stored at: {0}".format(sem_err_path + " ")
    )

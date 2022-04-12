#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os.path
import random
import sys
from datetime import datetime
from parser.parser import Parser
from pathlib import Path

from prettytable import PrettyTable


class background:
    BLUE = "\033[94m"
    CRITICAL = "\033[91m"
    CYAN = "\033[96m"
    FIN = "\033[0m"
    GREEN = "\033[92m"
    PURPLE = "\033[95m"
    RED = "\033[91m"
    STRONG = "\033[1m"
    YELLOW = "\033[93m"


header_table = PrettyTable()

header_table.field_names = ["Course", "Semester", "Professor", "Author"]

header_table.add_row(
    [
        "COMP 442 - Compiler Design",
        "Winter 2022",
        "Dr. Joey Paquet",
        "Vaansh Vikas Lakhwara",
    ]
)

DESC = (
    str(header_table)
    + """\n\nMoon Compiler.
A moon compiler written for the course COMP 442 at Concordia University.        

"""
)


def main():
    parser = argparse.ArgumentParser(
        description=DESC, formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "file",
        action="store",
        help="input file to be compiled (format: 'source/*.src').",
    )

    args = parser.parse_args()
    if not (args.file.startswith("source/") and args.file.endswith(".src")):
        print(background.RED + "Invalid file format." + background.FIN)
        print(
            background.YELLOW
            + "Ensure your file is placed in the 'source/' directory and ends with .src"
            + background.FIN
        )
        return

    if os.path.isfile(args.file):
        compile(args.file)
        return

    print("Couldn't find file on path. Make sure source file exists")


def location_handler(filepath):
    filepath = filepath
    now = datetime.now()
    hash_determiner = hash(
        ("{}-{}".format(now.strftime("%d/%m/%Y-%H:%M:%S"), filepath.split(".")[0]))
    )
    while hash_determiner in list(Path("./").glob("results/*")):
        hash_determiner = hash(
            ("{}-{}".format(now.strftime("%d/%m/%Y-%H:%M:%S"), filepath.split(".")[0]))
        )
    hash_determiner += sys.maxsize + 1
    hash_determiner = str(hash_determiner)
    _path_name_helper = "results/" + hash_determiner + "/" + filepath.split(".")[0]
    tree_output_path = _path_name_helper + ".outast"
    sym_tab_output_path = _path_name_helper + ".outsymboltable"
    output_path = _path_name_helper + ".outderivation"
    error_path = _path_name_helper + ".outsyntaxerrors"
    lex_output_path = _path_name_helper + ".outlextokens"
    lex_err_path = _path_name_helper + ".outlexerrors"
    sem_err_path = _path_name_helper + ".outsemanticerrors"
    code_gen_output_path = _path_name_helper + ".moon"

    return (
        (
            ("source/" + filepath),
            output_path,
            error_path,
            lex_output_path,
            lex_err_path,
            tree_output_path,
            sem_err_path,
            sym_tab_output_path,
            False,
        ),
        code_gen_output_path,
        hash_determiner,
    )


def compile(filepath):
    filepath = filepath.split("/", 1)[1]
    res = location_handler(filepath)

    parser_args, gen_output_loc, hash_val = res[0], res[1], res[2]
    os.mkdir("results/" + hash_val)
    Parser(
        path=parser_args[0],
        output_path=parser_args[1],
        error_path=parser_args[2],
        lex_output_path=parser_args[3],
        lex_err_path=parser_args[4],
        tree_output_path=parser_args[5],
        sem_err_path=parser_args[6],
        sem=parser_args[7],
        sem_test=parser_args[8],
        debug=True,
    ).parse()

    process_message = """

        ▄████████  ▄██████▄    ▄▄▄▄███▄▄▄▄      ▄███████▄  ▄█   ▄█        ▄█  ███▄▄▄▄      ▄██████▄  
        ███    ███ ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███ ███  ███       ███  ███▀▀▀██▄   ███    ███ 
        ███    █▀  ███    ███ ███   ███   ███   ███    ███ ███▌ ███       ███▌ ███   ███   ███    █▀  
        ███        ███    ███ ███   ███   ███   ███    ███ ███▌ ███       ███▌ ███   ███  ▄███        
        ███        ███    ███ ███   ███   ███ ▀█████████▀  ███▌ ███       ███▌ ███   ███ ▀▀███ ████▄  
        ███    █▄  ███    ███ ███   ███   ███   ███        ███  ███       ███  ███   ███   ███    ███ 
        ███    ███ ███    ███ ███   ███   ███   ███        ███  ███▌    ▄ ███  ███   ███   ███    ███ 
        ████████▀   ▀██████▀   ▀█   ███   █▀   ▄████▀      █▀   █████▄▄██ █▀    ▀█   █▀    ████████▀  
                                                                  ▀                                     

    """
    print("=" * 111)
    print(
        random.choice(
            [
                background.PURPLE,
                background.BLUE,
                background.CYAN,
                background.GREEN,
                background.RED,
                background.YELLOW,
            ]
        )
        + background.STRONG
        + process_message
        + background.FIN
    )

    line = background.STRONG + random.choice(
        [
            background.PURPLE,
            background.BLUE,
            background.CYAN,
            background.GREEN,
            background.RED,
            background.YELLOW,
        ]
    )
    half_line = (
        line + "                    ----------------------------   " + background.FIN
    )
    dot = "[X]"
    out = (
        half_line
        + random.choice(
            [
                background.PURPLE,
                background.BLUE,
                background.CYAN,
                background.GREEN,
                background.RED,
                background.YELLOW,
            ]
        )
        + background.STRONG
        + dot
        + line
        + "                    ----------------------------   "[::-1]
        + background.FIN
    )
    print(out)
    output = PrettyTable()
    output.field_names = ["STAGE", "OUTPUT"]

    output.add_row(["Compiling for source code file at:", parser_args[0] + " "])
    output.add_row(["Output tokens generated and stored at:", parser_args[3] + " "])
    output.add_row(["Invalid tokens and error logs stored at:", parser_args[4] + " "])
    output.add_row(["Derivation for the file stored at:", parser_args[1]])
    output.add_row(["Syntax errors for the file stored at:", parser_args[2]])
    output.add_row(["AST Tree for the file stored at:", parser_args[5]])
    output.add_row(["Symbol Table for the file stored at:", parser_args[7]])
    output.add_row(["Semantic Errors/Warning for the file stored at:", parser_args[6]])
    output.add_row(["Moon file for the file stored at:", gen_output_loc])

    print(str(output))

    return


if __name__ == "__main__":
    main()

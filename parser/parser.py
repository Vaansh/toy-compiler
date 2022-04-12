#! /usr/bin/python
# -*- coding: utf-8 -*-

from parser.ast_handler import ASTHandler
from parser.util import *

from lexer.lex import Lexer
from semantic.action import ActionKinds


class Parser:
    TERMINALS = [
        "and",
        "arrow",
        "assgn",
        "closecpr",
        "closepr",
        "closespr",
        "colon",
        "comma",
        "div",
        "dot",
        "else",
        "eq",
        "equal",
        "float",
        "floatlit",
        "func",
        "greateq",
        "gt",
        "id",
        "if",
        "impl",
        "inherits",
        "integer",
        "intlit",
        "invalid",
        "lesseq",
        "let",
        "lt",
        "minus",
        "mult",
        "neq",
        "not",
        "opencpr",
        "openpr",
        "openspr",
        "or",
        "plus",
        "private",
        "public",
        "read",
        "return",
        "semi",
        "struct",
        "then",
        "void",
        "while",
        "write",
    ]
    DOLLAR = "$"
    REPEAT = "progRep"
    START = "START"
    TOKENS = []

    def __init__(
        self,
        path,
        output_path,
        error_path,
        lex_output_path,
        lex_err_path,
        tree_output_path=None,
        sem_err_path=None,
        sem=None,
        sem_test=False,
        debug=True,
    ):
        self.path = path

        self.lex = Lexer(open(path).readlines())
        (
            self.output_path,
            self.error_path,
            self.lex_output_path,
            self.lex_err_path,
            self.tree_output_path,
            self.sem_err_path,
        ) = (
            output_path,
            error_path,
            lex_output_path,
            lex_err_path,
            tree_output_path,
            sem_err_path,
        )
        self.sem_test = sem_test
        self.first, self.follow = first_and_follow()
        self.parser_table = build_parse_table()
        self.sem_map = semantic_actions_mapper()
        self.sem_stack = []
        self.debug = debug
        self.tree_file, self.sem_file = None, sem

    def parse(self):
        stack, derivation, error = [Parser.START], [Parser.START], False

        with open(self.lex_output_path, "w") as lex_output_path:
            lex_output_path.write("")
        self.lex_output_path = open(self.lex_output_path, "a")

        with open(self.lex_err_path, "w") as lex_err_path:
            lex_err_path.write("")
        self.lex_err_path = open(self.lex_err_path, "a")

        with open(self.error_path, "w") as error_file:
            error_file.write("")
        error_file = open(self.error_path, "a")

        with open(self.output_path, "w") as derivation_file:
            derivation_file.write("")
        derivation_file = open(self.output_path, "a")

        if self.tree_output_path:
            with open(self.tree_output_path, "w") as tree_file:
                tree_file.write("=" * 102 + "\n")
                tree_file.write("|{:^69}|{:^30}|".format("Tree", "Lexeme") + "\n")
                tree_file.write("=" * 102 + "\n")
            self.tree_file = open(self.tree_output_path, "a")

        token = self.retrieve_token()

        if token.token_kind == "eof":
            print("EMPTY FILE.")
            error = True
            return error

        while stack and stack[-1] != Parser.DOLLAR:
            x = stack[-1]
            if self.is_semantic_action(x):
                self.sem_stack.append(
                    self.sem_map["Epsilon" if x[1:] == "EP" else x[1:]]
                )
                stack.pop()
                continue

            if x in Parser.TERMINALS:
                if x == token.token_kind:
                    stack.pop()
                    token = self.retrieve_token()
                    if token.token_kind == "EOF":
                        break
                else:
                    token, stack = self.error_recovery(
                        token,
                        stack,
                        self.first.get(x, ""),
                        self.follow.get(x, ""),
                        error_file,
                    )
                    error = True
                    if token == stack == "EOF":
                        break
            else:
                try:
                    table_rule = self.parser_table[x][token.token_kind]
                    derivation = self.derive(
                        derivation, stack, table_rule, derivation_file
                    )
                    stack.pop()
                    stack = self.inverse_rhs_multiple_push(stack, table_rule)
                except KeyError:
                    if self.lex.reader.end_of_file() and x == Parser.REPEAT:
                        derivation = self.derive(
                            derivation,
                            stack,
                            self.parser_table[x][Parser.DOLLAR],
                            derivation_file,
                        )
                        stack.pop()
                    else:
                        token, stack = self.error_recovery(
                            token, stack, self.first[x], self.follow[x], error_file
                        )
                        error = True
                        if token == stack == "EOF":
                            break
        if self.tree_file:
            ASTHandler(
                self.sem_stack,
                self.sem_file,
                self.tree_file,
                Parser.TOKENS,
                self.sem_test,
                self.sem_err_path,
            )

        return error

    def derive(self, derivation, stack, value, derivation_file):
        for i in range(len(derivation)):
            if derivation[i] == stack[-1]:
                _value = list(filter(lambda a: a != ActionKinds.EP.upper(), value))
                next_derivation_lhs = derivation[i]
                derivation = derivation[:i] + _value + derivation[i + 1 :]
                break

        _derivation = ""
        for d in derivation:
            if not self.is_semantic_action(d):
                _derivation += d + " "
        derivation_file.write(
            ("START " if next_derivation_lhs == Parser.START else "      ")
            + "=> "
            + _derivation
            + "\n"
        )

        return derivation

    def error_recovery(self, token, stack, first_set, follow_set, error_file):
        if self.debug:
            print(
                background.CRITICAL
                + "\nSyntactic Error(s): "
                + background.FIN
                + background.YELLOW
                + "logged in file - {0}".format(self.error_path)
                + background.FIN
            )
            self.debug = False
        if stack[-1] in Parser.TERMINALS:
            while token.token_kind != stack[-1]:
                error_file.write(
                    "Syntax error found on line {0} : token = {1}\n".format(
                        token.src_row, token
                    )
                )
                token = self.retrieve_token()
                if token.token_kind == "eof":
                    return "EOF", "EOF"
            return token, stack
        if token.token_kind in follow_set:
            error_file.write(
                "Syntax error found on line {0} : token = {1}\n".format(
                    token.src_row, token
                )
            )
            stack.pop()
        else:
            while token.token_kind not in first_set or (
                ActionKinds.EP.upper() in first_set
                and token.token_kind not in follow_set
            ):
                error_file.write(
                    "Syntax error found on line {0} : token = {1}\n".format(
                        token.src_row, token
                    )
                )
                token = self.retrieve_token()
                if token.token_kind == "eof":
                    return "EOF", "EOF"
        return token, stack

    def retrieve_token(self):
        token = self.lex.next_token()
        self.lex_output_path.write(str(token) + "\n")
        while token.is_error() or token.is_comment():
            if token.is_error():
                self.lex_err_path.write(str(token) + "\n")
            else:
                self.lex_output_path.write(str(token) + "\n")
            token = self.lex.next_token()
        if token.mean():
            Parser.TOKENS.append(token)
        return token

    def inverse_rhs_multiple_push(self, stack, rule):
        for r in rule[::-1]:
            if r != ActionKinds.EP.upper():
                stack.append(r)
        return stack

    def is_semantic_action(self, action):
        return action[0] == "^"

    def clear_up(self):
        Parser.TOKENS = []

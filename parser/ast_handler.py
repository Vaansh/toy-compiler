#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
from parser.util import *

from semantic.action import Action
from visitors.mem_size_visitor import MemorySizeVisitor
from visitors.table_creation_visitor import SymTabCreationVisitor
from visitors.type_check_visitor import TypeCheckVisitor


class ASTHandler:
    def __init__(self, sem_stack, sem_file, tree_file, tokens, sem_test, sem_err_path):
        self.ast_builder(sem_stack, sem_file, tree_file, tokens, sem_test, sem_err_path)

    def ast_builder(
        self, sem_stack, sem_file, tree_file, tokens, sem_test, sem_err_path
    ):
        ast = []
        actions = sem_stack[::-1]
        Action.TOKENS = tokens
        while len(actions) != 0:
            action = actions.pop()
            ast = Action.act(ast, action)
        self._out_ast(ast[-1], tree_file)

        if sem_file:
            self.ast_symbol_table_decorator(ast[-1], sem_file, sem_err_path)
            if self.ast_type_check_decorator(ast[-1], sem_err_path):
                if sem_test:
                    return
                self.ast_mem_size_decorator(ast[-1], sem_file)

    def ast_symbol_table_decorator(self, prog_node, sem_file, sem_err_path):
        sym = SymTabCreationVisitor(sem_file, sem_err_path)
        prog_node.accept(sym)
        self._format_table(sym.content, sem_file)

    def ast_type_check_decorator(self, prog_node, sem_err_path):
        _type = TypeCheckVisitor(sem_err_path)
        prog_node.accept(_type)
        if _type.error_flag:
            print(
                background.CRITICAL
                + "Semantic Errors: "
                + background.FIN
                + background.YELLOW
                + "logged in file - {0}".format(sem_err_path)
                + background.FIN
            )
            return False
        return True

    def ast_mem_size_decorator(self, prog_node, sem_file):
        mem_size_visitor = MemorySizeVisitor(sem_file)
        prog_node.accept(mem_size_visitor)
        self._format_table(mem_size_visitor.content, sem_file)

    def _out_ast(self, prog_node, tree_file):
        prog_node.traverse_tree(tree_file, False)
        tree_file.write("=" * 102)

    def _format_table(self, content, sem_file):
        res = []
        content = os.linesep.join([s for s in content.splitlines() if s])
        max_len_str = len(max(content.splitlines(), key=len))
        for c in content.splitlines():
            if len(c) < max_len_str and "=" in c:
                c += "=" * (max_len_str - len(c))
            elif "=" not in c:
                c += " " * (max_len_str - len(c) - 1) + "|"
            res.append(c + "\n")

        with open(sem_file, "w") as f:
            f.write("\n")

        with open(sem_file, "a") as f:
            for r in res:
                f.write(r)

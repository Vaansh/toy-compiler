#! /usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os

from semantic.action import Action


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


def first_and_follow():
    _first, _follow = {}, {}
    path = "{0}/parser/grammar/".format(os.getcwd())
    csv_file = []
    file_names = os.listdir(path)
    for file_names in file_names:
        if file_names.endswith(".csv"):
            csv_file.append(file_names)
    file = open("parser/grammar/first_and_follow.csv", "r")
    reader = csv.reader(file, delimiter=",")
    next(reader)
    for row in reader:
        first, follow = [s for _, s in enumerate(row[1].split(", "))], [
            s for _, s in enumerate(row[2].split(", "))
        ]
        _first[row[0]], _follow[row[0]] = first, follow
    return _first, _follow


def build_parse_table():
    file = open("parser/grammar/parser_table.csv", "r")
    reader = csv.reader(file, delimiter=",")
    table = {}
    header = next(reader)
    reader = list(reader)
    for row in reader:
        non_terminal = row[0]
        for i, a in enumerate(row):
            if i == 0:
                continue
            if a:
                terminal = header[i]
                rule = a
                _, r = rule.split("::=")
                rule = r.split()
                try:
                    table[non_terminal][terminal] = rule
                except KeyError:
                    table[non_terminal] = dict()
                    table[non_terminal][terminal] = rule
    return table


def semantic_actions_mapper():
    return {
        "AddOp": Action(value="AddOp", child_count="3"),
        "AParams": Action(value="AParams", child_count="0"),
        "ArithExpr": Action(value="ArithExpr", child_count="1"),
        "ArraySize": Action(value="ArraySize", child_count="0"),
        "ArraySizeZero": Action(value="ArraySizeZero", child_count=None),
        "AssignOp": Action(value="AssignOp", child_count=None),
        "And": Action(value="And", child_count=None),
        "AssignStatement": Action(value="AssignStatement", child_count="3"),
        "Dot": Action(value="Dot", child_count="2"),
        "DotList": Action(value="DotList", child_count="0"),
        "Div": Action(value="Div", child_count=None),
        "Epsilon": Action(value=None, child_count=None),
        "Expr": Action(value="Expr", child_count="1"),
        "Factor": Action(value="Factor", child_count="1"),
        "FParam": Action(value="FParam", child_count="3"),
        "FParamsList": Action(value="FParamsList", child_count="0"),
        "FuncDecl": Action(value="FuncDecl", child_count="3"),
        "FuncDef": Action(value="FuncDef", child_count="4"),
        "FuncBodiesMultiple": Action(value="FuncBodiesMultiple", child_count="0"),
        "FunctionCallStatement": Action(value="FunctionCallStatement", child_count="1"),
        "Id": Action(value="Id", child_count=None),
        "Impldef": Action(value="Impldef", child_count="2"),
        "IfStatement": Action(value="IfStatement", child_count="3"),
        "ImplFuncDefRep": Action(value="ImplFuncDefRep", child_count="0"),
        "IndiceReps": Action(value="IndiceReps", child_count="0"),
        "InheritsList": Action(value="InheritsList", child_count="0"),
        "MultOp": Action(value="MultOp", child_count="3"),
        "Member": Action(value="Member", child_count="2"),
        "MemberList": Action(value="MemberList", child_count="0"),
        "MemberFunc": Action(value="MemberFunc", child_count="4"),
        "Minus": Action(value="Minus", child_count=None),
        "Mult": Action(value="Mult", child_count=None),
        "NegativeFactor": Action(value="NegativeFactor", child_count="1"),
        "Or": Action(value="Or", child_count=None),
        "Prog": Action(value="Prog", child_count="0"),
        "Plus": Action(value="Plus", child_count=None),
        "RelExpr": Action(value="RelExpr", child_count="3"),
        "RelOp": Action(value="RelOp", child_count=None),
        "ReadStatement": Action(value="ReadStatement", child_count="1"),
        "ReturnStatement": Action(value="ReturnStatement", child_count="1"),
        "StatBlock": Action(value="StatBlock", child_count="0"),
        "Statement": Action(value="Statement", child_count="1"),
        "StructDecl": Action(value="StructDecl", child_count="3"),
        "Sign": Action(value="Sign", child_count=None),
        "SignFactor": Action(value="SignFactor", child_count="2"),
        "Term": Action(value="Term", child_count="1"),
        "Type": Action(value="Type", child_count=None),
        "VarDecl": Action(value="VarDecl", child_count="3"),
        "VarDeclOrStat": Action(value="VarDeclOrStat", child_count="0"),
        "Visibility": Action(value="Visibility", child_count=None),
        "WhileStatement": Action(value="WhileStatement", child_count="2"),
        "WriteStatement": Action(value="WriteStatement", child_count="1"),
        "FloatLit": Action(value="FloatLit", child_count=None),
        "IntLit": Action(value="IntLit", child_count=None),
    }

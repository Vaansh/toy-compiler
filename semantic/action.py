#! /usr/bin/python
# -*- coding: utf-8 -*-

from parser.ast import *

from semantic.util import *


class ActionKinds:
    EP = "Epsilon"
    LF = "Leaf"
    ST = "SubTree"
    MAP = {0: EP, 1: LF, 2: ST}
    NC = 0


class Action:
    sem_token_index = 0
    TOKENS = []

    def __init__(self, value=None, child_count=None):
        self.kind = ActionKinds.MAP[resolve_kind(value, child_count)]
        self.value = value if value else self.kind
        self.child_count = child_count

    def act(ast, action):
        stack, Action.sem_token_index = handle_act(
            ast, action, Action.sem_token_index, Action.TOKENS
        )
        return stack

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{}".format(self.value)

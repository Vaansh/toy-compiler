#! /usr/bin/python
# -*- coding: utf-8 -*-


from typing import Any, List, Optional

from lexer.token import Token


def resolve_kind(value: Optional[str], child_count: Optional[str]) -> int:
    if not value:
        return 0
    elif not child_count:
        return 1
    return 2


def handle_act(
    stack: List[Any], action: "Action", sem_token_index: int, tokens: List[Token]
) -> Any:
    val = action.value

    module = __import__("parser.ast", fromlist=["object"])
    class_instance_ = getattr(module, (val if val != "Epsilon" else "EP") + "Node")

    if val == "Epsilon" or val == "ArraySizeZero":
        node = class_instance_()
        stack.append(node)
    else:
        if action.child_count:
            if int(action.child_count) == 0:
                node = class_instance_()
                _next = stack.pop()
                while _next.value != "Epsilon":
                    node.adopt(_next)
                    _next = stack.pop()
                stack.append(node)
            else:
                node = class_instance_()
                for _ in range(int(action.child_count)):
                    _next = stack.pop()
                    node.adopt(_next)
                stack.append(node)
        else:
            node = class_instance_((tokens[sem_token_index].lexeme))
            stack.append(node)
            sem_token_index += 1

    return stack, sem_token_index

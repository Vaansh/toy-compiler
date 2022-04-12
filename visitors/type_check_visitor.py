#! /usr/bin/python
# -*- coding: utf-8 -*-

from parser.ast import *

from visitors.visitor import Visitor


class TypeCheckVisitor(Visitor):
    BEGIN_VISIT_FUNCDEF_NODE = 3

    def __init__(self, output_err: str) -> None:
        self.inherit_map = {}
        self.sem_err_output = open(output_err, "a")
        self.errors = []
        self.error_flag = False

    def _check_circular_dependency(self) -> None:
        tuple_form_dependency_list = []
        for k in self.inherit_map:
            tuple_form_dependency_list.append((k, self.inherit_map[k]))

        remaining, resolved = [
            (value, set(dependencies))
            for value, dependencies in tuple_form_dependency_list
        ], []

        while remaining:
            remain, resolve = [], []
            for rem in remaining:
                value, dependencies = rem
                dependencies.difference_update(resolved)
                remain.append(rem) if dependencies else resolve.append(value)
            if not resolve:
                self._log_error(
                    "Semantic Error - Circular class dependencies found: "
                    + ", ".join(
                        [
                            "'{}'".format(np[0])
                            + " -> "
                            + ", ".join("'{}'".format(dp) for dp in np[1])
                            for np in remain
                        ]
                    )
                    + "\n"
                )
                return
            remaining, resolved = remain, resolve

    def visit_addop_node(self, node: AddOpNode):
        return

    def visit_aparams_node(self, node: AParamsNode):
        return

    def visit_arithexpr_node(self, node: ArithExprNode) -> None:
        if (
            node.parent.__class__.__name__ == "IndiceRepsNode"
            and node.children[-1].children[-1].children[-1].__class__.__name__
            != "IntLitNode"
        ):
            self._log_error(
                "Semantic Error - Array index is not an integer: '"
                + node.children[-1].children[-1].children[-1].value
                + "'\n"
            )

    def visit_arraysize_node(self, node: ArraySizeNode) -> None:
        return

    def visit_arraysizezero_node(self, node: ArraySizeZeroNode):
        return

    def visit_assignop_node(self, node: AssignOpNode) -> None:
        return

    def visit_and_node(self, node: AndNode):
        return

    def visit_assignstatement_node(self, node: AssignStatementNode) -> None:
        for child in node.children[::-1]:
            child.accept(self)

    def visit_dot_node(self, node: DotNode) -> None:
        if node.symbol_table:
            call_arr_size = len(node.children[-2].children)
            arr_size = len(
                node.symbol_table.check_records(node.children[-1].value).dims
            )
            if call_arr_size != arr_size:
                self._log_error(
                    "Semantic Error - Use of array with wrong number of dimensions: Used '"
                    + str(call_arr_size)
                    + "' dimensions, but defined number of dimensions were '"
                    + str(arr_size)
                    + "'\n"
                )

        for child in node.children[::-1]:
            child.accept(self)

    def visit_dotlist_node(self, node: DotListNode) -> None:
        if len(node.children) > 1 and node.symbol_table:
            _type = node.symbol_table.check_records(
                node.children[-1].children[-1].value
            ).type
            if _type and node.symbol_table.check_records(_type).kind != "class":
                self._log_error(
                    "Semantic Error - '.' operator used on non-class type: '"
                    + _type
                    + "' with value '"
                    + node.children[-1].children[-1].value
                    + "'\n"
                )
        for child in node.children[::-1]:
            child.accept(self)

    def visit_div_node(self, node: DivNode):
        return

    def visit_expr_node(self, node: ExprNode) -> None:
        return

    def visit_factor_node(self, node: FactorNode):
        return

    def visit_fparam_node(self, node: FParamNode):
        return

    def visit_fparamslist_node(self, node: FParamsListNode) -> None:
        return

    def visit_funcdecl_node(self, node: FuncDeclNode):
        return

    def visit_funcdef_node(self, node: FuncDefNode) -> None:
        for i in range(TypeCheckVisitor.BEGIN_VISIT_FUNCDEF_NODE, len(node.children)):
            child = node.children[::-1][i]
            child.accept(self)

    def visit_functioncallstatement_node(self, node: FunctionCallStatementNode) -> None:
        return

    def visit_id_node(self, node: IdNode) -> None:
        return

    def visit_impldef_node(self, node: ImpldefNode) -> None:
        for child in node.children[::-1]:
            child.accept(self)

    def visit_ifstatement_node(self, node: IfStatementNode):
        return

    def visit_implfuncdefrep_node(self, node: ImplFuncDefRepNode) -> None:
        for child in node.children[::-1]:
            child.accept(self)

    def visit_indicereps_node(self, node: IndiceRepsNode) -> None:
        for child in node.children[::-1]:
            child.accept(self)

    def visit_inheritslist_node(self, node: InheritsListNode) -> None:
        return

    def visit_multop_node(self, node: MultOpNode):
        return

    def visit_member_node(self, node: MemberNode) -> None:
        return

    def visit_memberfunc_node(self, node: MemberFuncNode) -> None:
        for child in node.children[::-1]:
            child.accept(self)

    def visit_memberlist_node(self, node: MemberListNode) -> None:
        for child in node.children[::-1]:
            child.accept(self)

    def visit_minus_node(self, node: MinusNode):
        return

    def visit_mult_node(self, node: MultNode):
        return

    def visit_negativefactor_node(self, node: NegativeFactorNode):
        return

    def visit_or_node(self, node: OrNode):
        return

    def visit_prog_node(self, node: ProgNode) -> None:
        for child in node.children[::-1]:
            child.accept(self)
        self._check_circular_dependency()

    def visit_plus_node(self, node: PlusNode):
        return

    def visit_relexpr_node(self, node: RelExprNode):
        return

    def visit_relop_node(self, node: RelOpNode):
        return

    def visit_readstatement_node(self, node: ReadStatementNode):
        return

    def visit_returnstatement_node(self, node: ReturnStatementNode) -> None:
        return

    def visit_statblock_node(self, node: StatBlockNode):
        return

    def visit_statement_node(self, node: StatementNode):
        return

    def visit_structdecl_node(self, node: StructDeclNode) -> None:
        for child in node.children[::-1]:
            for c in child.symbol_table.list:
                if c.type == "inherit":
                    self.inherit_map[child.symbol_table.name] = c.inherited_list
            child.accept(self)

    def visit_sign_node(self, node: SignNode):
        return

    def visit_signfactor_node(self, node: SignFactorNode):
        return

    def visit_term_node(self, node: TermNode):
        return

    def visit_type_node(self, node: TypeNode) -> None:
        return

    def visit_vardecl_node(self, node: VarDeclNode) -> None:
        for child in node.children[::-1]:
            child.accept(self)

    def visit_vardeclorstat_node(self, node: VarDeclOrStatNode) -> None:
        for child in node.children[::-1]:
            child.accept(self)

    def visit_visibility_node(self, node: VisibilityNode):
        return

    def visit_whilestatement_node(self, node: WhileStatementNode) -> None:
        return

    def visit_writestatement_node(self, node: WriteStatementNode):
        return

    def visit_floatlit_node(self, node: FloatLitNode):
        return

    def visit_intlit_node(self, node: IntLitNode):
        return

    def visit_ep_node(self, node: EPNode):
        return

    def _log_error(self, msg: str) -> None:
        self._set_error_flag(msg)
        if msg not in self.errors:
            self.errors.append(msg)
            self.sem_err_output.write(msg)

    def _set_error_flag(self, msg: str) -> None:
        if self.error_flag:
            return
        self.error_flag = True if msg.split()[1].strip() != "Warning" else False

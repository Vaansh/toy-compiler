#! /usr/bin/python
# -*- coding: utf-8 -*-

from functools import reduce
from parser.ast import *
from typing import Union

from semantic.record import MemberVarRecord, VarRecord
from semantic.table import SymbolTable
from visitors.visitor import Visitor


class MemorySizeVisitor(Visitor):
    def __init__(self, output_err: str) -> None:
        self.sem_err_output = open(output_err, "a")

    def _calc_var_size(
        self, table: SymbolTable, record: Union[VarRecord, MemberVarRecord]
    ) -> int:
        size_map = {"integer": 4, "float": 8}
        size = size_map.get(record.type, 0)
        size = (table.check_records(record).size) if size == 0 else size
        size *= (
            reduce(lambda x, y: x * y, [x for x in record.dims if x], 1)
            if len(record.dims) > 0
            else 1
        )

        return size

    def _calc_scope_size(self, table: SymbolTable, name: str) -> None:
        record = table.check_records(name)
        size = record.size
        for r in record.table.link.list:
            size += 0 if r.kind == "function" else r.size
        record.size = size
        return

    def visit_addop_node(self, node: AddOpNode):
        return

    def visit_aparams_node(self, node: AParamsNode):
        return

    def visit_arithexpr_node(self, node: ArithExprNode):
        return

    def visit_arraysize_node(self, node: ArraySizeNode):
        return

    def visit_arraysizezero_node(self, node: ArraySizeZeroNode):
        return

    def visit_assignop_node(self, node: AssignOpNode):
        return

    def visit_and_node(self, node: AndNode):
        return

    def visit_assignstatement_node(self, node: AssignStatementNode) -> None:
        return

    def visit_dot_node(self, node: DotNode):
        return

    def visit_dotlist_node(self, node: DotListNode):
        return

    def visit_div_node(self, node: DivNode):
        return

    def visit_expr_node(self, node: ExprNode):
        return

    def visit_factor_node(self, node: FactorNode):
        return

    def visit_fparam_node(self, node: FParamNode) -> None:
        child = node.children[-1]
        if node.parent.parent.parent.symbol_table:
            record = node.parent.parent.parent.symbol_table.check_records(child.value)
            if record.__class__.__name__ == "VarRecord":
                record.size = self._calc_var_size(
                    node.parent.parent.parent.symbol_table, record
                )

    def visit_fparamslist_node(self, node: FParamsListNode) -> None:
        for child in node.children[::-1]:
            child.accept(self)

    def visit_funcdecl_node(self, node: FuncDeclNode) -> None:
        for child in node.children[::-1]:
            child.accept(self)

    def visit_funcdef_node(self, node: FuncDefNode) -> None:
        for child in node.children[::-1]:
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

    def visit_indicereps_node(self, node: IndiceRepsNode):
        return

    def visit_inheritslist_node(self, node: InheritsListNode) -> None:
        for child in node.children[::-1]:
            child.accept(self)

    def visit_multop_node(self, node: MultOpNode):
        return

    def visit_member_node(self, node: MemberNode) -> None:
        if node.children[-2].__class__.__name__ in ["VarDeclNode", "FuncDeclNode"]:
            node.children[-2].accept(self)

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
            child_record = node.symbol_table.check_records(child.children[-1].value)
            if child_record.kind == "function" and child_record.name == "main":
                self._calc_scope_size(node.symbol_table, "main")

        self.content = str(node.symbol_table)

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
            child.accept(self)
        self._calc_scope_size(node.symbol_table, node.record.name)

    def visit_sign_node(self, node: SignNode):
        return

    def visit_signfactor_node(self, node: SignFactorNode):
        return

    def visit_term_node(self, node: TermNode):
        return

    def visit_type_node(self, node: TypeNode) -> None:
        return

    def visit_vardecl_node(self, node: VarDeclNode) -> None:
        child = node.children[-1]
        if node.symbol_table:
            record = node.symbol_table.check_records(child.value)
            if record.__class__.__name__ in ["VarRecord", "MemberVarRecord"]:
                record.size = self._calc_var_size(node.symbol_table, record)
        elif node.parent.symbol_table:
            record = node.parent.symbol_table.check_records(child.value)
            if record.__class__.__name__ in ["VarRecord", "MemberVarRecord"]:
                record.size = self._calc_var_size(node.parent.symbol_table, record)
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

    def _log_error(self, msg):
        self._set_error_flag(msg)
        if msg not in self.errors:
            self.errors.append(msg)
            self.sem_err_output.write(msg)

    def _set_error_flag(self, msg):
        if self.error_flag:
            return
        self.error_flag = True if msg.split()[1].strip() != "Warning" else False

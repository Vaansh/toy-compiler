#! /usr/bin/python
# -*- coding: utf-8 -*-

from parser.ast import *

from semantic.record import *
from visitors.visitor import Visitor


class CodeGenerationVisitor(Visitor):
    def __init__(self, output, debug=False):
        pass

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

    def visit_assignstatement_node(self, node: AssignStatementNode):
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

    def visit_fparam_node(self, node: FParamNode):
        return

    def visit_fparamslist_node(self, node: FParamsListNode):
        return

    def visit_funcdecl_node(self, node: FuncDeclNode):
        return

    def visit_funcdef_node(self, node: FuncDefNode):
        return

    def visit_functioncallstatement_node(self, node: FunctionCallStatementNode):
        return

    def visit_id_node(self, node: IdNode):
        return

    def visit_impldef_node(self, node: ImpldefNode):
        return

    def visit_ifstatement_node(self, node: IfStatementNode):
        return

    def visit_implfuncdefrep_node(self, node: ImplFuncDefRepNode):
        return

    def visit_indicereps_node(self, node: IndiceRepsNode):
        return

    def visit_inheritslist_node(self, node: InheritsListNode):
        return

    def visit_multop_node(self, node: MultOpNode):
        return

    def visit_member_node(self, node: MemberNode):
        return

    def visit_memberfunc_node(self, node: MemberFuncNode):
        return

    def visit_memberlist_node(self, node: MemberListNode):
        return

    def visit_minus_node(self, node: MinusNode):
        return

    def visit_mult_node(self, node: MultNode):
        return

    def visit_negativefactor_node(self, node: NegativeFactorNode):
        return

    def visit_or_node(self, node: OrNode):
        return

    def visit_prog_node(self, node: ProgNode):
        return

    def visit_plus_node(self, node: PlusNode):
        return

    def visit_relexpr_node(self, node: RelExprNode):
        return

    def visit_relop_node(self, node: RelOpNode):
        return

    def visit_readstatement_node(self, node: ReadStatementNode):
        return

    def visit_returnstatement_node(self, node: ReturnStatementNode):
        return

    def visit_statblock_node(self, node: StatBlockNode):
        return

    def visit_statement_node(self, node: StatementNode):
        return

    def visit_structdecl_node(self, node: StructDeclNode):
        return

    def visit_sign_node(self, node: SignNode):
        return

    def visit_signfactor_node(self, node: SignFactorNode):
        return

    def visit_term_node(self, node: TermNode):
        return

    def visit_type_node(self, node: TypeNode):
        return

    def visit_vardecl_node(self, node: VarDeclNode):
        return

    def visit_vardeclorstat_node(self, node: VarDeclOrStatNode):
        return

    def visit_visibility_node(self, node: VisibilityNode):
        return

    def visit_whilestatement_node(self, node: WhileStatementNode):
        return

    def visit_writestatement_node(self, node: WriteStatementNode):
        return

    def visit_floatlit_node(self, node: FloatLitNode):
        return

    def visit_intlit_node(self, node: IntLitNode):
        return

    def visit_ep_node(self, node: EPNode):
        return

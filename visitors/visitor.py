#! /usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from parser.ast import *


class Visitor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def visit_addop_node(self, node: AddOpNode):
        pass

    @abstractmethod
    def visit_aparams_node(self, node: AParamsNode):
        pass

    @abstractmethod
    def visit_arithexpr_node(self, node: ArithExprNode):
        pass

    @abstractmethod
    def visit_arraysize_node(self, node: ArraySizeNode):
        pass

    @abstractmethod
    def visit_arraysizezero_node(self, node: ArraySizeZeroNode):
        pass

    @abstractmethod
    def visit_assignop_node(self, node: AssignOpNode):
        pass

    @abstractmethod
    def visit_and_node(self, node: AndNode):
        pass

    @abstractmethod
    def visit_assignstatement_node(self, node: AssignStatementNode):
        pass

    @abstractmethod
    def visit_dot_node(self, node: DotNode):
        pass

    @abstractmethod
    def visit_dotlist_node(self, node: DotListNode):
        pass

    @abstractmethod
    def visit_div_node(self, node: DivNode):
        pass

    @abstractmethod
    def visit_expr_node(self, node: ExprNode):
        pass

    @abstractmethod
    def visit_factor_node(self, node: FactorNode):
        pass

    @abstractmethod
    def visit_fparam_node(self, node: FParamNode):
        pass

    @abstractmethod
    def visit_fparamslist_node(self, node: FParamsListNode):
        pass

    @abstractmethod
    def visit_funcdecl_node(self, node: FuncDeclNode):
        pass

    @abstractmethod
    def visit_funcdef_node(self, node: FuncDefNode):
        pass

    @abstractmethod
    def visit_functioncallstatement_node(self, node: FunctionCallStatementNode):
        pass

    @abstractmethod
    def visit_id_node(self, node: IdNode):
        pass

    @abstractmethod
    def visit_impldef_node(self, node: ImpldefNode):
        pass

    @abstractmethod
    def visit_ifstatement_node(self, node: IfStatementNode):
        pass

    @abstractmethod
    def visit_implfuncdefrep_node(self, node: ImplFuncDefRepNode):
        pass

    @abstractmethod
    def visit_indicereps_node(self, node: IndiceRepsNode):
        pass

    @abstractmethod
    def visit_inheritslist_node(self, node: InheritsListNode):
        pass

    @abstractmethod
    def visit_multop_node(self, node: MultOpNode):
        pass

    @abstractmethod
    def visit_member_node(self, node: MemberNode):
        pass

    @abstractmethod
    def visit_memberfunc_node(self, node: MemberFuncNode):
        pass

    @abstractmethod
    def visit_memberlist_node(self, node: MemberListNode):
        pass

    @abstractmethod
    def visit_minus_node(self, node: MinusNode):
        pass

    @abstractmethod
    def visit_mult_node(self, node: MultNode):
        pass

    @abstractmethod
    def visit_negativefactor_node(self, node: NegativeFactorNode):
        pass

    @abstractmethod
    def visit_or_node(self, node: OrNode):
        pass

    @abstractmethod
    def visit_prog_node(self, node: ProgNode):
        pass

    @abstractmethod
    def visit_plus_node(self, node: PlusNode):
        pass

    @abstractmethod
    def visit_relexpr_node(self, node: RelExprNode):
        pass

    @abstractmethod
    def visit_relop_node(self, node: RelOpNode):
        pass

    @abstractmethod
    def visit_readstatement_node(self, node: ReadStatementNode):
        pass

    @abstractmethod
    def visit_returnstatement_node(self, node: ReturnStatementNode):
        pass

    @abstractmethod
    def visit_statblock_node(self, node: StatBlockNode):
        pass

    @abstractmethod
    def visit_statement_node(self, node: StatementNode):
        pass

    @abstractmethod
    def visit_structdecl_node(self, node: StructDeclNode):
        pass

    @abstractmethod
    def visit_sign_node(self, node: SignNode):
        pass

    @abstractmethod
    def visit_signfactor_node(self, node: SignFactorNode):
        pass

    @abstractmethod
    def visit_term_node(self, node: TermNode):
        pass

    @abstractmethod
    def visit_type_node(self, node: TypeNode):
        pass

    @abstractmethod
    def visit_vardecl_node(self, node: VarDeclNode):
        pass

    @abstractmethod
    def visit_vardeclorstat_node(self, node: VarDeclOrStatNode):
        pass

    @abstractmethod
    def visit_visibility_node(self, node: VisibilityNode):
        pass

    @abstractmethod
    def visit_whilestatement_node(self, node: WhileStatementNode):
        pass

    @abstractmethod
    def visit_writestatement_node(self, node: WriteStatementNode):
        pass

    @abstractmethod
    def visit_floatlit_node(self, node: FloatLitNode):
        pass

    @abstractmethod
    def visit_intlit_node(self, node: IntLitNode):
        pass

    @abstractmethod
    def visit_ep_node(self, node: EPNode):
        pass

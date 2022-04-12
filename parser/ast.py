#! /usr/bin/python
# -*- coding: utf-8 -*-


class ASTNode:
    depth = 0
    curr_id = 0
    pipe = "|"
    indent = " "

    def __init__(self, value=None, parent=None):
        self.value = None
        self.parent = None
        self.children = []

        if value:
            self.value = value

        self.id = ASTNode.curr_id
        ASTNode.curr_id += 1

        if parent:
            parent.adopt(self)

        self.symbol_table = None
        self.record = None

        def __repr__(self):
            return self.__str__()

        def __str__(self):
            return "{}".format(self.value if hasattr(self, "value") else "x")

    def adopt(self, child):
        child.parent = self
        self.children.append(child)

    def accept(self, visitor):
        visitor.visit(self)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[{0} {1}]".format(
            self.value if hasattr(self, "value") else "",
            str(len(self.children) if hasattr(self, "children") else ""),
        )

    def traverse_tree(self, tree_file, debug=False):
        res = "{indentation_and_node_name:<70}|{node_value:^30}|".format(
            indentation_and_node_name=((ASTNode.pipe + ASTNode.indent) * ASTNode.depth)
            + self.__class__.__name__[:-4],
            node_value=(
                " " + ((self.value) if (hasattr(self, "value") and self.value) else "")
            ),
        )
        if debug:
            print(res)
        tree_file.write(res + "\n")

        ASTNode.depth += 1
        if hasattr(self, "children"):
            [child.traverse_tree(tree_file, debug) for child in self.children[::-1]]
        ASTNode.depth -= 1


class AParamsNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_aparams_node(self)


class AddOpNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_addop_node(self)


class AndNode(ASTNode):
    def __init__(self, value):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_and_node(self)


class ArithExprNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_arithexpr_node(self)


class ArraySizeNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_arraysize_node(self)


class ArraySizeZeroNode(ASTNode):
    def __init__(self, value="0"):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_arraysizezero_node(self)


class AssignOpNode(ASTNode):
    def __init__(self, value):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_assignop_node(self)


class AssignStatementNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_assignstatement_node(self)


class DivNode(ASTNode):
    def __init__(self, value):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_div_node(self)


class DotNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_dot_node(self)


class DotListNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_dotlist_node(self)


class EPNode(ASTNode):
    def __init__(self, value="Epsilon"):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_ep_node(self)


class ExprNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_expr_node(self)


class FParamNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_fparam_node(self)


class FParamsListNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_fparamslist_node(self)


class FactorNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_factor_node(self)


class FloatLitNode(ASTNode):
    def __init__(self, value):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_floatlit_node(self)


class FunctionCallStatementNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_functioncallstatement_node(self)


class FuncDeclNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_funcdecl_node(self)


class FuncDefNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_funcdef_node(self)


class IdNode(ASTNode):
    def __init__(self, value):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_id_node(self)


class IfStatementNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_ifstatement_node(self)


class ImplFuncDefRepNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_implfuncdefrep_node(self)


class ImpldefNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_impldef_node(self)


class IndiceRepsNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_indicereps_node(self)


class InheritsListNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_inheritslist_node(self)


class IntLitNode(ASTNode):
    def __init__(self, value):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_intlit_node(self)


class MemberNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_member_node(self)


class MemberFuncNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_memberfunc_node(self)


class MemberListNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_memberlist_node(self)


class MinusNode(ASTNode):
    def __init__(self, value):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_minus_node(self)


class MultNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_mult_node(self)


class MultOpNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_multop_node(self)


class NegativeFactorNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_negativefactor_node(self)


class OrNode(ASTNode):
    def __init__(self, value):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_or_node(self)


class PlusNode(ASTNode):
    def __init__(self, value):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_plus_node(self)


class ProgNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_prog_node(self)


class ReadStatementNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_readstatement_node(self)


class RelExprNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_relexpr_node(self)


class RelOpNode(ASTNode):
    def __init__(self, value):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_relop_node(self)


class ReturnStatementNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_returnstatement_node(self)


class SignNode(ASTNode):
    def __init__(self, value):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_sign_node(self)


class SignFactorNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_signfactor_node(self)


class StatBlockNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_statblock_node(self)


class StatementNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_statement_node(self)


class StructDeclNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_structdecl_node(self)


class TermNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_term_node(self)


class TypeNode(ASTNode):
    def __init__(self, value):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_type_node(self)


class VarDeclNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_vardecl_node(self)


class VarDeclOrStatNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_vardeclorstat_node(self)


class VisibilityNode(ASTNode):
    def __init__(self, value):
        super().__init__(value=value)

    def accept(self, visitor):
        visitor.visit_visibility_node(self)


class WhileStatementNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_whilestatement_node(self)


class WriteStatementNode(ASTNode):
    def __init__(self, value=None):
        if not value:
            super().__init__()

    def accept(self, visitor):
        visitor.visit_writestatement_node(self)

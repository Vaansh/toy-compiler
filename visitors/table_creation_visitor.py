#! /usr/bin/python
# -*- coding: utf-8 -*-

from parser.ast import *

from semantic.record import *
from semantic.table import SymbolTable
from visitors.visitor import Visitor


class SymTabCreationVisitor(Visitor):
    BEGIN_VISIT_FUNCDEF_NODE = 3

    def __init__(self, output: str, output_err: str, debug: bool = False) -> None:
        with open(output, "w") as sym_tab_file:
            sym_tab_file.write("")
        with open(output_err, "w") as sem_err:
            sem_err.write("")
        self.sym_tab_output = open(output, "a")
        self.sem_err_output = open(output_err, "a")
        self.debug = debug
        self.errors = []
        self.error_flag = False

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

    def visit_assignop_node(self, node: AssignOpNode) -> None:
        return

    def visit_and_node(self, node: AndNode):
        return

    def visit_assignstatement_node(self, node: AssignStatementNode) -> None:
        for child in node.children[::-1]:
            child.symbol_table = node.symbol_table
            child.accept(self)

    def visit_dot_node(self, node: DotNode) -> None:
        return

    def visit_dotlist_node(self, node: DotListNode) -> None:
        for child in node.children[::-1]:
            child.symbol_table = node.symbol_table
            child.accept(self)

    def visit_div_node(self, node: DivNode):
        return

    def visit_expr_node(self, node: ExprNode) -> None:
        return

    def visit_factor_node(self, node: FactorNode):
        return

    def visit_fparam_node(self, node: FParamNode) -> None:
        dims = []
        for dim in node.children[-3].children[::-1]:
            dims.append(
                None
                if dim.__class__.__name__ == "ArraySizeZeroNode"
                else int(dim.value)
            )
        node.symbol_table.list.append(
            VarRecord("param", node.children[-2].value, node.children[-1].value, dims)
        )

    def visit_fparamslist_node(self, node: FParamsListNode) -> None:
        for child in node.children[::-1]:
            child.symbol_table = node.symbol_table
            child.accept(self)

    def visit_funcdecl_node(self, node: FuncDeclNode):
        return

    def visit_funcdef_node(self, node: FuncDefNode) -> None:
        function_name = node.children[-1].value
        paramater_types_list = []
        for parameter in node.children[-2].children[::-1]:
            paramater_types_list.append(parameter.children[-2].value)
        to_ret_type = node.children[-3].value
        if function_name == node.symbol_table.check_records(function_name).name:
            _function_record = node.symbol_table.check_records(function_name)
            _function_record.__class__ = FuncRecord

            if hasattr(_function_record, "params_type"):
                if _function_record.params_type:
                    if _function_record.params_type == paramater_types_list:
                        # 8.2
                        self._log_error(
                            "Semantic Error - multiply defined free function: '"
                            + "{} {}".format(
                                _function_record.name,
                                "(" + ", ".join(_function_record.params_type) + ")",
                            )
                            + "'\n"
                        )
                        return
                    # 9.1
                    else:
                        self._log_error(
                            "Semantic Warning - Overloaded free function: '"
                            + "{} {}".format(
                                function_name,
                                "(" + ", ".join(paramater_types_list) + ")",
                            )
                            + "'\n"
                        )
        _table = SymbolTable(
            name=(":" * 2) + function_name, link=node.symbol_table, level=1
        )
        node.record = FuncRecord(
            to_ret_type, function_name, paramater_types_list, _table
        )
        node.symbol_table.list.append(node.record)
        node.symbol_table = _table

        for i in range(
            SymTabCreationVisitor.BEGIN_VISIT_FUNCDEF_NODE, len(node.children)
        ):
            child = node.children[::-1][i]
            child.symbol_table = node.symbol_table
            child.accept(self)

    def visit_functioncallstatement_node(self, node: FunctionCallStatementNode) -> None:
        return

    def visit_id_node(self, node: IdNode) -> None:
        return

    def visit_impldef_node(self, node: ImpldefNode) -> None:
        node.record = node.symbol_table.check_records(node.children[-1].value)

        # 11.5
        if not node.record.name:
            self._log_error(
                "Semantic Error - Undeclared class: "
                + str(node.children[-1].value)
                + "\n"
            )
            return

        node.symbol_table = node.record.table
        for child in node.children[::-1]:
            child.symbol_table = node.symbol_table
            child.accept(self)

    def visit_ifstatement_node(self, node: IfStatementNode):
        return

    def visit_implfuncdefrep_node(self, node: ImplFuncDefRepNode) -> None:
        for child in node.children[::-1]:
            child.symbol_table = node.symbol_table
            child.accept(self)

    def visit_indicereps_node(self, node: IndiceRepsNode):
        return

    def visit_inheritslist_node(self, node: InheritsListNode) -> None:
        _vals = []
        for _val in node.children[::-1]:
            _vals.append(_val.value)
        node.symbol_table.list.append(InheritRepRecord(_vals, None))

    def visit_multop_node(self, node: MultOpNode):
        return

    def visit_member_node(self, node: MemberNode) -> None:
        visibility_value = node.children[-1].value
        declaration = node.children[-2]

        if declaration.__class__.__name__ == "FuncDeclNode":
            class_val = node.symbol_table.name
            function_name = declaration.children[-1].value
            funcReturnType = declaration.children[-3].value
            _table = SymbolTable(
                level=2,
                name=class_val + (":" * 2) + function_name,
                link=node.symbol_table,
            )
            paramater_types_list = []
            for param in declaration.children[-2].children[::-1]:
                parameter_type = param.children[-2].value
                dims = []
                for dim in param.children[-3].children[::-1]:
                    dims.append(
                        None
                        if dim.__class__.__name__ == "ArraySizeZeroNode"
                        else int(dim.value)
                    )
                for idx in dims:
                    parameter_type += "[" + "index" if idx else "" + "]"
                paramater_types_list.append(parameter_type)
            next_record = MemberFuncRecord(
                funcReturnType,
                function_name,
                paramater_types_list,
                visibility_value,
                _table,
            )

            node.record = next_record
            node.symbol_table.list.append(node.record)
            node.symbol_table = _table

        elif declaration.__class__.__name__ == "VarDeclNode":
            variable_name = declaration.children[-1].value
            # 8
            variable_type = declaration.children[-2].value
            dims = []
            for dim in declaration.children[-3].children[::-1]:
                dims.append(
                    None
                    if dim.__class__.__name__ == "ArraySizeZeroNode"
                    else int(dim.value)
                )
            node.record = MemberVarRecord(
                "data", variable_type, variable_name, dims, visibility_value
            )
            node.symbol_table.list.append(node.record)

    def visit_memberfunc_node(self, node: MemberFuncNode) -> None:
        function_name = node.children[-1].value

        def_parameter_types = []
        for child in node.children[-2].children[::-1]:
            def_parameter_types.append(child.children[-2].value)
        function_record = node.symbol_table.check_records(function_name)
        next_function_record = MemberFuncRecord(
            "function", function_name, def_parameter_types, None, None
        )

        if not function_record.kind and not function_record.name:
            self._log_error(
                "Semantic Error - undeclared member function definition: '"
                + next_function_record.name
                + " ("
                + ", ".join(def_parameter_types)
                + ")'\n"
            )
            return

        node.record = node.symbol_table.check_records(function_name)
        node.symbol_table = node.record.table
        for child in node.children[::-1]:
            child.symbol_table = node.symbol_table
            child.accept(self)

    def visit_memberlist_node(self, node: MemberListNode) -> None:
        for child in node.children[::-1]:
            child.symbol_table = node.symbol_table
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
        node.symbol_table = SymbolTable(level=0, name="global", link=None)
        for child in node.children[::-1]:
            child.symbol_table = node.symbol_table
            child.accept(self)

        if self.debug:
            print(node.symbol_table)

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
        class_val = node.children[-1].value
        if node.symbol_table.check_records(class_val).name:
            self._log_error(
                "Semantic Error - multiply declared class: '"
                + node.symbol_table.check_records(class_val).name
                + "'\n"
            )

        inherit = []
        for _id in node.children[-2].children[::-1]:
            inherit.append(_id.value)

        records = []
        for name in inherit:
            if node.symbol_table.check_records(name).table:
                records.extend(node.symbol_table.check_records(name).table.list)

        _table = SymbolTable(level=1, name=class_val, link=node.symbol_table)
        node.record = ClassRecord(class_val, _table)
        node.symbol_table.list.append(node.record)
        node.symbol_table = _table

        for child in node.children[::-1]:
            child.symbol_table = node.symbol_table
            child.accept(self)

        mult_id_decl_class, mult_func_decl_class = {}, {}
        for x in node.symbol_table.list:
            if x.kind == "data":
                mult_id_decl_class[x.name] = mult_id_decl_class.get(x.name, 0) + 1
            elif x.kind == "function":
                mult_func_decl_class[x.name] = mult_func_decl_class.get(x.name, [])
                mult_func_decl_class[x.name].append(x.params_type)

        for k in mult_id_decl_class:
            if mult_id_decl_class.get(k, 0) > 1:
                self._log_error(
                    "Semantic Error - multiply declared identifier in class: '"
                    + k
                    + "' initialized "
                    + str(mult_id_decl_class[k])
                    + " times"
                    + "\n"
                )
        for k in mult_func_decl_class:
            if len(mult_func_decl_class.get(k, [])) > 1:
                len_list = list(
                    dict.fromkeys([len(z) for z in mult_func_decl_class[k]])
                )
                for num_params in len_list:
                    overloaded_params = [
                        u for u in mult_func_decl_class.get(k) if len(u) == num_params
                    ]
                    self._log_error(
                        "Semantic Warning - Overloaded member function: '"
                        + k
                        + "' with "
                        + str(num_params)
                        + " parameter(s): "
                        + (
                            " & ".join(
                                ", ".join(overloaded_param)
                                for overloaded_param in overloaded_params
                            )
                        )
                        + "\n"
                    )

        for record in records:
            if record.__class__.__name__ != "InheritRepRecord":
                if node.symbol_table.check_records(record.name).name:
                    self._log_error(
                        "Semantic Error - Overridden inherited member function: '"
                        + str(node.symbol_table.check_records(record.name).name)
                        + "' in class '"
                        + class_val
                        + "'\n"
                    )
                else:
                    node.symbol_table.list.append(record)

    def visit_sign_node(self, node: SignNode):
        return

    def visit_signfactor_node(self, node: SignFactorNode):
        return

    def visit_term_node(self, node: TermNode):
        return

    def visit_type_node(self, node: TypeNode) -> None:
        return

    def visit_vardecl_node(self, node: VarDeclNode) -> None:
        variable_name = node.children[-1].value
        variable_type = node.children[-2].value

        if node.parent.parent.__class__.__name__ == "FuncDefNode":
            if node.symbol_table.check_records(variable_name).name == variable_name:
                self._log_error(
                    "Semantic Error - multiply declared identifier in function: '"
                    + variable_name
                    + "'\n"
                )
                return

        dims = []
        for dim in node.children[-3].children[::-1]:
            dims.append(
                None
                if dim.__class__.__name__ == "ArraySizeZeroNode"
                else int(dim.value)
            )
        node.record = VarRecord("local", variable_type, variable_name, dims)
        node.symbol_table.list.append(node.record)

    def visit_vardeclorstat_node(self, node: VarDeclOrStatNode) -> None:
        for child in node.children[::-1]:
            child.symbol_table = node.symbol_table
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

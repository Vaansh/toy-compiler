#! /usr/bin/python
# -*- coding: utf-8 -*-


class Record:
    def __init__(self, kind=None, type_=None, name=None, table=None):
        self.kind = kind
        self.type = type_
        self.name = name
        self.table = table
        self.dims = []
        self.size = 0
        self.offset = 0


class ClassRecord(Record):
    def __init__(self, name, table):
        super().__init__(kind="class", type_=name, name=name, table=table)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "| {:<10}| {:<10}".format(self.kind, self.name) + self.table.__str__(
            indentation=self.table.level
        )


class InheritRepRecord(Record):
    def __init__(self, inherited_list, table):
        super().__init__(
            kind="InheritsList", type_="inherit", name="inherit", table=table
        )
        self.inherited_list = inherited_list

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "| {:<15}| {:<84}".format(
            "inherit",
            "none" if len(self.inherited_list) == 0 else self.inherited_list_to_str(),
        )

    def inherited_list_to_str(self):
        res = ""
        if self.inherited_list:
            for i in self.inherited_list:
                res += str(i) + " "
        return res


class FuncRecord(Record):
    def __init__(self, type_, name, params_type, table):
        super().__init__(kind="function", type_=type_, name=name, table=table)
        self.params_type = params_type

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "| {:<15}| {:<20}| {:<20}".format(
            self.kind, self.name, self.params_type_to_str()
        ) + self.table.__str__(indentation=self.table.level)

    def params_type_to_str(self):
        res = "("
        for x in self.params_type:
            res += x + ", "
        return res[:-2] + "): " + self.type if len(self.params_type) > 0 else "(): "


class MemberFuncRecord(FuncRecord):
    def __init__(self, type_, name, params_type, visibility, table):
        super().__init__(type_, name, params_type, table)
        self.visibility = visibility

    def __eq__(self, other):
        if isinstance(other, MemberFuncRecord):
            if other.params_type:
                return (self.name == other.name) and (
                    self.params_type == other.params_type
                )

        return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (
            "| {:<15}| {:<20}| {:<40}| {:<20}".format(
                self.kind,
                self.name,
                (self.params_type_to_str() + self.type),
                self.visibility,
            )
            + self.table.__str__(indentation=self.table.level)
        )

    def params_type_to_str(self):
        res = "("
        for x in self.params_type:
            res += x + ", "
        return res[:-2] + "): "


class VarRecord(Record):
    def __init__(self, kind, type_, name, dims):
        super().__init__(kind=kind, type_=type_, name=name, table=None)
        self.dims = dims

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "| {:<20}| {:<20}| {:<40}| {:<20}".format(
            self.kind, self.name, (self.type + self.dims_to_str()), self.size
        )

    def dims_to_str(self):
        res = ""
        for i in self.dims:
            res += "[" + (str(i) if i else "x") + "]"
        return res


class MemberVarRecord(VarRecord):
    def __init__(self, kind, type_, name, dims, visibility):
        super().__init__(kind, type_, name, None)
        self.dims = dims
        self.visibility = visibility

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "| {:<15}| {:<20}| {:<40}| {:<20}| {:<19}".format(
            self.kind,
            self.name,
            (self.type + self.dims_to_str()),
            self.visibility,
            self.size,
        )

    def dims_to_str(self):
        res = ""
        if self.dims:
            for i in self.dims:
                res += "[" + str(i) if i else "" + "]"
        return res

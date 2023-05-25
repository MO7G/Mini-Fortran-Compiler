import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from tkinter import *
from nltk.tree import *


class Token_type(Enum):
    Program = 1
    Var = 2
    Const = 3
    Type = 4
    Function = 5
    Procedure = 6
    Begin = 7
    End = 8
    If = 9
    Then = 10
    Else = 11
    Case = 12
    Of = 13
    While = 14
    Do = 15
    Repeat = 16
    Until = 17
    For = 18
    To = 19
    Downto = 20
    Break = 21
    Continue = 22
    Exit = 23
    Array = 24
    Record = 25
    String = 26
    Integer = 27
    Real = 28
    Boolean = 29
    Char = 30
    Not = 31
    And = 32
    Or = 33
    Div = 34
    Mod = 35
    AssignOp = 36
    EqualOp = 37
    NotEqualOp = 38
    LessThanOp = 39
    GreaterThanOp = 40
    LessThanOrEqualOp = 41
    GreaterThanOrEqualOp = 42
    PlusOp = 43
    MinusOp = 44
    MultiplyOp = 45
    DivideOp = 46
    OpenParenthesis = 47
    CloseParenthesis = 48
    Semicolon = 49
    Colon = 50
    Comma = 51
    Dot = 52
    DoubleDot = 53
    SingleLineComment = 54
    MultiLineComment = 55
    Identifier = 56
    Number = 57
    LocalVariables = 58
    GlobalVariables = 59
    Read = 60
    ReadLn = 61
    Write = 62
    WriteLn = 63
    Uses = 64


# class token to hold string and token type
class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type

        }


ReservedWords = {
    Token_type.Program: "program",
    Token_type.Var: "var",
    Token_type.Const: "const",
    Token_type.Type: "type",
    Token_type.Function: "function",
    Token_type.Procedure: "procedure",
    Token_type.Begin: "begin",
    Token_type.End: "end",
    Token_type.If: "if",
    Token_type.Then: "then",
    Token_type.Else: "else",
    Token_type.Case: "case",
    Token_type.Of: "of",
    Token_type.While: "while",
    Token_type.Do: "do",
    Token_type.Repeat: "repeat",
    Token_type.Until: "until",
    Token_type.For: "for",
    Token_type.To: "to",
    Token_type.Downto: "downto",
    Token_type.Break: "break",
    Token_type.Continue: "continue",
    Token_type.Exit: "exit",
    Token_type.Array: "array",
    Token_type.Record: "record",
    Token_type.String: "string",
    Token_type.Integer: "integer",
    Token_type.Real: "real",
    Token_type.Boolean: "boolean",
    Token_type.Char: "char",
    Token_type.Not: "not",
    Token_type.And: "and",
    Token_type.Or: "or",
    Token_type.Div: "div",
    Token_type.Mod: "mod",
    Token_type.Identifier: "<identifier>",
    Token_type.Number: "<number>",
    Token_type.LocalVariables: "local variables",
    Token_type.GlobalVariables: "global variables",
    Token_type.Read: "read",
    Token_type.ReadLn: "readln",
    Token_type.Write: "write",
    Token_type.WriteLn: "writeln",
    Token_type.Uses: "uses"
}

Operators = {
    ":=": Token_type.AssignOp,
    "=": Token_type.EqualOp,
    "<>": Token_type.NotEqualOp,
    "<": Token_type.LessThanOp,
    ">": Token_type.GreaterThanOp,
    "<=": Token_type.LessThanOrEqualOp,
    ">=": Token_type.GreaterThanOrEqualOp,
    "+": Token_type.PlusOp,
    "-": Token_type.MinusOp,
    "*": Token_type.MultiplyOp,
    "/": Token_type.DivideOp,
    "(": Token_type.OpenParenthesis,
    ")": Token_type.CloseParenthesis,
    ";": Token_type.Semicolon,
    ":": Token_type.Colon,
    ",": Token_type.Comma,
    ".": Token_type.Dot,
    "..": Token_type.DoubleDot,
    "{": Token_type.SingleLineComment,
    "}": Token_type.SingleLineComment,
    "{*": Token_type.MultiLineComment,
    "*}": Token_type.MultiLineComment

}

Tokens = []
errors = []


def find_token(text):
    current_state = None
    current_lex = ""
    text = text.lower()
    i = 0
    while i < len(text):
        char = text[i]

        if current_state is None:
            if char.isalpha():
                current_state = Token_type.Identifier
                current_lex += char
            elif char.isdigit():
                current_state = Token_type.Number
                current_lex += char
            elif char.isspace():
                i += 1
                continue
            elif char == "{":
                if text[i:i + 2] == "{*":
                    current_state = Token_type.MultiLineComment
                    current_lex = "{*"
                    i += 1
                else:
                    current_state = Token_type.SingleLineComment
                    current_lex = "{"
            else:
                operators = [op for op in Operators.keys() if text[i:i + len(op)] == op]
                if operators:
                    operator = max(operators, key=len)
                    Tokens.append(token(operator, Operators[operator]))
                    i += len(operator)
                    continue
                else:
                    errors.append("Lexical error: Invalid character '" + char + "'")
        elif current_state == Token_type.Identifier:
            if char.isalnum() or char == '_':
                current_lex += char
            else:
                current_lex = current_lex.lower()
                if current_lex in ReservedWords.values():
                    for token_type, reserved_word in ReservedWords.items():
                        if reserved_word == current_lex:
                            Tokens.append(token(current_lex, token_type))
                            break
                else:
                    Tokens.append(token(current_lex, Token_type.Identifier))
                current_lex = ""
                current_state = None
                continue
        elif current_state == Token_type.Number:
            if char.isdigit() or char == '.':
                current_lex += char
            else:
                Tokens.append(token(current_lex, Token_type.Number))
                current_lex = ""
                current_state = None
                continue
        elif current_state == Token_type.SingleLineComment:
            if char == "}":
                Tokens.append(token(current_lex + char, Token_type.SingleLineComment))
                current_lex = ""
                current_state = None
            else:
                current_lex += char
        elif current_state == Token_type.MultiLineComment:
            if char == "*" and text[i:i + 2] == "*}":
                Tokens.append(token(current_lex + "*}", Token_type.MultiLineComment))
                current_lex = ""
                current_state = None
                i += 1
            else:
                current_lex += char

        i += 1

    if current_state == Token_type.Identifier and current_lex:
        current_lex = current_lex.lower()
        if current_lex in ReservedWords.values():
            for token_type, reserved_word in ReservedWords.items():
                if reserved_word == current_lex:
                    Tokens.append(token(current_lex, token_type))
                    break
        else:
            Tokens.append(token(current_lex, Token_type.Identifier))
    elif current_state == Token_type.Number and current_lex:
        Tokens.append(token(current_lex, Token_type.Number))
    elif current_state == Token_type.SingleLineComment and current_lex:
        Tokens.append(token(current_lex, Token_type.SingleLineComment))
    elif current_state == Token_type.MultiLineComment and current_lex:
        Tokens.append(token(current_lex, Token_type.MultiLineComment))


def Parse():
        j = 0
        Children = []
        Header_dict = Header(j)
        Children.append(Header_dict["node"])  ###############
        Block_dict = Block(Header_dict["index"])
        Children.append(Block_dict["node"])  ###############
        Node = Tree('Program', Children)
        return Node



def Header(j):
    Children = []
    out = dict()
    if Tokens[j].token_type == Token_type.Program:
        program_dict = Match(Token_type.Program, j)
        Children.append(program_dict["node"])
        identifier_dict = Match(Token_type.Identifier, program_dict["index"])
        Children.append(identifier_dict["node"])
        node = Tree("Header", Children)
        out["node"] = node
        out["index"] = identifier_dict["index"]
        return out
    else:
        node = Tree("error", Children)
        out["node"] = node
        out["index"] = j
        return out


def Block(j):
    Children = []
    out = dict()
    UsesCommand_dict = UsesCommand(j)
    Children.append(UsesCommand_dict["node"])
    ConstantDeclarations_dict = ConstantDeclarations(UsesCommand_dict("index"))
    Children.append(ConstantDeclarations_dict["node"])
    VariableDeclarations_dict = VariableDeclarations(ConstantDeclarations_dict["index"])
    Children.append(VariableDeclarations_dict["node"])
    MainProgramBlock_dict = MainProgramBlock(VariableDeclarations_dict["index"])
    Children.append(MainProgramBlock_dict["node"])
    node = Tree("Block", Children)
    out["node"] = node
    out["index"] = MainProgramBlock_dict["index"]
    return out

def UsesCommand(j):
    Children = []
    out = dict()
    uses_dict = Match(Token_type.Uses, j)
    Children.append(uses_dict["node"])
    IdentifierList_dict = IdentifierList(uses_dict["index"])
    Children.append(IdentifierList_dict["node"])
    semicolon_dict = Match(Token_type.Semicolon, IdentifierList_dict["index"])
    Children.append(semicolon_dict["node"])
    node = Tree("UsesCommand", Children)
    out["node"] = node
    out["index"] = semicolon_dict["index"]
    return out







def IdentifierList(j):
    Children = []
    out = dict()
    if Tokens[j].token_type == Token_type.Identifier:
        Identifier_dict = Match(Token_type.Identifier, j)
        Children.append(Identifier_dict["node"])

        node = Tree("IdentifierList", Children)
        out["node"] = node
        out["index"] = Identifier_dict["index"]
        return out
    else:
        IdentifierList_dict = IdentifierList(j)
        Children.append(IdentifierList_dict["node"])

        Identifier_dict = Match(Token_type.Identifier, IdentifierList_dict["index"])
        Children.append(Identifier_dict["node"])

        node = Tree("IdentifierList", Children)
        out["node"] = node
        out["index"] = Identifier_dict["index"]
        return out



def ConstantDeclarations(j):
    Children = []
    out = dict()

    const_dict = Match(Token_type.Const, j)
    Children.append(const_dict["node"])

    ConstantDeclarationList_dict = ConstantDeclarationList(const_dict["index"])
    Children.append(ConstantDeclarationList_dict["node"])

    node = Tree("ConstantDeclarations", Children)
    out["node"] = node
    out["index"] = ConstantDeclarationList_dict["index"]
    return out

def ConstantDeclarationList(j):
    Children = []
    out = dict()
    if Tokens[j].token_type == ConstantDeclarationList(j):
        ConstantDeclarationList_dict = ConstantDeclarationList(j)
        Children.append(ConstantDeclarationList_dict["node"])

        ConstantDeclaration_dict = ConstantDeclaration(ConstantDeclarationList_dict["index"])
        Children.append(ConstantDeclaration_dict["node"])

        node = Tree("ConstantDeclarationList", Children)
        out["node"] = node
        out["index"] = ConstantDeclaration_dict["index"]
        return out
    else:
        ConstantDeclaration_dict = ConstantDeclaration(j)
        Children.append(ConstantDeclaration_dict["node"])

        node = Tree("ConstantDeclarationList", Children)
        out["node"] = node
        out["index"] = ConstantDeclaration_dict["index"]
        return out


def ConstantDeclaration(j):
    Children = []
    out = dict()

    identifier_dict = Match(Token_type.Identifier, j)
    Children.append(identifier_dict["node"])

    equal_dict = Match(Token_type.EqualOp, identifier_dict["index"])
    Children.append(equal_dict["node"])

    ConstantValue_dict = ConstantValue(equal_dict["index"])
    Children.append(ConstantValue_dict["node"])

    Semicolon_dict = Match(Token_type.Semicolon, ConstantValue_dict["index"])
    Children.append(Semicolon_dict["node"])

    node = Tree("ConstantDeclaration", Children)
    out["node"] = node
    out["index"] = Semicolon_dict["index"]
    return out


def ConstantValue(j):
    Children = []
    out = dict()
    if Tokens[j].token_type in [Token_type.Number, Token_type.String]:
        value_dict = Match(Tokens[j].token_type, j)
        Children.append(value_dict["node"])
        node = Tree("ConstantValue", Children)
        out["node"] = node
        out["index"] = value_dict["index"]
        return out
    else:
        node = Tree("error", Children)
        out["node"] = node
        out["index"] = j
        return out



def VariableDeclarations(j):
    Children = []
    out = dict()

    var_dict = Match(Token_type.Var, j)
    Children.append(var_dict["node"])

    VariableDeclarationList_dict = VariableDeclarationList(var_dict["index"])
    Children.append(VariableDeclarationList_dict["node"])

    node = Tree("VariableDeclarations", Children)
    out["node"] = node
    out["index"] = VariableDeclarationList_dict["index"]
    return out


def VariableDeclarationList(j):
    Children = []
    out = dict()
    if Tokens[j].token_type == VariableDeclarationList(j):

        VariableDeclarationList_dict = VariableDeclarationList(j)
        Children.append(VariableDeclarationList_dict["node"])

        VariableDeclaration_dict = VariableDeclaration(VariableDeclarationList_dict["index"])
        Children.append(VariableDeclaration_dict["node"])

        node = Tree("VariableDeclarationList", Children)
        out["node"] = node
        out["index"] = VariableDeclaration_dict["index"]
        return out
    else:
        VariableDeclaration_dict = VariableDeclaration(j)
        Children.append(VariableDeclaration_dict["node"])

        node = Tree("VariableDeclarationList", Children)
        out["node"] = node
        out["index"] = VariableDeclaration_dict["index"]
        return out


def VariableDeclaration(j):
    Children = []
    out = dict()

    IdentifierList_dict = IdentifierList(j)
    Children.append(IdentifierList_dict["node"])

    colon_dict = Match(Token_type.Colon, IdentifierList_dict["index"])
    Children.append(colon_dict["node"])

    VariableType_dict = VariableType(colon_dict["index"])
    Children.append(VariableType_dict["node"])

    Semicolon_dict = Match(Token_type.Semicolon, VariableType_dict["index"])
    Children.append(Semicolon_dict["node"])

    node = Tree("VariableDeclaration", Children)
    out["node"] = node
    out["index"] = Semicolon_dict["index"]
    return out


def VariableType(j):
    Children = []
    out = dict()
    if Tokens[j].token_type in [Token_type.Integer, Token_type.Real, Token_type.Boolean, Token_type.Char, Token_type.String]:
        type_dict = Match(Tokens[j].token_type, j)
        Children.append(type_dict["node"])
        node = Tree("VariableType", Children)
        out["node"] = node
        out["index"] = type_dict["index"]
        return out
    else:
        node = Tree("error", Children)
        out["node"] = node
        out["index"] = j
        return out


def MainProgramBlock(j):
    Children = []
    out = dict()

    begin_dict = Match(Token_type.Begin, j)
    Children.append(begin_dict["node"])

    StatementList_dict = StatementList(begin_dict["index"])
    Children.append(StatementList_dict["node"])

    end_dict = Match(Token_type.End, StatementList_dict["index"])
    Children.append(end_dict["node"])

    dot_dict = Match(Token_type.Dot, end_dict["index"])
    Children.append(dot_dict["node"])

    Semicolon_dict = Match(Token_type.Semicolon, dot_dict["index"])
    Children.append(Semicolon_dict["node"])

    node = Tree("MainProgramBlock", Children)
    out["node"] = node
    out["index"] = Semicolon_dict["index"]
    return out



def StatementList(j):
    Children = []
    out = dict()
    if Tokens[j].token_type == StatementList(j):

        StatementList_dict = StatementList(j)
        Children.append(StatementList_dict["node"])

        Statement_dict = Statement(StatementList_dict["index"])
        Children.append(Statement_dict["node"])

        node = Tree("StatementList", Children)
        out["node"] = node
        out["index"] = Statement_dict["index"]
        return out
    else:
        Statement_dict = Statement(j)
        Children.append(Statement_dict["node"])

        node = Tree("StatementList", Children)
        out["node"] = node
        out["index"] = Statement_dict["index"]
        return out


def Statement(j):
    Children = []
    out = dict()
    if Tokens[j].token_type in AssignmentStatement(j):
        AssignmentStatement_dict = AssignmentStatement(j)
        Children.append(AssignmentStatement_dict["node"])
        node = Tree("Statement", Children)
        out["node"] = node
        out["index"] = AssignmentStatement_dict["index"]
        return out
    elif Tokens[j].token_type == IfStatement(j):
        IfStatement_dict = IfStatement(j)
        Children.append(IfStatement_dict["node"])
        node = Tree("Statement", Children)
        out["node"] = node
        out["index"] = IfStatement_dict["index"]
        return out
    elif Tokens[j].token_type == IfElseStatement(j):
        IfElseStatement_dict = IfElseStatement(j)
        Children.append(IfElseStatement_dict["node"])
        node = Tree("Statement", Children)
        out["node"] = node
        out["index"] = IfElseStatement_dict["index"]
        return out
    elif Tokens[j].token_type == ForStatement(j):
        ForStatement_dict = ForStatement(j)
        Children.append(ForStatement_dict["node"])
        node = Tree("Statement", Children)
        out["node"] = node
        out["index"] = ForStatement_dict["index"]
        return out
    elif Tokens[j].token_type == RepeatStatement(j):
        RepeatStatement_dict = RepeatStatement(j)
        Children.append(RepeatStatement_dict["node"])
        node = Tree("Statement", Children)
        out["node"] = node
        out["index"] = RepeatStatement_dict["index"]
        return out
    elif Tokens[j].token_type == ReadStatement(j):
        ReadStatement_dict = ReadStatement(j)
        Children.append(ReadStatement_dict["node"])
        node = Tree("Statement", Children)
        out["node"] = node
        out["index"] = ReadStatement_dict["index"]
        return out
    elif Tokens[j].token_type == ReadLnStatement(j):
        ReadLnStatement_dict = ReadLnStatement(j)
        Children.append(ReadLnStatement_dict["node"])
        node = Tree("Statement", Children)
        out["node"] = node
        out["index"] = ReadLnStatement_dict["index"]
        return out
    elif Tokens[j].token_type == WriteStatement(j):
        WriteStatement_dict = WriteStatement(j)
        Children.append(WriteStatement_dict["node"])
        node = Tree("Statement", Children)
        out["node"] = node
        out["index"] = WriteStatement_dict["index"]
        return out
    elif Tokens[j].token_type == WriteLnStatement(j):
        WriteLnStatement_dict = WriteLnStatement(j)
        Children.append(WriteLnStatement_dict["node"])
        node = Tree("Statement", Children)
        out["node"] = node
        out["index"] = WriteLnStatement_dict["index"]
        return out
    else:
        node = Tree("error", Children)
        out["node"] = node
        out["index"] = j
        return out

def AssignmentStatement(j):
    Children = []
    out = dict()
    identifier_dict = Match(Token_type.Identifier, j)
    Children.append(identifier_dict["node"])

    assign_dict = Match(Token_type.AssignOp, identifier_dict["index"])
    Children.append(assign_dict["node"])

    Expression_dict = Expression(assign_dict["index"])
    Children.append(Expression_dict["node"])

    Semicolon_dict = Match(Token_type.Semicolon, Expression_dict["index"])
    Children.append(Semicolon_dict["node"])

    node = Tree("AssignmentStatement", Children)
    out["node"] = node
    out["index"] = Semicolon_dict["index"]
    return out
def IfStatement(j):
    Children = []
    out = dict()

    If_dict = Match(Token_type.If, j)
    Children.append(If_dict["node"])

    Condition_dict = Condition(If_dict["index"])
    Children.append(Condition_dict["node"])

    Then_dict = Match(Token_type.Then, Condition_dict["index"])
    Children.append(Then_dict["node"])

    StatementList_dict = StatementList(Then_dict["index"])
    Children.append(StatementList_dict["node"])

    Semicolon_dict = Match(Token_type.Semicolon, StatementList_dict["index"])
    Children.append(Semicolon_dict["node"])

    node = Tree("IfStatement", Children)
    out["node"] = node
    out["index"] = Semicolon_dict["index"]
    return out


def IfElseStatement(j):
    Children = []
    out = dict()

    If_dict = Match(Token_type.If, j)
    Children.append(If_dict["node"])

    Condition_dict = Condition(If_dict["index"])
    Children.append(Condition_dict["node"])

    Then_dict = Match(Token_type.Then, Condition_dict["index"])
    Children.append(Then_dict["node"])

    StatementList1_dict = StatementList(Then_dict["index"])
    Children.append(StatementList1_dict["node"])

    Else_dict = Match("else", StatementList1_dict["index"])
    Children.append(Else_dict["node"])

    StatementList2_dict = StatementList(Else_dict["index"])
    Children.append(StatementList2_dict["node"])

    Semicolon_dict = Match(Token_type.Semicolon, StatementList2_dict["index"])
    Children.append(Semicolon_dict["node"])

    node = Tree("IfElseStatement", Children)
    out["node"] = node
    out["index"] = Semicolon_dict["index"]
    return out

def Condition(j):
    Children = []
    out = dict()

    Expression1_dict = Expression(j)
    Children.append(Expression1_dict["node"])

    Comparison_dict = Comparison(Expression1_dict["index"])
    Children.append(Comparison_dict["node"])

    Expression2_dict = Expression(Comparison_dict["index"])
    Children.append(Expression2_dict["node"])

    node = Tree("Condition", Children)
    out["node"] = node
    out["index"] = Expression2_dict["index"]
    return out

def Comparison(j):
    out = dict()
    if Tokens[j] in [Token_type.GreaterThanOp, Token_type.GreaterThanOrEqualOp, Token_type.LessThanOp, Token_type.LessThanOrEqualOp, Token_type.EqualOp ]:
        Operator_dict = Match(Tokens[j], j)
        out["node"] = Tree("Comparison", [Operator_dict["node"]])
        out["index"] = Operator_dict["index"]
        return out
    else:
        # Handle invalid or missing comparison operator
        raise Exception("Invalid or missing comparison operator at index " + str(j))


def ForStatement(j):
    Children = []
    out = dict()

    For_dict = Match(Token_type.For, j)
    Children.append(For_dict["node"])

    Identifier_dict = Match(Token_type.Identifier, For_dict["index"])
    Children.append(Identifier_dict["node"])

    Assign_dict = Match(Token_type.AssignOp, Identifier_dict["index"])
    Children.append(Assign_dict["node"])

    Expression1_dict = Expression(Assign_dict["index"])
    Children.append(Expression1_dict["node"])

    To_dict = Match(Token_type.To, Expression1_dict["index"])
    Children.append(To_dict["node"])

    Expression2_dict = Expression(To_dict["index"])
    Children.append(Expression2_dict["node"])

    Do_dict = Match(Token_type.Do, Expression2_dict["index"])
    Children.append(Do_dict["node"])

    StatementList_dict = StatementList(Do_dict["index"])
    Children.append(StatementList_dict["node"])

    Semicolon_dict = Match(Token_type.Semicolon, StatementList_dict["index"])
    Children.append(Semicolon_dict["node"])

    node = Tree("ForStatement", Children)
    out["node"] = node
    out["index"] = Semicolon_dict["index"]
    return out


def RepeatStatement(j):
    Children = []
    out = dict()

    Repeat_dict = Match(Token_type.Repeat, j)
    Children.append(Repeat_dict["node"])

    StatementList_dict = StatementList(Repeat_dict["index"])
    Children.append(StatementList_dict["node"])

    Semicolon_dict1 = Match(Token_type.Semicolon, StatementList_dict["index"])
    Children.append(Semicolon_dict1["node"])

    Until_dict = Match(Token_type.Until, Semicolon_dict1["index"])
    Children.append(Until_dict["node"])

    Expression_dict = Expression(Until_dict["index"])
    Children.append(Expression_dict["node"])

    Semicolon_dict2 = Match(Token_type.Semicolon, Expression_dict["index"])
    Children.append(Semicolon_dict2["node"])

    node = Tree("RepeatStatement", Children)
    out["node"] = node
    out["index"] = Semicolon_dict2["index"]
    return out

def ReadStatement(j):
    Children = []
    out = dict()

    Read_dict = Match(Token_type.Read, j)
    Children.append(Read_dict["node"])

    Open_paren_dict = Match(Token_type.OpenParenthesis, Read_dict["index"])
    Children.append(Open_paren_dict["node"])

    Identifier_dict = Match(Token_type.Identifier, Open_paren_dict["index"])
    Children.append(Identifier_dict["node"])

    Close_paren_dict = Match(Token_type.CloseParenthesis, Identifier_dict["index"])
    Children.append(Close_paren_dict["node"])

    Semicolon_dict = Match(Token_type.Semicolon, Close_paren_dict["index"])
    Children.append(Semicolon_dict["node"])

    node = Tree("ReadStatement", Children)
    out["node"] = node
    out["index"] = Semicolon_dict["index"]
    return out

def ReadLnStatement(j):
    Children = []
    out = dict()

    ReadLn_dict = Match(Token_type.ReadLn, j)
    Children.append(ReadLn_dict["node"])

    Open_paren_dict = Match(Token_type.OpenParenthesis, ReadLn_dict["index"])
    Children.append(Open_paren_dict["node"])

    Identifier_dict = Match(Token_type.Identifier, Open_paren_dict["index"])
    Children.append(Identifier_dict["node"])

    Close_paren_dict = Match(Token_type.CloseParenthesis, Identifier_dict["index"])
    Children.append(Close_paren_dict["node"])

    Semicolon_dict = Match(Token_type.Semicolon, Close_paren_dict["index"])
    Children.append(Semicolon_dict["node"])

    node = Tree("ReadLnStatement", Children)
    out["node"] = node
    out["index"] = Semicolon_dict["index"]
    return out

def WriteStatement(j):
    Children = []
    out = dict()

    Write_dict = Match(Token_type.Write, j)
    Children.append(Write_dict["node"])

    Open_paren_dict = Match(Token_type.OpenParenthesis, Write_dict["index"])
    Children.append(Open_paren_dict["node"])

    Expression_dict = Expression(Open_paren_dict["index"])
    Children.append(Expression_dict["node"])

    Close_paren_dict = Match(Token_type.CloseParenthesis, Expression_dict["index"])
    Children.append(Close_paren_dict["node"])

    Semicolon_dict = Match(Token_type.Semicolon, Close_paren_dict["index"])
    Children.append(Semicolon_dict["node"])

    node = Tree("WriteStatement", Children)
    out["node"] = node
    out["index"] = Semicolon_dict["index"]
    return out

def WriteLnStatement(j):
    Children = []
    out = dict()

    WriteLn_dict = Match(Token_type.WriteLn, j)
    Children.append(WriteLn_dict["node"])

    Open_paren_dict = Match(Token_type.OpenParenthesis, WriteLn_dict["index"])
    Children.append(Open_paren_dict["node"])

    Expression_dict = Expression(Open_paren_dict["index"])
    Children.append(Expression_dict["node"])

    Close_paren_dict = Match(Token_type.CloseParenthesis, Expression_dict["index"])
    Children.append(Close_paren_dict["node"])

    Semicolon_dict = Match(Token_type.Semicolon, Close_paren_dict["index"])
    Children.append(Semicolon_dict["node"])

    node = Tree("WriteLnStatement", Children)
    out["node"] = node
    out["index"] = Semicolon_dict["index"]
    return out



def Expression(j):
    Children = []
    out = dict()

    Term_dict = Term(j)
    Children.append(Term_dict["node"])

    if Term_dict["index"] < len(Tokens) and Tokens[Term_dict["index"]] in ["+", "-"]:
        Operator_dict = Match(Tokens[Term_dict["index"]], Term_dict["index"])
        Children.append(Operator_dict["node"])

        Expression_dict = Expression(Operator_dict["index"])
        Children.append(Expression_dict["node"])

        node = Tree("Expression", Children)
        out["node"] = node
        out["index"] = Expression_dict["index"]
        return out

    node = Tree("Expression", Children)
    out["node"] = node
    out["index"] = Term_dict["index"]
    return out


def Term(j):
    Children = []
    out = dict()

    Factor_dict = Factor(j)
    Children.append(Factor_dict["node"])

    if Factor_dict["index"] < len(Tokens) and Tokens[Factor_dict["index"]] in ["*", "/"]:
        Operator_dict = Match(Tokens[Factor_dict["index"]], Factor_dict["index"])
        Children.append(Operator_dict["node"])

        Term_dict = Term(Operator_dict["index"])
        Children.append(Term_dict["node"])

        node = Tree("Term", Children)
        out["node"] = node
        out["index"] = Term_dict["index"]
        return out

    node = Tree("Term", Children)
    out["node"] = node
    out["index"] = Factor_dict["index"]
    return out


def Factor(j):
    Children = []
    out = dict()

    if Tokens[j].type == Token_type.Identifier:
        Identifier_dict = Match(Token_type.Identifier, j)
        Children.append(Identifier_dict["node"])
        node = Tree("Factor", Children)
        out["node"] = node
        out["index"] = Identifier_dict["index"]
        return out

    if Tokens[j].type == Token_type.Number:
        Number_dict = Match(Token_type.Number, j)
        Children.append(Number_dict["node"])
        node = Tree("Factor", Children)
        out["node"] = node
        out["index"] = Number_dict["index"]
        return out

    if Tokens[j] == "(":
        OpenParen_dict = Match("(", j)
        Children.append(OpenParen_dict["node"])

        Expression_dict = Expression(OpenParen_dict["index"])
        Children.append(Expression_dict["node"])

        CloseParen_dict = Match(")", Expression_dict["index"])
        Children.append(CloseParen_dict["node"])

        node = Tree("Factor", Children)
        out["node"] = node
        out["index"] = CloseParen_dict["index"]
        return out






def Match(a, j):
    output = dict()
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == a):
            j += 1
            output["node"] = [Temp['Lex']]
            output["index"] = j
            return output
        else:
            output["node"] = ["error"]
            output["index"] = j
            errors.append("Syntax error : " + Temp['Lex'] + " Expected " + str(a))
            return output
    else:
        output["node"] = ["error"]
        output["index"] = j + 1
        return output


class LexicalAnalyzerGUI:
    def _init_(self, root):
        self.root = root
        self.root.title("Pascal Lexical Analyzer")
        self.text_input = None
        self.output_frame = None
        self.output_text = None

        self.create_widgets()

    def create_widgets(self):
        # Text input
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        input_label = tk.Label(input_frame, text="Input:", background="black", font='bold', fg='white')
        input_label.pack(side=tk.LEFT)

        self.text_input = tk.Text(input_frame, height=15, width=60)
        self.text_input.pack()

        analyze_button = tk.Button(self.root, text="Analyze", command=self.analyze_text, background="black",
                                   font='bold', fg='white')
        analyze_button.pack(pady=10)

        # Output
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack()

    def analyze_text(self):
        text = self.text_input.get("1.0", tk.END).strip()
        Tokens.clear()
        errors.clear()
        find_token(text)

        self.display_output()

    def display_output(self):
        if self.output_text:
            self.output_text.destroy()

        self.output_text = tk.Text(self.output_frame, height=15, width=60)
        self.output_text.pack()

        # Display Tokens
        self.output_text.insert(tk.END, "Tokens:\n")
        for token in Tokens:
            self.output_text.insert(tk.END, f"Lex: {token.lex}, Token Type: {token.token_type}\n")

        # Display errors
        self.output_text.insert(tk.END, "\nErrors:\n")
        for error in errors:
            self.output_text.insert(tk.END, f"{error}\n")



def Scan(text):
    x1 = text
    find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    # print(df)

    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    # start Parsing
    Node = Parse()

    # to display errorlist
    df1 = pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()
    # clear your list

    # label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    # canvas1.create_window(200, 210, window=label3)

    # label4 = tk.Label(root, text="Token_type"+x1, font=('helvetica', 10, 'bold'))
    # canvas1.create_window(200, 230, window=label4)


Scan("Program x; int x=0; void function1 begin int y=1; end")


if _name_ == "_main_":
    root = tk.Tk()
    app = LexicalAnalyzerGUI(root)
    root.mainloop()
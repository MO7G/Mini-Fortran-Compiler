import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import *
from Scanner import theScanner as S
import sys
import pandas as pd
sys.setrecursionlimit(10000)



errors = []
Tokens = []

def readTheToknes(arr):
    for items in arr:
        Tokens.append(items);


def Parse():
    j = 0
    Children = []
    Header_dict = Header(j)
    Children.append(Header_dict["node"])

    Block_dict = Block(Header_dict["index"])
    Children.append(Block_dict["node"])

    Footer_dict = footer(Block_dict["index"]);
    Children.append(Footer_dict["node"])
    Node = Tree('Program', Children)
    return Node






def Header(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    if Tokens[j].token_type == S.Token_type.Program:
        program_dict = Match(S.Token_type.Program, j)
        Children.append(program_dict["node"])
        identifier_dict = Match(S.Token_type.Identifier, program_dict["index"])
        Children.append(identifier_dict["node"])

        implicit_dict = Match(S.Token_type.Implicit , identifier_dict["index"])
        Children.append(implicit_dict["node"])

        none_dict = Match(S.Token_type.none ,implicit_dict["index"])
        Children.append(none_dict["node"])


        node = Tree("Header", Children)
        leafroot["node"] = node
        leafroot["index"] = none_dict["index"]
        return leafroot
    else:
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j ;
        return leafroot



okayy = "PROGRAM A ; BEGIN write x END ;";


def Block(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    ConstSec_dict = ConstSec(j)
    Children.append(ConstSec_dict["node"])

    DeclareSec_dict = DeclareSec(ConstSec_dict["index"])
    Children.append(DeclareSec_dict["node"])

    Statements_dict = Statements(DeclareSec_dict["index"])
    Children.append(Statements_dict["node"])

    node = Tree("Block", Children)
    leafroot["node"] = node
    leafroot["index"] = Statements_dict["index"]
    return leafroot


def footer(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    end_dict = Match(S.Token_type.End,j)
    Children.append(end_dict["node"])

    program_dict = Match(S.Token_type.Program,end_dict["index"])
    Children.append(program_dict["node"])

    ProgramEnd_dict = ProgramEnd(program_dict["index"]);
    Children.append(ProgramEnd_dict["node"])


    node = Tree("Footer", Children)
    leafroot["node"] = node
    leafroot["index"] = ProgramEnd_dict["index"]
    return leafroot

def ProgramEnd(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    if Tokens[j].token_type == S.Token_type.Identifier:
        identifier_dict = Match(S.Token_type.Identifier, j)
        Children.append(identifier_dict["node"])
        node = Tree("ProgramEnd", Children)
        leafroot["node"] = node
        leafroot["index"] = identifier_dict["index"]
        return leafroot
    else:
        node = Tree("Epsilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

def FooterEnd(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    if Tokens[j].token_type == S.Token_type.NewLine:
        newLine_dict = Match(S.Token_type.NewLine, j)
        Children.append(newLine_dict["node"])
        node = Tree("FooterEnd", Children)
        leafroot["node"] = node
        leafroot["index"] = newLine_dict["index"]
        return leafroot
    else:
        node = Tree("Epsilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot


def Statements(j):
    leafroot = dict()

    Children = [];
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    Statements_dict = StatementsDash(j);
    Children.append(Statements_dict["node"])
    node = Tree("Statements", Children)
    leafroot["node"] = node
    leafroot["index"] = Statements_dict["index"];
    return leafroot

def StatementsDash(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    if checkStatement(j) == True:
        Statement_dict = Statement(j);
        Children.append(Statement_dict["node"])



        StatementDash_dict = StatementsDash(Statement_dict["index"])
        Children.append(StatementDash_dict["node"])

        node = Tree("StatementsDash", Children)
        leafroot["node"] = node
        leafroot["index"] = StatementDash_dict["index"];
        return leafroot
    else:
        node = Tree("Epsilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot


def checkStatement(j):
    if Tokens[j].token_type == S.Token_type.Identifier or  Tokens[j].token_type == S.Token_type.If or  Tokens[j].token_type == S.Token_type.Do or Tokens[j].token_type == S.Token_type.Print    or  Tokens[j].token_type == S.Token_type.Read \
        and j < len(Tokens):
        return True;


def Statement(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    if checkStatement(j) == True:
        Children = []
        Temp = Tokens[j].to_dict()
        if Temp["token_type"] == S.Token_type.If:
            IfStatement_dict = IfStatement(j);
            Children.append(IfStatement_dict["node"]);

            ElseIfSec_dict = ElseIfSec(IfStatement_dict["index"])
            Children.append(ElseIfSec_dict["node"])

            ElseSec_dict = ElseSec(ElseIfSec_dict["index"]);
            Children.append(ElseSec_dict["node"])

            else_dict = Match(S.Token_type.End, ElseSec_dict["index"])
            Children.append(else_dict["node"])

            final_dict = Match(S.Token_type.If, else_dict["index"])
            Children.append(final_dict["node"])

        elif Temp["token_type"] == S.Token_type.Do:
            do_dict = Match(S.Token_type.Do, j);
            Children.append(do_dict["node"]);

            var_dict = Match(S.Token_type.Var, do_dict["index"])
            Children.append(var_dict["node"])

            equal_dict = Match(S.Token_type.Equal, var_dict["index"])
            Children.append(equal_dict["node"])

            int_val_dict = Match(S.Token_type.IntegerVal, equal_dict["index"])
            Children.append(int_val_dict["node"])

            coma_dict = Match(S.Token_type.Coma, int_val_dict["index"])
            Children.append(coma_dict["node"])

            int_val2_dict = Match(S.Token_type.IntegerVal, coma_dict["index"])
            Children.append(int_val2_dict["node"])

            flag = 0;
            if Tokens[j].token_type == S.Token_type.Openb:
                Step_dict = Step(int_val2_dict["index"]);
                Children.append(Step_dict["node"])
                flag = 1
            else:
                Epsilon_dict = createEpsilon(int_val2_dict["index"]);
                Children.append(Epsilon_dict["node"]);
                flag = 2;

            if flag == 1:
                Statements_dict = Statements(Step_dict["index"])
            elif flag == 2:
                Statements_dict = Statements(Epsilon_dict["index"])


            Children.append(Statements_dict["node"])

            end_dict = Match(S.Token_type.End,Statements_dict["index"])
            Children.append(end_dict["node"])

            final_dict = Match(S.Token_type.Do,end_dict["index"])
            Children.append(final_dict["node"])
        elif Temp["token_type"] == S.Token_type.Print:
            print_dict = Match(S.Token_type.Print,j)
            Children.append(print_dict["node"])

            multiplicatoin_dict = Match(S.Token_type.Multiplication,print_dict["index"])
            Children.append(multiplicatoin_dict["node"])


            final_dict = PrintList(multiplicatoin_dict["index"]);
            Children.append(final_dict["node"])





        elif Temp["token_type"] == S.Token_type.Read:
            read_dict = Match(S.Token_type.Read,j)
            Children.append(read_dict["node"])

            multiplication_dict = Match(S.Token_type.Multiplication,read_dict["index"]);
            Children.append(multiplication_dict["node"])

            comma_dict = Match(S.Token_type.Coma,multiplication_dict["index"])
            Children.append(comma_dict["node"])

            final_dict = Match(S.Token_type.Identifier,comma_dict["index"])
            Children.append(final_dict["node"])
        else:
            final_dict = Assignment_st(j);
            Children.append(final_dict["node"])


        node = Tree("Statement", Children)
        leafroot["node"] = node
        leafroot["index"] = final_dict["index"];
        return leafroot
    else:
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot


def createEpsilon(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    node = Tree("Epsilon", Children)
    leafroot["node"] = node
    leafroot["index"] = j
    return leafroot






def Assignment_st(j):
    Children= [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    identifier_dict = Match(S.Token_type.Identifier,j)
    Children.append(identifier_dict["node"])

    equal_dict = Match(S.Token_type.Equal,identifier_dict["index"])
    Children.append(equal_dict["node"])

    Expression_dict = Expression(equal_dict["index"])
    Children.append(Expression_dict["node"])

    node = Tree("Assignment_st", Children)
    leafroot["node"] = node
    leafroot["index"] = Expression_dict["index"]
    return leafroot


def ConstSec(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    if CheckVar(j) == True and Tokens[j+1].token_type == S.Token_type.Coma:
        VarType_dict = VarType(j);
        Children.append(VarType_dict["node"]);

        Coma_dict = Match(S.Token_type.Coma , VarType_dict["index"])
        Children.append(Coma_dict["node"])

        parameter_dict = Match(S.Token_type.Parameter,Coma_dict["index"])
        Children.append(parameter_dict["node"])

        Dcolon_dict = Match(S.Token_type.Dcolon , parameter_dict["index"])
        Children.append(Dcolon_dict["node"])

        Assignment_st_dict = Assignment_st(Dcolon_dict["index"])
        Children.append(Assignment_st_dict["node"])

        ConstantContinue_dict = ConstantContinue(Assignment_st_dict["index"])
        Children.append(ConstantContinue_dict["index"])

        newLine_dict = Match(S.Token_type.NewLine,ConstantContinue_dict["index"])
        Children.append(newLine_dict["node"])

        node = Tree("ConstSec", Children)
        leafroot["node"] = node
        leafroot["index"] = newLine_dict["index"]
        return leafroot
    else:
        node = Tree("Epsilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j
        return leafroot



def ConstantContinue(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    ConstantContinueDash_dict = ConstantContinueDash(j);
    Children.append(ConstantContinueDash_dict["node"])
    node = Tree("ConstantContinue", Children)
    leafroot["node"] = node
    leafroot["index"] = ConstantContinueDash_dict["index"]
    return leafroot

def ConstantContinueDash(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    if Tokens[j].token_type == S.Token_type.Coma:
        comma_dict = Match(S.Token_type.Coma,j)
        Children.append(comma_dict["node"])
        Assignment_st_dict = Assignment_st(comma_dict["index"])
        Children.append(Assignment_st_dict["node"])

        ConstantContinueDash_dict = ConstantContinueDash(Assignment_st_dict["index"])
        Children.append(ConstantContinueDash_dict["node"]);
        node = Tree("ConstantContinueDash", Children)
        leafroot["node"] = node
        leafroot["index"] = ConstantContinueDash_dict["index"]
        return leafroot
    else:
        node = Tree("Epsilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j
        return leafroot


def DeclareSec(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    DeclareSecDash_dict  = DeclareSecDash(j)
    Children.append(DeclareSecDash_dict["node"]);

    node = Tree("DeclareSec", Children)
    leafroot["node"] = node
    leafroot["index"] = DeclareSecDash_dict["index"]
    return leafroot

# for now we used CharacterVal for Chartype !!! Reminder
def CheckVar(j):
    if Tokens[j].token_type == S.Token_type.Integer or Tokens[j].token_type == S.Token_type.Real or Tokens[j].token_type == S.Token_type.CharacterVal \
        or Tokens[j].token_type == S.Token_type.Complex or Tokens[j].token_type == S.Token_type.Logical:
        return True;

def VarType(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    Temp = Tokens[j].to_dict()
    if CheckVar(j) == True:
        if Temp["token_type"] == S.Token_type.Integer:
            varType_dict = Match(S.Token_type.Integer, j)
        elif Temp["token_type"] == S.Token_type.Real:
            varType_dict = Match(S.Token_type.Real, j)
        elif Temp["token_type"] == S.Token_type.CharacterVal:
            varType_dict = Match(S.Token_type.CharacterVal, j)
        elif Temp["token_type"] == S.Token_type.Complex:
            varType_dict = Match(S.Token_type.Complex, j)
        elif Temp["token_type"] == S.Token_type.Logical:
            varType_dict = Match(S.Token_type.Logical, j)

        Children.append(varType_dict["node"])
        node = Tree("VarType", Children)
        leafroot["node"] = node
        leafroot["index"] = varType_dict["index"]
        return leafroot
    else:
        node = Tree("Error", Children)
        leafroot["node"] = node
        leafroot["index"] = j
        return leafroot







def DeclareSecDash(j):
    Children=[]
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    if CheckVar(j) == True:
        Declaration_dict = Declaration(j);
        Children.append(Declaration_dict["node"])

        DeclareSecDash_dict = DeclareSecDash(Declaration_dict["index"]);
        Children.append(DeclareSecDash_dict["node"])

        node = Tree("DeclareSecDash", Children)
        leafroot["node"] = node
        leafroot["index"] = DeclareSecDash_dict["index"];
        return leafroot


    else:
        node = Tree("Epsilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot


def IdDeclaration(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    if Tokens[j].token_type == S.Token_type.Identifier and Tokens[j+1].token_type == S.Token_type.Equal:
        final_dict = IdDeclarationDash(j);
        Children.append(final_dict["node"])

    else:
        final_dict = Match(S.Token_type.Identifier,j);
        Children.append(final_dict["node"])

    node = Tree("IdDeclaration", Children)
    leafroot["node"] = node
    leafroot["index"] = final_dict["index"]
    return leafroot


def IdDeclarationDash(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    if Tokens[j].token_type == S.Token_type.Identifier:
        Assignment_st_dict = Assignment_st(j);
        Children.append(Assignment_st_dict["node"])
        node = Tree("IdDeclarationDash", Children)
        leafroot["node"] = node
        leafroot["index"] = Assignment_st_dict["index"]
        return leafroot
    else:
        node = Tree("Espilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j
        return leafroot


def Declaration(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    VarType_dict = VarType(j)
    Children.append(VarType_dict["node"])

    Dcolon_dict = Match(S.Token_type.Dcolon,VarType_dict["index"])
    Children.append(Dcolon_dict["node"])

    IdDeclaration_dict = IdDeclaration(Dcolon_dict["index"])
    Children.append(IdDeclaration_dict["node"])

    DeclarationCont_dict = DeclarationCont(IdDeclaration_dict["index"])
    Children.append(DeclarationCont_dict["node"])



    node = Tree("Declaration", Children)
    leafroot["node"] = node
    leafroot["index"] = DeclarationCont_dict["index"]
    return leafroot

def DeclarationCont(j):
    Children =[]
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    DeclarationContDash_dict = DeclarationContDash(j);
    Children.append(DeclarationContDash_dict["node"])

    node = Tree("DeclarationCont", Children)
    leafroot["node"] = node
    leafroot["index"] = DeclarationContDash_dict["index"]
    return leafroot

def DeclarationContDash(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    if Tokens[j].token_type == S.Token_type.Coma:
        coma_dict = Match(S.Token_type.Coma,j)
        Children.append(coma_dict["node"])

        IdDeclaration_dict = IdDeclaration(coma_dict["index"])
        Children.append(IdDeclaration_dict["node"])


        DeclarationCont_dict = DeclarationContDash(IdDeclaration_dict["index"])
        Children.append(DeclarationCont_dict["node"])

        node = Tree("DeclarationContDash", Children)
        leafroot["node"] = node
        leafroot["index"] = DeclarationCont_dict["index"]
        return leafroot
    else:
        node = Tree("Epsilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot


def CheckValue(j):
    if Tokens[j].token_type == S.Token_type.IntegerVal or Tokens[j].token_type == S.Token_type.RealVal or Tokens[j].token_type == S.Token_type.LogicVal \
        or Tokens[j].token_type == S.Token_type.ComplexVal or Tokens[j].token_type == S.Token_type.CharacterVal:
        return True;

#problem in grammar its string here its character which one is true ????
def Value(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    Temp = Tokens[j].to_dict()
    if Temp["token_type"] == S.Token_type.IntegerVal:
        varType_dict = Match(S.Token_type.IntegerVal, j)
    elif Temp["token_type"] == S.Token_type.RealVal:
        varType_dict = Match(S.Token_type.RealVal, j)
    elif Temp["token_type"] == S.Token_type.CharacterVal:
        varType_dict = Match(S.Token_type.CharacterVal, j)
    elif Temp["token_type"] == S.Token_type.ComplexVal:
        varType_dict = Match(S.Token_type.ComplexVal, j)
    else:
        varType_dict = Match(S.Token_type.LogicVal, j)

    Children.append(varType_dict["node"])
    node = Tree("VarType", Children)
    leafroot["node"] = node
    leafroot["index"] = varType_dict["index"]
    return leafroot

def PrintList(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    PrintListDash_dict = PrintListDash(j);
    Children.append(PrintListDash_dict["node"])

    node = Tree("Printlist", Children)
    leafroot["node"] = node
    leafroot["index"] = PrintListDash_dict["index"];
    return leafroot

def PrintListDash(j):
    Chidlren = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    if Tokens[j].token_type == S.Token_type.Coma:
        coma_dict = Match(S.Token_type.Coma , j);
        Chidlren.append(coma_dict["node"])

        PrintItem_dict = PrintItem(coma_dict["index"])
        Chidlren.append(PrintItem_dict["node"])

        PrintListDash_dict = PrintListDash(PrintItem_dict["index"])
        Chidlren.append(PrintListDash_dict["node"])

        node = Tree("PrintListDash", Chidlren)
        leafroot["node"] = node
        leafroot["index"] = PrintListDash_dict["index"];
        return leafroot

    else:
        node = Tree("Epsilon", Chidlren)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot


def PrintItem(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    Temp = Tokens[j].to_dict()
    if CheckValue(j) == True:
        final_dict = Value(j);
        Children.append(final_dict["node"])
    else:
        final_dict= Match(S.Token_type.Identifier,j);
        Children.append(final_dict["node"]);

    node = Tree("PrintItem", Children)
    leafroot["node"] = node
    leafroot["index"] = final_dict["index"];
    return leafroot

def ReadList(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    ReadListDash_dict=ReadListDash(j);
    Children.append(ReadListDash_dict["node"])

    node = Tree("Readlist", Children)
    leafroot["node"] = node
    leafroot["index"] = ReadListDash["index"];
    return leafroot

def ReadListDash(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    if Tokens[j].token_type == S.Token_type.Coma:
        coma_dict = Match(S.Token_type.Coma,j);
        Children.append(coma_dict["index"]);

        identifier_dict = Match(S.Token_type.Identifier , coma_dict["index"])
        Children.append(identifier_dict["node"])

        PrintListDash_dict = PrintListDash(identifier_dict["index"])
        Children.append(PrintListDash_dict["node"])

        node = Tree("ReadListDash", Children)
        leafroot["node"] = node
        leafroot["index"] = PrintListDash_dict["index"];
        return leafroot


    else:
        node = Tree("Epsilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot


# here we used openB and CloseB as [ ] butt token there are ( ) we will see later
def Step(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot
    if Tokens[j].token_type == S.Token_type.Openb:
        openB_dict = Match(S.Token_type.Openb , j);
        Children.append(openB_dict["node"])

        int_val_dict = match(S.Token_type.IntegerVal , openB_dict["index"])
        Children.append(int_val_dict["node"])

        closeB_dict = Match((S.Token_type.Closedb,int_val_dict["index"]))
        Children.append(closeB_dict["node"])

        node = Tree("Step", Children)
        leafroot["node"] = node
        leafroot["index"] = closeB_dict["index"]
        return leafroot

    else:
        node = Tree("Epsilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

def IfStatement(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    If_dict = Match(S.Token_type.If , j)
    Children.append(If_dict["node"])

    openB = Match(S.Token_type.Openb,If_dict["index"])
    Children.append(openB["node"])

    Condition_dict = Condition(openB["index"])
    Children.append(Condition_dict["node"])

    closeB_dict = Match(S.Token_type.Closedb, Condition_dict["index"])
    Children.append(closeB_dict["node"])

    then_dict = Match(S.Token_type.Then, closeB_dict["index"])
    Children.append(then_dict["node"])

    Statements_dict = Statements(then_dict["index"])
    Children.append(Statements_dict["node"])

    node = Tree("IfStatement", Children)
    leafroot["node"] = node
    leafroot["index"] = Statements_dict["index"];
    return leafroot


def ElseSec(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    if Tokens[j].token_type == S.Token_type.Else:
        else_dict = Match(S.Token_type.Else,j)
        Children.append(else_dict["node"])


        Statements_dict = Statements(else_dict["index"])
        Children.append(Statements_dict["node"])

        node = Tree("ElseSec", Children)
        leafroot["node"] = node
        leafroot["index"] = Statements_dict["index"];
        return leafroot
    else:
        node = Tree("Epsilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot


def ElseIfSec(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    ElseSecDash_dict = ElseIfSecDash(j);
    Children.append(ElseSecDash_dict["node"])
    node = Tree("ElseIfSec", Children)
    leafroot["node"] = node
    leafroot["index"] = ElseSecDash_dict["index"] ;
    return leafroot

def ElseIfSecDash(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    if Tokens[j].token_type == S.Token_type.Elif:
        else_dict = Match(S.Token_type.Elif,j);
        Children.append(else_dict["node"])

        IfStatement_dict = IfStatement(else_dict["index"])
        Children.append(IfStatement_dict["node"])

        ElseIfSecDash_dict = ElseIfSecDash(IfStatement_dict["index"])
        Children.append(ElseIfSecDash_dict["node"])

        node = Tree("ElseIfSecDash", Children)
        leafroot["node"] = node
        leafroot["index"] = ElseIfSecDash_dict["index"];
        return leafroot

    else:
        node = Tree("Epsilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot


def NewLine(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    newLine_dict = Match(S.Token_type.NewLine , j);
    Children.append(newLine_dict["node"])

    node = Tree("NewLine", Children)
    leafroot["node"] = node
    leafroot["index"] = newLine_dict["index"];
    return leafroot


def Condition(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    Expression_dict = Expression(j);
    Children.append(Expression_dict["index"])

    RelationOp_dict = RelationOp(Expression_dict["index"])
    Children.append(RelationOp_dict["node"])

    Expression1_dict = Expression(RelationOp_dict["index"]);
    Children.append(Expression1_dict["node"])

    node = Tree("Condition", Children)
    leafroot["node"] = node
    leafroot["index"] = Expression1_dict["index"];
    return leafroot

def checkFactor(j):
    if Tokens[j].token_type == S.Token_type.Identifier or Tokens[j].token_type == S.Token_type.IntegerVal \
        or Tokens[j].token_type == S.Token_type.RealVal or Tokens[j].token_type == S.Token_type.Openb:
        return True;


def Expression(j):
    Children  = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    Temp = Tokens[j].to_dict()
    if checkFactor(j) == True:
        Term_dict = Term(j);
        Children.append(Term_dict["node"])

        final = ExpressionDash(Term_dict["index"])
        Children.append(final["node"])

        node = Tree("Expression", Children)
        leafroot["node"] = node
        leafroot["index"] = final["index"]
        return leafroot

    elif Temp["token_type"] == S.Token_type.Openb:
        OpenB_dict = Match(S.Token_type.Openb , j);
        Children.append(OpenB_dict["node"])

        Expression_dict = Expression(OpenB_dict["index"])
        Children.append(Expression_dict["node"])

        Close_dict = Match(S.Token_type.Closedb, Expression_dict["index"]);
        Children.append(Close_dict["node"])

        final =ExpressionDash(Close_dict["index"]);
        Children.append(final["node"])

        node = Tree("Expression", Children)
        leafroot["node"] = node
        leafroot["index"] = final["index"]
        return leafroot



    node = Tree("Error", Children)
    leafroot["node"] = node
    leafroot["index"] = j+1
    return leafroot





def ExpressionDash(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    if Tokens[j].token_type ==  S.Token_type.Plus or Tokens[j].token_type == S.Token_type.Minus:
        AddOp_dict = AddOp(j);
        Children.append(AddOp_dict["node"])

        Term_dict = Term(AddOp_dict["index"])
        Children.append(Term_dict["node"])

        ExpressionDash_dict = ExpressionDash(Term_dict["index"])
        Children.append(ExpressionDash_dict["node"])

        node = Tree("ExpressionDash", Children)
        leafroot["node"] = node
        leafroot["index"] = ExpressionDash_dict["index"]
        return leafroot
    else:
        node = Tree("Epsilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j
        return leafroot

def Term(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    Factor_dict = Factor(j);
    Children.append(Factor_dict["node"])

    TermDash_dict = TermDash(Factor_dict["index"])
    Children.append(TermDash_dict["node"])

    node = Tree("Term", Children)
    leafroot["node"] = node
    leafroot["index"] = TermDash_dict["index"]
    return leafroot


def TermDash(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    if Tokens[j].token_type ==  S.Token_type.Multiplication or Tokens[j].token_type == S.Token_type.Division:
        MultipyOp_dict = MultipyOp(j);
        Children.append(MultipyOp_dict["node"])

        Factor_dict = Factor(MultipyOp_dict["index"])
        Children.append(Factor_dict["node"])

        TermDash_dict = TermDash(Factor_dict["index"])
        Children.append(TermDash_dict["node"])

        node = Tree("TermDash", Children)
        leafroot["node"] = node
        leafroot["index"] = TermDash_dict["index"]
        return leafroot
    else:
        node = Tree("Epsilon", Children)
        leafroot["node"] = node
        leafroot["index"] = j
        return leafroot





def Factor(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    Temp = Tokens[j].to_dict()
    if Temp["token_type"] == S.Token_type.Identifier:
        final = Match(S.Token_type.Identifier, j);
        Children.append(final["node"])

    elif Temp["token_type"] == S.Token_type.RealVal:

        final = Match(S.Token_type.RealVal, j)
        Children.append(final["node"])

    elif Temp["token_type"] == S.Token_type.IntegerVal:
        final = Match(S.Token_type.IntegerVal, j)
        Children.append(final["node"])
    else:
        OpenB_dict = Match(S.Token_type.Openb, j);
        Children.append(OpenB_dict["node"])

        Expression_dict = Expression(OpenB_dict["index"])
        Children.append(Expression_dict["node"])

        final = Match(S.Token_type.Closedb, j);
        Children.append(final["node"])
    node = Tree("Factor", Children)
    leafroot["node"] = node
    leafroot["index"] = final["index"]
    return leafroot


def MultipyOp(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    Temp = Tokens[j].to_dict()
    if Temp["token_type"] == S.Token_type.Multiplication:
        final = Match(S.Token_type.Multiplication, j)
        Children.append(final["node"])
    else:
        final = Match(S.Token_type.Division, j)
        Children.append(final["node"])


    node = Tree("MutlipyOp", Children)
    leafroot["node"] = node
    leafroot["index"] = final["index"]
    return leafroot

def AddOp(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    Temp = Tokens[j].to_dict()
    if Temp["token_type"] == S.Token_type.Plus:
        final = Match(S.Token_type.Plus, j)
        Children.append(final["node"])
    else:
        final = Match(S.Token_type.Minus, j)
        Children.append(final["node"])

    node = Tree("AddOp", Children)
    leafroot["node"] = node
    leafroot["index"] = final["index"]
    return leafroot


def RelationOp(j):
    Children = []
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    Temp = Tokens[j].to_dict()
    if Temp["token_type"] == S.Token_type.Morethan:
        final = Match(S.Token_type.Morethan, j)
        Children.append(final["node"])

    elif Temp["token_type"] == S.Token_type.Lessthan:
        final = Match(S.Token_type.Lessthan, j)
        Children.append(final["node"])

    elif Temp["token_type"] == S.Token_type.Morethanorequal:
        final = Match(S.Token_type.Morethanorequal, j)
        Children.append(final["node"])

    elif Temp["token_type"] == S.Token_type.Lessthanorequal:
        final = Match(S.Token_type.Lessthanorequal, j)
        Children.append(final["node"])

    elif Temp["token_type"] == S.Token_type.Equalequal:
        final = Match(S.Token_type.Equalequal, j)
        Children.append(final["node"])

    else:
        final = Match(S.Token_type.Notequal, j)
        Children.append(final["node"])

    node = Tree("RelationShip", Children)
    leafroot["node"] = node
    leafroot["index"] = final["index"]
    return leafroot


def CharType(j):
    Children = [];
    leafroot = dict()
    if j >= len(Tokens):
        node = Tree("error", Children)
        leafroot["node"] = node
        leafroot["index"] = j;
        return leafroot

    character_dict = Match(S.Token_type.Character,j);
    Children.append(character_dict["node"]);

    OpenB_dict = Match(S.Token_type.Openb, character_dict["index"])
    Children.append(OpenB_dict["node"])

    Len_dict = Match(S.Token_type.Identifier , OpenB_dict["index"])
    Children.append(Len_dict["node"])

    equal_dict = Match(S.Token_type.Equal , Len_dict["index"])
    Children.append(equal_dict["node"])

    int_val_dict = Match(S.Token_type.IntegerVal,equal_dict["index"])
    Children.append(int_val_dict["node"])

    closeB_dict = Match(S.Token_type.Closedb , int_val_dict["index"])
    Children.append(closeB_dict["node"])

    node = Tree("CharType", Children)
    leafroot["node"] = node
    leafroot["index"] = closeB_dict["index"]
    return leafroot

class analyize:
    def __init__(self,messege ,expected,after,line):
        self.message = messege
        self.expected = expected
        self.after = after
        self.line = line

    def to_tokens(self):
        return {
            'error messege': self.message,
            'expected': self.expected,
            'After': self.after,
            'Line' : self.line
        }
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
            print("error at line ",S.rows[j] , "expected here ",a.name)

            # Check if the enum instance is in the Operators dictionary
            print("temp is here " ,a)
            if a in S.Operators.values():
                operator = next(key for key, value in S.Operators.items() if value == a)
                #  errors.append(f'error at line {S.rows[j]} expected here {a.name} after the {Tokens[j-1].lex}')
                tempObject = analyize(f'Error expected Operator', "Operator", Tokens[j - 1].lex, S.rows[j])
                # tempObject = analyize()
                errors.append(tempObject)
            else:
                #  errors.append(f'error at line {S.rows[j]} expected here {a.name} after the {Tokens[j-1].lex}')
                tempObject = analyize(f'Error expected {a.name}', a.name, Tokens[j - 1].lex, S.rows[j])
                # tempObject = analyize()
                errors.append(tempObject)




            return output
    else:
        output["node"] = ["error"]
        output["index"] = j + 1
        return output


def rootScan(text):
    Scan(text);


def Scan(text):
    x1 = text
    S.find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    # print(df)

    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    # start Parsing
    Node = Parse()
    for i in errors:
        print(i);
    # to display errorlist
    df = pd.DataFrame.from_records([t.to_tokens() for t in errors])
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    Node.draw()
    # clear your list

    # label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    # canvas1.create_window(200, 210, window=label3)

    # label4 = tk.Label(root, text="S.Token_type"+x1, font=('helvetica', 10, 'bold'))
    # canvas1.create_window(200, 230, window=label4)




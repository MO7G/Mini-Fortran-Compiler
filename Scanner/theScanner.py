import pandas as pd
import tkinter as tk
from enum import Enum
import re
import pandastable as pt
from Parser.parser import  readTheToknes as rd
import  sys as os

class Token_type(Enum):  # listing all tokens type
    Program = 1
    Implicit = 2
    none = 3
    End = 4
    Real = 5
    Complex = 6
    Logical = 7
    Character = 8
    Parameter = 9
    If = 10
    Then = 11
    Else = 12
    Do = 13
    Var = 14
    Read = 15
    Print = 16
    Identifier = 17
    Constant = 18
    Procedure = 19
    Equal = 20
    Error = 21
    Dcolon = 22
    Openb = 23
    Closedb = 24
    Coma = 25
    Plus = 26
    Minus = 27
    Division = 28
    Multiplication = 29
    Notequal = 30
    Lessthan = 31
    Morethan = 32
    Equalequal = 33
    Lessthanorequal = 34
    Morethanorequal = 35
    Comment = 36
    Integer = 37
    IntegerVal = 38
    RealVal = 39
    LogicVal = 40
    CharacterVal = 41
    ComplexVal = 42
    NewLine = 43
    Len = 44
    OpenSquBrack = 45
    ClosedSquBrack = 46
    Elif = 47




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
    "if": Token_type.If,
    "program": Token_type.Program,
    "implicit": Token_type.Implicit,
    "none": Token_type.none,
    "end": Token_type.End,
    "integer": Token_type.Integer,
    "real": Token_type.Real,
    "complex": Token_type.Complex,
    "parameter": Token_type.Parameter,
    "character": Token_type.Character,
    "logical": Token_type.Logical,
    "do": Token_type.Do,
    "else": Token_type.Else,
    "elif": Token_type.Elif,
    "then": Token_type.Then,
    "var": Token_type.Var,
    "read": Token_type.Read,
    "print": Token_type.Print,
    "\\n" : Token_type.NewLine
}

Operators = {
    "=": Token_type.Equal,
    "+": Token_type.Plus,
    "-": Token_type.Minus,
    "*": Token_type.Multiplication,
    "/": Token_type.Division,
    "::": Token_type.Dcolon,
    "(": Token_type.Openb,
    ")": Token_type.Closedb,
    ",": Token_type.Coma,
    "==": Token_type.Equalequal,
    "/=": Token_type.Notequal,
    ">": Token_type.Morethan,
    "<": Token_type.Lessthan,
    ">=": Token_type.Morethanorequal,
    "<=": Token_type.Lessthanorequal,
    "[": Token_type.OpenSquBrack,
    "]":Token_type.ClosedSquBrack
}
Tokens = []
errors = []
lexems = []
videos = []
rows = []
errorRowsInScanner = []
COUNTER =1;
NumberOfComments = 0;
FlagOfComment = False;
def split_lexems(line):
    add_NewlineFlag = True
    i = 0

    while (i < len(line)):
        le = ''
        # if line[i] == ' ':
        if line[i] == '!':
            global COUNTER
            COUNTER=COUNTER+1
            add_NewlineFlag = False
            global FlagOfComment;
            FlagOfComment=True;
            return

        ##############################
        elif line[i] == '.':
            while True:
                le += line[i]
                i += 1
                if i >= len(line):
                    lexems.append(le)
                    break
                elif line[i] == '.':
                    le += line[i]
                    lexems.append(le)
                    break
                elif line[i] == ' ' or line[i] in Operators:  # | (line[i] == ' '):
                    lexems.append(le)
                    i -= 1
                    break
        ##############################
        elif line[i] == '\"':
            while True:
                le += line[i]
                i += 1
                if i >= len(line):
                    lexems.append(le)
                    break
                elif line[i] == '\"':
                    le += line[i]
                    lexems.append(le)
                    break
        ##############################
        elif line[i] == '\'':
            while True:
                le += line[i]
                i += 1
                if i >= len(line):
                    lexems.append(le)
                    break
                elif line[i] == '\'':  # | (line[i] == ' '):
                    le += line[i]
                    lexems.append(le)
                    break
        ##############################
        elif line[i].isalpha():
            while True:
                le += line[i]
                i += 1
                if i >= len(line):
                    lexems.append(le)
                    break
                elif line[i] == ' ' or line[i] in Operators: # | (line[i] == ' '):
                    lexems.append(le)
                    i-=1
                    break
        ##############################
        elif line[i] == ':':
            while True:
                le += line[i]
                i += 1
                if i >= len(line):
                    lexems.append(le)
                    break
                elif line[i] == ':':  # | (line[i] == ' '):
                    le += line[i]
                    lexems.append(le)
                    break
                elif line[i] == ' ' or line[i] in Operators:  # | (line[i] == ' '):
                    lexems.append(le)
                    i -= 1
                    break
        ##############################
        elif line[i] in ['*',')','(',',',']','[']:
            le += line[i]
            lexems.append(le)
        ##############################
        elif line[i] in ['=','/','<','>',]:
            le += line[i]
            i += 1
            if i >= len(line):
                lexems.append(le)
            elif line[i] =='=':
                le += line[i]
                lexems.append(le)
            else:
                lexems.append(le)
        ##############################
        elif line[i] in ['+','-']:
            le += line[i]
            i += 1
            while True:
                if i >= len(line):
                    lexems.append(le)
                    break
                elif line[i] == '.' or line[i].isdigit():
                    le += line[i]
                    i+=1
                elif line[i] == ' ':
                    lexems.append(le)
                    break

        ##############################
        elif line[i].isdigit():
            le += line[i]
            i += 1
            while True:
                if i >= len(line):
                    lexems.append(le)
                    break
                elif line[i] == '.' or line[i].isdigit():
                    le += line[i]
                    i+=1

                elif line[i] == ' ' or line[i] in Operators:
                    lexems.append(le)
                    i -=1
                    break
                elif line[i].isdigit() == False and (line[i] == ' '):
                    lexems.append(le)
                    i-=1;
                    break;
                elif line[i].isdigit() == False and line[i].isalpha() == True:
                    le+=line[i]
                    i+=1
                    continue;
        ##############################
        i += 1

    return add_NewlineFlag


def find_token(text):

    # Splitting the string and storing each split along with its index
    lines = text.split('\n')
    for line in lines:
        if split_lexems(line):
            lexems.append('\n')
    # lexems = text.split()


            intValPtrn = re.compile("[-+]?\d+")
            realValPtrn = re.compile(f"({intValPtrn.pattern}\.\d*)|([+-]?.\d+)")
            complexPtrn = re.compile("complex", flags=re.I)
            # complxValPtrn = re.compile(
            #     f"{complexPtrn.pattern}\(({intValPtrn.pattern}|{realValPtrn.pattern}),({intValPtrn.pattern}|{realValPtrn.pattern})\)",
            #     flags=re.I)

            global COUNTER
            for le in lexems:
                if (le == '\n'):
                    continue;
                elif (re.fullmatch("if", le, flags=re.I)):
                    new_token = token(le, Token_type.If)
                    Tokens.append(new_token)
                    videos.append('if.mp4')
                    rows.append(COUNTER)

                elif (re.fullmatch("program", le, flags=re.I)):
                    new_token = token(le, Token_type.Program)
                    Tokens.append(new_token)
                    videos.append('program.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("implicit", le, flags=re.I)):
                    new_token = token(le, Token_type.Implicit)
                    Tokens.append(new_token)
                    videos.append('implicit.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("none", le, flags=re.I)):
                    new_token = token(le, Token_type.none)
                    Tokens.append(new_token)
                    videos.append('none.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("end", le, flags=re.I)):
                    new_token = token(le, Token_type.End)
                    Tokens.append(new_token)
                    videos.append('end.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("elif", le, flags=re.I)):
                    new_token = token(le, Token_type.Elif)
                    Tokens.append(new_token)
                    rows.append(COUNTER)



                elif (re.fullmatch("integer", le, flags=re.I)):
                    new_token = token(le, Token_type.Integer)
                    Tokens.append(new_token)
                    videos.append('integer.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("real", le, flags=re.I)):
                    new_token = token(le, Token_type.Real)
                    Tokens.append(new_token)
                    videos.append('real.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch(complexPtrn.pattern, le, flags=re.I)):
                    new_token = token(le, Token_type.Complex)
                    Tokens.append(new_token)
                    videos.append('complex.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("logical", le, flags=re.I)):
                    new_token = token(le, Token_type.Logical)
                    Tokens.append(new_token)
                    videos.append('logical.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("character", le, flags=re.I)):
                    new_token = token(le, Token_type.Character)
                    Tokens.append(new_token)
                    videos.append('character.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("parameter", le, flags=re.I)):
                    new_token = token(le, Token_type.Parameter)
                    Tokens.append(new_token)
                    videos.append('parameter.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("then", le, flags=re.I)):
                    new_token = token(le, Token_type.Then)
                    Tokens.append(new_token)
                    videos.append('then.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("else", le, flags=re.I)):
                    new_token = token(le, Token_type.Else)
                    Tokens.append(new_token)
                    videos.append('else.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("do", le, flags=re.I)):
                    new_token = token(le, Token_type.Do)
                    Tokens.append(new_token)
                    videos.append('do.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("len", le, flags=re.I)):
                    new_token = token(le, Token_type.Len)
                    Tokens.append(new_token)
                    videos.append('len.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("var", le, flags=re.I)):
                    new_token = token(le, Token_type.Var)
                    Tokens.append(new_token)
                    videos.append('var.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("read", le, flags=re.I)):
                    new_token = token(le, Token_type.Read)
                    Tokens.append(new_token)
                    videos.append('read.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("print", le, flags=re.I)):
                    new_token = token(le, Token_type.Print)
                    Tokens.append(new_token)
                    videos.append('print.mp4')
                    rows.append(COUNTER)


                elif (le in Operators):
                    new_token = token(le, Operators[le])
                    Tokens.append(new_token)
                    videos.append('operators.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch("[a-zA-Z][\w_]*", le)):
                    new_token = token(le, Token_type.Identifier)
                    Tokens.append(new_token)
                    videos.append('identifier.mp4')
                    rows.append(COUNTER)



                elif (re.fullmatch(intValPtrn.pattern, le)):
                    new_token = token(le, Token_type.IntegerVal)
                    Tokens.append(new_token)
                    videos.append('intVal.mp4')
                    rows.append(COUNTER)


                elif (re.fullmatch(realValPtrn.pattern, le)):
                    new_token = token(le, Token_type.RealVal)
                    Tokens.append(new_token)
                    videos.append("intOrrealVal.mp4")
                    rows.append(COUNTER)




                # elif (re.fullmatch(complxValPtrn.pattern, le,flags=re.I)):
                #     new_token = token(le, Token_type.ComplexVal)
                #     Tokens.append(new_token)
                elif (re.fullmatch("(\".*\")|(\'.*\')", le)):
                    new_token = token(le, Token_type.CharacterVal)
                    Tokens.append(new_token)
                    videos.append("charVal.mp4")
                    rows.append(COUNTER)



                elif (re.fullmatch(".false.", le, flags=re.I)):
                    new_token = token(le, Token_type.LogicVal)
                    Tokens.append(new_token)
                    videos.append(".false..mp4")
                    rows.append(COUNTER)



                elif (re.fullmatch(".true.", le, flags=re.I)):
                    new_token = token(le, Token_type.LogicVal)
                    Tokens.append(new_token)
                    videos.append(".true..mp4")
                    rows.append(COUNTER)



                elif (re.fullmatch("!.*", le)):
                    new_token = token(le, Token_type.Comment)
                    Tokens.append(new_token)
                    videos.append("coment.mp4")
                    rows.append(COUNTER)

                else:
                    new_token = token(le, Token_type.Error)
                    Tokens.append(new_token)
                    errors.append(new_token)
                    errorRowsInScanner.append(COUNTER)
                    rows.append(COUNTER);
                    print("!!!!!!   Error is found  !!!!!!")

            COUNTER = COUNTER + 1
            lexems[:] = []

# GUI
def rootScan(text):
    Scan(text)
    rd(Tokens)

def ClearMe():
    Tokens.clear()
    errors.clear();

def fillVideos():
    with open("animation/array_module.py", "w") as f:
        f.write("my_array = " + repr(videos))
    print(videos)

def Scan(x1):
    find_token(x1)
    df = pd.DataFrame.from_records([t.to_dict() for t in Tokens])
    rd(Tokens)
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()

    # to display errorlist
    df1 = pd.DataFrame.from_records([t.to_dict() for t in errors])
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()

    for string,index in zip(Tokens,rows):
       print(string.lex , "  " , index)

    fillVideos()
    del Tokens[:]
    del errors[:]
    del lexems[:]
    del videos[:]
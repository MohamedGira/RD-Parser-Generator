import sys
import os
sys.path.append(os.path.dirname(__file__))
import globals
from Tokens import *
from nltk.tree import *
neeew=1
from enum import Enum
class Token_type(Enum):  # listing all tokens type

    # List Representation
    OpenParenthesis = 1
    CloseParenthesis = 2

    # ReservedWords
    Dotimes = 3
    When = 4
    Read = 5
    Write = 6
    LogicalTrue = 7
    LogicalFalse = 8

    # Operators
    Semicolon = 9
    PlusOp = 10
    MinusOp = 11
    MultiplyOp = 12
    DivideOp = 13
    ModOp = 14
    RemOp = 15
    IncrementOp = 16
    DecrementOp = 17
    GreaterThanOrEqualOp = 18
    LessThanOrEqualOp = 19
    EqualOp = 20
    NotEqualOp = 21

    # Other
    String = 22
    Setq = 23
    Error = 24
    Number = 25
    Identifier = 26
    Cos = 27
    Sin = 28
    Tan = 29
    Function=30
    GreaterThanOp=31
    LessThanOp=32

# class token to hold string and token type
class Token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type
        self.line=0
    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }

# Reserved word Dictionary
ReservedWords = {"(": Token_type.OpenParenthesis,
            ")": Token_type.CloseParenthesis,
            "dotimes": Token_type.Dotimes,
            "when": Token_type.When,
            "read": Token_type.Read,
            "write": Token_type.Write,
            "nil": Token_type.LogicalFalse,
            "setq": Token_type.Setq,
            "cos": Token_type.Cos,
            "tan": Token_type.Tan,
            "t": Token_type.LogicalTrue,
            "sin": Token_type.Sin
            }

Operators = {";": Token_type.Semicolon,
             "+": Token_type.PlusOp,
             "-": Token_type.MinusOp,
             "*": Token_type.MultiplyOp,
             "/": Token_type.DivideOp,
             "mod": Token_type.ModOp,
             "rem": Token_type.RemOp,
             "incf": Token_type.IncrementOp,
             "decf": Token_type.DecrementOp,
             "<=": Token_type.LessThanOrEqualOp,
             ">=": Token_type.GreaterThanOrEqualOp,
             "=": Token_type.EqualOp,
             "<>": Token_type.NotEqualOp,
             ">": Token_type.GreaterThanOp,
             "<": Token_type.LessThanOp

             }


#lisp
def Program (ind):
 out={}
 matches=[Lists]
 return applyfills(matches,ind,"program")

def Lists (ind):
 out={}
 matches=[List,Lists_dash]
 return applyfills(matches,ind,"lists")

def Lists_dash (ind):
 out={}
 if Match(Token_type.OpenParenthesis,ind,False)["node"]!=["error"]:
     matches=[List,Lists_dash]
     return applyfills(matches,ind,"lists_dash")
 else:
   out["node"]=Tree("Lists_dash",["ε"])
   out["index"]=ind
   return out

def List (ind):
 out={}
 matches=[Token_type.OpenParenthesis,Contents,Token_type.CloseParenthesis]
 return applyfills(matches,ind,"list")

def Contents (ind):
 out={}
 matches=[Content,Contents_dash]
 return applyfills(matches,ind,"contents")

def Contents_dash (ind):
 out={}
 if MatchArr([Token_type.OpenParenthesis,Token_type.Dotimes,Token_type.When,Token_type.IncrementOp,Token_type.DecrementOp,Token_type.Write,Token_type.Sin,Token_type.Cos,Token_type.Tan,Token_type.Setq,Token_type.PlusOp,Token_type.MinusOp,Token_type.MultiplyOp,Token_type.DivideOp,Token_type.ModOp,Token_type.RemOp,Token_type.GreaterThanOrEqualOp,Token_type.LessThanOrEqualOp,Token_type.GreaterThanOp,Token_type.LessThanOp,Token_type.EqualOp,Token_type.NotEqualOp,Token_type.Identifier,Token_type.Read,Token_type.LogicalTrue,Token_type.LogicalFalse],ind,False):
     matches=[Content,Contents_dash]
     return applyfills(matches,ind,"contents_dash")
 else:
   out["node"]=Tree("Contents_dash",["ε"])
   out["index"]=ind
   return out

def Content (ind):
 out={}
 if Match(Token_type.OpenParenthesis,ind,False)["node"]!=["error"]:
     matches=[List]
     return applyfills(matches,ind,"content")
 elif MatchArr([Token_type.Dotimes,Token_type.When],ind,False):
     matches=[Block]
     return applyfills(matches,ind,"content")
 elif MatchArr([Token_type.IncrementOp,Token_type.DecrementOp,Token_type.Write,Token_type.Sin,Token_type.Cos,Token_type.Tan,Token_type.Setq,Token_type.PlusOp,Token_type.MinusOp,Token_type.MultiplyOp,Token_type.DivideOp,Token_type.ModOp,Token_type.RemOp,Token_type.GreaterThanOrEqualOp,Token_type.LessThanOrEqualOp,Token_type.GreaterThanOp,Token_type.LessThanOp,Token_type.EqualOp,Token_type.NotEqualOp,Token_type.Identifier,Token_type.Read,Token_type.LogicalTrue,Token_type.LogicalFalse],ind,False):
     matches=[Expression]
     return applyfills(matches,ind,"content")
 else:
   out["node"]=Tree("Content",["ε"])
   out["index"]=ind
   return out

def Block (ind):
 out={}
 if Match(Token_type.Dotimes,ind,False)["node"]!=["error"]:
     matches=[Token_type.Dotimes,Token_type.OpenParenthesis,Token_type.Identifier,Token_type.Number,Token_type.CloseParenthesis,Lists]
     return applyfills(matches,ind,"block")
 elif Match(Token_type.When,ind,False)["node"]!=["error"]:
     matches=[Token_type.When,Token_type.OpenParenthesis,Expression,Token_type.CloseParenthesis,Lists]
     return applyfills(matches,ind,"block")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=ind
     return out

def Expression (ind):
 out={}
 if MatchArr([Token_type.IncrementOp,Token_type.DecrementOp,Token_type.Write,Token_type.Sin,Token_type.Cos,Token_type.Tan,Token_type.Setq,Token_type.PlusOp,Token_type.MinusOp,Token_type.MultiplyOp,Token_type.DivideOp,Token_type.ModOp,Token_type.RemOp,Token_type.GreaterThanOrEqualOp,Token_type.LessThanOrEqualOp,Token_type.GreaterThanOp,Token_type.LessThanOp,Token_type.EqualOp,Token_type.NotEqualOp,Token_type.Identifier,Token_type.Read],ind,False):
     matches=[Function]
     return applyfills(matches,ind,"expression")
 elif Match(Token_type.LogicalTrue,ind,False)["node"]!=["error"]:
     matches=[Token_type.LogicalTrue]
     return applyfills(matches,ind,"expression")
 elif Match(Token_type.LogicalFalse,ind,False)["node"]!=["error"]:
     matches=[Token_type.LogicalFalse]
     return applyfills(matches,ind,"expression")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=ind
     return out

def Function (ind):
 out={}
 if MatchArr([Token_type.IncrementOp,Token_type.DecrementOp,Token_type.Write,Token_type.Sin,Token_type.Cos,Token_type.Tan],ind,False):
     matches=[UnaryFunction]
     return applyfills(matches,ind,"function")
 elif MatchArr([Token_type.Setq,Token_type.PlusOp,Token_type.MinusOp,Token_type.MultiplyOp,Token_type.DivideOp,Token_type.ModOp,Token_type.RemOp,Token_type.GreaterThanOrEqualOp,Token_type.LessThanOrEqualOp,Token_type.GreaterThanOp,Token_type.LessThanOp,Token_type.EqualOp,Token_type.NotEqualOp],ind,False):
     matches=[BinaryFunction]
     return applyfills(matches,ind,"function")
 elif Match(Token_type.Identifier,ind,False)["node"]!=["error"]:
     matches=[OtherFunction]
     return applyfills(matches,ind,"function")
 elif Match(Token_type.Read,ind,False)["node"]!=["error"]:
     matches=[Token_type.Read]
     return applyfills(matches,ind,"function")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=ind
     return out

def UnaryFunction (ind):
 out={}
 matches=[UnaryFunctionName,Value]
 return applyfills(matches,ind,"unaryfunction")

def UnaryFunctionName (ind):
 out={}
 if MatchArr([Token_type.IncrementOp,Token_type.DecrementOp],ind,False):
     matches=[UnaryOperator]
     return applyfills(matches,ind,"unaryfunctionname")
 elif Match(Token_type.Write,ind,False)["node"]!=["error"]:
     matches=[Token_type.Write]
     return applyfills(matches,ind,"unaryfunctionname")
 elif Match(Token_type.Sin,ind,False)["node"]!=["error"]:
     matches=[Token_type.Sin]
     return applyfills(matches,ind,"unaryfunctionname")
 elif Match(Token_type.Cos,ind,False)["node"]!=["error"]:
     matches=[Token_type.Cos]
     return applyfills(matches,ind,"unaryfunctionname")
 elif Match(Token_type.Tan,ind,False)["node"]!=["error"]:
     matches=[Token_type.Tan]
     return applyfills(matches,ind,"unaryfunctionname")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=ind
     return out

def BinaryFunction (ind):
 out={}
 if Match(Token_type.Setq,ind,False)["node"]!=["error"]:
     matches=[SetqFunction]
     return applyfills(matches,ind,"binaryfunction")
 elif MatchArr([Token_type.PlusOp,Token_type.MinusOp,Token_type.MultiplyOp,Token_type.DivideOp,Token_type.ModOp,Token_type.RemOp,Token_type.GreaterThanOrEqualOp,Token_type.LessThanOrEqualOp,Token_type.GreaterThanOp,Token_type.LessThanOp,Token_type.EqualOp,Token_type.NotEqualOp],ind,False):
     matches=[BinaryOperatorFunction]
     return applyfills(matches,ind,"binaryfunction")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=ind
     return out

def SetqFunction (ind):
 out={}
 matches=[Token_type.Setq,Token_type.Identifier,Value]
 return applyfills(matches,ind,"setqfunction")

def BinaryOperatorFunction (ind):
 out={}
 matches=[BinaryOperator,Value,Value]
 return applyfills(matches,ind,"binaryoperatorfunction")

def OtherFunction (ind):
 out={}
 matches=[Token_type.Identifier,Parameters]
 return applyfills(matches,ind,"otherfunction")

def UnaryOperator (ind):
 out={}
 if Match(Token_type.IncrementOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.IncrementOp]
     return applyfills(matches,ind,"unaryoperator")
 elif Match(Token_type.DecrementOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.DecrementOp]
     return applyfills(matches,ind,"unaryoperator")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=ind
     return out

def BinaryOperator (ind):
 out={}
 if Match(Token_type.PlusOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.PlusOp]
     return applyfills(matches,ind,"binaryoperator")
 elif Match(Token_type.MinusOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.MinusOp]
     return applyfills(matches,ind,"binaryoperator")
 elif Match(Token_type.MultiplyOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.MultiplyOp]
     return applyfills(matches,ind,"binaryoperator")
 elif Match(Token_type.DivideOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.DivideOp]
     return applyfills(matches,ind,"binaryoperator")
 elif Match(Token_type.ModOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.ModOp]
     return applyfills(matches,ind,"binaryoperator")
 elif Match(Token_type.RemOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.RemOp]
     return applyfills(matches,ind,"binaryoperator")
 elif Match(Token_type.GreaterThanOrEqualOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.GreaterThanOrEqualOp]
     return applyfills(matches,ind,"binaryoperator")
 elif Match(Token_type.LessThanOrEqualOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.LessThanOrEqualOp]
     return applyfills(matches,ind,"binaryoperator")
 elif Match(Token_type.GreaterThanOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.GreaterThanOp]
     return applyfills(matches,ind,"binaryoperator")
 elif Match(Token_type.LessThanOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.LessThanOp]
     return applyfills(matches,ind,"binaryoperator")
 elif Match(Token_type.EqualOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.EqualOp]
     return applyfills(matches,ind,"binaryoperator")
 elif Match(Token_type.NotEqualOp,ind,False)["node"]!=["error"]:
     matches=[Token_type.NotEqualOp]
     return applyfills(matches,ind,"binaryoperator")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=ind
     return out

def Parameters (ind):
 out={}
 if MatchArr([Token_type.Identifier,Token_type.Number,Token_type.IncrementOp,Token_type.DecrementOp,Token_type.Write,Token_type.Sin,Token_type.Cos,Token_type.Tan,Token_type.Setq,Token_type.PlusOp,Token_type.MinusOp,Token_type.MultiplyOp,Token_type.DivideOp,Token_type.ModOp,Token_type.RemOp,Token_type.GreaterThanOrEqualOp,Token_type.LessThanOrEqualOp,Token_type.GreaterThanOp,Token_type.LessThanOp,Token_type.EqualOp,Token_type.NotEqualOp,Token_type.Identifier,Token_type.Read,Token_type.LogicalTrue,Token_type.LogicalFalse,Token_type.String],ind,False):
     matches=[Value,Parameters_dash]
     return applyfills(matches,ind,"parameters")
 else:
   out["node"]=Tree("Parameters",["ε"])
   out["index"]=ind
   return out

def Parameters_dash (ind):
 out={}
 if MatchArr([Token_type.Identifier,Token_type.Number,Token_type.IncrementOp,Token_type.DecrementOp,Token_type.Write,Token_type.Sin,Token_type.Cos,Token_type.Tan,Token_type.Setq,Token_type.PlusOp,Token_type.MinusOp,Token_type.MultiplyOp,Token_type.DivideOp,Token_type.ModOp,Token_type.RemOp,Token_type.GreaterThanOrEqualOp,Token_type.LessThanOrEqualOp,Token_type.GreaterThanOp,Token_type.LessThanOp,Token_type.EqualOp,Token_type.NotEqualOp,Token_type.Identifier,Token_type.Read,Token_type.LogicalTrue,Token_type.LogicalFalse,Token_type.String],ind,False):
     matches=[Value,Parameters_dash]
     return applyfills(matches,ind,"parameters_dash")
 else:
   out["node"]=Tree("Parameters_dash",["ε"])
   out["index"]=ind
   return out

def Value (ind):
 out={}
 if MatchArr([Token_type.Identifier,Token_type.Number],ind,False):
     matches=[Atom]
     return applyfills(matches,ind,"value")
 elif MatchArr([Token_type.IncrementOp,Token_type.DecrementOp,Token_type.Write,Token_type.Sin,Token_type.Cos,Token_type.Tan,Token_type.Setq,Token_type.PlusOp,Token_type.MinusOp,Token_type.MultiplyOp,Token_type.DivideOp,Token_type.ModOp,Token_type.RemOp,Token_type.GreaterThanOrEqualOp,Token_type.LessThanOrEqualOp,Token_type.GreaterThanOp,Token_type.LessThanOp,Token_type.EqualOp,Token_type.NotEqualOp,Token_type.Identifier,Token_type.Read],ind,False):
     matches=[Function]
     return applyfills(matches,ind,"value")
 elif Match(Token_type.LogicalTrue,ind,False)["node"]!=["error"]:
     matches=[Token_type.LogicalTrue]
     return applyfills(matches,ind,"value")
 elif Match(Token_type.LogicalFalse,ind,False)["node"]!=["error"]:
     matches=[Token_type.LogicalFalse]
     return applyfills(matches,ind,"value")
 elif Match(Token_type.String,ind,False)["node"]!=["error"]:
     matches=[Token_type.String]
     return applyfills(matches,ind,"value")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=ind
     return out

def Atom (ind):
 out={}
 if Match(Token_type.Identifier,ind,False)["node"]!=["error"]:
     matches=[Token_type.Identifier]
     return applyfills(matches,ind,"atom")
 elif Match(Token_type.Number,ind,False)["node"]!=["error"]:
     matches=[Token_type.Number]
     return applyfills(matches,ind,"atom")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=ind
     return out

def is_there_error(arr):
    return 'mode' in arr[-1].keys() and arr[-1]['mode']==['error']
    
def fillmatch(arr,match,position,j):
    if(callable(match)):
        if position==0:
            arr.append(match(j))
        else:
            arr.append(match(arr[-1]['index']))
    else:
        if position==0:
            arr.append(Match(match,j))
        else:
            arr.append(Match(match,arr[-1]['index']))
    return arr
def MatchArr(Arr,ind,appendToError):
  for i in Arr:
    if Match(i,ind,appendToError)["node"]!=["error"]:
      return True
  return False
def applyfills(matches,ind,func_name):
    arr=[]
    out={}
    Children=[]
    i=0
    while i< len (matches):
        match=matches[i]
        arr=fillmatch(arr,match,i,ind)
        ind=arr[-1]["index"]
        Children.append(arr[-1]["node"])
        if is_there_error(arr):
            while ind<len(globals.Tokens) and globals.Tokens[ind].lex!="\\n" :
                ind+=1
            arr[-1]["index"]=ind
            if Token_type.newLine in matches[i:]:
                i=matches[i:].index(Token_type.newLine)+i
                continue
            else:
                out["mode"]=["error"]
                out["index"]=ind
                out["node"]=Tree(func_name,Children)
                return out
        
        ind+=1
        i+=1
    out["node"]=Tree(func_name,Children)
    out["index"]=arr[-1]["index"]
    return out
def Match(a,j,report=True):
    output=dict()
    if(j<len(globals.Tokens)):
        Temp=globals.Tokens[j].to_dict()
        if(Temp["token_type"]==a):
            output["node"]=[Temp["Lex"]]
            output["index"]=j+1
            return output
        else:
            output["mode"]=["error"]
            output["node"]=["error"]
            output["index"]=j
            if(report):
                globals.errors.append("Syntax error : "+Temp["Lex"]+F" Expected {a}")
            return output
    else:
        output["node"]=["error"]
        output["index"]=j
        return output
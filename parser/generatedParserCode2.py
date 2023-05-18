import sys
sys.path.append("D:\Materials\compilers\project\Lexical-Analyser\\")  # Adds the parent directory to the sys.path

from Tokens.TokenTypes import *
from parser.utils.Matches import Match,MatchArr
from nltk.tree import *

import globals
intrealchar=[Token_type.Integer,Token_type.Real,Token_type.Literal]
plusMinus=[Token_type.Plusop,Token_type.Minusop]
DevMul=[Token_type.Divideop,Token_type.Multiplyop]
numbersarr=[Token_type.ConstantI,Token_type.ConstantR]
#program definition
def Parse (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 arr.append(Match(Token_type.Program,ind,Tokens))
 arr.append(Match(Token_type.Identifier,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.newLine,arr[len(arr)-1]["index"],Tokens))
 arr.append(body(arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.End,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.Program,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.Identifier,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.newLine,arr[len(arr)-1]["index"],Tokens))
 for child in arr:
     Children.append(child["node"])
 node=Tree("parse",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def body (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 arr.append(Match(Token_type.Implicit,ind,Tokens))
 arr.append(Match(Token_type.none,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.newLine,arr[len(arr)-1]["index"],Tokens))
 arr.append(declarations(arr[len(arr)-1]["index"],Tokens))
 arr.append(statements(arr[len(arr)-1]["index"],Tokens))
 for child in arr:
     Children.append(child["node"])
 node=Tree("body",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out



#declaration
def declarations (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if MatchArr([Token_type.Integer,Token_type.Real,Token_type.Character],ind,Tokens,False):
   arr.append(constant_declarations(ind,Tokens))
   arr.append(variable_declarations(arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=Tree("declarations",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("declarations",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def constant_declarations (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Comma,ind+1,Tokens,False)["node"]!=["error"]:        
   arr.append(constant_declaration(ind,Tokens))
   arr.append(constant_declarations_dash(arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=Tree("constant_declarations",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("constant_declarations",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def constant_declaration (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Comma,ind+1,Tokens,False)["node"]!=["error"] and MatchArr([Token_type.Integer,Token_type.Real,Token_type.Character],ind,Tokens,False):
   arr.append(type(ind,Tokens))
   arr.append(Match(Token_type.Comma,arr[len(arr)-1]["index"],Tokens))
   arr.append(Match(Token_type.Parameter,arr[len(arr)-1]["index"],Tokens))
   arr.append(Match(Token_type.Scopeop,arr[len(arr)-1]["index"],Tokens))
   arr.append(Match(Token_type.Identifier,arr[len(arr)-1]["index"],Tokens))
   arr.append(Match(Token_type.Equalop,arr[len(arr)-1]["index"],Tokens))
   arr.append(number(arr[len(arr)-1]["index"],Tokens))
   arr.append(Match(Token_type.newLine,arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=Tree("constant_declaration",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("constant_declaration",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def constant_declarations_dash (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Comma,ind+1,Tokens,False)["node"]!=["error"] and MatchArr([Token_type.Integer,Token_type.Real,Token_type.Character],ind,Tokens,False):
   arr.append(constant_declarations(ind,Tokens))
 else:
   out["node"]=Tree("constant_declarations_dash",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("constant_declarations_dash",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def variable_declarations (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Scopeop,ind+1,Tokens,False)["node"]!=["error"] and MatchArr([Token_type.Integer,Token_type.Real,Token_type.Character],ind,Tokens,False):
   arr.append(variable_declaration(ind,Tokens))
   arr.append(variable_declarations_dash(arr[len(arr)-1]["index"],Tokens))
 else:
   arr.append(variable_declarations_dash(ind,Tokens))
 """ else:
   out["node"]=Tree("variable_declarations",["ε"])
   out["index"]=ind
   return out """
 """ else:
   out["node"]=["error"]
   out["index"]=ind+1
   return out """
 for child in arr:
     Children.append(child["node"])
 node=Tree("variable_declarations",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out



def variable_declaration (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if MatchArr(intrealchar,ind,Tokens,False):
   arr.append(type(ind,Tokens))
   arr.append(Match(Token_type.Scopeop,arr[len(arr)-1]["index"],Tokens))   
   arr.append(Match(Token_type.Identifier,arr[len(arr)-1]["index"],Tokens))
   arr.append(equals_something(arr[len(arr)-1]["index"],Tokens))
   arr.append(Match(Token_type.newLine,arr[len(arr)-1]["index"],Tokens))   
 else:
   out["node"]=Tree("variable_declaration",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("variable_declaration",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out


def equals_something (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Equalop,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Equalop,ind,Tokens))
   arr.append(number(arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=Tree("equals_something",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("equals_something",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def variable_declarations_dash (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Scopeop,ind+1,Tokens,False)["node"]!=["error"] and MatchArr([Token_type.Integer,Token_type.Real,Token_type.Character],ind,Tokens,False):
   arr.append(variable_declarations(ind,Tokens))
 else:
   out["node"]=Tree("variable_declarations_dash",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("variable_declarations_dash",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out


#statments section
def statements (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if MatchArr([Token_type.If,Token_type.Identifier,Token_type.Do,Token_type.Print,Token_type.Read],ind,Tokens,False):
   arr.append(statement(ind,Tokens))
   arr.append(statements_dash(arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=Tree("statements",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("statements",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def statement (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Identifier,ind,Tokens,False)["node"]!=["error"]:
   arr.append(assignment_statement(ind,Tokens))
 elif Match(Token_type.If,ind,Tokens,False)["node"]!=["error"]:
   arr.append(if_statement(ind,Tokens))
 elif Match(Token_type.Do,ind,Tokens,False)["node"]!=["error"]:
   arr.append(do_loop_statement(ind,Tokens))
 elif MatchArr([Token_type.Read,Token_type.Print],ind,Tokens,False):
   arr.append(input_output_statement(ind,Tokens))
 else:
   out["node"]=["error"]
   out["index"]=ind+1
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("statement",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def statements_dash (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if MatchArr([Token_type.If,Token_type.Identifier,Token_type.Do,Token_type.Print,Token_type.Read,Token_type.Write],ind,Tokens,False):
   arr.append(statement(ind,Tokens))
   arr.append(statements_dash(arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=Tree("statements_dash",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("statements_dash",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def assignment_statement (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 arr.append(Match(Token_type.Identifier,ind,Tokens))
 arr.append(Match(Token_type.Equalop,arr[len(arr)-1]["index"],Tokens))
 arr.append(expression(arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.newLine,arr[len(arr)-1]["index"],Tokens))
 for child in arr:
     Children.append(child["node"])
 node=Tree("assignment_statement",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def if_statement (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 arr.append(Match(Token_type.If,ind,Tokens))
 arr.append(Match(Token_type.OpenParan,arr[len(arr)-1]["index"],Tokens))
 arr.append(boolean_expression(arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.CloseParan,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.Then,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.newLine,arr[len(arr)-1]["index"],Tokens))
 arr.append(statements(arr[len(arr)-1]["index"],Tokens))
 arr.append(else_statement(arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.End,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.If,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.newLine,arr[len(arr)-1]["index"],Tokens))
 for child in arr:
     Children.append(child["node"])
 node=Tree("if_statement",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def else_statement (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Else,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Else,ind,Tokens))
   arr.append(Match(Token_type.newLine,arr[len(arr)-1]["index"],Tokens))
   arr.append(statements(arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=Tree("else_statement",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("else_statement",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def do_loop_statement (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 arr.append(Match(Token_type.Do,ind,Tokens))
 arr.append(Match(Token_type.Identifier,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.Equalop,arr[len(arr)-1]["index"],Tokens))
 arr.append(sss(arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.Comma,arr[len(arr)-1]["index"],Tokens))
 arr.append(sss(arr[len(arr)-1]["index"],Tokens))
 arr.append(step(arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.newLine,arr[len(arr)-1]["index"],Tokens))
 arr.append(statements(arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.End,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.Do,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.newLine,arr[len(arr)-1]["index"],Tokens))
 for child in arr:
     Children.append(child["node"])
 node=Tree("do_loop_statement",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def sss (ind,Tokens):
 a='sss'
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.ConstantI,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.ConstantI,ind,Tokens))
 elif Match(Token_type.Identifier,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Identifier,ind,Tokens))
 else:
   out["node"]=["error"]
   globals.errors.append(f"Syntax error at line {Tokens[ind].line}:  Expected {a} found ` {Tokens[ind].lex} `")
   out["index"]=ind+1
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("sss",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def step (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Comma,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Comma,ind,Tokens))
   arr.append(sss(arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=Tree("step",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("step",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out


#input oupput
def input_output_statement (ind,Tokens):
 a='input_output_statement'
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Print,ind,Tokens,False)["node"]!=["error"]:
   arr.append(output_statement(ind,Tokens))
 elif Match(Token_type.Read,ind,Tokens,False)["node"]!=["error"]:
   arr.append(input_statement(ind,Tokens))
 else:
   out["node"]=["error"]
   globals.errors.append(f"Syntax error at line {Tokens[ind].line}:  Expected {a} found ` {Tokens[ind].lex} `")
   out["index"]=ind+1
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("input_output_statement",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def output_statement (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 arr.append(Match(Token_type.Print,ind,Tokens))
 arr.append(Match(Token_type.Multiplyop,arr[len(arr)-1]["index"],Tokens))
 arr.append(display_line(arr[len(arr)-1]["index"],Tokens))
 arr.append(output_statement_dash(arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.newLine,arr[len(arr)-1]["index"],Tokens))
 for child in arr:
     Children.append(child["node"])
 node=Tree("output_statement",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def output_statement_dash (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Comma,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Comma,ind,Tokens))
   arr.append(Match(Token_type.Identifier,arr[len(arr)-1]["index"],Tokens))
   arr.append(output_statement_dash(arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=Tree("output_statement_dash",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("output_statement_dash",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def display_line (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 
 if Match(Token_type.Literal,ind+1,Tokens,False)["node"]!=["error"] and Match(Token_type.Comma,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Comma,ind,Tokens))
   arr.append(Match(Token_type.Literal,arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=Tree("display_line",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("display_line",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def input_statement (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 arr.append(Match(Token_type.Read,ind,Tokens))
 arr.append(Match(Token_type.Multiplyop,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.Comma,arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.Identifier,arr[len(arr)-1]["index"],Tokens))
 arr.append(input_statement_dash(arr[len(arr)-1]["index"],Tokens))
 arr.append(Match(Token_type.newLine,arr[len(arr)-1]["index"],Tokens))
 for child in arr:
     Children.append(child["node"])
 node=Tree("input_statement",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def input_statement_dash (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Comma,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Comma,ind,Tokens))
   arr.append(Match(Token_type.Identifier,arr[len(arr)-1]["index"],Tokens))
   arr.append(input_statement_dash(arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=Tree("input_statement_dash",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("input_statement_dash",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out


#expressions with precedence
def boolean_expression (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 arr.append(expression(ind,Tokens))
 arr.append(relational_operator(arr[len(arr)-1]["index"],Tokens))
 arr.append(expression(arr[len(arr)-1]["index"],Tokens))
 for child in arr:
     Children.append(child["node"])
 node=Tree("boolean_expression",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def relational_operator (ind,Tokens):
 a='relational_operator'
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Greaterthanop,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Greaterthanop,ind,Tokens))
 elif Match(Token_type.Lessthanop,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Lessthanop,ind,Tokens))
 elif Match(Token_type.Lessthanorequalop,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Lessthanorequalop,ind,Tokens))
 elif Match(Token_type.Greaterthanorequalop,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Greaterthanorequalop,ind,Tokens))
 elif Match(Token_type.Isequalop,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Isequalop,ind,Tokens))
 elif Match(Token_type.Notequalop,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Notequalop,ind,Tokens))
 else:
   out["node"]=["error"]
   globals.errors.append(f"Syntax error at line {Tokens[ind].line}:  Expected {a} found ` {Tokens[ind].lex} `")
   out["index"]=ind+1
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("relational_operator",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def expression (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 arr.append(term(ind,Tokens))
 arr.append(expression_dash(arr[len(arr)-1]["index"],Tokens))
 for child in arr:
     Children.append(child["node"])
 node=Tree("expression",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def expression_dash (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if MatchArr(plusMinus,ind,Tokens,False):
   arr.append(additive_operator(ind,Tokens))
   arr.append(term(arr[len(arr)-1]["index"],Tokens))
   arr.append(expression_dash(arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=Tree("expression_dash",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("expression_dash",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def term (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 arr.append(factor(ind,Tokens))
 arr.append(term_dash(arr[len(arr)-1]["index"],Tokens))
 for child in arr:
     Children.append(child["node"])
 node=Tree("term",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def term_dash (ind,Tokens):
 arr=[]
 Children=[]
 out={}
 if MatchArr(DevMul,ind,Tokens,False):
   arr.append(multiplicative_operator(ind,Tokens))
   arr.append(factor(arr[len(arr)-1]["index"],Tokens))
   arr.append(term_dash(arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=Tree("term_dash",["ε"])
   out["index"]=ind
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("term_dash",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def factor (ind,Tokens):
 a='factor'
 arr=[]
 Children=[]
 out={}
 if MatchArr(numbersarr,ind,Tokens,False):
   arr.append(number(ind,Tokens))
 elif Match(Token_type.Identifier,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Identifier,ind,Tokens))
 elif Match(Token_type.OpenParan,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.OpenParan,ind,Tokens))
   arr.append(expression(arr[len(arr)-1]["index"],Tokens))
   arr.append(Match(Token_type.CloseParan,arr[len(arr)-1]["index"],Tokens))
 else:
   out["node"]=["error"]
   globals.errors.append(f"Syntax error at line {Tokens[ind].line}:  Expected {a} found ` {Tokens[ind].lex} `")
   out["index"]=ind+1
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("factor",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def additive_operator (ind,Tokens):
 a='additive_operator'
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Plusop,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Plusop,ind,Tokens))
 elif Match(Token_type.Minusop,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Minusop,ind,Tokens))
 else:
   out["node"]=["error"]
   globals.errors.append(f"Syntax error at line {Tokens[ind].line}:  Expected {a} found ` {Tokens[ind].lex} `")
   out["index"]=ind+1
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("additive_operator",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def multiplicative_operator (ind,Tokens):
 a='multiplicative_operator'
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Multiplyop,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Multiplyop,ind,Tokens))
 elif Match(Token_type.Divideop,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Divideop,ind,Tokens))
 else:
   out["node"]=["error"]
   globals.errors.append(f"Syntax error at line {Tokens[ind].line}:  Expected {a} found ` {Tokens[ind].lex} `")
   out["index"]=ind+1
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("multiplicative_operator",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out


#Token Types
def type (ind,Tokens):
 a='type'
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Integer,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Integer,ind,Tokens))
 elif Match(Token_type.Real,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Real,ind,Tokens))
 elif Match(Token_type.Character,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Character,ind,Tokens))
 else:
   out["node"]=["error"]
   globals.errors.append(f"Syntax error at line {Tokens[ind].line}:  Expected {a} found ` {Tokens[ind].lex} `")
   out["index"]=ind+1
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("type",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def number (ind,Tokens):
 a='number'
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.ConstantI,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.ConstantI,ind,Tokens))
 elif Match(Token_type.ConstantR,ind,Tokens,False)["node"]!=["error"]:
   arr.append(Match(Token_type.ConstantR,ind,Tokens))
 else:
   out["node"]=["error"]
   globals.errors.append(f"Syntax error at line {Tokens[ind].line}:  Expected {a} found ` {Tokens[ind].lex} `")
   out["index"]=ind+1
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("number",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out



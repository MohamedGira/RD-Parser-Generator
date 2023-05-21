import sys
sys.path.append("D:\Materials\compilers\project\Lexical-Analyser\\")  # Adds the parent directory to the sys.path
from Tokens.TokenTypes import *
from utils.Matches import Match,MatchArr
from nltk.tree import *
import globals
#program definition
def Parse (ind):
 arr=[]
 Children=[]
 out={}
 matches=[Token_type.Program,Token_type.Identifier,Token_type.newLine,body,Token_type.End,Token_type.Program,Token_type.Identifier,Token_type.newLine]
 return applyfills(matches,Children,ind,"parse")

def body (ind):
 arr=[]
 Children=[]
 out={}
 matches=[Token_type.Implicit,Token_type.none,Token_type.newLine,declarations,statements]
 return applyfills(matches,Children,ind,"body")
neeew=True

#declaration
def declarations (ind):
 arr=[]
 Children=[]
 out={}
 if MatchArr([Token_type.Integer,Token_type.Real,Token_type.Character,],ind,False):
     matches=[constant_declarations,variable_declarations]
     return applyfills(matches,Children,ind,"declarations")
 else:
   out["node"]=Tree("declarations",["ε"])
   out["index"]=ind
   return out

def constant_declarations (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Comma,ind+1,False)["node"]!=["error"]:
     matches=[constant_declaration,constant_declarations_dash]
     return applyfills(matches,Children,ind,"constant_declarations")
 else:
   out["node"]=Tree("constant_declarations",["ε"])
   out["index"]=ind
   return out

def constant_declaration (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Comma,ind+1,False)["node"]!=["error"] and MatchArr([Token_type.Integer,Token_type.Real,Token_type.Character],ind,False):
     matches=[type,Token_type.Comma,Token_type.Parameter,Token_type.Scopeop,Token_type.Identifier,Token_type.Equalop,number,Token_type.newLine]
     return applyfills(matches,Children,ind,"constant_declaration")
 else:
   out["node"]=Tree("constant_declaration",["ε"])
   out["index"]=ind
   return out

def constant_declarations_dash (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Comma,ind+1,False)["node"]!=["error"] and MatchArr([Token_type.Integer,Token_type.Real,Token_type.Character],ind,False):
     matches=[constant_declarations]
     return applyfills(matches,Children,ind,"constant_declarations_dash")
 else:
   out["node"]=Tree("constant_declarations_dash",["ε"])
   out["index"]=ind
   return out

def variable_declarations (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Scopeop,ind+1,False)["node"]!=["error"] and MatchArr([Token_type.Integer,Token_type.Real,Token_type.Character],ind,False):
     matches=[variable_declaration,variable_declarations_dash]
     return applyfills(matches,Children,ind,"variable_declarations")
 else:
   out["node"]=Tree("variable_declarations",["ε"])
   out["index"]=ind
   return out

def variable_declaration (ind):
 arr=[]
 Children=[]
 out={}
 if MatchArr([Token_type.Integer,Token_type.Real,Token_type.Character,],ind,False):
     matches=[type,Token_type.Scopeop,Token_type.Identifier,equals_something,Token_type.newLine]
     return applyfills(matches,Children,ind,"variable_declaration")
 else:
   out["node"]=Tree("variable_declaration",["ε"])
   out["index"]=ind
   return out

def equals_something (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Equalop,ind,False)["node"]!=["error"]:
     matches=[Token_type.Equalop,number]
     return applyfills(matches,Children,ind,"equals_something")
 else:
   out["node"]=Tree("equals_something",["ε"])
   out["index"]=ind
   return out

def variable_declarations_dash (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Scopeop,ind+1,False)["node"]!=["error"] and MatchArr([Token_type.Integer,Token_type.Real,Token_type.Character],ind,False):
     matches=[variable_declarations]
     return applyfills(matches,Children,ind,"variable_declarations_dash")
 else:
   out["node"]=Tree("variable_declarations_dash",["ε"])
   out["index"]=ind
   return out


#statments section
def statements (ind):
 arr=[]
 Children=[]
 out={}
 if MatchArr([Token_type.If,Token_type.Identifier,Token_type.Do,Token_type.Print,Token_type.Read],ind,False):
     matches=[statement,statements_dash]
     return applyfills(matches,Children,ind,"statements")
 else:
   out["node"]=Tree("statements",["ε"])
   out["index"]=ind
   return out

def statement (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Identifier,ind,False)["node"]!=["error"]:
     matches=[assignment_statement]
     return applyfills(matches,Children,ind,"statement")
 elif Match(Token_type.If,ind,False)["node"]!=["error"]:
     matches=[if_statement]
     return applyfills(matches,Children,ind,"statement")
 elif Match(Token_type.Do,ind,False)["node"]!=["error"]:
     matches=[do_loop_statement]
     return applyfills(matches,Children,ind,"statement")
 elif MatchArr([Token_type.Read,Token_type.Print],ind,False):
     matches=[input_output_statement]
     return applyfills(matches,Children,ind,"statement")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=arr[-1]["index"]
     return out

def statements_dash (ind):
 arr=[]
 Children=[]
 out={}
 if MatchArr([Token_type.If,Token_type.Identifier,Token_type.Do,Token_type.Print,Token_type.Read,Token_type.Write],ind,False):
     matches=[statement,statements_dash]
     return applyfills(matches,Children,ind,"statements_dash")
 else:
   out["node"]=Tree("statements_dash",["ε"])
   out["index"]=ind
   return out

def assignment_statement (ind):
 arr=[]
 Children=[]
 out={}
 matches=[Token_type.Identifier,Token_type.Equalop,expression,Token_type.newLine]
 return applyfills(matches,Children,ind,"assignment_statement")

def if_statement (ind):
 arr=[]
 Children=[]
 out={}
 matches=[Token_type.If,Token_type.OpenParan,boolean_expression,Token_type.CloseParan,Token_type.Then,Token_type.newLine,statements,else_statement,Token_type.End,Token_type.If,Token_type.newLine]
 return applyfills(matches,Children,ind,"if_statement")

def else_statement (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Else,ind,False)["node"]!=["error"]:
     matches=[Token_type.Else,Token_type.newLine,statements]
     return applyfills(matches,Children,ind,"else_statement")
 else:
   out["node"]=Tree("else_statement",["ε"])
   out["index"]=ind
   return out

def do_loop_statement (ind):
 arr=[]
 Children=[]
 out={}
 matches=[Token_type.Do,Token_type.Identifier,Token_type.Equalop,sss,Token_type.Comma,sss,step,Token_type.newLine,statements,Token_type.End,Token_type.Do,Token_type.newLine]
 return applyfills(matches,Children,ind,"do_loop_statement")

def sss (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.ConstantI,ind,False)["node"]!=["error"]:
     matches=[Token_type.ConstantI]
     return applyfills(matches,Children,ind,"sss")
 elif Match(Token_type.Identifier,ind,False)["node"]!=["error"]:
     matches=[Token_type.Identifier]
     return applyfills(matches,Children,ind,"sss")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=arr[-1]["index"]
     return out

def step (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Comma,ind,False)["node"]!=["error"]:
     matches=[Token_type.Comma,sss]
     return applyfills(matches,Children,ind,"step")
 else:
   out["node"]=Tree("step",["ε"])
   out["index"]=ind
   return out


#input oupput
def input_output_statement (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Print,ind,False)["node"]!=["error"]:
     matches=[output_statement]
     return applyfills(matches,Children,ind,"input_output_statement")
 elif Match(Token_type.Read,ind,False)["node"]!=["error"]:
     matches=[input_statement]
     return applyfills(matches,Children,ind,"input_output_statement")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=arr[-1]["index"]
     return out

def output_statement (ind):
 arr=[]
 Children=[]
 out={}
 matches=[Token_type.Print,Token_type.Multiplyop,display_line,output_statement_dash,Token_type.newLine]
 return applyfills(matches,Children,ind,"output_statement")

def output_statement_dash (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Comma,ind,False)["node"]!=["error"]:
     matches=[Token_type.Comma,Token_type.Identifier,output_statement_dash]
     return applyfills(matches,Children,ind,"output_statement_dash")
 else:
   out["node"]=Tree("output_statement_dash",["ε"])
   out["index"]=ind
   return out

def display_line (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Literal,ind+1,False)["node"]!=["error"] and Match(Token_type.Comma,ind,False)["node"]!=["error"]:
     matches=[Token_type.Comma,Token_type.Literal]
     return applyfills(matches,Children,ind,"display_line")
 else:
   out["node"]=Tree("display_line",["ε"])
   out["index"]=ind
   return out

def input_statement (ind):
 arr=[]
 Children=[]
 out={}
 matches=[Token_type.Read,Token_type.Multiplyop,Token_type.Comma,Token_type.Identifier,input_statement_dash,Token_type.newLine]
 return applyfills(matches,Children,ind,"input_statement")

def input_statement_dash (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Comma,ind,False)["node"]!=["error"]:
     matches=[Token_type.Comma,Token_type.Identifier,input_statement_dash]
     return applyfills(matches,Children,ind,"input_statement_dash")
 else:
   out["node"]=Tree("input_statement_dash",["ε"])
   out["index"]=ind
   return out


#expressions with precedence
def boolean_expression (ind):
 arr=[]
 Children=[]
 out={}
 matches=[expression,relational_operator,expression]
 return applyfills(matches,Children,ind,"boolean_expression")

def relational_operator (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Greaterthanop,ind,False)["node"]!=["error"]:
     matches=[Token_type.Greaterthanop]
     return applyfills(matches,Children,ind,"relational_operator")
 elif Match(Token_type.Lessthanop,ind,False)["node"]!=["error"]:
     matches=[Token_type.Lessthanop]
     return applyfills(matches,Children,ind,"relational_operator")
 elif Match(Token_type.Lessthanorequalop,ind,False)["node"]!=["error"]:
     matches=[Token_type.Lessthanorequalop]
     return applyfills(matches,Children,ind,"relational_operator")
 elif Match(Token_type.Greaterthanorequalop,ind,False)["node"]!=["error"]:
     matches=[Token_type.Greaterthanorequalop]
     return applyfills(matches,Children,ind,"relational_operator")
 elif Match(Token_type.Isequalop,ind,False)["node"]!=["error"]:
     matches=[Token_type.Isequalop]
     return applyfills(matches,Children,ind,"relational_operator")
 elif Match(Token_type.Notequalop,ind,False)["node"]!=["error"]:
     matches=[Token_type.Notequalop]
     return applyfills(matches,Children,ind,"relational_operator")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=arr[-1]["index"]
     return out

def expression (ind):
 arr=[]
 Children=[]
 out={}
 matches=[term,expression_dash]
 return applyfills(matches,Children,ind,"expression")

def expression_dash (ind):
 arr=[]
 Children=[]
 out={}
 if MatchArr([Token_type.Plusop,Token_type.Minusop,],ind,False):
     matches=[additive_operator,term,expression_dash]
     return applyfills(matches,Children,ind,"expression_dash")
 else:
   out["node"]=Tree("expression_dash",["ε"])
   out["index"]=ind
   return out

def term (ind):
 arr=[]
 Children=[]
 out={}
 matches=[factor,term_dash]
 return applyfills(matches,Children,ind,"term")

def term_dash (ind):
 arr=[]
 Children=[]
 out={}
 if MatchArr([Token_type.Multiplyop,Token_type.Divideop,],ind,False):
     matches=[multiplicative_operator,factor,term_dash]
     return applyfills(matches,Children,ind,"term_dash")
 else:
   out["node"]=Tree("term_dash",["ε"])
   out["index"]=ind
   return out

def factor (ind):
 arr=[]
 Children=[]
 out={}
 if MatchArr([Token_type.ConstantI,Token_type.ConstantR,],ind,False):
     matches=[number]
     return applyfills(matches,Children,ind,"factor")
 elif Match(Token_type.Identifier,ind,False)["node"]!=["error"]:
     matches=[Token_type.Identifier]
     return applyfills(matches,Children,ind,"factor")
 elif Match(Token_type.OpenParan,ind,False)["node"]!=["error"]:
     matches=[Token_type.OpenParan,expression,Token_type.CloseParan]
     return applyfills(matches,Children,ind,"factor")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=arr[-1]["index"]
     return out

def additive_operator (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Plusop,ind,False)["node"]!=["error"]:
     matches=[Token_type.Plusop]
     return applyfills(matches,Children,ind,"additive_operator")
 elif Match(Token_type.Minusop,ind,False)["node"]!=["error"]:
     matches=[Token_type.Minusop]
     return applyfills(matches,Children,ind,"additive_operator")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=arr[-1]["index"]
     return out

def multiplicative_operator (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Multiplyop,ind,False)["node"]!=["error"]:
     matches=[Token_type.Multiplyop]
     return applyfills(matches,Children,ind,"multiplicative_operator")
 elif Match(Token_type.Divideop,ind,False)["node"]!=["error"]:
     matches=[Token_type.Divideop]
     return applyfills(matches,Children,ind,"multiplicative_operator")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=arr[-1]["index"]
     return out


#Token Types
def type (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Integer,ind,False)["node"]!=["error"]:
     matches=[Token_type.Integer]
     return applyfills(matches,Children,ind,"type")
 elif Match(Token_type.Real,ind,False)["node"]!=["error"]:
     matches=[Token_type.Real]
     return applyfills(matches,Children,ind,"type")
 elif Match(Token_type.Character,ind,False)["node"]!=["error"]:
     matches=[Token_type.Character]
     return applyfills(matches,Children,ind,"type")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=arr[-1]["index"]
     return out

def number (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.ConstantI,ind,False)["node"]!=["error"]:
     matches=[Token_type.ConstantI]
     return applyfills(matches,Children,ind,"number")
 elif Match(Token_type.ConstantR,ind,False)["node"]!=["error"]:
     matches=[Token_type.ConstantR]
     return applyfills(matches,Children,ind,"number")
 else:
     print("souldn't reach here")
     out["mode"]=["error"]
     out["node"]=["error"]
     out["index"]=arr[-1]["index"]
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
    if(is_there_error(arr)):
        pass
    return arr
def MatchArr(Arr,ind,appendToError):
  for i in Arr:
    if Match(i,ind,appendToError)["node"]!=["error"]:
      return True
  return False
def applyfills(matches,Children,ind,func_name):
    arr=[]
    out={}
    i=0
    while i< len (matches):
        match=matches[i]
        arr=fillmatch(arr,match,i,ind)
        Children.append(arr[-1]["node"])
        if is_there_error(arr):
            
            while ind<len(globals.Tokens) and globals.Tokens[ind].lex!="\n" :
                ind+=1
            arr[-1]["index"]=ind
            if Token_type.newLine in matches[i:]:
                i=matches.index(Token_type.newLine)
                continue
            else:
                out["mode"]=["error"]
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
            output["index"]=j+1
            if(report):
                globals.errors.append(f"Syntax error at line {globals.Tokens[j].line}:  Expected {a} found ` {globals.Tokens[j].lex} `")
            return output
    else:
        output["node"]=["error"]
        output["index"]=j+1
        return output

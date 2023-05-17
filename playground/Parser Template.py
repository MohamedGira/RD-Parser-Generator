import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import *

class Token_type(Enum): # listing all tokens type
    Begin=1
    End=2
    Do=3 
    Else=4
    EndIf=5 
    If=6
    Integer=7
    Dot=8
    Semicolon=9
    EqualOp=10 
    LessThanOp=11
    GreaterThanOp=12
    NotEqualOp=13
    PlusOp=14 
    MinusOp=15
    MultiplyOp=16
    DivideOp=17
    Identifier=18
    Constant=19
    Program=20
    Procedure=21
    Parameters=22
    Declare=23
    Error=24
    Read=25
    Write=26
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
            
#Reserved word Dictionary
ReservedWords={"IF":Token_type.If,
               "PROGRAM":Token_type.Program,
               "PROCEDURE":Token_type.Procedure,
                "Parameters":Token_type.Parameters,
                "Declare":Token_type.Declare,
                "END":Token_type.End,
                "BEGIN":Token_type.Begin,
                "BEGIN":Token_type.Begin,
                "BEGIN":Token_type.Begin,
                "DO":Token_type.Do,
                "ElSE":Token_type.Else,
                "ENDIF":Token_type.EndIf,
                "INTEGER":Token_type.Integer,
                "READ":Token_type.Read,
                "WRITE":Token_type.Write
               }
Operators={".":Token_type.Dot,
          ";":Token_type.Semicolon,
          "=":Token_type.EqualOp,
          "+":Token_type.PlusOp,
           "-":Token_type.MinusOp,
           "*":Token_type.MultiplyOp,
           "/":Token_type.DivideOp
          }
Tokens=[]
errors=[]

def find_token(text):
    lexems=text.split()
    for le in  lexems:
        if(le in ReservedWords ):
            new_token=token(le,ReservedWords[le])
            Tokens.append(new_token)
        elif(le in Operators):
            new_token=token(le,Operators[le])
            Tokens.append(new_token)
        elif (re.match("^\d+(\.[0-9]*)?$",le)):
            new_token=token(le,Token_type.Constant)
            Tokens.append(new_token)    
        elif (re.match("^([a-zA-Z][a-zA-Z0-9]*)$",le)):
            new_token=token(le,Token_type.Identifier)
            Tokens.append(new_token)    
        else : 
            new_token=token(le,Token_type.Error)
            errors.append("Lexical error  "+ le)
           
    

"""
<Parse>       -> <header> <block>\n\
<header>    -> [Program] <identifier> [;]\n\
<block>     -> [Begin] <Statments> [End]\n\

Statments -> [Read] <identifier> | [Write] <identifier>
"""

""""PROGRAM AAAA ; BEGIN READ haha END"""
""""PROGRAM AAAA ; BEGIN WRITE haha END"""
def Parse (ind):
 arr=[None] * 2
 Children=[]
 out={}
 arr[0]=header(ind)
 arr[1]=block(arr[0]["index"])     
 for child in arr:
     Children.append(child["node"])
 node=Tree("parse",Children)       
 out["node"]=node
 out["index"]=arr[-1]["index"]     
 return out

def header (ind):
 arr=[None] * 3
 Children=[]
 out={}
 arr[0]=Match(Token_type.Program,ind)
 arr[1]=Match(Token_type.Identifier,arr[0]["index"])
 arr[2]=Match(Token_type.Semicolon,arr[1]["index"])
 for child in arr:
     Children.append(child["node"])
 node=Tree("header",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out

def block (ind):
 arr=[None] * 3
 Children=[]
 out={}
 arr[0]=Match(Token_type.Begin,ind)
 arr[1]=Statments(arr[0]["index"])
 arr[2]=Match(Token_type.End,arr[1]["index"])
 for child in arr:
     Children.append(child["node"])
 node=Tree("block",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out
    
""" def Statments(j):
    Children=[]
    out=dict()
    out_read_write=dict()

    if(Match(Token_type.Read,j,False)['node']!=['error']):
        out_read_write=Match(Token_type.Read,j)
        out_identifier=Match(Token_type.Identifier,out_read_write['index'])
    elif(Match(Token_type.Write,j,False)['node']!=['error']):
        out_read_write=Match(Token_type.Write,j)
        out_identifier=Match(Token_type.Identifier,out_read_write['index'])
    else:
        out["node"]=["error"]
        out["index"]=j+1
        return out
    Children.append(out_read_write["node"])
    Children.append(out_identifier["node"])
    node=Tree("Statments",Children)
    out['node']=node
    out['index']=out_identifier['index']
    return out    """
        
 
def Statments (ind):
 arr=[]
 Children=[]
 out={}
 if Match(Token_type.Read,ind,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Read,ind))
   arr.append(Match(Token_type.Identifier,arr[0]["index"]))
 elif Match(Token_type.Write,ind,False)["node"]!=["error"]:
   arr.append(Match(Token_type.Write,ind))
   arr.append(Match(Token_type.Identifier,arr[2]["index"]))
 else:
   out["node"]=["error"]
   out["index"]=ind+1
   return out
 for child in arr:
     Children.append(child["node"])
 node=Tree("statments",Children)
 out["node"]=node
 out["index"]=arr[-1]["index"]
 return out



def Match(a,j,appendToError=True):
    output=dict()
    if(j<len(Tokens)):
        Temp=Tokens[j].to_dict()
        if(Temp['token_type']==a):
            j+=1
            output["node"]=[Temp['Lex']]
            output["index"]=j
            return output
        else:
            output["node"]=["error"]
            output["index"]=j+1
            if(appendToError):
                errors.append("Syntax error : "+Temp['Lex']+f" Expected {a}")
            return output
    else:
        output["node"]=["error"]
        output["index"]=j+1
        return output
    
def MatchTry(a,j):
    if(j>len(Tokens)):
        return False
    Temp=Tokens[j].to_dict()
    print(Temp['Lex'])
    if(Temp['token_type']==a):
        return True
    else:
        return False
        
#GUI
root= tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Scanner Phase')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Source code:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root) 
canvas1.create_window(200, 140, window=entry1)

def Scan():
    x1 = entry1.get()
    find_token(x1)
    df=pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    #print(df)
      
    #to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    # start Parsing
    Node=Parse(0)["node"]
     
    
    # to display errorlist
    df1=pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()
    #clear your list
    
    #label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    #canvas1.create_window(200, 210, window=label3)
    
    #label4 = tk.Label(root, text="Token_type"+x1, font=('helvetica', 10, 'bold'))
    #canvas1.create_window(200, 230, window=label4)
    
    
button1 = tk.Button(text='Scan', command=Scan, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)
root.mainloop()


# ### 
















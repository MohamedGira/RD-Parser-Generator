import re
import sys
import os
sys.path.append("D:\Materials\compilers\project\Lexical-Analyser\\")  # Adds the parent directory to the sys.path
   
from Tokens.TokenTypes import *

    

def add_line(s,line,num=None,end='\n'):
    return s+line+f'{end}' if not num else s+line+f'           {s}{end}'

def merge_dicts(dict1,dict2):
    for i in dict2.keys():
        if i in dict1:
            dict1[i]+=dict2[i]
        else:
            dict1[i]=dict2[i]
    return dict1

def txtToCode(something,ind,s,initial=False,ident=' '):
    if(something[0]=='<'):
        callee_name=re.sub(r'<|>',r'',something)
        if(initial):
            s=add_line(s,f'{ident}arr.append({callee_name}(ind,Tokens))')
        else:
            s=add_line(s,f'{ident}arr.append({callee_name}(arr[len(arr)-1]["index"],Tokens))')
    elif(something[0]=='['):
        token_name=re.sub(r'\[|]',r'',something).lower()
        if(initial):
            s=add_line(s,f'{ident}arr.append(Match({lowerdict[token_name]},ind,Tokens))')
        else:
            s=add_line(s,f'{ident}arr.append(Match({lowerdict[token_name]},arr[len(arr)-1]["index"],Tokens))')
    return s
global_dict={}
def matchfunc(onething):
    
    if(onething[0]=='<'):
        res=[onething]
        while(res[0][0]=='<'):
            print(res[0].split(' ')[0])
            res=global_dict[res[0].split(' ')[0]]
            print(res[0])
        return matchfunc(res[0])
    elif(onething[0]=='['):
        token_name=re.sub(r'\[|]',r'',onething).lower()
        s=add_line('',f'Match({lowerdict[token_name]},ind,Tokens,False)["node"]!=["error"]',end='')
    if(not s):
        raise (IndexError('s is not [ or <'))
        
    return s
def is_terminal(thing):
    return thing[0]=='['
def is_non_terminal(thing):
    return thing[0]=='<'
lowerdict=merge_dicts(get_lower_dict(Token_type),Operators)
class section:
    def __init__(self,name="#undefined",grammer=''):
        self.name=name
        self.grammer=grammer
    def __str__(self) -> str:
        return f'section name:{self.name} \n section grammer:{self.grammer}'
def extract_section(filename):
    sec=section()
    sections=[]
    with open(filename, "r",encoding = "utf-8") as file:
        for line in file:
            if(line=='DICTEOF\n'):
                break
            if line!='\n' and line.strip():
                things=line.split(' ')
                things= [i.strip() for i in things if i.strip()]
                rightSide=' '.join(things[2:])
                split_string = re.split(r'\s+|\|', rightSide)
                global_dict[things[0]]=split_string
    with open(filename, "r",encoding = "utf-8") as file:
 
        for line in file:
            # Do something with the line
            if(line=='EOF\n'):
                return sections
            if(line[0]=='#'):
                sec.name=line
            elif(line[0]=='_'):
                sections.append(sec)
                sec=section()
            elif(line!='\n'and line.strip()):
                sec.grammer+=line
                s=''
                
    
    return sections
    
def write_to(file,content,clear=True):
    mode = "w"  
    if not clear:
        mode = "a"  # Append mode (keeps the existing content)
    with open(file, mode ,encoding = "utf-8") as file:
        file.write(content)

    return content

def generate_parse_functions(rules):
    
    grammer=rules.split('\n')
    grammer= [i.strip() for i in grammer if i.strip()!='']
    gens=[]
    for rule in grammer:
        s=''
        things=rule.split(' ')
        things= [i.strip() for i in things if i!='' and i!=[]]
        
        #add function name and defining array to put matches and calls in
        function_name = re.sub(r'<|>',r'',things[0])
        s=add_line(s,f'def {function_name} (ind,Tokens):')
        s=add_line(s,f' arr=[]')
        s=add_line(s,f' Children=[]')
        s=add_line(s,f' out={"{}"}')

        ind=0 #index of the element of the array, if we are in first thing, we get the one provided by finction
        rightSide=' '.join(things[2:])
        Ors=[i.strip() for i in rightSide.split('|') if i.strip()]
        if(len(Ors)==1):
             for i in range(2,len(things)):
                if(i==2):
                    s=txtToCode(things[i],ind,s,True)
                else:
                    s=txtToCode(things[i],ind,s,False)
            
                ind+=1
        elif len(Ors)>1:
            #add the initial if, then for the rest ors,
            for i in range(len(Ors)):
                workingOn=Ors[i]
                workingOnThings=[i.strip() for i in workingOn.split(' ') if i.strip()]
                if i==0:
                    s=add_line(s,f' if {matchfunc(workingOnThings[0])}:')
                    for j in range(len(workingOnThings)):
                        if(j==0):
                            s=txtToCode(workingOnThings[j],ind,s,True,ident=f'   ')
                        else:
                            s=txtToCode(workingOnThings[j],ind,s,False,ident=f'   ')
                        ind+=1
                else:
                    if workingOnThings[0]!='ε':
                        s=add_line(s,f' elif {matchfunc(workingOnThings[0])}:')
                        for j in range(len(workingOnThings)):
                            if(j==0):
                                s=txtToCode(workingOnThings[j],ind,s,True,ident=f'   ')
                            else:
                                s=txtToCode(workingOnThings[j],ind,s,False,ident=f'   ')
                            ind+=1     
                    if(i==len(Ors)-1):
                        if(workingOnThings[0]=='ε'):
                            s=add_line(s,' else:')
                            s=add_line(s,f'   out["node"]=Tree("{function_name.lower()}",["ε"])')
                            s=add_line(s,'   out["index"]=ind')
                            s=add_line(s,'   return out')
                        else:
                            s=add_line(s,' else:')
                            s=add_line(s,'   out["node"]=["error"]')
                            s=add_line(s,f'   globals.errors.append(f"Syntax error at line {"{Tokens[ind].line}"}:  Expected {function_name.lower()} found ` {"{Tokens[ind].lex}"} `")')
                            s=add_line(s,'   out["index"]=ind+1')
                            s=add_line(s,'   return out')
        
            
        s=add_line(s,f' for child in arr:')
        s=add_line(s,f'     Children.append(child["node"])')
        s=add_line(s,f' node=Tree("{function_name.lower()}",Children)')
        s=add_line(s,f' out["node"]=node')
        s=add_line(s,f' out["index"]=arr[-1]["index"]')
        s=add_line(s,f' return out')
        gens.append(s)
    a=''
    a=add_line(a,'def MatchArr(Arr,ind,Tokens,appendToError):')
    a=add_line(a,'  for i in Arr:')
    a=add_line(a,'    if Match(i,ind,Tokens,appendToError)["node"]!=["error"]:')
    a=add_line(a,'      return True')
    a=add_line(a,'  return False')
    gens.append(a)
    return gens
        
 

def treeGenerator():
    pass

secs=extract_section(os.path.join(os.path.dirname(__file__),'../playground/a V2.txt'))
""" for i in secs:
    functions=generate_parse_functions(i.grammer)
    fname='separate\\'+i.name[1:-1]
    write_to(os.path.join(os.path.dirname(__file__),f'{fname}.py'),f'\n{i.name}',False)
    for i in functions:
        write_to(os.path.join(os.path.dirname(__file__),f'{fname}.py'),i,False)
        write_to(os.path.join(os.path.dirname(__file__),f'{fname}.py'),'\n',False)
 """


print(generate_parse_functions('<variable_declaration> -> <type> [::] [IDENTIFIER] <equals_something> [NEWLINE] | ε\n\
<equals_something> -> [=] <number> | ε')[0])
print(generate_parse_functions('<variable_declaration> -> <type> [::] [IDENTIFIER] <equals_something> [NEWLINE] | ε\n\
<equals_something> -> [=] <number> | ε')[1])
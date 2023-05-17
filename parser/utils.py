import re
import sys
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
            s=add_line(s,f'{ident}arr.append({callee_name}(ind))')
        else:
            s=add_line(s,f'{ident}arr.append({callee_name}(arr[{ind-1}]["index"]))')
    elif(something[0]=='['):
        token_name=re.sub(r'\[|]',r'',something).lower()
        if(initial):
            s=add_line(s,f'{ident}arr.append(Match({lowerdict[token_name]},ind))')
        else:
            s=add_line(s,f'{ident}arr.append(Match({lowerdict[token_name]},arr[{ind-1}]["index"]))')
    return s

def matchfunc(onething):
    if(onething[0]=='<'):
        callee_name=re.sub(r'<|>',r'',onething)
        s=add_line('',f' {callee_name}(ind)',end='')
    elif(onething[0]=='['):
        token_name=re.sub(r'\[|]',r'',onething).lower()
        s=add_line('',f'Match({lowerdict[token_name]},ind,False)',end='')
    return s
def is_terminal(thing):
    return thing[0]=='['
def is_non_terminal(thing):
    return thing[0]=='<'
lowerdict=merge_dicts(get_lower_dict(Token_type),Operators)
def generate_parse_functions(rules):
    grammer=rules.split('\n')
    grammer= [i.strip() for i in grammer if i.strip()!='']
    
    for rule in grammer:

        things=rule.split(' ')
        things= [i.strip() for i in things if i!='' and i!=[]]
        s=''
        #add function name and defining array to put matches and calls in
        function_name = re.sub(r'<|>',r'',things[0])
        s=add_line(s,f'def {function_name} (ind):')
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
                    s=add_line(s,f' if {matchfunc(workingOnThings[0])}["node"]!=["error"]:')
                    for i in range(len(workingOnThings)):
                        if(i==0):
                            s=txtToCode(workingOnThings[i],ind,s,True,ident=f'   ')
                        else:
                            s=txtToCode(workingOnThings[i],ind,s,False,ident=f'   ')
                        ind+=1
                else:
                    s=add_line(s,f' elif {matchfunc(workingOnThings[0])}["node"]!=["error"]:')
                    for i in range(len(workingOnThings)):
                        if(i==0):
                            s=txtToCode(workingOnThings[i],ind,s,True,ident=f'   ')
                        else:
                            s=txtToCode(workingOnThings[i],ind,s,False,ident=f'   ')
                        ind+=1

            s=add_line(s,' else:')
            s=add_line(s,'   out["node"]=["error"]')
            s=add_line(s,'   out["index"]=ind+1')
            s=add_line(s,'   return out')
        
        
        
            
        s=add_line(s,f' for child in arr:')
        s=add_line(s,f'     Children.append(child["node"])')
        s=add_line(s,f' node=Tree("{function_name.lower()}",Children)')
        s=add_line(s,f' out["node"]=node')
        s=add_line(s,f' out["index"]=arr[-1]["index"]')
        s=add_line(s,f' return out')
        print(s)
        
        
 

def treeGenerator():
    pass

generate_parse_functions(
'<statement> -> <assignment_statement> | <if_statement> | <do_loop_statement> | <input_output_statement>'
)


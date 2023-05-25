#dont use this shit, you will edit more, use basic then edit neceicities
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
            s=add_line(s,f'{ident}arr.append({callee_name}(ind))')
        else:
            s=add_line(s,f'{ident}arr.append({callee_name}(arr[len(arr)-1]["index"]))')
    elif(something[0]=='['):
        token_name=re.sub(r'\[|]',r'',something).lower()
        if(initial):
            s=add_line(s,f'{ident}arr.append(Match({lowerdict[token_name]},ind))')
        else:
            s=add_line(s,f'{ident}arr.append(Match({lowerdict[token_name]},arr[len(arr)-1]["index"]))')
    return s

def get_matches(oneOfOrs):
    things=oneOfOrs.split(' ')
    
    llist=[]
    for something in things:
        if(something[0]=='<'):
            callee_name=re.sub(r'<|>',r'',something)
            llist.append(callee_name)
        elif(something[0]=='['):
            token_name=re.sub(r'\[|]',r'',something).lower()
            llist.append(f'{lowerdict[token_name]}')
            
    s='['+','.join(llist)+']'
    return s
def matchesTocode(functionName,indentation=' '):
    s=''
    s=add_line(s,f'{indentation}while i< len (matches):')
    s=add_line(s,f'{indentation} match=matches[i]')
    s=add_line(s,f'{indentation} arr=fillmatch(arr,match,i,ind)')
    s=add_line(s,f'{indentation} Children.append(arr[-1]["node"])')
    s=add_line(s,f'{indentation} if is_there_error(arr):  ')
    s=add_line(s,f'{indentation}     while globals.Tokens[ind].lex!=";":')
    s=add_line(s,f'{indentation}         ind+=1')
    s=add_line(s,f'{indentation}     arr[-1]["index"]=ind')
    s=add_line(s,f'{indentation}     if Token_type.Semicolon in matches[i:]:')
    s=add_line(s,f'{indentation}         i=matches.index(Token_type.Semicolon)')
    s=add_line(s,f'{indentation}         continue')
    s=add_line(s,f'{indentation}     else:')
    s=add_line(s,f'{indentation}         out["mode"]=["error"]')
    s=add_line(s,f'{indentation}         out["node"]=Tree("{functionName}",Children)')
    s=add_line(s,f'{indentation}         out["index"]=ind')
    s=add_line(s,f'{indentation}         return out')
    s=add_line(s,f'{indentation} i+=1')

    return s
def handleErrorTocode(functionName,indentation=' '):
    s=''
    s=add_line(s,f'{indentation}while globals.Tokens[ind].lex!=";":')
    s=add_line(s,f'{indentation}    ind+=1')
    s=add_line(s,f'{indentation}arr[-1]["index"]=ind')
    s=add_line(s,f'{indentation}if Token_type.Semicolon in matches[i:]:')
    s=add_line(s,f'{indentation}    i=matches.index(Token_type.Semicolon)')
    s=add_line(s,f'{indentation}    continue')
    s=add_line(s,f'{indentation}else:')
    s=add_line(s,f'{indentation}    out["mode"]=["error"]')
    s=add_line(s,f'{indentation}    out["node"]=Tree("{functionName}",["ε"])')
    s=add_line(s,f'{indentation}    out["index"]=ind')
    s=add_line(s,f'{indentation}    return out')
    return s
    
    
    
    
    
    
    
    
    
    
    
global_dict={}
global_dict_str={}

def matchfunc(rightSideStr,many=False):
    rightSideStr=rightSideStr.strip() 
    firstelement=rightSideStr[0]
    if(firstelement=='<'):
        many=True
        #its a non terminal
        first_token=rightSideStr.split(' ')[0]
        while(first_token[0]=='<'):
            newRHS=global_dict_str[first_token]
            first_token=newRHS.split(' ')[0]
           
        return matchfunc(newRHS,many)
    elif(firstelement=='['):
        if(many):
            #we reached a  terminal
            lowest_level_array=rightSideStr.split('|')
            #splitting it by ors
            for i in lowest_level_array:
                entities=[i for i in i.strip().split(' ') if i.strip()]
                #checking if there are multiple entities in the or, if so, we cant automate match arr
                if len(entities)>1:
                    token_name=re.sub(r'\[|]',r'',entities[0]).lower()
                    s=add_line('',f'Match({lowerdict[token_name]},ind,False)["node"]!=["error"]',end='')
                    return s
            lowest_level_array_tokens=[re.sub(r'\[|]',r'',i).lower().strip() for i in lowest_level_array]
            lowest_level_array_tokens=[f'Token_type.{lowerdict[i].name}' for i in lowest_level_array_tokens]
            sa='['
            for i in lowest_level_array_tokens:
                sa+=i
                sa+=','
            sa+=']'
            if(len(lowest_level_array)>1):
                for i in lowest_level_array:
                    i=i.split(' ')[0]
                s=add_line('',f'MatchArr({sa},ind,False)',end='')
                print('lowest level array:  ',lowest_level_array_tokens)
            else:
                token_name=re.sub(r'\[|]',r'',lowest_level_array[0]).lower()
                s=add_line('',f'Match({lowerdict[token_name]},ind,False)["node"]!=["error"]',end='')
        else:
            token_name=re.sub(r'\[|]',r'',rightSideStr.split(' ')[0]).lower()
            s=add_line('',f'Match({lowerdict[token_name]},ind,False)["node"]!=["error"]',end='')

        
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
                global_dict_str[things[0]]=rightSide
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
        s=add_line(s,f'def {function_name} (ind):')
        s=add_line(s,f' arr=[]')
        s=add_line(s,f' Children=[]')
        s=add_line(s,f' out={"{}"}')

        ind=0 #index of the element of the array, if we are in first thing, we get the one provided by finction
        #joining the right side to one string
        rightSide=' '.join(things[2:])
        #splitting the right side by ors
        Ors=[i.strip() for i in rightSide.split('|') if i.strip()]
        if(len(Ors)==1):
             matches=get_matches(Ors[0])
             s=add_line(s,f' i=0')
             s=add_line(s,f' matches={matches}')
             s=add_line(s,matchesTocode(function_name))
        elif len(Ors)>1:
            #add the initial if, then for the rest ors,
            for i in range(len(Ors)):
                workingOn=Ors[i]
                workingOnThings=[i.strip() for i in workingOn.split(' ') if i.strip()]
                if i==0:
                    s=add_line(s,f' if {matchfunc(rightSide)}:')
                    matches=get_matches(workingOn)
                    s=add_line(s,f'  i=0')
                    s=add_line(s,f'  matches={matches}')
                    s=add_line(s,matchesTocode(function_name,'  '))
                else:
                    if workingOnThings[0]!='ε':
                        s=add_line(s,f' elif {matchfunc(rightSide)}:')
                        matches=get_matches(workingOn)
                        s=add_line(s,f'  i=0')
                        s=add_line(s,f'  matches={matches}')
                        s=add_line(s,matchesTocode(function_name,'  '))
                            
                    if(i==len(Ors)-1):
                        if(workingOnThings[0]=='ε'):
                            s=add_line(s,' else:')
                            s=add_line(s,f'   out["node"]=Tree("{function_name.lower()}",["ε"])')
                            s=add_line(s,F'   out["index"]=ind')
                            s=add_line(s,F'   return out')
                        else:
                            s=add_line(s,' else:')
                            s=add_line(s,f'  out["mode"]=["error"]')
                            s=add_line(s,f'  out["node"]=Tree("{function_name.lower()}",["error"])')
                            s=add_line(s,f'  out["index"]=ind')
                            s=add_line(s,f'  return out')
                            
                            #s=add_line(s,f'  globals.errors.append(f"Syntax error at line {"{globals.Tokens[ind].line}"}:  Expected {function_name.lower()} found ` {"{globals.Tokens[ind].lex}"} `")')
                            

            
        
        s=add_line(s,f' node=Tree("{function_name.lower()}",Children)')
        s=add_line(s,f' out["node"]=node')
        s=add_line(s,f' out["index"]=arr[-1]["index"]')
        s=add_line(s,f' return out')
        gens.append(s)
   
    return gens
        
 

def treeGenerator():
    pass

secs=extract_section(os.path.join(os.path.dirname(__file__),'Grammer.txt'))
""" for i in secs:
    functions=generate_parse_functions(i.grammer)
    fname='separate\\'+i.name[1:-1]
    write_to(os.path.join(os.path.dirname(__file__),f'{fname}.py'),f'\n{i.name}',False)
    for i in functions:
        write_to(os.path.join(os.path.dirname(__file__),f'{fname}.py'),i,False)
        write_to(os.path.join(os.path.dirname(__file__),f'{fname}.py'),'\n',False)
 """


for i in secs:
    functions=generate_parse_functions(i.grammer)
    fname='separate\\'+i.name[1:-1]
    write_to(os.path.join(os.path.dirname(__file__),f'generatedparstcodeDevTr.py'),f'\n{i.name}',False)
    for i in functions:
        write_to(os.path.join(os.path.dirname(__file__),f'generatedparstcodeDevTr.py'),i,False)
        write_to(os.path.join(os.path.dirname(__file__),f'generatedparstcodeDevTr.py'),'\n',False)


a=''
a=add_line(a,'def MatchArr(Arr,ind,appendToError):')
a=add_line(a,'  for i in Arr:')
a=add_line(a,'    if Match(i,ind,appendToError)["node"]!=["error"]:')
a=add_line(a,'      return True')
a=add_line(a,'  return False')





a=add_line(a,f'def is_there_error(arr):')
a=add_line(a,f'    return "mode" in arr[-1].keys() and arr[-1]["mode"]==["error"]')
a=add_line(a,f'    ')
a=add_line(a,f'def fillmatch(arr,match,position,j):')
a=add_line(a,f'    if(callable(match)):')
a=add_line(a,f'        if position==0:')
a=add_line(a,f'            arr.append(match(j))')
a=add_line(a,f'        else:')
a=add_line(a,f'            arr.append(match(arr[-1]["index"]))')
a=add_line(a,f'    else:')
a=add_line(a,f'        if position==0:')
a=add_line(a,f'            arr.append(Match(match,j))')
a=add_line(a,f'        else:')
a=add_line(a,f'            arr.append(Match(match,arr[-1]["index"]))')
a=add_line(a,f'    return arr')

write_to(os.path.join(os.path.dirname(__file__),f'generatedparstcodeDevTr.py'),a,False)

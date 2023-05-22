import re
import sys
import os
sys.path.append("D:\Materials\compilers\project\Lexical-Analyser\\")  # Adds the parent directory to the sys.path
from Tokens.TokenTypes import *

def get_lower_dict(enum):
    d={}
    enum_keys = list(enum.__members__.keys())
    for key in enum_keys:
        d[key.lower()]=enum[key]
    return d


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

def add_line(s,line,num=None,end='\n'):
    return s+line+f'{end}' if not num else s+line+f'           {s}{end}'

def get_matches_array(rightSideStr,matches):
    Ors= [i.strip() for i in rightSideStr.split('|') if i.strip() and i.strip()!='ε']
    
    for i in Ors:
        mytoken=[t.strip() for t in i.split(' ') if t.strip()and i!='ε'][0]
        if (mytoken[0]=='<'):
            get_matches_array(global_dict_str[mytoken],matches)
        else:
            token_name=re.sub(r'\[|]',r'',mytoken).lower()
            matches.append(lowerdict[token_name])
    return matches



global_dict={}
global_dict_str={}
def matchfunc(onething,rightSideStr):
    lowest_level_array_tokens=get_matches_array(rightSideStr,[])
    if(onething[0]=='<'):
        lowest_level_array_tokens=[f'Token_type.{i.name}' for i in lowest_level_array_tokens]
        lowest_level_array_tokens_str=f'[{",".join(lowest_level_array_tokens)}]'
        if(len(lowest_level_array_tokens)>1):
            print(len(lowest_level_array_tokens))
            s=add_line('',f'MatchArr({lowest_level_array_tokens_str},ind,False)',end='')
        else:
            s=add_line('',f'Match({lowest_level_array_tokens[0]},ind,False)["node"]!=["error"]',end='')
    elif(onething[0]=='['):
        token_name=re.sub(r'\[|]',r'',onething).lower()
        s=add_line('',f'Match({lowerdict[token_name]},ind,False)["node"]!=["error"]',end='')
    try:
        if(s):
            pass
    except:
        raise (IndexError('s is not [ or <'))
    return s
def matchfunc2(rightSideStr,many=False):
    rightSideStr=rightSideStr.strip() 
    firstelement=rightSideStr[0]
    if(firstelement=='<'):
        many=True
        #its a non terminal
        first_token=rightSideStr.split(' ')[0]
        while(first_token[0]=='<'):
            newRHS=global_dict_str[first_token]
            first_token=newRHS.split(' ')[0]
           
        return matchfunc2(newRHS,many)
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
    return s
def merge_dicts(*dicts):
    """merge dicts into one dict, if there are similar keys, the latter one will overrite the former"""
    d={}
    if(dicts):
        for dic in dicts:
            for key in dic:
                d[key.lower()]=dic[key]
    return d
merge_dicts
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
        s=add_line(s,f' out={"{}"}')

        ind=0 #index of the element of the array, if we are in first thing, we get the one provided by finction
        rightSide=' '.join(things[2:])
        Ors=[i.strip() for i in rightSide.split('|') if i.strip()]
        if(len(Ors)==1):
             matches=get_matches(Ors[0])
             s=add_line(s,f' matches={matches}')
             s=add_line(s,f' return applyfills(matches,ind,"{function_name.lower()}")')
        elif len(Ors)>1:
            #add the initial if, then for the rest ors,
            for i in range(len(Ors)):
                workingOn=Ors[i]
                workingOnThings=[i.strip() for i in workingOn.split(' ') if i.strip()]
                if i==0:
                    s=add_line(s,f' if {matchfunc(workingOnThings[0],Ors[i])}:')
                    matches=get_matches(workingOn)
                    s=add_line(s,f'     matches={matches}')
                    s=add_line(s,f'     return applyfills(matches,ind,"{function_name.lower()}")')
                else:
                    if workingOnThings[0]!='ε':
                        s=add_line(s,f' elif {matchfunc(workingOnThings[0],Ors[i])}:')
                        matches=get_matches(workingOn)
                        s=add_line(s,f'     matches={matches}')
                        s=add_line(s,f'     return applyfills(matches,ind,"{function_name.lower()}")')

                    if(i==len(Ors)-1):
                        if(workingOnThings[0]=='ε'):
                            s=add_line(s,' else:')
                            s=add_line(s,f'   out["node"]=Tree("{function_name}",["ε"])')
                            s=add_line(s,f'   out["index"]=ind')
                            s=add_line(s,f'   return out')
                        else:
                            s=add_line(s,' else:')
                            s=add_line(s,f'     print("souldn\'t reach here")')
                            s=add_line(s,f'     out["mode"]=["error"]')
                            s=add_line(s,f'     out["node"]=["error"]')
                            s=add_line(s,f'     out["index"]=ind')
                            s=add_line(s,f'     return out')
        
            
        gens.append(s)
  
    return gens
        

sss=''
sss=add_line(sss,'import sys')
sss=add_line(sss,r'sys.path.append("D:\Materials\compilers\project\Lexical-Analyser\\")  # Adds the parent directory to the sys.path')
sss=add_line(sss,'import globals')
sss=add_line(sss,'from Tokens.TokenTypes import *')
sss=add_line(sss,'from nltk.tree import *')
sss=add_line(sss,'neeew=1')

write_to(os.path.join(os.path.dirname(__file__),f'generatedparstcodeDevTry11.py'),sss,False)



secs=extract_section(os.path.join(os.path.dirname(__file__),'Grammer.txt'))
for i in secs:
    functions=generate_parse_functions(i.grammer)
    fname='separate\\'+i.name[1:-1]
    write_to(os.path.join(os.path.dirname(__file__),f'generatedparstcodeDevTry11.py'),f'\n{i.name}',False)
    for i in functions:
        write_to(os.path.join(os.path.dirname(__file__),f'generatedparstcodeDevTry11.py'),i,False)
        write_to(os.path.join(os.path.dirname(__file__),f'generatedparstcodeDevTry11.py'),'\n',False)





#utils that he generated functions will need
s=''
s=add_line(s,"def is_there_error(arr):")
s=add_line(s,"    return 'mode' in arr[-1].keys() and arr[-1]['mode']==['error']")
s=add_line(s,"    ")
s=add_line(s,"def fillmatch(arr,match,position,j):")
s=add_line(s,"    if(callable(match)):")
s=add_line(s,"        if position==0:")
s=add_line(s,"            arr.append(match(j))")
s=add_line(s,"        else:")
s=add_line(s,"            arr.append(match(arr[-1]['index']))")
s=add_line(s,"    else:")
s=add_line(s,"        if position==0:")
s=add_line(s,"            arr.append(Match(match,j))")
s=add_line(s,"        else:")
s=add_line(s,"            arr.append(Match(match,arr[-1]['index']))")
#s=add_line(s,"    if(is_there_error(arr)):")
#s=add_line(s,"        print(f'{match} != {globals.Tokens[j].lex} ')")
s=add_line(s,"    return arr")
s=add_line(s,'def MatchArr(Arr,ind,appendToError):')
s=add_line(s,'  for i in Arr:')
s=add_line(s,'    if Match(i,ind,appendToError)["node"]!=["error"]:')
s=add_line(s,'      return True')
s=add_line(s,'  return False')
s=add_line(s,'def applyfills(matches,ind,func_name):')
s=add_line(s,'    arr=[]')
s=add_line(s,'    out={}')
s=add_line(s,'    Children=[]')
s=add_line(s,'    i=0')
s=add_line(s,'    while i< len (matches):')
s=add_line(s,'        match=matches[i]')
s=add_line(s,'        arr=fillmatch(arr,match,i,ind)')
s=add_line(s,'        ind=arr[-1]["index"]')
s=add_line(s,'        Children.append(arr[-1]["node"])')
s=add_line(s,'        if is_there_error(arr):')
#s=add_line(s,"            print(f'error at {func_name}','at',globals.Tokens[ind].lex,'at',ind,'at',globals.Tokens[ind].token_type)")
s=add_line(s,'            while ind<len(globals.Tokens) and globals.Tokens[ind].lex!="\\n" :')
s=add_line(s,'                ind+=1')
s=add_line(s,'            arr[-1]["index"]=ind')
s=add_line(s,'            if Token_type.newLine in matches[i:]:')
s=add_line(s,'                i=matches[i:].index(Token_type.newLine)+i')
s=add_line(s,'                continue')
s=add_line(s,'            else:')
s=add_line(s,'                out["mode"]=["error"]')
s=add_line(s,'                out["index"]=ind')
s=add_line(s,'                out["node"]=Tree(func_name,Children)')
s=add_line(s,'                return out')
s=add_line(s,'        ')
s=add_line(s,'        ind+=1')
s=add_line(s,'        i+=1')
s=add_line(s,'    out["node"]=Tree(func_name,Children)')
s=add_line(s,'    out["index"]=arr[-1]["index"]')
s=add_line(s,'    return out')
s=add_line(s,'def Match(a,j,report=True):')
s=add_line(s,'    output=dict()')
s=add_line(s,'    if(j<len(globals.Tokens)):')
s=add_line(s,'        Temp=globals.Tokens[j].to_dict()')
s=add_line(s,'        if(Temp["token_type"]==a):')
s=add_line(s,'            output["node"]=[Temp["Lex"]]')
s=add_line(s,'            output["index"]=j+1')
s=add_line(s,'            return output')
s=add_line(s,'        else:')
s=add_line(s,'            output["mode"]=["error"]')
s=add_line(s,'            output["node"]=["error"]')
s=add_line(s,'            output["index"]=j')
s=add_line(s,'            if(report):')
s=add_line(s,'                globals.errors.append("Syntax error : "+Temp["Lex"]+F" Expected {a}")')
s=add_line(s,'            return output')
s=add_line(s,'    else:')
s=add_line(s,'        output["node"]=["error"]')
s=add_line(s,'        output["index"]=j')
s=add_line(s,'        return output')
write_to(os.path.join(os.path.dirname(__file__),f'generatedparstcodeDevTry11.py'),s,False)

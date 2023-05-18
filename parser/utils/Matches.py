import globals
def Match(a,j,Tokens,appendToError=True):
    output=dict()
    if(j<len(Tokens)):
        Temp=Tokens[j].to_dict()
        tok=Temp['token_type']
        #print( f' matching {a} with {tok} ')
        if(Temp['token_type']==a):
            j+=1
            output["node"]=[Temp['Lex']]
            output["index"]=j
            return output
        else:
            #print(f'error found  token {j} on comparing  {a} to {tok}')
            if(appendToError):
                globals.errors.append(f"Syntax error at line {Temp['Line']}:  Expected {a} found ` {Temp['Lex']} `")
            output["node"]=["error"]
            output["index"]=j+1
            return output
    else:
        output["node"]=["error"]
        output["index"]=j+1
        return output
    
def MatchTry(a,j,Tokens):

    if(j>len(Tokens)):
        return False
    Temp=Tokens[j].to_dict()
    print(Temp['Lex'])
    if(Temp['token_type']==a):
        return True
    else:
        return False
def MatchArr(Arr,ind,Tokens,appendToError):
  for i in Arr:
    if Match(i,ind,Tokens,appendToError)["node"]!=["error"]:
      return True
  return False
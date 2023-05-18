from grapher import *
from Tokens.TokenTypes import *


def regictify_dict(dic):
    """
    takes dfa dict representation and completes it by adding reject state
    """
    d={}
    
    reject_node=Node('reject')
    for i in dic.keys():
        s=[]
        for j in dic[i].keys():
          s.append(dic[i][j])
        a='|'.join(s)
        dic[i].update({reject_node:f'^(?!{a})'})
    dic.update({reject_node:{reject_node:'(.)+'}})
       
    return dic

words=[
['Begin'],
['End'],
['Do'],
['If'],
['Then'],
['Else'],
['Integer'],
['Real'],
['Parameter'],
['Character'],
['Equalop','='],
['Lessthanop','<'],
['Greaterthanop','>'],
['Lessthanorequalop','<='],
['Greaterthanorequalop','>='],
['Notequalop','/='],
['Isequalop','=='],
['Plusop','+'],
['Minusop','-'],
['Multiplyop','*'],
['Divideop','/'],
['Identifier',-1],
['Constant',-1],
['Error',-1],
['Program',],
['Implicit',],
['none',],
['Print',],
['Read',],
['Comment',-1],#not implemented yet
['Scopeop','::'],
['Comma',','],
['newLine','\n'],
['OpenParan','('],
['CloseParan',')'],
['Dot','.'],
['Complex',],
['OpenBrac','['],
['CloseBrac',']'],
['Literal',-1],
]

DFA_dict={}

for wordarr in words:
    if len(wordarr)==1:
        DFA_dict[Token_type[wordarr[0]]]=DFA(wordarr[0])
    elif len(wordarr)==2 and wordarr[1]!=-1:
        DFA_dict[Token_type[wordarr[0]]]=DFA(wordarr[1])

#identifier DFA
i_arr=[Node('1'),Node('2',state=1)]
identifier_dict=regictify_dict({
    i_arr[0]:{i_arr[1]:'[_A-Za-z]'},
    i_arr[1]:{i_arr[1]:'[_a-zA-Z0-9]'},    
})
#test
#Visualizer.GIF_NO_SPLIT(i_arr[0],identifier_dict,'2aa22_s',True)


#Const DFA
i=[Node('q0'),Node('q1'),Node('q2',state=1),Node('q3',state=1)]
constr_dict=regictify_dict( {
    i[0]:{i[1]:'\+|-',i[2]:'[0-9]'},#start state
    i[1]:{i[2]:'[0-9]',i[3]:'\.'},#sign state
    i[2]:{i[2]:'[0-9]',i[3]:'\.',},#int state
    i[3]:{i[3]:'[0-9]'},#double state
})

i=[Node('q0'),Node('q1'),Node('q2',state=1)]
consti_dict=regictify_dict( {
    i[0]:{i[1]:'\+|-',i[2]:'[0-9]'},#start state
    i[1]:{i[2]:'[0-9]'},#sign state
    i[2]:{i[2]:'[0-9]'},#int state
})
#test
#Visualizer.GIF_NO_SPLIT(i[0],const_dict,'2aa22_s',True)

#Literal DFA
i=[Node('q0'),Node('q1'),Node('q2'),Node('q3',state=1)]

literal_dict=regictify_dict( {
    i[0]:{i[1]:'\'',i[2]:'"'},#start state
    i[1]:{i[1]:'^(?!\')',i[3]:'\''},#singe qoutation state
    i[2]:{i[2]:'^(?!")',i[3]:'"'},#double qoutation state
    i[3]:{i[3]:''},#final state
})

#test
#Visualizer.GIF_NO_SPLIT(i[0],literal_dict,"'2aa22_s'",True)
def inDFA_dict(dfadic,strr,strrdict):
    dfadic[Token_type[strr]]=DFA('')
    dfadic[Token_type[strr]].dict=strrdict

inDFA_dict(DFA_dict,'Literal',literal_dict)
inDFA_dict(DFA_dict,'ConstantI',consti_dict)
inDFA_dict(DFA_dict,'ConstantR',constr_dict)
inDFA_dict(DFA_dict,'Identifier',identifier_dict)
#print(DFA_dict)
#DFA_dict[Token_type.ConstantI].try_word('43242342.3')


from DFA.grapher import *
from Tokens.TokenTypes import *




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
identifier_dict=DFA.regictify_dict({
    i_arr[0]:{i_arr[1]:'[_A-Za-z]'},
    i_arr[1]:{i_arr[1]:'[_a-zA-Z0-9]'},    
})

#Const real DFA
i=[Node('q0'),Node('q1'),Node('q2',state=1),Node('q3',state=1)]
constr_dict=DFA.regictify_dict( {
    i[0]:{i[1]:'\+|-',i[2]:'[0-9]'},#start state
    i[1]:{i[2]:'[0-9]',i[3]:'\.'},#sign state
    i[2]:{i[2]:'[0-9]',i[3]:'\.',},#int state
    i[3]:{i[3]:'[0-9]'},#double state
})
#Const int DFA
i=[Node('q0'),Node('q1'),Node('q2',state=1)]
consti_dict=DFA.regictify_dict( {
    i[0]:{i[1]:'\+|-',i[2]:'[0-9]'},#start state
    i[1]:{i[2]:'[0-9]'},#sign state
    i[2]:{i[2]:'[0-9]'},#int state
})

#Literal DFA
i=[Node('q0'),Node('q1'),Node('q2'),Node('q3',state=1),Node('reject')]
literal_dict= {
    i[0]:{i[1]:'\'',i[2]:'"',i[4]:'^(?!\'|")'},#start state
    i[1]:{i[1]:'^(?!\')',i[3]:'\''},#singe qoutation state
    i[2]:{i[2]:'^(?!")',i[3]:'"'},#double qoutation state
    i[3]:{i[3]:'',i[4]:'(.)+'},#final state
    i[4]:{i[4]:'(.)+'},#reject state
}

#Comment DFA
i=[Node('q0'),Node('q1',state=1),Node('reject')]
comment_dict= {
    i[0]:{i[1]:'!',i[2]:'^(?!!)'},#nothing state
    i[1]:{i[2]:'\n',i[1]:'^(?!\n)'},#comment state   
    i[2]:{i[2]:'(.)+'},#final state
}
#test

def inDFA_dict(dfadic,strr,strrdict):
    dfadic[Token_type[strr]]=DFA('')
    dfadic[Token_type[strr]].dict=strrdict

inDFA_dict(DFA_dict,'Literal',literal_dict)
inDFA_dict(DFA_dict,'ConstantI',consti_dict)
inDFA_dict(DFA_dict,'ConstantR',constr_dict)
inDFA_dict(DFA_dict,'Identifier',identifier_dict)
inDFA_dict(DFA_dict,'Comment',comment_dict)



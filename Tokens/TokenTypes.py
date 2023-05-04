from enum import Enum

class Token_type(Enum): # listing all tokens type
    ["program implicit none end if else end integer real parameter do character print* read* ! :: ="]
    
    
    Begin=1
    End=2
    Do=3 
    If=4
    Then=5
    Else=6  
    Integer=7
    Real=8
    Parameter=9
    Character=10
    Equalop=11
    Lessthanop=12
    Greaterthanop=13       
    Lessthanorequalop=14   
    Greaterthanorequalop=15
    Notequalop=16
    Isequalop=17
    Plusop=18
    Minusop=19
    Multiplyop=20
    Divideop=21
    Identifier=22
    Constant=23
    Error=24
    Program=25
    Implicit=26
    none=27
    Prints=28
    Reads=29
    Comment=30
    Scopeop=31
    Comma=32
    OpenParan=33
    CloseParan=34
    Dot=35
    Complex=36
    OpenBrac=37
    CloseBrac=38
    Literal=39

print(Token_type['Begin'])
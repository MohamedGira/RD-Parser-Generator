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
    Read=29
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
    newLine=40
    Semicolon=41
    Write=42




ReservedWords={
            "begin":Token_type.Begin,
            "end":Token_type.End,
            "do":Token_type.Do,
            "if":Token_type.If,
            "then":Token_type.Then,
            "else":Token_type.Else,
            "integer":Token_type.Integer,
            "real":Token_type.Real,
            "complex":Token_type.Complex,
            "parameter":Token_type.Parameter,
            "character":Token_type.Character,
            "program":Token_type.Program,
            "implicit":Token_type.Implicit,
            "none":Token_type.none,
            "print":Token_type.Prints,
            "read":Token_type.Read,
            "write":Token_type.Read,
            "!":Token_type.Comment,
            
            }
Operators={
            ",":Token_type.Comma,
            "::":Token_type.Scopeop,
            "<":Token_type.Lessthanop,
            ">":Token_type.Greaterthanop,
            "<=":Token_type.Lessthanorequalop,
            ">=":Token_type.Greaterthanorequalop,
            "/=":Token_type.Notequalop,
            "==":Token_type.Isequalop,
            "=":Token_type.Equalop,
            "+":Token_type.Plusop,
            "-":Token_type.Minusop,
            "*":Token_type.Multiplyop,
            "/":Token_type.Divideop,
            "(":Token_type.OpenParan,
            ")":Token_type.CloseParan,
            "[":Token_type.OpenBrac,
            "]":Token_type.CloseBrac,
            ".":Token_type.Dot,
            ";":Token_type.Semicolon
          }


def get_lower_dict(enum):
    d={}
    enum_keys = list(enum.__members__.keys())
    for key in enum_keys:
        d[key.lower()]=enum[key]
    return d




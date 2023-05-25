from enum import Enum
class Token_type(Enum):  # listing all tokens type

    # List Representation
    OpenParenthesis = 1
    CloseParenthesis = 2

    # ReservedWords
    Dotimes = 3
    When = 4
    Read = 5
    Write = 6
    LogicalTrue = 7
    LogicalFalse = 8

    # Operators
    Semicolon = 9
    PlusOp = 10
    MinusOp = 11
    MultiplyOp = 12
    DivideOp = 13
    ModOp = 14
    RemOp = 15
    IncrementOp = 16
    DecrementOp = 17
    GreaterThanOrEqualOp = 18
    LessThanOrEqualOp = 19
    EqualOp = 20
    NotEqualOp = 21

    # Other
    String = 22
    Setq = 23
    Error = 24
    Number = 25
    Identifier = 26
    Cos = 27
    Sin = 28
    Tan = 29
    Function=30
    GreaterThanOp=31
    LessThanOp=32

# class token to hold string and token type
class Token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type
        self.line=0
    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }

# Reserved word Dictionary
ReservedWords = {"(": Token_type.OpenParenthesis,
            ")": Token_type.CloseParenthesis,
            "dotimes": Token_type.Dotimes,
            "when": Token_type.When,
            "read": Token_type.Read,
            "write": Token_type.Write,
            "nil": Token_type.LogicalFalse,
            "setq": Token_type.Setq,
            "cos": Token_type.Cos,
            "tan": Token_type.Tan,
            "t": Token_type.LogicalTrue,
            "sin": Token_type.Sin
            }

Operators = {";": Token_type.Semicolon,
             "+": Token_type.PlusOp,
             "-": Token_type.MinusOp,
             "*": Token_type.MultiplyOp,
             "/": Token_type.DivideOp,
             "mod": Token_type.ModOp,
             "rem": Token_type.RemOp,
             "incf": Token_type.IncrementOp,
             "decf": Token_type.DecrementOp,
             "<=": Token_type.LessThanOrEqualOp,
             ">=": Token_type.GreaterThanOrEqualOp,
             "=": Token_type.EqualOp,
             "<>": Token_type.NotEqualOp,
             ">": Token_type.GreaterThanOp,
             "<": Token_type.LessThanOp

             }


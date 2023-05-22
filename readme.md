# Recursive Descent Parser Generator

Welcome to the Recursive Descent Parser Generator documentation!

This Repo ws meant hold the frontend compiler stages for Fortran programming language. But... I did A Thing!

Instead of Writing the functions one by one, then facing hell when a bug is found or a mistake in the grammer is found. I made a Parser generator 😃

The Recursive Descent Compiler Compiler is a groundbreaking tool designed to simplify the process of generating parsing functions in Python based on valid grammar rules **with respect to Recursive Descent parser rules** . With this tool, you can easily build language processors, parsers, and compilers without the need for manual implementation of complex parsing logic.



## Key Features

  **✅ Automatic Conversion**: The Recursive Descent Parser Generator automatically converts valid grammar rules into parsing functions (not 100% accurate yet) , saving you time and effort in implementing parsers from scratch, and giving you the chance to focus on more complex features
  
 **✅ Support for Recursive Grammar**: The tool seamlessly handles right recursive grammar rules, allowing you to define and parse complex language structures.

 **✅ Error Recovery**: Incorporates Panic Mode Error Recovery to handle and recover from syntax errors during parsing, more robustness for your processor!


## Interface
### Grammer Structure
In order for this tool to work correctly, the grammer must be presented in the following format.
`Grammer.txt`
```
#section name
#program definition
<Parse> -> [PROGRAM] [IDENTIFIER] [NEWLINE] <body> [END] [PROGRAM] [IDENTIFIER] [NEWLINE]
<body> ->  [IMPLICIT] [NONE] [NEWLINE] <declarations> <statements> 
___________
.
.
EOF
```
- The section name,  preceded by a `#`

- `[]` are not part of the language, they mean that whats inside is a Terminal
- `<>` are not part of the language, they mean that whats inside is a Non-Terminal
- The section is ended with one or more &nbsp; `_` .
- The grammer text file is ended with `EOF`
- Each entity is spearated by Spaces
### Notes : 
- `<whats_here>` will be treated as function name, so only use python valid idntifiers
- `[whats_here]` will be searched for in the `Token_type` enum members lowercase representation, so they must match, in case you wish to use operators, delimiters, etc... you can add them to `Operators` and `ReservedWord` dictionaries as follows:
 ``` 
ReservedWords={
            "begin":Token_type.Begin,
            "end":Token_type.End,...          
            }
Operators={
            ">":Token_type.Greaterthanop,
            "<=":Token_type.Lessthanorequalop,...
          }
```
- the `Token_type`, `Operators`,and` ReservedWords` are concatinated together in one array and used in parsing

## Output
The output of this parser is the Recursive Descent Parsing Code that can be later used to parse the language of the given grammer

import sys
sys.path.append("D:\Materials\compilers\project\Lexical-Analyser\\")  # Adds the parent directory to the sys.path
import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import *
from Tokens.TokenTypes import *
import globals
from parser.generatedParseCode import *
from scanner.scanner import find_token,token


def get_tests(path):
    tests=[]
    with open(path, "r",encoding = "utf-8") as file:
        test=''
        for line in file:
            # Do something with the line
            if(line=='EOF\n'):
                return tests
            elif(line[0]=='_'):
                tests.append(test)if test.strip() else None
                test=''
            elif(line!='\n'and line.strip()):
                test+=line
    return tests
import os
from nltk.draw import draw_trees

if __name__ == "__main__":
    
    """GUI TO Test Phase 2"""
    
    
    globals.errorsScreen,globals.dtDa1=None,None
    tests=get_tests(os.path.join(os.path.dirname(__file__), '..\\parser\\FORTRAN_testcases.txt'))
    trees=[]
    for i,test in enumerate(tests):

        globals.errors=[]
        globals.Tokens=find_token(test)
        Node=None
        if(not Token_type.Error in [t.token_type for t in globals.Tokens]):
            if(neeew):
                Node=Parse(0)["node"]
            else:
                Node=Parse(0,globals.Tokens)["node"]
                
            trees.append(Node)
       
        if(not globals.errors):
            print(f'test {i+1}: Syntax is correct')
            print('test:___________________________________________________________')
    
            print(test)
            print('_________________________________________________________________')

        else:
            if (not Node):
                print(f'test {i+1}: had lexical errors, it didn\'t enter the parsing process: ({len(globals.errors)} error/s found)')
            else:
                print(f'test {i+1}: ({len(globals.errors)} error/s found)')
            errorified_test=test.split('\n')
            
            
            for i,error in enumerate(globals.errors):
                line=error.split(':')[0].split(' ')[-1]
                errorified_test[int(line)-1]=errorified_test[int(line)-1].replace('\n',' ')+f' \033[0;31m  <--- Error  {" ".join(error.split(":")[1:])} \033[0m'
                try:
                    errorlex=re.compile(globals.errors_lexemes[i],re.IGNORECASE)
                    errorified_test[int(line)-1]=errorlex.sub(f"\033[0;31m\x1B[4m" + globals.errors_lexemes[i].replace('\n',' ') + "\x1B[0m\033[0m",errorified_test[int(line)-1])
                except:
                    pass
            print('test:___________________________________________________________')
            for line in errorified_test:
                print(line)
            print('_________________________________________________________________')

            df1=pandas.DataFrame(globals.errors)
            errorsScreen = tk.Toplevel()
            errorsScreen.geometry("800x800")
            errorsScreen.title(test.split(' ')[1])
            errorsTable = pt.Table(errorsScreen, dataframe=df1, showtoolbar=True, showstatusbar=True,maxcellwidth=800,cols=1)
            errorsTable.columnwidths[0]=800
            errorsTable.show()

    draw_trees(*trees)
    



# ### 
















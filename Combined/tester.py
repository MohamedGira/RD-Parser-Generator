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
from parser.generatedparstcodeDevTry999 import *
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
    
    
    globals.dtDa2,globals.dtDa1=None,None
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
        else:
            if (not Node):
                print(f'test {i+1}: had lexical errors, it didn\'t enter the parsing process: ({len(globals.errors)} error/s found)')
            else:
                print(f'test {i+1}: ({len(globals.errors)} error/s found)')
            errorified_test=test.split('\n')
            for error in globals.errors:
                line=error.split(':')[0].split(' ')[-1]
                errorified_test[int(line)-1]=errorified_test[int(line)-1].replace('\n','')+'\033[0;31m  <--- Error'+ ' '.join(error.split(':')[1:])+' \033[0m'
            for line in errorified_test:
                print(line)
            print()
            df1=pandas.DataFrame(globals.errors)
            dtDa2 = tk.Toplevel()
            dtDa2.geometry("800x800")
            dtDa2.title(test.split(' ')[1])
            dtDaPT2 = pt.Table(dtDa2, dataframe=df1, showtoolbar=True, showstatusbar=True,maxcellwidth=800,cols=1)
            dtDaPT2.columnwidths[0]=800
            dtDaPT2.show()

    draw_trees(*trees)
    



# ### 
















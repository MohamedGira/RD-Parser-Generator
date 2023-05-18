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
from generatedParserCode2 import *
from scanner.scanner import find_token,token



if __name__ == "__main__":
    
    """GUI TO Test Phase 2"""
    
    root= tk.Tk()
    WIDTH=800
    canvas1 = tk.Canvas(root, width=WIDTH, height=800, relief='raised')
    canvas1.pack()

    label1 = tk.Label(root, text='Parser Phase')
    label1.config(font=('helvetica', 14))
    canvas1.create_window(WIDTH/2, 25, window=label1)

    label2 = tk.Label(root, text='Source code:')
    label2.config(font=('helvetica', 10))
    canvas1.create_window(WIDTH/2, 50, window=label2)

    entry1 = tk.Text(root) 
    canvas1.create_window(WIDTH/2, 300, window=entry1)
    globals.dtDa2,globals.dtDa1=None,None
    def Scan():
        globals.errors=[]
        x1 = entry1.get('1.0', 'end-1c')
        globals.Tokens=find_token(x1)
        #print(globals.Tokens)
        df=pandas.DataFrame.from_records([t.to_dict() for t in globals.Tokens])
        #print(df)
        try:
            globals.dtDa1.destroy()
        except:
            pass
        finally:
            #to display token stream as table
            globals.dtDa1 = tk.Toplevel()
            globals.dtDa1.title('Token Stream')
            globals.dtDaPT = pt.Table(globals.dtDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
            globals.dtDaPT.show()
        # start Parsing
        Node=Parse(0,globals.Tokens)["node"]
        
        try:
            globals.dtDa2.destroy()
        except:
            pass
        finally:
        # to display errorlist
            df1=pandas.DataFrame(globals.errors)
            globals.dtDa2 = tk.Toplevel()
            globals.dtDa2.title('Error List')
            globals.dtDaPT2 = pt.Table(globals.dtDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
            globals.dtDaPT2.show()
        Node.draw()



    
        
    button1 = tk.Button(text='Scan', command=Scan, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
    canvas1.create_window(WIDTH/2, 600, window=button1)
    root.mainloop()


# ### 

















import tkinter as tk
from enum import Enum
import re
from pandastable import Table
from Tokens.TokenTypes import *
import pandas
from DFA_Generator import DFA_dict

from grapher import *
# class token to hold string and token type
class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type
    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }
            
#Reserved word Dictionary
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
            "read":Token_type.Reads,
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
            ".":Token_type.Dot
            
          }

def spacify(text,lst):
    for i in lst:
        text=text.replace(f'{i}',f' {i} ')
        for ind,t in enumerate(text):
            if(t=='.'and re.match(r'\d',text[ind-2])):
                text=text[0:ind-1]+text[ind]+text[ind+2:]
                    
    return text

def find_token(text):
    Tokens=[] # to add tokens to list
    
    lines=spacify(text,list(Operators.keys())).lower().split('\n')
    for line in lines:
        line=line.strip()
        tokens=[a for a in line.split(' ') if a!=' ' and a !='']
        ind=0
        while ind < len(tokens):
            tok=tokens[ind]
            if(re.match(r'^!',tok)):
                Tokens.append(token(' '.join(tokens[ind:]),ReservedWords[tok]))
                break
            elif(re.match(r'^"|^\'',tok)):
                oind=ind
                str=tokens[oind]
                if re.match(r'^"',tok):
                    str=r'"\s*$'
                else:
                    str=r'\'\s*$'
                
                while(ind<len(tokens)and not re.search(str,tokens[ind])):
                    ind+=1
                if (ind>=len(tokens)):
                    Tokens.append(token(' '.join(tokens[ind:]),Token_type.Error))    
                else:
                    Tokens.append(token(' '.join(tokens[oind:ind+1]),Token_type.Literal))
                
            elif tok in ReservedWords:
                Tokens.append(token(tok,ReservedWords[tok]))
            elif tok in Operators:
                Tokens.append(token(tok,Operators[tok]))
            elif(re.match(r'^[a-zA-z][a-zA-z0-9]*$',tok)):
                Tokens.append(token(tok,Token_type.Identifier))
            elif(re.match(r'([0-9]+.[0-9])|[0-9]+',tok)):
                Tokens.append(token(tok,Token_type.Constant))
            else:
                Tokens.append(token(tok,Token_type.Error))
            ind+=1
      
    return Tokens
       
    # complete 
       
    pass


#GUI

import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk
from pandastable import Table,TableModel
# Create the Tkinter window
root = tk.Tk()


def Scan():
    

    x1 = entry.get('1.0', 'end-1c')
    tokens=find_token(x1)
    arr=[t.to_dict() for t in tokens]
    df=pandas.DataFrame.from_records([t.to_dict() for t in tokens])    
    table.model.df=df
   
    
    fpath='dne.gif'
    frames=[]
    def on_click(event):
        frames.clear()
        selected_item = table.get_row_clicked(event)
        lex=table.model.df.iloc[selected_item,0]
        token_type=table.model.df.iloc[selected_item,1]
        fpath=DFA_dict[token_type].try_word(lex)

        with Image.open(fpath) as image:
            for i in range(image.n_frames):
                image.seek(i)
                resized_image = image.resize((root.winfo_width()//4, root.winfo_width()//4))
                tk_image = ImageTk.PhotoImage(resized_image)
                frames.append(tk_image)
        os.remove(fpath)
        
    
    def update_frame(frame_number):               
        print(len(frames))
        if len(frames)>0:
            label3.config(image=frames[frame_number%len(frames)])
    import threading
    def animate():
        i=0
        while True:
            time.sleep(0.8)
            root.after(0, update_frame, i)
            i+=1
    t1 = threading.Thread(target=animate)
    try:
        t1.start()
    except:
        pass
     
    table.bind('<ButtonRelease-1>', on_click)
    table.show()

    
    
    


# Define the first section with a text input prompt and a button
frame1 = tk.Frame(root)
label = tk.Label(frame1, text="Enter text:")
label.pack(side="left")
entry = tk.Text(frame1)
entry.pack(side="left")
button = tk.Button(frame1, text="Scan",command=Scan)
button.pack(side="left")
frame1.grid(row=0, column=0, sticky="nsew")

# Define the second section with a table
frame2 = tk.Frame(root)
table = Table(frame2, model=TableModel())
data = {'Column 1': [1, 2, 3], 'Column 2': [4, 5, 6]}

# Populate the table with the sample data
table.model.df = pd.DataFrame(data)
table.show()



frame2.grid(row=0, column=2, sticky="nsew")

# Define the third section with an image
frame3 = tk.Frame(root)

label3 = tk.Label(frame3)
label3.pack()
frame3.grid(row=0, column=1, sticky="nsew")

# Configure grid weights for dynamic resizing
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)

# Start the Tkinter event loop

root.mainloop()

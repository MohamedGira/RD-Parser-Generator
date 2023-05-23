import sys
sys.path.append("D:\Materials\compilers\project\Lexical-Analyser\\")  # Adds the parent directory to the sys.path
import globals
import tkinter as tk
from enum import Enum
import re
from pandastable import Table
from Tokens.TokenTypes import *
import pandas
from DFA_Generator import DFA_dict

from grapher import *


    
#Reserved word Dictionary


def spacify(text,lst,exclude=['.']):

    for i in lst  :
        if i not in exclude:
            text=text.replace(f'{i}',f' {i} ')
            for i in [longel for longel in lst if len(longel)>1]:
                text=text.replace('  '.join([*i]),i)
              
    return text

def find_token(text):
    Tokens=[] # to add tokens to list
    
    text=spacify(text,list(Operators.keys())).lower()
    text=text.replace("\n", " \n ")
    text_tokens=[a for a in text.split(' ') if a!=' ' and a !='']
    for ind,i in enumerate(text_tokens):
        text_tokens[ind]=i.strip() if i !='\n' else i

    ind=0
    line=1
    while ind < len(text_tokens):
        tok=text_tokens[ind]
        if(tok=='\n'):
            line+=1
            if Tokens[-1].token_type!=Token_type.newLine:
                Tokens.append(token(tok,Token_type.newLine,line))
        elif(re.match(r'^!',tok)):
            globals.comments.append(token(' '.join(text_tokens[ind:text_tokens[ind:].index('\n')+ind]),ReservedWords[tok],line))
            ind=text_tokens[ind:].index('\n')+ind
        elif(re.match(r'^"|^\'',tok)):
            oind=ind
            str=text_tokens[oind]
            if re.match(r'^"',tok):
                str=r'"\s*$'
            else:
                str=r'\'\s*$'
            
            while(ind<len(text_tokens)and not re.search(str,text_tokens[ind])):
                ind+=1
            if (ind>=len(text_tokens)):
                Tokens.append(token(' '.join(text_tokens[ind:]),Token_type.Error,line))    
            else:
                Tokens.append(token(' '.join(text_tokens[oind:ind+1]),Token_type.Literal,line))
            
        elif tok in ReservedWords:
            Tokens.append(token(tok,ReservedWords[tok],line))
        elif tok in Operators:
            Tokens.append(token(tok,Operators[tok],line))
        elif(re.match(r'^[a-zA-z][a-zA-z0-9]*$',tok)):
            Tokens.append(token(tok,Token_type.Identifier,line))
        elif(re.match(r'^\d*\.\d+$|^\d+\.\d*$',tok)):
            Tokens.append(token(tok,Token_type.ConstantR,line))
        elif(re.match(r'^[+-]?\d+$',tok)):
            Tokens.append(token(tok,Token_type.ConstantI,line))
        else:
            Tokens.append(token(tok,Token_type.Error,line))
            globals.errors.append(f'Lexical Error at line {line }: {tok} is not a valid token')
        ind+=1
      
    return Tokens
       
    # complete 
       
    pass
import re

pattern = r'^[+-]?\d+$'
integer_regex = re.compile(pattern)

# Test some sample inputs
inputs = ["42", "-123", "0", "+999", "abc", "3.14"]
for input_str in inputs:
    if integer_regex.match(input_str):
        print(f"{input_str} is a valid integer.")
    else:
        print(f"{input_str} is not a valid integer.")



#GUI
if __name__ == "__main__":
    """Scanner GUI"""
    
    window_width = 800  # Specify the desired width
    window_height = 600  # Specify the desired height
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
    

        globals.frames=[]

        def on_click(event):
            # Define the third section with an image
            try:
                globals.frame3.destroy()
            except Exception as e:
                print(str(e))
                
            finally:
                globals.frame3 = tk.Toplevel()
                # Set the window size
                
                globals.frame3.geometry(f"{window_width}x{window_height}")
            
                label3 = tk.Label(globals.frame3)
                label3.pack()
                fpath='dne.gif'
            
            globals.frames.clear()
            selected_item = table.get_row_clicked(event)
            lex=table.model.df.iloc[selected_item,0]
            token_type=table.model.df.iloc[selected_item,2]
            globals.frame3.title('loading')
            time.sleep(.2)
            globals.frame3.title('almost there')
            time.sleep(.2)
            globals.frame3.title(f'{lex}')
            fpath=DFA_dict[token_type].try_word(lex)
            with Image.open(fpath) as image:
                for i in range(image.n_frames):
                    width, height = image.size
                    aspect_ratio = width / height
                    
                   
                    # Resize the image while maintaining aspect ratio
                    aspect_ratio = image.width / image.height
                    window_ratio = window_width / window_height

                    if window_ratio > aspect_ratio:
                        # Fit the image height to the window height
                        new_height = window_height
                        new_width = int(new_height * aspect_ratio)
                    else:
                        # Fit the image width to the window width
                        new_width = window_width
                        new_height = int(new_width / aspect_ratio)
                    print(new_height,new_width,window_width,window_height)
                    image.seek(i)
                    resized_image = image.resize((new_width, new_height),resample=Image.ANTIALIAS)
                    tk_image = ImageTk.PhotoImage(resized_image)
                    globals.frames.append(tk_image)
            os.remove(fpath)
            
        
            def update_frame(frame_number):               
                
                image=globals.frames[frame_number%len(globals.frames)]
                
                if len(globals.frames)>0:
                    label3.config(image=image)
            import threading
            def animate():
                i=0
                while True:
                    time.sleep(0.8)
                    try:
                        root.after(0, update_frame, i)
                    except:
                        pass
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



    frame2.grid(row=0, column=1, sticky="nsew")



    # Configure grid weights for dynamic resizing
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    # Start the Tkinter event loop

    root.mainloop()

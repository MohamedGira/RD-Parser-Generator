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
from DFA_Generator import DFA_dict
import time
import os

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
    # Define the first section with a text input prompt and a button
    frame1 = tk.Frame(root)
    label = tk.Label(frame1, text="Enter text:")
    label.pack(side="left")
    entry = tk.Text(frame1)
    entry.pack(side="left")
    def Scan():

        globals.errors=[]
        globals.Tokens=[]
        globals.frames=[]
        WIDTH=root.winfo_screenheight()*0.9
        HEIGHT=root.winfo_screenheight()*0.9

        x1 = entry.get('1.0', 'end-1c')
    
        globals.Tokens=find_token(x1)

        arr=[t.to_dict() for t in globals.Tokens]
        df=pandas.DataFrame.from_records([t.to_dict() for t in globals.Tokens])    
        table.model.df=df
    
        table.show()

        
        df=pandas.DataFrame.from_records([t.to_dict() for t in globals.Tokens])
        
        
        Node=Parse(0,globals.Tokens)["node"]
        
        


        
        
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
        
        
        


    
    
    frame1.grid(row=0, column=0, sticky="nsew")

      # Define the first section with a text input prompt and a button
    frame1 = tk.Frame(root)
    label = tk.Label(frame1, text="Enter text:")
    label.config(font=('helvetica', 14))
    label.pack(side="left")
    entry = tk.Text(frame1)
    entry.pack(side="left")
    button = tk.Button(frame1,text='Scan', command=Scan, bg='deep sky blue', fg='black', font=('helvetica', 9, 'bold'))
    button.pack(side="left")
    frame1.grid(row=0, column=0, sticky="nsew")

    # Define the second section with a table
    frame2 = tk.Frame(root)
    table = Table(frame2, model=TableModel())

 


    frame2.grid(row=0, column=1, sticky="nsew")



    # Configure grid weights for dynamic resizing
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    # Start the Tkinter event loop

    root.mainloop()

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from pathlib import *

#create a root widget
root=Tk()
root.title("This is a GUI for P1120 configuration.")
root.geometry("600x600")

#create a wedget with 2 tabs, the 2nd tab has a scrollbar
#create a notebook
note=ttk.Notebook(root)
#create 2 tabs    
tab1=Frame(note)
note.add(tab1,text='choose config_file')
tab2=Frame(note)
note.add(tab2,text='create config_file')
note.pack(fill='both', expand=1)
#scrollbar require 2 canvas in 2nd tab
#create a canvas in main frame
canvas=Canvas(tab2)
canvas.pack(side='left',fill='both',expand=1)
#add a scrollbar to the canvas
scrollbar=ttk.Scrollbar(tab2,orient='vertical',command=canvas.yview)
scrollbar.pack(side='right',fill='y')
#configure the canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
#create another frame inside the canvas
frame2=Frame(canvas)
#add that new frame to a window in the canvas
canvas.create_window((0,0),window=frame2,anchor="nw")


########### select a config file for p1120 (tab1 row 1)#####################
folder= r'K:\ModelsResource\lib\py1120\Config_files'
filelist = [fname for fname in os.listdir(folder) if fname.startswith('config')]

clicked=StringVar()
clicked.set('config.check_db')
con_file = StringVar()
con_file.set(r'K:\ModelsResource\lib\py1120\Config_files\config.check_db')
cal=Label(tab1,text='Select Config').grid(row=1, column=1, sticky = W, pady = 2)
combo_a=ttk.Combobox(tab1,width = 51, textvariable=clicked, value=filelist)


def comboclick(event):
    clicked=combo_a.get()
    #print (clicked)
    cf=folder+'\\'+clicked
    #print (cf)
    con_file.set(cf)
    return


#combobox setting
combo_a.bind("<<ComboboxSelected>>", comboclick)
combo_a.grid(row = 1, column = 2, columnspan = 2, sticky = W, pady = 2)


def browseFiles():
    filename1 = filedialog.askopenfilename(initialdir = r'K:\ModelsResource\lib\py1120\Config_files') 
    path1=Path(filename1)
    #print (path1) 
    con_file.set(path1) 
    combo_a.set(filename1)
    return


button_a = Button(tab1,text = "Browse Config", width=20,command = browseFiles).grid(row = 1, column = 4, sticky = W, padx=5, pady = 2)                     


########### select the database (tab1 row 2)#####################
db_dir = StringVar()
db_dir.set('K:\\SystemOptimization\\systemDB\\system_current.mdb')
db_dir_l=Label(tab1,text='Select Database').grid(row=2, column=1, sticky = W, pady = 2)


def browse_dbs(): 
    filename2 = filedialog.askopenfilename(initialdir = "",title = "Select Database",filetypes=(("access 2000","*.mdb"),("access 2010","*.accdb"))) 
    db_dir.set(Path(filename2))
    entry_db.delete(0, END)
    entry_db.insert(0, filename2)                                  
    return                     
   

   
button_b= Button(tab1,text = "Browse HVD Database", width=20,command = browse_dbs).grid(row=2,column = 4, sticky = W, padx=5, pady = 2)    

entry_db = Entry(tab1,width = 55)
entry_db.grid(row=2, column = 2, columnspan = 2, sticky = W, pady = 2)

entry_db.delete(0, END)
entry_db.insert(0, "K:/SystemOptimization/systemDB/system_current.mdb")

########### select the output folder (tab1 row 3)#####################
op_dir = StringVar()
dialog_labe3=Label(tab1,text='Output Folder').grid(row=3, column=1, sticky = W, pady = 2)



def browse_folder(): 
    folder_op = filedialog.askdirectory()
    op_dir.set(Path(folder_op))
    entry_op.delete(0, END)
    entry_op.insert(0, folder_op)                                  
    return    
 
 

             
button_op= Button(tab1,text = "Select Output Folder", width=20,command = browse_folder).grid(row=3, column=4, sticky = W, padx=5, pady = 2)
entry_op = Entry(tab1,width = 55)
entry_op.grid(row=3, column = 2, columnspan = 2, sticky = W, pady = 2)
entry_op.delete(0, END)


########### run p1120 (tab1 row 4)#####################
p1120_log=[]

def run_py1120():
    s1=db_dir.get()
    s2=con_file.get()
    s3=op_dir.get()
    os.chdir(s3)  
    os.system('setlocal')
    command_bash='python K:\\ModelsResource\\bin\\p1120.py -d "'+s1+'"  -o "'+s2+'" > p1120.logfile'
    #print(command_bash)
    os.system(command_bash)
    with open(op_dir.get()+'\\'+'p1120.logfile','r') as file_log:
        for line in (file_log.readlines() [-5:]):
            p1120_log.append(line)
    return

    
    
    
button_py1120 = Button(tab1,text = "run p1120",width=30,command = run_py1120)  
button_py1120.grid(row=4, column=2, sticky = W, padx=5, pady = 2)


########### print the last line of p1120.logfile (tab1 row 5)#####################
text = Text(tab1,wrap=WORD, width=71, height=20)
text.grid(row=5,column = 1,columnspan = 4, sticky = W, padx=13, pady = 2)

button_clear = Button(tab1,text = "clear p1120.log text",width=30)  
button_clear.grid(row=6, column=2,columnspan = 4,sticky = W, padx=75, pady = 2)


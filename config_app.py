from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.scrolledtext
import os
from pathlib import *
import json

#create a root widget
root=Tk()
root.title("This is a GUI for P1120 configuration.")
root.geometry("600x600")


last_entry=r'C:\Users\yfan1\Desktop\data\python\New folder\p1120_gui.json'

with open(last_entry) as gui_cf:
    gui_cf_history = json.load(gui_cf)
    

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

#click=gui_cf_history['config']
#clicked.set(gui_cf_history['config'])
con_file = StringVar()
con_file.set(gui_cf_history['config'])
cal=Label(tab1,text='Select Config').grid(row=1, column=1, sticky = W, pady = 2)
combo_a=ttk.Combobox(tab1,width = 51, value=filelist)
combo_a.set(gui_cf_history['config'])

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
db_dir.set(gui_cf_history['database'])
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
entry_db.insert(0, Path(db_dir.get()))

########### select the output folder (tab1 row 3)#####################
op_dir = StringVar()
op_dir.set(gui_cf_history['dir'])
dialog_labe3=Label(tab1,text='Output Folder').grid(row=3, column=1, sticky = W, pady = 2)



def browse_folder(): 
    folder_op = filedialog.askdirectory()
    op_dir.set(Path(folder_op))
    entry_op.delete(0, END)
    entry_op.insert(0, folder_op)                                  
    return    
 
 

             
button_op= Button(tab1,text = "Select Output Folder", width=20,command = browse_folder).grid(row=3, column=4, sticky = W, padx=5, pady = 2)
entry_op = Entry(tab1,width = 55)

entry_op.delete(0, END)
entry_op.insert(0, Path(op_dir.get()))
entry_op.grid(row=3, column = 2, columnspan = 2, sticky = W, pady = 2)



########### run p1120 (tab1 row 4)#####################
########### print the last line of p1120.logfile (tab1 row 5)#####################
p1120_log=[]
#text = Text(tab1,wrap=WORD, width=71, height=20)
text = tkinter.scrolledtext.ScrolledText(tab1,wrap=WORD, width=71, height=20)
text.grid(row=5,column = 1,columnspan = 4, sticky = W, padx=13, pady = 2)


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
        for line in (file_log.readlines() [-20:]):
            p1120_log.append(line)
    text.config(state='normal')
    text.delete(1.0,END)
    for i in p1120_log:
        text.insert(END, i)    
    # text read only    
    text.config(state=DISABLED)
    return

    
    
    
button_py1120 = Button(tab1,text = "run p1120",width=30,command = run_py1120)  
button_py1120.grid(row=4, column=2, sticky = W, padx=5, pady = 2)


def open_log():
    if os.path.isfile("p1120.logfile") is True:    
        os.startfile("p1120.logfile")
    return



    
button_clear = Button(tab1,text = "open p1120.log",width=30,command = open_log)  
button_clear.grid(row=6, column=2,columnspan = 4,sticky = W, padx=65, pady = 5)

########################## write the lastest configuration into gui_config.json when the window closed #################
def history(event):
    gui_cf_history['config']=con_file.get()
    gui_cf_history['database']=db_dir.get()
    gui_cf_history['dir']=op_dir.get()
    with open(last_entry,'w') as outfile:
        json.dump(gui_cf_history, outfile) 
    return
    
    

root.bind("<Destroy>",history)

###################### tab2 content py1120 configuration####################################

###################### read tables ####################################
v1 = StringVar()
v1.set("Y")
L1=Label(frame2,text="1. Read Table BRANCHid?").grid(row=1,column=0,sticky = W)
R11 = Radiobutton(frame2, text = "Y",value = "Y",variable=v1).grid(row=1, column=1)
R10 = Radiobutton(frame2, text = "N",value = "N",variable=v1).grid(row=1, column=2)

v2 = StringVar()
v2.set("Y")
L2=Label(frame2,text="2. Read Table SEGMENTdata?").grid(row=2,column=0,sticky = W)
R21 = Radiobutton(frame2, text = "Y",value = "Y",variable=v2).grid(row=2, column=1)
R20 = Radiobutton(frame2, text = "N",value = "N",variable=v2).grid(row=2, column=2)

v3 = StringVar()
v3.set("Y")
L3=Label(frame2,text="3. Read Table CONDUCTOR?").grid(row=3,column=0,sticky = W)
R31 = Radiobutton(frame2, text = "Y",value = "Y",variable=v3).grid(row=3, column=1)
R30 = Radiobutton(frame2, text = "N",value = "N",variable=v3).grid(row=3, column=2)


v4 = StringVar()
v4.set("Y")
L4=Label(frame2,text="4. Read Table STRUCTURE?").grid(row=4,column=0,sticky = W)
R41 = Radiobutton(frame2, text = "Y",value = "Y",variable=v4).grid(row=4, column=1)
R40 = Radiobutton(frame2, text = "N",value = "N",variable=v4).grid(row=4, column=2)

v5 = StringVar()
v5.set("Y")
L5=Label(frame2,text="5. Read Table SIXwire?").grid(row=5,column=0,sticky = W)
R51 = Radiobutton(frame2, text = "Y",value = "Y",variable=v5).grid(row=5, column=1)
R50 = Radiobutton(frame2, text = "N",value = "N",variable=v5).grid(row=5, column=2)

v6 = StringVar()
v6.set("Y")
L6=Label(frame2,text="6. Read Table TRANSFORMER?").grid(row=6,column=0,sticky = W)
R61 = Radiobutton(frame2, text = "Y",value = "Y",variable=v6).grid(row=6, column=1)
R60 = Radiobutton(frame2, text = "N",value = "N",variable=v6).grid(row=6, column=2)

v7 = StringVar()
v7.set("Y")
L7=Label(frame2,text="7. Read Table TRANSFORMERdata?").grid(row=7,column=0,sticky = W)
R71 = Radiobutton(frame2, text = "Y",value = "Y",variable=v7).grid(row=7, column=1)
R70 = Radiobutton(frame2, text = "N",value = "N",variable=v7).grid(row=7, column=2)

v8 = StringVar()
v8.set("Y")
L8=Label(frame2,text="8. Read Table TRANSFORMERtest?").grid(row=8,column=0,sticky = W)
R81 = Radiobutton(frame2, text = "Y",value = "Y",variable=v8).grid(row=8, column=1)
R80 = Radiobutton(frame2, text = "N",value = "N",variable=v8).grid(row=8, column=2)

v9 = StringVar()
v9.set("Y")
L9=Label(frame2,text="9. Read Table BREAKERdata?").grid(row=9,column=0,sticky = W)
R91 = Radiobutton(frame2, text = "Y",value = "Y",variable=v9).grid(row=9, column=1)
R90 = Radiobutton(frame2, text = "N",value = "N",variable=v9).grid(row=9, column=2)

v10 = StringVar()
v10.set("Y")
L10=Label(frame2,text="10. Read Table BREAKERconnection?").grid(row=10,column=0,sticky = W)
R101 = Radiobutton(frame2, text = "Y",value = "Y",variable=v10).grid(row=10, column=1)
R100 = Radiobutton(frame2, text = "N",value = "N",variable=v10).grid(row=10, column=2)

v11 = StringVar()
v11.set("Y")
L11=Label(frame2,text="11. Read Table SWITCHdata?").grid(row=11,column=0,sticky = W)
R111 = Radiobutton(frame2, text = "Y",value = "Y",variable=v11).grid(row=11, column=1)
R110 = Radiobutton(frame2, text = "N",value = "N",variable=v11).grid(row=11, column=2)

v12 = StringVar()
v12.set("Y")
L12=Label(frame2,text="12. Read Table SWITCHconnection?").grid(row=12,column=0,sticky = W)
R121 = Radiobutton(frame2, text = "Y",value = "Y",variable=v12).grid(row=12, column=1)
R120 = Radiobutton(frame2, text = "N",value = "N",variable=v12).grid(row=12, column=2)

v13 = StringVar()
v13.set("Y")
L13=Label(frame2,text="13. Read Table NONSECTdata?").grid(row=13,column=0,sticky = W)
R131 = Radiobutton(frame2, text = "Y",value = "Y",variable=v13).grid(row=13, column=1)
R130 = Radiobutton(frame2, text = "N",value = "N",variable=v13).grid(row=13, column=2)

v14 = StringVar()
v14.set("Y")
L14=Label(frame2,text="14. Read Table BUSlist?").grid(row=14,column=0,sticky = W)
R141 = Radiobutton(frame2, text = "Y",value = "Y",variable=v14).grid(row=14, column=1)
R140 = Radiobutton(frame2, text = "N",value = "N",variable=v14).grid(row=14, column=2)

v15 = StringVar()
v15.set("Y")
L15=Label(frame2,text="15. Read Table COMPOSITEdata?").grid(row=15,column=0,sticky = W)
R151 = Radiobutton(frame2, text = "Y",value = "Y",variable=v15).grid(row=15, column=1)
R150 = Radiobutton(frame2, text = "N",value = "N",variable=v15).grid(row=15, column=2)

v16 = StringVar()
v16.set("Y")
L16=Label(frame2,text="16. Read Table BUSTIEdata?").grid(row=16,column=0,sticky = W)
R161 = Radiobutton(frame2, text = "Y",value = "Y",variable=v16).grid(row=16, column=1)
R160 = Radiobutton(frame2, text = "N",value = "N",variable=v16).grid(row=16, column=2)

v17 = StringVar()
v17.set("Y")
L17=Label(frame2,text="17. Read Table DISTcircuit?").grid(row=17,column=0,sticky = W)
R171 = Radiobutton(frame2, text = "Y",value = "Y",variable=v17).grid(row=17, column=1)
R170 = Radiobutton(frame2, text = "N",value = "N",variable=v17).grid(row=17, column=2)

v18 = StringVar()
v18.set("Y")
L18=Label(frame2,text="18. Read Table DISTcapacitors?").grid(row=18,column=0,sticky = W)
R181 = Radiobutton(frame2, text = "Y",value = "Y",variable=v18).grid(row=18, column=1)
R180 = Radiobutton(frame2, text = "N",value = "N",variable=v18).grid(row=18, column=2)

v19 = StringVar()
v19.set("Y")
L19=Label(frame2,text="19. Read Table GENERATOR?").grid(row=19,column=0,sticky = W)
R191 = Radiobutton(frame2, text = "Y",value = "Y",variable=v19).grid(row=19, column=1)
R190 = Radiobutton(frame2, text = "N",value = "N",variable=v19).grid(row=19, column=2)

v20 = StringVar()
v20.set("Y")
L20=Label(frame2,text="20. Read Table BULKcapacitors?").grid(row=20,column=0,sticky = W)
R201 = Radiobutton(frame2, text = "Y",value = "Y",variable=v20).grid(row=20, column=1)
R200 = Radiobutton(frame2, text = "N",value = "N",variable=v20).grid(row=20, column=2)

v21 = StringVar()
v21.set("Y")
L21=Label(frame2,text="21. Read Table REACTOR?").grid(row=21,column=0,sticky = W)
R211 = Radiobutton(frame2, text = "Y",value = "Y",variable=v21).grid(row=21, column=1)
R210 = Radiobutton(frame2, text = "N",value = "N",variable=v21).grid(row=21, column=2)

v22 = StringVar()
v22.set("Y")
L22=Label(frame2,text="22. Read Table WDNAME?").grid(row=22,column=0,sticky = W)
R221 = Radiobutton(frame2, text = "Y",value = "Y",variable=v22).grid(row=22, column=1)
R220 = Radiobutton(frame2, text = "N",value = "N",variable=v22).grid(row=22, column=2)

v23 = StringVar()
v23.set("Y")
L23=Label(frame2,text="23. Read Table GROUPdata?").grid(row=23,column=0,sticky = W)
R231 = Radiobutton(frame2, text = "Y",value = "Y",variable=v23).grid(row=23, column=1)
R230 = Radiobutton(frame2, text = "N",value = "N",variable=v23).grid(row=23, column=2)

v24 = StringVar()
v24.set("Y")
L24=Label(frame2,text="24. Read Table AREAdata?").grid(row=24,column=0,sticky = W)
R241 = Radiobutton(frame2, text = "Y",value = "Y",variable=v24).grid(row=24, column=1)
R240 = Radiobutton(frame2, text = "N",value = "N",variable=v24).grid(row=24, column=2)

v25 = StringVar()
v25.set("Y")
L25=Label(frame2,text="25. Read Table GENERICequip?").grid(row=25,column=0,sticky = W)
R251 = Radiobutton(frame2, text = "Y",value = "Y",variable=v25).grid(row=25, column=1)
R250 = Radiobutton(frame2, text = "N",value = "N",variable=v25).grid(row=25, column=2)

v26 = StringVar()
v26.set("Y")
L26=Label(frame2,text="26. Read Table GENERICbus?").grid(row=26,column=0,sticky = W)
R261 = Radiobutton(frame2, text = "Y",value = "Y",variable=v26).grid(row=26, column=1)
R260 = Radiobutton(frame2, text = "N",value = "N",variable=v26).grid(row=26, column=2)

v27 = StringVar()
v27.set("Y")
L27=Label(frame2,text="27. Read Table GENERICgenerator?").grid(row=27,column=0,sticky = W)
R271 = Radiobutton(frame2, text = "Y",value = "Y",variable=v27).grid(row=27, column=1)
R270 = Radiobutton(frame2, text = "N",value = "N",variable=v27).grid(row=27, column=2)

v28 = StringVar()
v28.set("Y")
L28=Label(frame2,text="28. Read Table GENERICsegment?").grid(row=28,column=0,sticky = W)
R281 = Radiobutton(frame2, text = "Y",value = "Y",variable=v28).grid(row=28, column=1)
R280 = Radiobutton(frame2, text = "N",value = "N",variable=v28).grid(row=28, column=2)

v29 = StringVar()
v29.set("Y")
L29=Label(frame2,text="29. Read Table GENERICtransformer?").grid(row=29,column=0,sticky = W)
R291 = Radiobutton(frame2, text = "Y",value = "Y",variable=v29).grid(row=29, column=1)
R290 = Radiobutton(frame2, text = "N",value = "N",variable=v29).grid(row=29, column=2)

v30 = StringVar()
v30.set("Y")
L30=Label(frame2,text="30. Read Table STATION?").grid(row=30,column=0,sticky = W)
R301 = Radiobutton(frame2, text = "Y",value = "Y",variable=v30).grid(row=30, column=1)
R300 = Radiobutton(frame2, text = "N",value = "N",variable=v30).grid(row=30, column=2)

###################### read tables ####################################
# Bus Elimination Options: ------------------------------------------------------
v31 = StringVar()
v31.set("N")
LBUS1=Label(frame2,text="31. Delete Xfmr Terminal Buses with 'U' in Col 8 of Name?").grid(row=31,column=0,sticky = W)
RBUS11 = Radiobutton(frame2, text = "Y",value = "Y",variable=v31).grid(row=31, column=1)
RBUS10 = Radiobutton(frame2, text = "N",value = "N",variable=v31).grid(row=31, column=2)

v32 = StringVar()
v32.set("N")
LBUS2=Label(frame2,text="32. Delete Xfmr Terminal Buses with 'L' in Col 8 of Name?").grid(row=32,column=0,sticky = W)
RBUS21 = Radiobutton(frame2, text = "Y",value = "Y",variable=v32).grid(row=32, column=1)
RBUS20 = Radiobutton(frame2, text = "N",value = "N",variable=v32).grid(row=32, column=2)
# Low Impedance Line Tap Branch Elimination Options: ----------------------------
v33 = DoubleVar()
v33.set(0.0)
E_LI= Entry(frame2,textvariable=v33,width=7)
E_LI.grid(row=33, column = 2, sticky = W)
E_LI.insert(0,0)
L33=Label(frame2,text="33. Low Impedance Cutoff (PU) (Zero - Delete No Lines)").grid(row=33,column=0,columnspan = 2,sticky = W)

v34 = StringVar()
v34.set("N")
LEqu1=Label(frame2,text="34. Allow Fast & Slow Sectionalizing Equip to be Deleted?").grid(row=34,column=0,sticky = W)
REqu11 = Radiobutton(frame2, text = "Y",value = "Y",variable=v34).grid(row=34, column=1)
REqu10 = Radiobutton(frame2, text = "N",value = "N",variable=v34).grid(row=34, column=2)

v35 = tkinter.StringVar()
v35.set("N")
LEqu2=tkinter.Label(frame2,text="35. Allow Double Circuit Branch Segments to be Deleted?").grid(row=35,column=0,sticky = W)
REqu21 = tkinter.Radiobutton(frame2, text = "Y",value = "Y",variable=v35).grid(row=35, column=1)
REqu20 = tkinter.Radiobutton(frame2, text = "N",value = "N",variable=v35).grid(row=35, column=2)


##########
root.mainloop()  


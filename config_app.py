from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
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

v35 = StringVar()
v35.set("N")
LEqu2=Label(frame2,text="35. Allow Double Circuit Branch Segments to be Deleted?").grid(row=35,column=0,sticky = W)
REqu21 = Radiobutton(frame2, text = "Y",value = "Y",variable=v35).grid(row=35, column=1)
REqu20 = Radiobutton(frame2, text = "N",value = "N",variable=v35).grid(row=35, column=2)

# Area and Zone Reset Option: ---------------------------------------------------
v36 = StringVar()
v36.set("N")
L36=Label(frame2,text="36. Reset Area 23 Zone 64 to Area 1 Zone 2?").grid(row=36,column=0,sticky = W)
R361 = Radiobutton(frame2, text = "Y",value = "Y",variable=v36).grid(row=36, column=1)
R362 = Radiobutton(frame2, text = "N",value = "N",variable=v36).grid(row=36, column=2)
# Input Data Check Option: ------------------------------------------------------
v37 = StringVar()
v37.set("Y")
L37=Label(frame2,text="37. Check for the Following?").grid(row=37,column=0,sticky = W)
R371 = Radiobutton(frame2, text = "Y",value = "Y",variable=v37).grid(row=37, column=1)
R372 = Radiobutton(frame2, text = "N",value = "N",variable=v37).grid(row=37, column=2)
L371=Label(frame2,text="Inconsistent Short Circuit Capability").grid(row=38,column=0,sticky = W)
L372=Label(frame2,text="Zero Breaker Short Circuit Capability").grid(row=39,column=0,sticky = W)
L373=Label(frame2,text="Missing Equipment Amp Ratings").grid(row=40,column=0,sticky = W)
L374=Label(frame2,text="Zero MW bus loads").grid(row=41,column=0,sticky = W)
L374=Label(frame2,text="Inconsistent Operating Capability").grid(row=42,column=0,sticky = W)
##########
# Generator Probability Data Option: --------------------------------------------
v38 = StringVar()
v38.set("F")
L38=Label(frame2,text="38. Generator Probability Type (F-Forced, T-Total)").grid(row=43,column=0,sticky = W)
R381 = Radiobutton(frame2, text = "F",value = "F",variable=v38).grid(row=43, column=1)
R382 = Radiobutton(frame2, text = "T",value = "T",variable=v38).grid(row=43, column=2)
# Generator Maximum MW Output Option: ------------------------------------------
v39 = StringVar()
v39.set("S")
L39=Label(frame2,text="39. Generator Maximum MW Output Type (S-Summer, W-Winter)").grid(row=44,column=0,sticky = W)
R391 = Radiobutton(frame2, text = "S",value = "S",variable=v39).grid(row=44, column=1)
R392 = Radiobutton(frame2, text = "W",value = "W",variable=v39).grid(row=44, column=2)
# 3-Winder Xfmr Conversion Option: ----------------------------------------------
v40 = StringVar()
v40.set("N")
L40=Label(frame2,text="40. Replace 3-Winder Xfmrs with 2-Winder Xfmrs? (Y/N)").grid(row=45,column=0,sticky = W)
R401 = Radiobutton(frame2, text = "Y",value = "Y",variable=v40).grid(row=45, column=1)
R402 = Radiobutton(frame2, text = "N",value = "N",variable=v40).grid(row=45, column=2)
# Distribution Capacitor Output Options: ----------------------------------------
v41 = StringVar()
v41.set("Y")
L41=Label(frame2,text="41. Output Unswitched Caps? (Y/N)").grid(row=46,column=0,sticky = W)
R411 = Radiobutton(frame2, text = "Y",value = "Y",variable=v41).grid(row=46, column=1)
R412 = Radiobutton(frame2, text = "N",value = "N",variable=v41).grid(row=46, column=2)

v42 = StringVar()
v42.set("Y")
L42=Label(frame2,text="42. Output KRY Calendar Electronic Time Clock Caps? (Y/N)").grid(row=47,column=0,sticky = W)
R421 = Radiobutton(frame2, text = "Y",value = "Y",variable=v42).grid(row=47, column=1)
R422 = Radiobutton(frame2, text = "N",value = "N",variable=v42).grid(row=47, column=2)

v43 = StringVar()
v43.set("Y")
L43=Label(frame2,text="43. Output NTH Calendar Electronic Time Clock Caps? (Y/N)").grid(row=48,column=0,sticky = W)
R431 = Radiobutton(frame2, text = "Y",value = "Y",variable=v43).grid(row=48, column=1)
R432 = Radiobutton(frame2, text = "N",value = "N",variable=v43).grid(row=48, column=2)

v44 = StringVar()
v44.set("Y")
L44=Label(frame2,text="44. Output SMR Calendar Electronic Time Clock Caps? (Y/N)").grid(row=49,column=0,sticky = W)
R441 = Radiobutton(frame2, text = "Y",value = "Y",variable=v44).grid(row=49, column=1)
R442 = Radiobutton(frame2, text = "N",value = "N",variable=v44).grid(row=49, column=2)

v45 = StringVar()
v45.set("Y")
L45=Label(frame2,text="45. Output STD Calendar Electronic Time Clock Caps? (Y/N)").grid(row=50,column=0,sticky = W)
R451 = Radiobutton(frame2, text = "Y",value = "Y",variable=v45).grid(row=50, column=1)
R452 = Radiobutton(frame2, text = "N",value = "N",variable=v45).grid(row=50, column=2)

v46 = StringVar()
v46.set("Y")
L46=Label(frame2,text="46. Output ERR Calendar Electronic Time Clock Caps? (Y/N)").grid(row=51,column=0,sticky = W)
R461 = Radiobutton(frame2, text = "Y",value = "Y",variable=v46).grid(row=51, column=1)
R462 = Radiobutton(frame2, text = "N",value = "N",variable=v46).grid(row=51, column=2)

v47 = StringVar()
v47.set("Y")
L47=Label(frame2,text="47. Output Voltage Controlled Caps? (Y/N)").grid(row=52,column=0,sticky = W)
R471 = Radiobutton(frame2, text = "Y",value = "Y",variable=v47).grid(row=52, column=1)
R472 = Radiobutton(frame2, text = "N",value = "N",variable=v47).grid(row=52, column=2)

v48 = StringVar()
v48.set("Y")
L48=Label(frame2,text="48. Output In-Service and Repaired In-Service Caps? (Y/N)").grid(row=53,column=0,sticky = W)
R481 = Radiobutton(frame2, text = "Y",value = "Y",variable=v48).grid(row=53, column=1)
R482 = Radiobutton(frame2, text = "N",value = "N",variable=v48).grid(row=53, column=2)

v49 = StringVar()
v49.set("Y")
L49=Label(frame2,text="49. Output Intentional Out-of-Service Caps? (Y/N)").grid(row=54,column=0,sticky = W)
R491 = Radiobutton(frame2, text = "Y",value = "Y",variable=v49).grid(row=54, column=1)
R492 = Radiobutton(frame2, text = "N",value = "N",variable=v49).grid(row=54, column=2)

v50 = StringVar()
v50.set("Y")
L50=Label(frame2,text="50. Output Problem     Out-of-Service Caps? (Y/N)").grid(row=55,column=0,sticky = W)
R501 = Radiobutton(frame2, text = "Y",value = "Y",variable=v50).grid(row=55, column=1)
R502 = Radiobutton(frame2, text = "N",value = "N",variable=v50).grid(row=55, column=2)

# create a subframe of frame2 to host checkboxes: ----------------------------------------
frame2.rowconfigure(56, weight=100)

L_cb=Label(frame2,text="----------------------------Radio Control Tone Group Output? (Y/N)----------------------------------------").grid(row=56,column=0,columnspan = 3,sticky = W)
subFrame = Frame(frame2,width=580, height=200, borderwidth=2)
subFrame.grid(row=57,column=0,rowspan=20,columnspan = 3,sticky = W)
subFrame.columnconfigure(0,weight=0)
subFrame.columnconfigure((1, 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20), weight=0,pad=0)
XMT=Label(subFrame,text="XMT     01     02     03     04     05     06     07     08     09     10     11     12     13     14     15     16     17     18     19    20").grid(row=0,column=0, columnspan = 21,sticky = W) 

var1_1,var1_2,var1_3,var1_4,var1_5,var1_6,var1_7,var1_8,var1_9,var1_10,var1_11,var1_12,var1_13,var1_14,var1_15,var1_16,var1_17,var1_18,var1_19,var1_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

var2_1,var2_2,var2_3,var2_4,var2_5,var2_6,var2_7,var2_8,var2_9,var2_10,var2_11,var2_12,var2_13,var2_14,var2_15,var2_16,var2_17,var2_18,var2_19,var2_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

var3_1,var3_2,var3_3,var3_4,var3_5,var3_6,var3_7,var3_8,var3_9,var3_10,var3_11,var3_12,var3_13,var3_14,var3_15,var3_16,var3_17,var3_18,var3_19,var3_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

var4_1,var4_2,var4_3,var4_4,var4_5,var4_6,var4_7,var4_8,var4_9,var4_10,var4_11,var4_12,var4_13,var4_14,var4_15,var4_16,var4_17,var4_18,var4_19,var4_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

var5_1,var5_2,var5_3,var5_4,var5_5,var5_6,var5_7,var5_8,var5_9,var5_10,var5_11,var5_12,var5_13,var5_14,var5_15,var5_16,var5_17,var5_18,var5_19,var5_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

var6_1,var6_2,var6_3,var6_4,var6_5,var6_6,var6_7,var6_8,var6_9,var6_10,var6_11,var6_12,var6_13,var6_14,var6_15,var6_16,var6_17,var6_18,var6_19,var6_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

var7_1,var7_2,var7_3,var7_4,var7_5,var7_6,var7_7,var7_8,var7_9,var7_10,var7_11,var7_12,var7_13,var7_14,var7_15,var7_16,var7_17,var7_18,var7_19,var7_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

var8_1,var8_2,var8_3,var8_4,var8_5,var8_6,var8_7,var8_8,var8_9,var8_10,var8_11,var8_12,var8_13,var8_14,var8_15,var8_16,var8_17,var8_18,var8_19,var8_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

var9_1,var9_2,var9_3,var9_4,var9_5,var9_6,var9_7,var9_8,var9_9,var9_10,var9_11,var9_12,var9_13,var9_14,var9_15,var9_16,var9_17,var9_18,var9_19,var9_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

var10_1,var10_2,var10_3,var10_4,var10_5,var10_6,var10_7,var10_8,var10_9,var10_10,var10_11,var10_12,var10_13,var10_14,var10_15,var10_16,var10_17,var10_18,var10_19,var10_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

var11_1,var11_2,var11_3,var11_4,var11_5,var11_6,var11_7,var11_8,var11_9,var11_10,var11_11,var11_12,var11_13,var11_14,var11_15,var11_16,var11_17,var11_18,var11_19,var11_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

var12_1,var12_2,var12_3,var12_4,var12_5,var12_6,var12_7,var12_8,var12_9,var12_10,var12_11,var12_12,var12_13,var12_14,var12_15,var12_16,var12_17,var12_18,var12_19,var12_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

var13_1,var13_2,var13_3,var13_4,var13_5,var13_6,var13_7,var13_8,var13_9,var13_10,var13_11,var13_12,var13_13,var13_14,var13_15,var13_16,var13_17,var13_18,var13_19,var13_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

var14_1,var14_2,var14_3,var14_4,var14_5,var14_6,var14_7,var14_8,var14_9,var14_10,var14_11,var14_12,var14_13,var14_14,var14_15,var14_16,var14_17,var14_18,var14_19,var14_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

area=["ADR -","ALG -","BCK -","FEN -","FLI -","GRA -","ION -","JAC -","KAL -","LAN -","MUS -","OWS -","SAG -","UNK -"]
virt_im=PhotoImage(width=1, height=1)
for q in range(14):
    Label(subFrame,text=area[q]).grid(row=q+1,column=0,sticky = W)

    

v_list=[[var1_1,var1_2,var1_3,var1_4,var1_5,var1_6,var1_7,var1_8,var1_9,var1_10,var1_11,var1_12,var1_13,var1_14,var1_15,var1_16,var1_17,var1_18,var1_19,var1_20],[var2_1,var2_2,var2_3,var2_4,var2_5,var2_6,var2_7,var2_8,var2_9,var2_10,var2_11,var2_12,var2_13,var2_14,var2_15,var2_16,var2_17,var2_18,var2_19,var2_20],[var3_1,var3_2,var3_3,var3_4,var3_5,var3_6,var3_7,var3_8,var3_9,var3_10,var3_11,var3_12,var3_13,var3_14,var3_15,var3_16,var3_17,var3_18,var3_19,var3_20],[var4_1,var4_2,var4_3,var4_4,var4_5,var4_6,var4_7,var4_8,var4_9,var4_10,var4_11,var4_12,var4_13,var4_14,var4_15,var4_16,var4_17,var4_18,var4_19,var4_20],[var5_1,var5_2,var5_3,var5_4,var5_5,var5_6,var5_7,var5_8,var5_9,var5_10,var5_11,var5_12,var5_13,var5_14,var5_15,var5_16,var5_17,var5_18,var5_19,var5_20],[var6_1,var6_2,var6_3,var6_4,var6_5,var6_6,var6_7,var6_8,var6_9,var6_10,var6_11,var6_12,var6_13,var6_14,var6_15,var6_16,var6_17,var6_18,var6_19,var6_20],[var7_1,var7_2,var7_3,var7_4,var7_5,var7_6,var7_7,var7_8,var7_9,var7_10,var7_11,var7_12,var7_13,var7_14,var7_15,var7_16,var7_17,var7_18,var7_19,var7_20],[var8_1,var8_2,var8_3,var8_4,var8_5,var8_6,var8_7,var8_8,var8_9,var8_10,var8_11,var8_12,var8_13,var8_14,var8_15,var8_16,var8_17,var8_18,var8_19,var8_20],[var9_1,var9_2,var9_3,var9_4,var9_5,var9_6,var9_7,var9_8,var9_9,var9_10,var9_11,var9_12,var9_13,var9_14,var9_15,var9_16,var9_17,var9_18,var9_19,var9_20],[var10_1,var10_2,var10_3,var10_4,var10_5,var10_6,var10_7,var10_8,var10_9,var10_10,var10_11,var10_12,var10_13,var10_14,var10_15,var10_16,var10_17,var10_18,var10_19,var10_20],[var11_1,var11_2,var11_3,var11_4,var11_5,var11_6,var11_7,var11_8,var11_9,var11_10,var11_11,var11_12,var11_13,var11_14,var11_15,var11_16,var11_17,var11_18,var11_19,var11_20],[var12_1,var12_2,var12_3,var12_4,var12_5,var12_6,var12_7,var12_8,var12_9,var12_10,var12_11,var12_12,var12_13,var12_14,var12_15,var12_16,var12_17,var12_18,var12_19,var12_20],[var13_1,var13_2,var13_3,var13_4,var13_5,var13_6,var13_7,var13_8,var13_9,var13_10,var13_11,var13_12,var13_13,var13_14,var13_15,var13_16,var13_17,var13_18,var13_19,var13_20],[var14_1,var14_2,var14_3,var14_4,var14_5,var14_6,var14_7,var14_8,var14_9,var14_10,var14_11,var14_12,var14_13,var14_14,var14_15,var14_16,var14_17,var14_18,var14_19,var14_20]]



for i in range(14):
    for j in range(20):
        Checkbutton(subFrame, image=virt_im, variable=v_list[i][j],onvalue = 1,offvalue = 0,width=1,height=1).grid(row=i+1,column=j+1,sticky=W)
   

L_pg=Label(subFrame,text="----------------------------Pager Control Tone Group Output? (Y/N)----------------------------------------").grid(row=15,column=0,columnspan = 21,sticky = W)

pg_n=Label(subFrame,text="XMT     01     02     03     04     05     06     07     08     09     10     11     12     13     14     15     16     17     18     19    20").grid(row=16,column=0, columnspan = 21,sticky = W)
 
var15_1,var15_2,var15_3,var15_4,var15_5,var15_6,var15_7,var15_8,var15_9,var15_10,var15_11,var15_12,var15_13,var15_14,var15_15,var15_16,var15_17,var15_18,var15_19,var15_20=IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 1),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0),IntVar(subFrame,value = 0)

v_list2=[var15_1,var15_2,var15_3,var15_4,var15_5,var15_6,var15_7,var15_8,var15_9,var15_10,var15_11,var15_12,var15_13,var15_14,var15_15,var15_16,var15_17,var15_18,var15_19,var15_20]

for v in range(20):
    Checkbutton(subFrame, image=virt_im, variable=v_list2[v],onvalue = 1,offvalue = 0,width=1,height=1).grid(row=17,column=v+1,sticky=W)

# go back to frame2 : ----------------------------------------
v51 = StringVar(frame2,value = '9999  9999')
E_v51= Entry(frame2,textvariable=v51,width=10)
E_v51.grid(row=77, column = 2, sticky = W)
L51=Label(frame2,text="51. Flow Control Pager Line SS#, Last Sequence # On)").grid(row=77,column=0,columnspan = 2,sticky = W)

L51a=Label(frame2,text="(For All Flow Controlled Pagers Enter '9999  9999') 2 spaces").grid(row=78,column=0,columnspan = 3,sticky = W)
L51b=Label(frame2,text="(When Entering Individual SS#, Last Entry is '   0     0')3&5 spaces").grid(row=79,column=0,columnspan = 3,sticky = W)

v52 = DoubleVar(frame2,value = 0.980)
E_v52= Entry(frame2,textvariable=v52,width=10)
E_v52.grid(row=80, column = 2, sticky = W)
L52=Label(frame2,text="52. Capacitance Multiplier").grid(row=80,column=0,columnspan = 2,sticky = W)

# Bus and Bulk Power Capacitor Output Options: ----------------------------------
v53 = IntVar(frame2,value = 1330)
E_v53= Entry(frame2,textvariable=v53,width=10)
E_v53.grid(row=81, column = 2, sticky = W)
L53=Label(frame2,text="53. Time (hhmm)").grid(row=81,column=0,columnspan = 2,sticky = W)

v54 = IntVar(frame2,value = 0)
E_v54= Entry(frame2,textvariable=v54,width=10)
E_v54.grid(row=82, column = 2, sticky = W)
L54=Label(frame2,text="54. Day Code (0-Weekday, 1-Saturday, 2-Sunday, 3-Holiday)").grid(row=82,column=0,columnspan = 2,sticky = W)

v55 = IntVar(frame2,value = 2)
L55=Label(frame2,text="55. Initial Capacitance Option").grid(row=83,column=0,columnspan = 2,sticky = W)
R55a = Radiobutton(frame2, text = "0 - Zero                 ",value = 0,variable=v55).grid(row=84,column=0,columnspan = 3,sticky = W)
R55b = Radiobutton(frame2, text = "1 - Total Installed Value",value = 1,variable=v55).grid(row=85,column=0,columnspan = 3,sticky = W)
R55c = Radiobutton(frame2, text = "2 - Total On Value       ",value = 2,variable=v55).grid(row=86,column=0,columnspan = 3,sticky = W)


v56 = IntVar(frame2,value = 1)
L56=Label(frame2,text="56. Voltage On Limit Option").grid(row=87,column=0,columnspan = 2,sticky = W)
R56a = Radiobutton(frame2, text = "1 - Use Minimum On Voltage Limit for Switching On",value = 1,variable=v56).grid(row=88,column=0,columnspan = 3,sticky = W)
R56b = Radiobutton(frame2, text = "2 - Use Maximum On Voltage Limit for Switching On",value = 2,variable=v56).grid(row=89,column=0,columnspan = 3,sticky = W)
R56c = Radiobutton(frame2, text = "3 - Use Average On Voltage Limit for Switching On",value = 3,variable=v56).grid(row=90,column=0,columnspan = 3,sticky = W)


v57 = IntVar(frame2,value = 2)
L57=Label(frame2,text="57. Voltage Off Limit Option").grid(row=91,column=0,columnspan = 2,sticky = W)
R57a = Radiobutton(frame2, text = "1 - Use Minimum Off Voltage Limit for Switching Off",value = 1,variable=v57).grid(row=92,column=0,columnspan = 3,sticky = W)
R57b = Radiobutton(frame2, text = "2 - Use Maximum Off Voltage Limit for Switching Off",value = 2,variable=v57).grid(row=93,column=0,columnspan = 3,sticky = W)
R57c = Radiobutton(frame2, text = "3 - Use Average Off Voltage Limit for Switching Off",value = 3,variable=v57).grid(row=94,column=0,columnspan = 3,sticky = W)


v58 = DoubleVar(frame2,value = 1.000)
E_v58= Entry(frame2,textvariable=v58,width=10)
E_v58.grid(row=95, column = 2, sticky = W)
L58=Label(frame2,text="58. Capacitance Multiplier").grid(row=95,column=0,columnspan = 2,sticky = W)

# Transmission Rating Options: --------------------------------------------------
subFrame2 = Frame(frame2,width=580, height=100, borderwidth=2)
subFrame2.grid(row=96,column=0,rowspan=19,columnspan = 3,sticky = W)
subFrame2.columnconfigure(0,weight=0)
subFrame2.columnconfigure((1,2,3,4,5,6), weight=0,pad=0)
XM_L1=Label(subFrame2,text="Transmission Rating Options: ---------------------------------------------------------------------------------------").grid(row=0,column=0, columnspan = 6,sticky = W) 

v59=StringVar()
v59.set('S')
L_59=Label(subFrame2,text="59. Output Rating Type (Summer,Winter)").grid(row=1,column=0, sticky = W) 
R59a = Radiobutton(subFrame2, text = "S",value = 'S',variable=v59).grid(row=1,column=1,sticky = W)
R59b = Radiobutton(subFrame2, text = "W",value = 'W',variable=v59).grid(row=1,column=2,sticky = W)

XM_0=Label(subFrame2,text=" ").grid(row=2,column=0,sticky = W) 
XM_y=Label(subFrame2,text="Y").grid(row=2,column=1,sticky = W) 
XM_z=Label(subFrame2,text="Z").grid(row=2,column=2,sticky = W) 
XM_n=Label(subFrame2,text="N").grid(row=2,column=3,sticky = W) 
XM_a=Label(subFrame2,text="A").grid(row=2,column=4,sticky = W) 
XM_b=Label(subFrame2,text="B").grid(row=2,column=5,sticky = W) 


v60=StringVar()
v60.set('Z')
L_60=Label(subFrame2,text="60. Check Conductor?                             ").grid(row=3,column=0, sticky = W) 
R60y = Radiobutton(subFrame2, value = 'Y', variable=v60).grid(row=3,column=1,sticky = W)
R60z = Radiobutton(subFrame2, value = 'Z', variable=v60).grid(row=3,column=2,sticky = W)
R60n = Radiobutton(subFrame2, value = 'N', variable=v60).grid(row=3,column=3,sticky = W)

v61=StringVar()
v61.set('Z')
L_61=Label(subFrame2,text="61. Check Transformer?                           ").grid(row=4,column=0, sticky = W) 
R61y = Radiobutton(subFrame2, value = 'Y', variable=v61).grid(row=4,column=1,sticky = W)
R61z = Radiobutton(subFrame2, value = 'Z', variable=v61).grid(row=4,column=2,sticky = W)
R61n = Radiobutton(subFrame2, value = 'N', variable=v61).grid(row=4,column=3,sticky = W)

v62=StringVar()
v62.set('Z')
L_62=Label(subFrame2,text="62. Check Breaker?                               ").grid(row=5,column=0, sticky = W) 
R62y = Radiobutton(subFrame2, value = 'Y', variable=v62).grid(row=5,column=1,sticky = W)
R62z = Radiobutton(subFrame2, value = 'Z', variable=v62).grid(row=5,column=2,sticky = W)
R62n = Radiobutton(subFrame2, value = 'N', variable=v62).grid(row=5,column=3,sticky = W)
R62a = Radiobutton(subFrame2, value = 'A', variable=v62).grid(row=5,column=4,sticky = W)
R62b = Radiobutton(subFrame2, value = 'B', variable=v62).grid(row=5,column=5,sticky = W)

v63=StringVar()
v63.set('Z')
L_63=Label(subFrame2,text="63. Check Disc   Switch?                         ").grid(row=6,column=0, sticky = W) 
R63y = Radiobutton(subFrame2, value = 'Y', variable=v63).grid(row=6,column=1,sticky = W)
R63z = Radiobutton(subFrame2, value = 'Z', variable=v63).grid(row=6,column=2,sticky = W)
R63n = Radiobutton(subFrame2, value = 'N', variable=v63).grid(row=6,column=3,sticky = W)
R63a = Radiobutton(subFrame2, value = 'A', variable=v63).grid(row=6,column=4,sticky = W)
R63b = Radiobutton(subFrame2, value = 'B', variable=v63).grid(row=6,column=5,sticky = W)

v64=StringVar()
v64.set('Z')
L_64=Label(subFrame2,text="64. Check Bypass Switch?                         ").grid(row=8,column=0, sticky = W) 
R64y = Radiobutton(subFrame2, value = 'Y', variable=v64).grid(row=8,column=1,sticky = W)
R64z = Radiobutton(subFrame2, value = 'Z', variable=v64).grid(row=8,column=2,sticky = W)
R64n = Radiobutton(subFrame2, value = 'N', variable=v64).grid(row=8,column=3,sticky = W)
R64a = Radiobutton(subFrame2, value = 'A', variable=v64).grid(row=8,column=4,sticky = W)
R64b = Radiobutton(subFrame2, value = 'B', variable=v64).grid(row=8,column=5,sticky = W)

v65=StringVar()
v65.set('Z')
L_65=Label(subFrame2,text="65. Check Dual   Switch?                         ").grid(row=9,column=0, sticky = W) 
R65y = Radiobutton(subFrame2, value = 'Y', variable=v65).grid(row=9,column=1,sticky = W)
R65z = Radiobutton(subFrame2, value = 'Z', variable=v65).grid(row=9,column=2,sticky = W)
R65n = Radiobutton(subFrame2, value = 'N', variable=v65).grid(row=9,column=3,sticky = W)
R65a = Radiobutton(subFrame2, value = 'A', variable=v65).grid(row=9,column=4,sticky = W)
R65b = Radiobutton(subFrame2, value = 'B', variable=v65).grid(row=9,column=5,sticky = W)

v66=StringVar()
v66.set('Z')
L_67=Label(subFrame2,text="66. Check Bus    Switch?                         ").grid(row=10,column=0, sticky = W) 
R67y = Radiobutton(subFrame2, value = 'Y', variable=v66).grid(row=10,column=1,sticky = W)
R67z = Radiobutton(subFrame2, value = 'Z', variable=v66).grid(row=10,column=2,sticky = W)
R67n = Radiobutton(subFrame2, value = 'N', variable=v66).grid(row=10,column=3,sticky = W)
R67a = Radiobutton(subFrame2, value = 'A', variable=v66).grid(row=10,column=4,sticky = W)
R67b = Radiobutton(subFrame2, value = 'B', variable=v66).grid(row=10,column=5,sticky = W)

v67=StringVar()
v67.set('Z')
L_68=Label(subFrame2,text="67. Check Line   Switch?                         ").grid(row=11,column=0, sticky = W) 
R68y = Radiobutton(subFrame2, value = 'Y', variable=v67).grid(row=11,column=1,sticky = W)
R68z = Radiobutton(subFrame2, value = 'Z', variable=v67).grid(row=11,column=2,sticky = W)
R68n = Radiobutton(subFrame2, value = 'N', variable=v67).grid(row=11,column=3,sticky = W)
R68a = Radiobutton(subFrame2, value = 'A', variable=v67).grid(row=11,column=4,sticky = W)
R68b = Radiobutton(subFrame2, value = 'B', variable=v67).grid(row=11,column=5,sticky = W)

v68=StringVar()
v68.set('B')
L_69=Label(subFrame2,text="68. Check Current Transformer?                   ").grid(row=12,column=0, sticky = W) 
R69y = Radiobutton(subFrame2, value = 'Y', variable=v68).grid(row=12,column=1,sticky = W)
R69z = Radiobutton(subFrame2, value = 'Z', variable=v68).grid(row=12,column=2,sticky = W)
R69n = Radiobutton(subFrame2, value = 'N', variable=v68).grid(row=12,column=3,sticky = W)
R69a = Radiobutton(subFrame2, value = 'A', variable=v68).grid(row=12,column=4,sticky = W)
R69b = Radiobutton(subFrame2, value = 'B', variable=v68).grid(row=12,column=5,sticky = W)

v69=StringVar()
v69.set('Z')
L_70=Label(subFrame2,text="69. Check Wavetrap?                              ").grid(row=13,column=0, sticky = W) 
R70y = Radiobutton(subFrame2, value = 'Y', variable=v69).grid(row=13,column=1,sticky = W)
R70z = Radiobutton(subFrame2, value = 'Z', variable=v69).grid(row=13,column=2,sticky = W)
R70n = Radiobutton(subFrame2, value = 'N', variable=v69).grid(row=13,column=3,sticky = W)
R70a = Radiobutton(subFrame2, value = 'A', variable=v69).grid(row=13,column=4,sticky = W)
R70b = Radiobutton(subFrame2, value = 'B', variable=v69).grid(row=13,column=5,sticky = W)

v70=StringVar()
v70.set('Z')
L_71=Label(subFrame2,text="70. Check Circuit Connector?                     ").grid(row=14,column=0, sticky = W) 
R71y = Radiobutton(subFrame2, value = 'Y', variable=v70).grid(row=14,column=1,sticky = W)
R71z = Radiobutton(subFrame2, value = 'Z', variable=v70).grid(row=14,column=2,sticky = W)
R71n = Radiobutton(subFrame2, value = 'N', variable=v70).grid(row=14,column=3,sticky = W)
R71a = Radiobutton(subFrame2, value = 'A', variable=v70).grid(row=14,column=4,sticky = W)
R71b = Radiobutton(subFrame2, value = 'B', variable=v70).grid(row=14,column=5,sticky = W)

v71=StringVar()
v71.set('Z')
L_72=Label(subFrame2,text="71. Check Buswork?                               ").grid(row=15,column=0, sticky = W) 
R72y = Radiobutton(subFrame2, value = 'Y', variable=v71).grid(row=15,column=1,sticky = W)
R72z = Radiobutton(subFrame2, value = 'Z', variable=v71).grid(row=15,column=2,sticky = W)
R72n = Radiobutton(subFrame2, value = 'N', variable=v71).grid(row=15,column=3,sticky = W)
R72a = Radiobutton(subFrame2, value = 'A', variable=v71).grid(row=15,column=4,sticky = W)
R72b = Radiobutton(subFrame2, value = 'B', variable=v71).grid(row=15,column=5,sticky = W)

v72=StringVar()
v72.set('Z')
L_73=Label(subFrame2,text="72. Check Sag Limit?                             ").grid(row=16,column=0, sticky = W) 
R73y = Radiobutton(subFrame2, value = 'Y', variable=v72).grid(row=16,column=1,sticky = W)
R73z = Radiobutton(subFrame2, value = 'Z', variable=v72).grid(row=16,column=2,sticky = W)
R73n = Radiobutton(subFrame2, value = 'N', variable=v72).grid(row=16,column=3,sticky = W)

v73=StringVar()
v73.set('Y')
L_74=Label(subFrame2,text="73. Check MISO Base Model Rating?                ").grid(row=17,column=0, sticky = W) 
R74y = Radiobutton(subFrame2, value = 'Y', variable=v73).grid(row=17,column=1,sticky = W)
R74z = Radiobutton(subFrame2, value = 'Z', variable=v73).grid(row=17,column=2,sticky = W)
R74n = Radiobutton(subFrame2, value = 'N', variable=v73).grid(row=17,column=3,sticky = W)

v74=StringVar()
v74.set('Z')
L_75=Label(subFrame2,text="74. Check Interconnection Limit?                 ").grid(row=18,column=0, sticky = W) 
R75y = Radiobutton(subFrame2, value = 'Y', variable=v74).grid(row=18,column=1,sticky = W)
R75z = Radiobutton(subFrame2, value = 'Z', variable=v74).grid(row=18,column=2,sticky = W)
R75n = Radiobutton(subFrame2, value = 'N', variable=v74).grid(row=18,column=3,sticky = W)

#----------subFrame2 ends------------------------
L_75y=Label(subFrame2,text="Y - Yes, Use Rating Data                                       ").grid(row=115,column=0, columnspan=3,sticky = W) 
L_75z=Label(subFrame2,text="Z - Yes, Use Rating Data, Don't Use to Calculate Minimum       ").grid(row=116,column=0, columnspan=3,sticky = W) 
L_75a=Label(subFrame2,text="A - Yes, Use Nameplate Amp Data                                ").grid(row=117,column=0, columnspan=3,sticky = W) 
L_75b=Label(subFrame2,text="B - Yes, Use Nameplate Amp Data, Don't Use to Calculate Minimum").grid(row=118,column=0, columnspan=3,sticky = W) 
L_75n=Label(subFrame2,text="N - No                                                         ").grid(row=119,column=0, columnspan=3,sticky = W) 

# subFrame3 --------------------------------------------------
subFrame3 = Frame(frame2,width=580, height=30, borderwidth=2)
subFrame3.grid(row=120,column=0,rowspan=3,columnspan = 3,sticky = W)
subFrame3.columnconfigure(0,weight=0)
subFrame3.columnconfigure((0,1,2,3,4,5), weight=0,pad=0)

ct_L1=Label(subFrame3,text=" ").grid(row=0,column=0,sticky = W) 
ct_L2=Label(subFrame3,text="N").grid(row=0,column=1,sticky = W)
ct_L2=Label(subFrame3,text="P").grid(row=0,column=2,sticky = W)
ct_L2=Label(subFrame3,text="R").grid(row=0,column=3,sticky = W)
ct_L2=Label(subFrame3,text="O").grid(row=0,column=4,sticky = W)
ct_L2=Label(subFrame3,text="Q").grid(row=0,column=5,sticky = W)

v75=StringVar()
v75.set('Q')
L_76=Label(subFrame3,text="75. Check Time Over Current Relay Loadability Limit?").grid(row=1,column=0, sticky = W) 
R76n = Radiobutton(subFrame3, value = 'N', variable=v75).grid(row=1,column=1,sticky = W)
R76p = Radiobutton(subFrame3, value = 'P', variable=v75).grid(row=1,column=2,sticky = W)
R76r = Radiobutton(subFrame3, value = 'R', variable=v75).grid(row=1,column=3,sticky = W)
R76o = Radiobutton(subFrame3, value = 'O', variable=v75).grid(row=1,column=4,sticky = W)
R76q = Radiobutton(subFrame3, value = 'Q', variable=v75).grid(row=1,column=5,sticky = W)

v76=StringVar()
v76.set('R')
L_77=Label(subFrame3,text="76.Check Impedance Relay Loadability Limit?         ").grid(row=2,column=0, sticky = W) 
R77n = Radiobutton(subFrame3, value = 'N', variable=v76).grid(row=2,column=1,sticky = W)
R77p = Radiobutton(subFrame3, value = 'P', variable=v76).grid(row=2,column=2,sticky = W)
R77r = Radiobutton(subFrame3, value = 'R', variable=v76).grid(row=2,column=3,sticky = W)
R77o = Radiobutton(subFrame3, value = 'O', variable=v76).grid(row=2,column=4,sticky = W)
R77q = Radiobutton(subFrame3, value = 'Q', variable=v76).grid(row=2,column=5,sticky = W)

# subFrame3 end --------------------------------------------------
L_77n=Label(frame2,text="N - Don't Check                       ").grid(row=123,column=0, columnspan=3,sticky = W) 
L_77p=Label(frame2,text="P - Check Using Rating Multiplier of 1.0").grid(row=124,column=0, columnspan=3,sticky = W) 
L_77r=Label(frame2,text="R - Check Using Rating Multiplier of 1.0,").grid(row=125,column=0, columnspan=3,sticky = W) 
L_77rr=Label(frame2,text="      Don't Use to Calculate Minimum").grid(row=126,column=0, columnspan=3,sticky = W) 
L_77o=Label(frame2,text="O - Check Using Rating Multiplier of 1.2").grid(row=127,column=0, columnspan=3,sticky = W) 
L_77q=Label(frame2,text="Q - Check Using Rating Multiplier of 1.2,").grid(row=128,column=0, columnspan=3,sticky = W) 
L_77qq=Label(frame2,text="      Don't Use to Calculate Minimum").grid(row=129,column=0, columnspan=3,sticky = W) 

v77=StringVar()
v77.set(' ')
L_78=Label(frame2,text="77.Output Branch Mileage in Place of Rating?        ").grid(row=130,column=0, sticky = W) 
R78b = Radiobutton(frame2, text='Blank - Output Ratings                      ', value = ' ', variable=v77).grid(row=131,column=0,sticky = W)
R78n = Radiobutton(frame2, text='N - Output Mileage in Place of Normal Rating', value = 'N', variable=v77).grid(row=132,column=0,sticky = W)
R78l = Radiobutton(frame2, text='L - Output Mileage in Place of LTE    Rating', value = 'L', variable=v77).grid(row=133,column=0,sticky = W)
R78s = Radiobutton(frame2, text='S - Output Mileage in Place of STE    Rating', value = 'S', variable=v77).grid(row=134,column=0,sticky = W)

v78=StringVar()
v78.set('L')
L_79=Label(frame2,text="78.Overwrite Emergency Ratings?                     ").grid(row=135,column=0, sticky = W) 
R79n = Radiobutton(frame2, text='N - No Change (Rate B = LTE; Rate C = STE                   )', value = 'N', variable=v78).grid(row=136,column=0,sticky = W)
R79l = Radiobutton(frame2, text='L - Output LTE in Place of STE Rating (Rate B = Rate C = LTE)', value = 'L', variable=v78).grid(row=137,column=0,sticky = W)
R79s = Radiobutton(frame2, text='S - Output STE in Place of LTE Rating (Rate B = Rate C = STE)', value = 'S', variable=v78).grid(row=138,column=0,sticky = W)

v79=StringVar()
v79.set('Y')
L_80=Label(frame2,text="79.Psse branch rating file output code             ").grid(row=139,column=0, sticky = W) 
R80y = Radiobutton(frame2, text='Y - If none of the three ratings are set, output branch entry     ', value = 'Y', variable=v79).grid(row=140,column=0,sticky = W)
R80n = Radiobutton(frame2, text='N - If none of the three ratings are set, dont output branch entry', value = 'N', variable=v79).grid(row=141,column=0,sticky = W)

v80=StringVar()
v80.set('Y')
L_81=Label(frame2,text="80.Check Ring Bus Breakers?                     ").grid(row=142,column=0, sticky = W) 
R81y = Radiobutton(frame2, text='Y', value = 'Y', variable=v80).grid(row=142,column=1,sticky = W)
R81n = Radiobutton(frame2, text='N', value = 'N', variable=v80).grid(row=142,column=2,sticky = W)
 
v81=StringVar()
v81.set('Y')
L_82=Label(frame2,text="81.Check Ring Bus Disc   Switch?                ").grid(row=143,column=0, sticky = W) 
R82y = Radiobutton(frame2, text='Y', value = 'Y', variable=v81).grid(row=143,column=1,sticky = W)
R82n = Radiobutton(frame2, text='N', value = 'N', variable=v81).grid(row=143,column=2,sticky = W)
 
v82=StringVar()
v82.set('Y')
L_83=Label(frame2,text="82.Check Ring Bus Bypass Switch?                ").grid(row=144,column=0, sticky = W) 
R83y = Radiobutton(frame2, text='Y', value = 'Y', variable=v82).grid(row=144,column=1,sticky = W)
R83n = Radiobutton(frame2, text='N', value = 'N', variable=v82).grid(row=144,column=2,sticky = W)
 
v83=StringVar()
v83.set('Y')
L_84=Label(frame2,text="83.Check Ring Bus Dual   Switch?                ").grid(row=145,column=0, sticky = W) 
R84y = Radiobutton(frame2, text='Y', value = 'Y', variable=v83).grid(row=145,column=1,sticky = W)
R84n = Radiobutton(frame2, text='N', value = 'N', variable=v83).grid(row=145,column=2,sticky = W)

v84=StringVar()
v84.set('Y')
L_85=Label(frame2,text="84.Check Ring Bus Bus    Switch?                ").grid(row=146,column=0, sticky = W) 
R85y = Radiobutton(frame2, text='Y', value = 'Y', variable=v84).grid(row=146,column=1,sticky = W)
R85n = Radiobutton(frame2, text='N', value = 'N', variable=v84).grid(row=146,column=2,sticky = W)

v85=StringVar()
v85.set('Y')
L_86=Label(frame2,text="85.Check Ring Bus Line   Switch?                ").grid(row=147,column=0, sticky = W) 
R86y = Radiobutton(frame2, text='Y', value = 'Y', variable=v85).grid(row=147,column=1,sticky = W)
R86n = Radiobutton(frame2, text='N', value = 'N', variable=v85).grid(row=147,column=2,sticky = W)

v86=StringVar()
v86.set('Y')
L_87=Label(frame2,text="86.Check Ring Bus Current Transformers?         ").grid(row=148,column=0, sticky = W) 
R87y = Radiobutton(frame2, text='Y', value = 'Y', variable=v86).grid(row=148,column=1,sticky = W)
R87n = Radiobutton(frame2, text='N', value = 'N', variable=v86).grid(row=148,column=2,sticky = W)

v87=StringVar()
v87.set('Y')
L_88=Label(frame2,text="87.Check Ring Bus Wavetraps?                    ").grid(row=149,column=0, sticky = W) 
R88y = Radiobutton(frame2, text='Y', value = 'Y', variable=v87).grid(row=149,column=1,sticky = W)
R88n = Radiobutton(frame2, text='N', value = 'N', variable=v87).grid(row=149,column=2,sticky = W)
 
v88=StringVar()
v88.set('Y')
L_89=Label(frame2,text="88.Check Ring Bus Circuit Connectors?           ").grid(row=150,column=0, sticky = W) 
R89y = Radiobutton(frame2, text='Y', value = 'Y', variable=v88).grid(row=150,column=1,sticky = W)
R89n = Radiobutton(frame2, text='N', value = 'N', variable=v88).grid(row=150,column=2,sticky = W)
 
v89=StringVar()
v89.set('Y')
Label_90=Label(frame2,text="89.Check Ring Bus Buswork?                      ").grid(row=151,column=0, sticky = W) 
b90y = Radiobutton(frame2, text='Y', value = 'Y', variable=v89).grid(row=151,column=1,sticky = W)
b90n = Radiobutton(frame2, text='N', value = 'N', variable=v89).grid(row=151,column=2,sticky = W)
 
# High-Voltage Distribution Rating Options: -------------------------------------
# subFrame4-------------------------------------
subFrame4 = Frame(frame2,width=580, height=100, borderwidth=2)
subFrame4.grid(row=152,column=0,rowspan=19,columnspan = 3,sticky = W)
subFrame4.columnconfigure(0,weight=0)
subFrame4.columnconfigure((0,1,2,3,4,5), weight=0,pad=0)
Label(subFrame4,text="---------------------High-Voltage Distribution Rating Options: -------------------------------------").grid(row=0,column=0,columnspan = 6,sticky = W) 

v90=StringVar()
v90.set('S')
L_90=Label(subFrame4,text="90.Output Rating Type (Summer,Winter)").grid(row=1,column=0, sticky = W) 
R90y = Radiobutton(subFrame4, text='S', value = 'S', variable=v90).grid(row=1,column=1,sticky = W)
R90n = Radiobutton(subFrame4, text='W', value = 'W', variable=v90).grid(row=1,column=2,sticky = W)
 

Label(subFrame4,text=" ").grid(row=2,column=0,sticky = W) 
Label(subFrame4,text="Y").grid(row=2,column=1,sticky = W)
Label(subFrame4,text="Z").grid(row=2,column=2,sticky = W)
Label(subFrame4,text="N").grid(row=2,column=3,sticky = W)
Label(subFrame4,text="A").grid(row=2,column=4,sticky = W)
Label(subFrame4,text="B").grid(row=2,column=5,sticky = W)

v91=StringVar()
v91.set('Y')
L_91=Label(subFrame4,text="91.Check Conductor?  ").grid(row=3,column=0, sticky = W) 
R91y = Radiobutton(subFrame4, value = 'Y', variable=v91).grid(row=3,column=1,sticky = W)
R91n = Radiobutton(subFrame4, value = 'Z', variable=v91).grid(row=3,column=2,sticky = W)
R91z = Radiobutton(subFrame4, value = 'N', variable=v91).grid(row=3,column=3,sticky = W) 

v92=StringVar()
v92.set('Y')
L_92=Label(subFrame4,text="92.Check Transformer?  ").grid(row=4,column=0, sticky = W) 
R92y = Radiobutton(subFrame4, value = 'Y', variable=v92).grid(row=4,column=1,sticky = W)
R92n = Radiobutton(subFrame4, value = 'Z', variable=v92).grid(row=4,column=2,sticky = W)
R92z = Radiobutton(subFrame4, value = 'N', variable=v92).grid(row=4,column=3,sticky = W) 

v93=StringVar()
v93.set('Y')
L_93=Label(subFrame4,text="93.Check Breaker?      ").grid(row=5,column=0, sticky = W) 
R93y = Radiobutton(subFrame4, value = 'Y', variable=v93).grid(row=5,column=1,sticky = W)
R93n = Radiobutton(subFrame4, value = 'Z', variable=v93).grid(row=5,column=2,sticky = W)
R93z = Radiobutton(subFrame4, value = 'N', variable=v93).grid(row=5,column=3,sticky = W) 
R93a = Radiobutton(subFrame4, value = 'A', variable=v93).grid(row=5,column=4,sticky = W)
R93b = Radiobutton(subFrame4, value = 'B', variable=v93).grid(row=5,column=5,sticky = W) 
  
v94=StringVar()
v94.set('Y')
L_94=Label(subFrame4,text="94.Check Disc   Switch?").grid(row=6,column=0, sticky = W) 
R94y = Radiobutton(subFrame4, value = 'Y', variable=v94).grid(row=6,column=1,sticky = W)
R94n = Radiobutton(subFrame4, value = 'Z', variable=v94).grid(row=6,column=2,sticky = W)
R94z = Radiobutton(subFrame4, value = 'N', variable=v94).grid(row=6,column=3,sticky = W) 
R94a = Radiobutton(subFrame4, value = 'A', variable=v94).grid(row=6,column=4,sticky = W)
R94b = Radiobutton(subFrame4, value = 'B', variable=v94).grid(row=6,column=5,sticky = W) 

v95=StringVar()
v95.set('Y')
L_95=Label(subFrame4,text="95.Check Bypass Switch?").grid(row=7,column=0, sticky = W) 
R95y = Radiobutton(subFrame4, value = 'Y', variable=v95).grid(row=7,column=1,sticky = W)
R95n = Radiobutton(subFrame4, value = 'Z', variable=v95).grid(row=7,column=2,sticky = W)
R95z = Radiobutton(subFrame4, value = 'N', variable=v95).grid(row=7,column=3,sticky = W) 
R95a = Radiobutton(subFrame4, value = 'A', variable=v95).grid(row=7,column=4,sticky = W)
R95b = Radiobutton(subFrame4, value = 'B', variable=v95).grid(row=7,column=5,sticky = W) 
    
v96=StringVar()
v96.set('Y')
L_96=Label(subFrame4,text="96.Check Dual   Switch?").grid(row=8,column=0, sticky = W) 
R96y = Radiobutton(subFrame4, value = 'Y', variable=v96).grid(row=8,column=1,sticky = W)
R96n = Radiobutton(subFrame4, value = 'Z', variable=v96).grid(row=8,column=2,sticky = W)
R96z = Radiobutton(subFrame4, value = 'N', variable=v96).grid(row=8,column=3,sticky = W) 
R96a = Radiobutton(subFrame4, value = 'A', variable=v96).grid(row=8,column=4,sticky = W)
R96b = Radiobutton(subFrame4, value = 'B', variable=v96).grid(row=8,column=5,sticky = W) 
    
v97=StringVar()
v97.set('Y')
L_97=Label(subFrame4,text="97.Check Bus    Switch?").grid(row=9,column=0, sticky = W) 
R97y = Radiobutton(subFrame4, value = 'Y', variable=v97).grid(row=9,column=1,sticky = W)
R97n = Radiobutton(subFrame4, value = 'Z', variable=v97).grid(row=9,column=2,sticky = W)
R97z = Radiobutton(subFrame4, value = 'N', variable=v97).grid(row=9,column=3,sticky = W) 
R97a = Radiobutton(subFrame4, value = 'A', variable=v97).grid(row=9,column=4,sticky = W)
R97b = Radiobutton(subFrame4, value = 'B', variable=v97).grid(row=9,column=5,sticky = W) 
    
v98=StringVar()
v98.set('Y')
L_98=Label(subFrame4,text="98.Check Line   Switch?").grid(row=10,column=0, sticky = W) 
R98y = Radiobutton(subFrame4, value = 'Y', variable=v98).grid(row=10,column=1,sticky = W)
R98n = Radiobutton(subFrame4, value = 'Z', variable=v98).grid(row=10,column=2,sticky = W)
R98z = Radiobutton(subFrame4, value = 'N', variable=v98).grid(row=10,column=3,sticky = W) 
R98a = Radiobutton(subFrame4, value = 'A', variable=v98).grid(row=10,column=4,sticky = W)
R98b = Radiobutton(subFrame4, value = 'B', variable=v98).grid(row=10,column=5,sticky = W) 
    
v99=StringVar()
v99.set('A')
L_99=Label(subFrame4,text="99.Check Current Transformer?").grid(row=11,column=0, sticky = W) 
R99y = Radiobutton(subFrame4, value = 'Y', variable=v99).grid(row=11,column=1,sticky = W)
R99n = Radiobutton(subFrame4, value = 'Z', variable=v99).grid(row=11,column=2,sticky = W)
R99z = Radiobutton(subFrame4, value = 'N', variable=v99).grid(row=11,column=3,sticky = W) 
R99a = Radiobutton(subFrame4, value = 'A', variable=v99).grid(row=11,column=4,sticky = W)
R99b = Radiobutton(subFrame4, value = 'B', variable=v99).grid(row=11,column=5,sticky = W) 
    
v100=StringVar()
v100.set('Y')
L_100=Label(subFrame4,text="100.Check Wavetrap?").grid(row=12,column=0, sticky = W) 
R100y = Radiobutton(subFrame4, value = 'Y', variable=v100).grid(row=12,column=1,sticky = W)
R100n = Radiobutton(subFrame4, value = 'Z', variable=v100).grid(row=12,column=2,sticky = W)
R100z = Radiobutton(subFrame4, value = 'N', variable=v100).grid(row=12,column=3,sticky = W) 
R100a = Radiobutton(subFrame4, value = 'A', variable=v100).grid(row=12,column=4,sticky = W)
R100b = Radiobutton(subFrame4, value = 'B', variable=v100).grid(row=12,column=5,sticky = W) 
    
v101=StringVar()
v101.set('Y')
L_101=Label(subFrame4,text="101.Check Circuit Connector?").grid(row=13,column=0, sticky = W) 
R101y = Radiobutton(subFrame4, value = 'Y', variable=v101).grid(row=13,column=1,sticky = W)
R101n = Radiobutton(subFrame4, value = 'Z', variable=v101).grid(row=13,column=2,sticky = W)
R101z = Radiobutton(subFrame4, value = 'N', variable=v101).grid(row=13,column=3,sticky = W) 
R101a = Radiobutton(subFrame4, value = 'A', variable=v101).grid(row=13,column=4,sticky = W)
R101b = Radiobutton(subFrame4, value = 'B', variable=v101).grid(row=13,column=5,sticky = W) 
    
v102=StringVar()
v102.set('Y')
L_102=Label(subFrame4,text="102.Check Buswork?").grid(row=14,column=0, sticky = W) 
R102y = Radiobutton(subFrame4, value = 'Y', variable=v102).grid(row=14,column=1,sticky = W)
R102n = Radiobutton(subFrame4, value = 'Z', variable=v102).grid(row=14,column=2,sticky = W)
R102z = Radiobutton(subFrame4, value = 'N', variable=v102).grid(row=14,column=3,sticky = W) 
R102a = Radiobutton(subFrame4, value = 'A', variable=v102).grid(row=14,column=4,sticky = W)
R102b = Radiobutton(subFrame4, value = 'B', variable=v102).grid(row=14,column=5,sticky = W) 

v103=StringVar()
v103.set('Y')
L_103=Label(subFrame4,text="103.Check Sag Limit?").grid(row=15,column=0, sticky = W) 
R103y = Radiobutton(subFrame4, value = 'Y', variable=v103).grid(row=15,column=1,sticky = W)
R103n = Radiobutton(subFrame4, value = 'Z', variable=v103).grid(row=15,column=2,sticky = W)
R103z = Radiobutton(subFrame4, value = 'N', variable=v103).grid(row=15,column=3,sticky = W) 

v104=StringVar()
v104.set('Z')
L_104=Label(subFrame4,text="104.Check MISO Base Model Rating?").grid(row=16,column=0, sticky = W) 
R104y = Radiobutton(subFrame4, value = 'Y', variable=v104).grid(row=16,column=1,sticky = W)
R104n = Radiobutton(subFrame4, value = 'Z', variable=v104).grid(row=16,column=2,sticky = W)
R104z = Radiobutton(subFrame4, value = 'N', variable=v104).grid(row=16,column=3,sticky = W) 

v105=StringVar()
v105.set('Y')
L_105=Label(subFrame4,text="105.Check Interconnection Limit?").grid(row=17,column=0, sticky = W) 
R105y = Radiobutton(subFrame4, value = 'Y', variable=v105).grid(row=17,column=1,sticky = W)
R105n = Radiobutton(subFrame4, value = 'Z', variable=v105).grid(row=17,column=2,sticky = W)
R105z = Radiobutton(subFrame4, value = 'N', variable=v105).grid(row=17,column=3,sticky = W) 

# subFrame4 end-------------------------------------
L105y=Label(frame2,text="Y - Yes, Use Rating Data                                       ").grid(row=171,column=0, columnspan=3,sticky = W) 
L105z=Label(frame2,text="Z - Yes, Use Rating Data, Don't Use to Calculate Minimum       ").grid(row=172,column=0, columnspan=3,sticky = W) 
L105a=Label(frame2,text="A - Yes, Use Nameplate Amp Data                                ").grid(row=173,column=0, columnspan=3,sticky = W) 
L105b=Label(frame2,text="B - Yes, Use Nameplate Amp Data, Don't Use to Calculate Minimum").grid(row=174,column=0, columnspan=3,sticky = W) 
L105n=Label(frame2,text="N - No                                                         ").grid(row=175,column=0, columnspan=3,sticky = W) 

# subFrame5-------------------------------------
subFrame5 = Frame(frame2,width=580, height=50, borderwidth=2)
subFrame5.grid(row=176,column=0,rowspan=3,columnspan = 3,sticky = W)
subFrame5.columnconfigure(0,weight=0)
subFrame5.columnconfigure((0,1,2,3,4,5), weight=0,pad=0)

Label(subFrame5,text=" ").grid(row=0,column=0,sticky = W) 
Label(subFrame5,text="N").grid(row=0,column=1,sticky = W)
Label(subFrame5,text="P").grid(row=0,column=2,sticky = W)
Label(subFrame5,text="R").grid(row=0,column=3,sticky = W)
Label(subFrame5,text="O").grid(row=0,column=4,sticky = W)
Label(subFrame5,text="Q").grid(row=0,column=5,sticky = W)

v106=StringVar()
v106.set('O')
L_106=Label(subFrame5,text="106.Check Time Over Current Relay Loadability Limit? ").grid(row=1,column=0, sticky = W) 
R106y = Radiobutton(subFrame5, value = 'N', variable=v106).grid(row=1,column=1,sticky = W)
R106n = Radiobutton(subFrame5, value = 'P', variable=v106).grid(row=1,column=2,sticky = W)
R106z = Radiobutton(subFrame5, value = 'R', variable=v106).grid(row=1,column=3,sticky = W) 
R106n = Radiobutton(subFrame5, value = 'O', variable=v106).grid(row=1,column=4,sticky = W)
R106z = Radiobutton(subFrame5, value = 'Q', variable=v106).grid(row=1,column=5,sticky = W) 

v107=StringVar()
v107.set('P')
L_107=Label(subFrame5,text="107. Check Impedance Relay Loadability Limit? ").grid(row=2,column=0, sticky = W) 
R107y = Radiobutton(subFrame5, value = 'N', variable=v107).grid(row=2,column=1,sticky = W)
R107n = Radiobutton(subFrame5, value = 'P', variable=v107).grid(row=2,column=2,sticky = W)
R107z = Radiobutton(subFrame5, value = 'R', variable=v107).grid(row=2,column=3,sticky = W) 
R107n = Radiobutton(subFrame5, value = 'O', variable=v107).grid(row=2,column=4,sticky = W)
R107z = Radiobutton(subFrame5, value = 'Q', variable=v107).grid(row=2,column=5,sticky = W) 

# subFrame5 ends-------------------------------------

L_1071=Label(frame2,text="N - Don't Check                                       ").grid(row=180,column=0, columnspan=3,sticky = W) 
L_1072=Label(frame2,text="P - Check Using Rating Multiplier of 1.0              ").grid(row=181,column=0, columnspan=3,sticky = W) 
L_1073=Label(frame2,text="R - Check Using Rating Multiplier of 1.0,             ").grid(row=182,column=0, columnspan=3,sticky = W) 
L_1074=Label(frame2,text="      Don't Use to Calculate Minimum                  ").grid(row=183,column=0, columnspan=3,sticky = W) 
L_1075=Label(frame2,text="O - Check Using Rating Multiplier of 1.2              ").grid(row=184,column=0, columnspan=3,sticky = W) 
L_1076=Label(frame2,text="Q - Check Using Rating Multiplier of 1.2,             ").grid(row=185,column=0, columnspan=3,sticky = W) 
L_1077=Label(frame2,text="       Don't Use to Calculate Minimum                 ").grid(row=186,column=0, columnspan=3,sticky = W) 

v108=StringVar()
v108.set(' ')
L_108=Label(frame2,text="108.Output Branch Mileage in Place of Rating? ").grid(row=187,column=0, sticky = W) 
R108b = Radiobutton(frame2, text='Blank - Output Ratings                      ', value = ' ', variable=v108).grid(row=188,column=0,sticky = W)
R108n = Radiobutton(frame2, text='N - Output Mileage in Place of Normal Rating', value = 'N', variable=v108).grid(row=189,column=0,sticky = W)
R108l = Radiobutton(frame2, text='L - Output Mileage in Place of LTE    Rating', value = 'L', variable=v108).grid(row=190,column=0,sticky = W) 
R108s = Radiobutton(frame2, text='S - Output Mileage in Place of STE    Rating', value = 'S', variable=v108).grid(row=191,column=0,sticky = W)

v109=StringVar()
v109.set('L')
L_109=Label(frame2,text="109.Overwrite Emergency Ratings? ").grid(row=192,column=0, sticky = W) 
R109n = Radiobutton(frame2, text='N - No Change (Rate B = LTE; Rate C = STE)                   ', value = 'N', variable=v109).grid(row=193,column=0,sticky = W)
R109l = Radiobutton(frame2, text='L - Output LTE in Place of STE Rating (Rate B = Rate C = LTE)', value = 'L', variable=v109).grid(row=194,column=0,sticky = W) 
R109s = Radiobutton(frame2, text='S - Output STE in Place of LTE Rating (Rate B = Rate C = STE)', value = 'S', variable=v109).grid(row=195,column=0,sticky = W)

v110=StringVar()
v110.set('Y')
L_110=Label(frame2,text="110.Psse branch rating file output code               ").grid(row=196,column=0, sticky = W) 
R110y = Radiobutton(frame2, text=' Y - If none of the three ratings are set, output branch entry     ', value = 'Y', variable=v110).grid(row=197,column=0,sticky = W)
R110n = Radiobutton(frame2, text=' N - If none of the three ratings are set, dont output branch entry', value = 'N', variable=v110).grid(row=198,column=0,sticky = W) 

v111=StringVar()
v111.set('Y')
L_111=Label(frame2,text="111.Check Ring Bus Breakers?          ").grid(row=199,column=0,sticky = W) 
R111y = Radiobutton(frame2, text='Y', value = 'Y', variable=v111).grid(row=199,column=1,sticky = W)
R111n = Radiobutton(frame2, text='N', value = 'N', variable=v111).grid(row=199,column=2,sticky = W) 

v112=StringVar()
v112.set('Y')
L_112=Label(frame2,text="112.Check Ring Bus Disc   Switch?     ").grid(row=200,column=0,sticky = W) 
R112y = Radiobutton(frame2, text='Y', value = 'Y', variable=v112).grid(row=200,column=1,sticky = W)
R112n = Radiobutton(frame2, text='N', value = 'N', variable=v112).grid(row=200,column=2,sticky = W) 

v113=StringVar()
v113.set('Y')
L_113=Label(frame2,text="113.Check Ring Bus Bypass Switch?     ").grid(row=201,column=0,sticky = W) 
R113y = Radiobutton(frame2, text='Y', value = 'Y', variable=v113).grid(row=201,column=1,sticky = W)
R113n = Radiobutton(frame2, text='N', value = 'N', variable=v113).grid(row=201,column=2,sticky = W) 

v114=StringVar()
v114.set('Y')
L_114=Label(frame2,text="114.Check Ring Bus Dual   Switch?     ").grid(row=202,column=0,sticky = W) 
R114y = Radiobutton(frame2, text='Y', value = 'Y', variable=v114).grid(row=202,column=1,sticky = W)
R114n = Radiobutton(frame2, text='N', value = 'N', variable=v114).grid(row=202,column=2,sticky = W) 

v115=StringVar()
v115.set('Y')
L_115=Label(frame2,text="115.Check Ring Bus Bus    Switch?     ").grid(row=203,column=0,sticky = W) 
R115y = Radiobutton(frame2, text='Y', value = 'Y', variable=v115).grid(row=203,column=1,sticky = W)
R115n = Radiobutton(frame2, text='N', value = 'N', variable=v115).grid(row=203,column=2,sticky = W) 

v116=StringVar()
v116.set('Y')
L_116=Label(frame2,text="116.Check Ring Bus Line   Switch?     ").grid(row=204,column=0,sticky = W) 
R116y = Radiobutton(frame2, text='Y', value = 'Y', variable=v116).grid(row=204,column=1,sticky = W)
R116n = Radiobutton(frame2, text='N', value = 'N', variable=v116).grid(row=204,column=2,sticky = W) 

v117=StringVar()
v117.set('Y')
L_117=Label(frame2,text="117.Check Ring Bus Current Transformers?").grid(row=205,column=0,sticky = W) 
R117y = Radiobutton(frame2, text='Y', value = 'Y', variable=v117).grid(row=205,column=1,sticky = W)
R117n = Radiobutton(frame2, text='N', value = 'N', variable=v117).grid(row=205,column=2,sticky = W) 

v118=StringVar()
v118.set('Y')
L_118=Label(frame2,text="118.Check Ring Bus Wavetraps?         ").grid(row=206,column=0,sticky = W) 
R118y = Radiobutton(frame2, text='Y', value = 'Y', variable=v118).grid(row=206,column=1,sticky = W)
R118n = Radiobutton(frame2, text='N', value = 'N', variable=v118).grid(row=206,column=2,sticky = W) 

v119=StringVar()
v119.set('Y')
L_119=Label(frame2,text="119.Check Ring Bus Circuit Connectors?").grid(row=207,column=0,sticky = W) 
R119y = Radiobutton(frame2, text='Y', value = 'Y', variable=v119).grid(row=207,column=1,sticky = W)
R119n = Radiobutton(frame2, text='N', value = 'N', variable=v119).grid(row=207,column=2,sticky = W) 

v120=StringVar()
v120.set('Y')
L_120=Label(frame2,text="120.Check Ring Bus Buswork?           ").grid(row=208,column=0,sticky = W) 
R120y = Radiobutton(frame2, text='Y', value = 'Y', variable=v120).grid(row=208,column=1,sticky = W)
R120n = Radiobutton(frame2, text='N', value = 'N', variable=v120).grid(row=208,column=2,sticky = W) 

# PSSE and SSAM Output Options: ------------------------------------------------
#
#

Label(frame2,text="PSSE and SSAM Output Options: --------------------------------------").grid(row=209,column=0,columnspan=3,sticky = W)
Label(frame2,text="# Transformer Delta/Wye 30 Degree Angular Shift:                    ").grid(row=210,column=0,columnspan=3,sticky = W)

 
v121=StringVar()
v121.set('Y')
L_121=Label(frame2,text="121.Create Delta/Wye 30 Degree Angular Shift? (Y/N)     ").grid(row=211,column=0,sticky = W) 
R121y = Radiobutton(frame2, text='Y', value = 'Y', variable=v121).grid(row=211,column=1,sticky = W)
R121n = Radiobutton(frame2, text='N', value = 'N', variable=v121).grid(row=211,column=2,sticky = W) 

Label(frame2,text="#                                                                    ").grid(row=212,column=0,columnspan=3,sticky = W)
Label(frame2,text="# Line Branch Impedance:                                             ").grid(row=213,column=0,columnspan=3,sticky = W)
Label(frame2,text="#   If line branch impedance < Line Branch Minimum Impedance Allowed,").grid(row=214,column=0,columnspan=3,sticky = W)
Label(frame2,text="#     reset resistance = 0                                           ").grid(row=215,column=0,columnspan=3,sticky = W)
Label(frame2,text="#           reactance  = Line Branch Zero Reactance Value            ").grid(row=216,column=0,columnspan=3,sticky = W)
Label(frame2,text="#           charging   = 0                                           ").grid(row=217,column=0,columnspan=3,sticky = W)
Label(frame2,text="#   When creating SSAM files, a branch impedance will not equal the total").grid(row=218,column=0,columnspan=3,sticky = W)
Label(frame2,text="#     of its segment impedances if the branch impedance is reset         ").grid(row=219,column=0,columnspan=3,sticky = W)


v122 = DoubleVar(frame2,value = 0.000)
E_v122= Entry(frame2,textvariable=v122,width=10)
E_v122.grid(row=220, column = 2, sticky = W)
L122=Label(frame2,text="122.Line Branch Zero Reactive Value (PU)").grid(row=220,column=0,columnspan = 2,sticky = W)

v123 = DoubleVar(frame2,value = 0.000)
E_v123= Entry(frame2,textvariable=v123,width=10)
E_v123.grid(row=221, column = 2, sticky = W)
L123=Label(frame2,text="123.Line Branch Minimum Impedance Allowed (PU)").grid(row=221,column=0,columnspan = 2,sticky = W)

Label(frame2,text="# Tie Branch Impedance:                                           ").grid(row=222,column=0,columnspan=3,sticky = W)
Label(frame2,text="#   If a tie branch connects two buses with bulk power capacitors,").grid(row=223,column=0,columnspan=3,sticky = W)
Label(frame2,text="#     set  resistance = 0                                         ").grid(row=224,column=0,columnspan=3,sticky = W)
Label(frame2,text="#          reactance  = Tie Branch Zero Reactance Value           ").grid(row=225,column=0,columnspan=3,sticky = W)
Label(frame2,text="#          charging   = 0                                         ").grid(row=226,column=0,columnspan=3,sticky = W)
Label(frame2,text="#     else resistance = charging = 0, reactance = .00001          ").grid(row=227,column=0,columnspan=3,sticky = W)

v124 = DoubleVar(frame2,value =  0.00200)
E_v124= Entry(frame2,textvariable=v124,width=10)
E_v124.grid(row=228, column = 2, sticky = W)
L124=Label(frame2,text="124.Tie Branch Zero Reactive Value (PU)").grid(row=228,column=0,columnspan = 2,sticky = W)

Label(frame2,text="# Distribution Circuit:          ").grid(row=229,column=0,columnspan=2,sticky = W)

v125=StringVar()
v125.set('Y')
L_125=Label(frame2,text="125.Allocate Bus Load to Distribution Circuits?      ").grid(row=230,column=0,sticky = W) 
R125y = Radiobutton(frame2, text='Y', value = 'Y', variable=v125).grid(row=230,column=1,sticky = W)
R125n = Radiobutton(frame2, text='N', value = 'N', variable=v125).grid(row=230,column=2,sticky = W) 

Label(frame2,text="# Distribution Capacitor:          ").grid(row=231,column=0,columnspan=2,sticky = W)

v126=StringVar()
v126.set('S')
L_126=Label(frame2,text="126.Distribution Capacitor Load Model Code?      ").grid(row=232,column=0,sticky = W) 
R126y = Radiobutton(frame2, text='S - Model Total of All Capacitors as Load ID 2', value = 'S', variable=v126).grid(row=233,column=0,sticky = W)
R126n = Radiobutton(frame2, text='M - Model Capacitors as Multiple Load ID Entries as Follows:', value = 'M', variable=v126).grid(row=234,column=0,sticky = W) 
Label(frame2,text="#Distribution Circuit Number < 40    - PSS/E Load ID = 2").grid(row=235,column=0,columnspan=2,sticky = W)
Label(frame2,text="#Distribution Circuit Number = 40-49 - PSS/E Load ID = 3").grid(row=236,column=0,columnspan=2,sticky = W)
Label(frame2,text="#Distribution Circuit Number = 50-59 - PSS/E Load ID = 4").grid(row=237,column=0,columnspan=2,sticky = W)
Label(frame2,text="#Distribution Circuit Number = 60-69 - PSS/E Load ID = 5").grid(row=238,column=0,columnspan=2,sticky = W)
Label(frame2,text="#Distribution Circuit Number = 70-79 - PSS/E Load ID = 6").grid(row=239,column=0,columnspan=2,sticky = W)
Label(frame2,text="#Distribution Circuit Number = 80-89 - PSS/E Load ID = 7").grid(row=240,column=0,columnspan=2,sticky = W)

v127=StringVar()
v127.set('Y')
L_127=Label(frame2,text="127.Move 138/46kv and 138/ind Xfmrs to 138kv Area? ").grid(row=241,column=0,sticky = W) 
R127y = Radiobutton(frame2, text='Y', value = 'Y', variable=v127).grid(row=241,column=1,sticky = W)
R127n = Radiobutton(frame2, text='N', value = 'N', variable=v127).grid(row=241,column=2,sticky = W) 
Label(frame2,text="#This option will reset the midpoint and tertiary of all 138/46kv").grid(row=242,column=0,columnspan=2,sticky = W)
Label(frame2,text="#and 138/industrial 3-winder transformers to the 138kv area      ").grid(row=243,column=0,columnspan=2,sticky = W)
Label(frame2,text="#(area 1 or 23). It will also move the meter end of all 138/46kv ").grid(row=244,column=0,columnspan=2,sticky = W)
Label(frame2,text="#and 138/industrial 2-winder transformers to the 46kv bus.       ").grid(row=245,column=0,columnspan=2,sticky = W)

# Output Options: ---------------------------------------------------------------
Label(frame2,text="Output Options: ---------------------------------------------------------------").grid(row=246,column=0,columnspan=3,sticky = W)

v128=StringVar()
v128.set('Y')
L_128=Label(frame2,text="128.Create Table Data Dump?").grid(row=247,column=0,sticky = W) 
R128Y = Radiobutton(frame2, text='Y', value = 'Y', variable=v128).grid(row=247,column=1,sticky = W)
R128N = Radiobutton(frame2, text='N', value = 'N', variable=v128).grid(row=247,column=2,sticky = W) 

v129=StringVar()
v129.set('A')
L_129=Label(frame2,text="129.Create Branch Rating Listing?").grid(row=248,column=0,sticky = W) 
R129N = Radiobutton(frame2, text='N - No Output         ', value = 'N', variable=v129).grid(row=249,column=0,sticky = W)
R129A = Radiobutton(frame2, text='A - Output Amp Ratings', value = 'A', variable=v129).grid(row=250,column=0,sticky = W) 
R129M = Radiobutton(frame2, text='M - Output MVA Ratings', value = 'M', variable=v129).grid(row=251,column=0,sticky = W) 

v130=StringVar()
v130.set('Y')
L_130=Label(frame2,text="130.Create SSAM Files").grid(row=252,column=0,sticky = W) 
R130N = Radiobutton(frame2, text='N - No Output                                   ', value = 'N', variable=v130).grid(row=253,column=0,sticky = W)
R130A = Radiobutton(frame2, text='I - Create with Interchange Load Set to Zero    ', value = 'I', variable=v130).grid(row=254,column=0,sticky = W) 
R130M = Radiobutton(frame2, text='Y - Create with Interchange Load Not Set to Zero', value = 'Y', variable=v130).grid(row=255,column=0,sticky = W) 

Label(frame2,text="N - Use PSSE Three Winder Card (Elim Midpnt Bus)").grid(row=256,column=0,columnspan=3,sticky = W)

v131=StringVar()
v131.set('33')
L_131=Label(frame2,text="131.Create PSSE Loadflow File").grid(row=257,column=0,sticky = W) 
R131nN = Radiobutton(frame2, text='N  - No Output        ', value = 'N', variable=v131).grid(row=258,column=0,sticky = W)
R13133 = Radiobutton(frame2, text='33 - Version 33 Format', value = '33', variable=v131).grid(row=259,column=0,sticky = W) 
R13132 = Radiobutton(frame2, text='32 - Version 32 Format', value = '32', variable=v131).grid(row=260,column=0,sticky = W) 
R13130 = Radiobutton(frame2, text='30 - Version 30 Format', value = '30', variable=v131).grid(row=261,column=0,sticky = W) 

v132=StringVar()
v132.set('33')
L_132=Label(frame2,text="132.Create PSSE Sequence File").grid(row=262,column=0,sticky = W) 
R132nN = Radiobutton(frame2, text='N  - No Output        ', value = 'N', variable=v132).grid(row=263,column=0,sticky = W)
R13233 = Radiobutton(frame2, text='33 - Version 33 Format', value = '33', variable=v132).grid(row=264,column=0,sticky = W) 
R13232 = Radiobutton(frame2, text='32 - Version 32 Format', value = '32', variable=v132).grid(row=265,column=0,sticky = W) 
R13230 = Radiobutton(frame2, text='30 - Version 30 Format', value = '30', variable=v132).grid(row=266,column=0,sticky = W) 

v133=StringVar()
v133.set('33')
L_133=Label(frame2,text="133.Create PSSE Branch Ratings File").grid(row=267,column=0,sticky = W) 
R133nN = Radiobutton(frame2, text='N  - No Output        ', value = 'N', variable=v133).grid(row=268,column=0,sticky = W)
R13333 = Radiobutton(frame2, text='33 - Version 33 Format', value = '33', variable=v133).grid(row=269,column=0,sticky = W) 
R13332 = Radiobutton(frame2, text='32 - Version 32 Format', value = '32', variable=v133).grid(row=270,column=0,sticky = W) 
R13330 = Radiobutton(frame2, text='30 - Version 30 Format', value = '30', variable=v133).grid(row=271,column=0,sticky = W) 

v134=StringVar()
v134.set('33')
L_134=Label(frame2,text="134.Create PSSE Distribution Capacitor File").grid(row=272,column=0,sticky = W) 
R134nN = Radiobutton(frame2, text='N  - No Output        ', value = 'N', variable=v134).grid(row=273,column=0,sticky = W)
R13433 = Radiobutton(frame2, text='33 - Version 33 Format', value = '33', variable=v134).grid(row=274,column=0,sticky = W) 
R13432 = Radiobutton(frame2, text='32 - Version 32 Format', value = '32', variable=v134).grid(row=275,column=0,sticky = W) 
R13430 = Radiobutton(frame2, text='30 - Version 30 Format', value = '30', variable=v134).grid(row=276,column=0,sticky = W) 

v135=StringVar()
v135.set('Y')
L_135=Label(frame2,text="135.Create DCM  Capacitor File?").grid(row=277,column=0,sticky = W) 
R135y = Radiobutton(frame2, text='Y', value = 'Y', variable=v135).grid(row=277,column=1,sticky = W)
R135n = Radiobutton(frame2, text='N', value = 'N', variable=v135).grid(row=277,column=2,sticky = W)

v136=StringVar()
v136.set('Y')
L_136=Label(frame2,text="136.Create DCM  Capacitor Data Dump File?").grid(row=278,column=0,sticky = W) 
R136y = Radiobutton(frame2, text='Y', value = 'Y', variable=v136).grid(row=278,column=1,sticky = W)
R136n = Radiobutton(frame2, text='N', value = 'N', variable=v136).grid(row=278,column=2,sticky = W)

v137=StringVar()
v137.set('Y')
L_137=Label(frame2,text="137.Create MAV  File? ").grid(row=279,column=0,sticky = W) 
R137y = Radiobutton(frame2, text='Y', value = 'Y', variable=v137).grid(row=279,column=1,sticky = W)
R137n = Radiobutton(frame2, text='N', value = 'N', variable=v137).grid(row=279,column=2,sticky = W)

v138=StringVar()
v138.set('N')
L_138=Label(frame2,text="138.Create 1147 File? ").grid(row=280,column=0,sticky = W) 
R138y = Radiobutton(frame2, text='Y', value = 'Y', variable=v138).grid(row=280,column=1,sticky = W)
R138n = Radiobutton(frame2, text='N', value = 'N', variable=v138).grid(row=280,column=2,sticky = W)


Label(frame2,text="Database          Data Label - 'PREVIOUS YR '         ").grid(row=281,column=0,columnspan=3,sticky = W)
Label(frame2,text="PSSE Summary File Data Label - 'LOAD SEARCH '         ").grid(row=282,column=0,columnspan=3,sticky = W)
Label(frame2,text="Max Load Sum File - 'maxloadsummary'                  ").grid(row=283,column=0,columnspan=3,sticky = W)
Label(frame2,text="PSSE Summary File - 'pssesummary'                     ").grid(row=284,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area   2 - User - ALR  (ADRIAN)                       ").grid(row=285,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area   3 - User - ERM  (ALMA)                         ").grid(row=286,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area   4 - User - ERM  (AU SABLE)                     ").grid(row=287,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area   5 - User - WEE  (BAY CITY)                     ").grid(row=288,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area   6 - User - ALR  (BATTLE CREEK)                 ").grid(row=289,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area   7 - User - DAL  (BELDING)                      ").grid(row=290,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area   8 - User - WEE  (FLINT)                        ").grid(row=291,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area   9 - User - DAL  (GRAND RAPIDS RURAL)           ").grid(row=292,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area  10 - User - DAL  (GRAND RAPIDS URBAN)           ").grid(row=293,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area  11 - User - ERM  (HIGGINS)                      ").grid(row=294,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area  12 - User - ALR  (JACKSON)                      ").grid(row=295,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area  13 - User - DAL  (KALAMAZOO)                    ").grid(row=296,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area  14 - User - ALR  (LANSING)                      ").grid(row=297,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area  15 - User - DAL  (MECOSTA)                      ").grid(row=298,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area  16 - User - ERM  (MIDLAND)                      ").grid(row=299,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area  17 - User - DAL  (MUSKEGON)                     ").grid(row=300,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area  18 - User - DAL  (NORTHWEST)                    ").grid(row=301,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area  19 - User - ALR  (OWOSSO)                       ").grid(row=302,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area  20 - User - ERM  (PETOSKEY)                     ").grid(row=303,column=0,columnspan=3,sticky = W)
Label(frame2,text="Area  21 - User - WEE  (SAGINAW)                      ").grid(row=304,column=0,columnspan=3,sticky = W)

v139=StringVar()
v139.set('Y')
L_139=Label(frame2,text="139.Create Group/Subgroup Contingency Files? ").grid(row=305,column=0,sticky = W) 
R139y = Radiobutton(frame2, text='Y', value = 'Y', variable=v139).grid(row=305,column=1,sticky = W)
R139n = Radiobutton(frame2, text='N', value = 'N', variable=v139).grid(row=305,column=2,sticky = W)

v140=StringVar()
v140.set('Y')
L_140=Label(frame2,text="140.Create Generator Contingency Files? ").grid(row=306,column=0,sticky = W) 
R140y = Radiobutton(frame2, text='Y', value = 'Y', variable=v140).grid(row=306,column=1,sticky = W)
R140n = Radiobutton(frame2, text='N', value = 'N', variable=v140).grid(row=306,column=2,sticky = W)

v141=StringVar()
v141.set('Y')
L_141=Label(frame2,text="141.Create Capacitor Contingency Files?").grid(row=307,column=0,sticky = W) 
R141y = Radiobutton(frame2, text='Y', value = 'Y', variable=v141).grid(row=307,column=1,sticky = W)
R141n = Radiobutton(frame2, text='N', value = 'N', variable=v141).grid(row=307,column=2,sticky = W)

v142=StringVar()
v142.set('Y')
L_142=Label(frame2,text="142.Create Plant     Contingency Files?").grid(row=308,column=0,sticky = W) 
R142y = Radiobutton(frame2, text='Y', value = 'Y', variable=v142).grid(row=308,column=1,sticky = W)
R142n = Radiobutton(frame2, text='N', value = 'N', variable=v142).grid(row=308,column=2,sticky = W)

v143=StringVar()
v143.set('Y')
L_143=Label(frame2,text="143.Create Open Sectionalizing Device Contingency Files?").grid(row=309,column=0,sticky = W) 
R143y = Radiobutton(frame2, text='Y', value = 'Y', variable=v143).grid(row=309,column=1,sticky = W)
R143n = Radiobutton(frame2, text='N', value = 'N', variable=v143).grid(row=309,column=2,sticky = W)

v144=StringVar()
v144.set('Y')
L_144=Label(frame2,text="144.Contingency Output Code?").grid(row=310,column=0,sticky = W) 
R144y = Radiobutton(frame2, text='Y - Output Fast, Slow, Manual and Rating Only Devices', value = 'Y', variable=v144).grid(row=311,column=0,sticky = W)
R144n = Radiobutton(frame2, text='N - Output Only Fast, Slow, and Manual Devices       ', value = 'N', variable=v144).grid(row=312,column=0,sticky = W)

v145=StringVar()
v145.set('N')
L_145=Label(frame2,text="145.Create Open 345KV Breaker         Contingencies?").grid(row=313,column=0,sticky = W) 
R145y = Radiobutton(frame2, text='Y', value = 'Y', variable=v145).grid(row=313,column=1,sticky = W)
R145n = Radiobutton(frame2, text='N', value = 'N', variable=v145).grid(row=313,column=2,sticky = W)

v146=StringVar()
v146.set('N')
L_146=Label(frame2,text="146.Create Open 345KV Bus  Switch     Contingencies?").grid(row=314,column=0,sticky = W) 
R146y = Radiobutton(frame2, text='Y', value = 'Y', variable=v146).grid(row=314,column=1,sticky = W)
R146n = Radiobutton(frame2, text='N', value = 'N', variable=v146).grid(row=314,column=2,sticky = W)

v147=StringVar()
v147.set('Y')
L_147=Label(frame2,text="147.Create Open 345KV Line Switch     Contingencies?").grid(row=315,column=0,sticky = W) 
R147y = Radiobutton(frame2, text='Y', value = 'Y', variable=v147).grid(row=315,column=1,sticky = W)
R147n = Radiobutton(frame2, text='N', value = 'N', variable=v147).grid(row=315,column=2,sticky = W)

v148=StringVar()
v148.set('N')
L_148=Label(frame2,text="148.Create Open 69-138KV Breaker      Contingencies?").grid(row=316,column=0,sticky = W) 
R148y = Radiobutton(frame2, text='Y', value = 'Y', variable=v148).grid(row=316,column=1,sticky = W)
R148n = Radiobutton(frame2, text='N', value = 'N', variable=v148).grid(row=316,column=2,sticky = W)

v149=StringVar()
v149.set('N')
L_149=Label(frame2,text="149.Create Open 69-138KV Bus  Switch  Contingencies?").grid(row=317,column=0,sticky = W) 
R149y = Radiobutton(frame2, text='Y', value = 'Y', variable=v149).grid(row=317,column=1,sticky = W)
R149n = Radiobutton(frame2, text='N', value = 'N', variable=v149).grid(row=317,column=2,sticky = W)

v150=StringVar()
v150.set('Y')
L_150=Label(frame2,text="150.Create Open 69-138KV Line Switch  Contingencies?").grid(row=318,column=0,sticky = W) 
R150y = Radiobutton(frame2, text='Y', value = 'Y', variable=v150).grid(row=318,column=1,sticky = W)
R150n = Radiobutton(frame2, text='N', value = 'N', variable=v150).grid(row=318,column=2,sticky = W)

v151=StringVar()
v151.set('N')
L_151=Label(frame2,text="151.Create Open 23,46KV  Breaker      Contingencies?").grid(row=319,column=0,sticky = W) 
R151y = Radiobutton(frame2, text='Y', value = 'Y', variable=v151).grid(row=319,column=1,sticky = W)
R151n = Radiobutton(frame2, text='N', value = 'N', variable=v151).grid(row=319,column=2,sticky = W)

v152=StringVar()
v152.set('N')
L_152=Label(frame2,text="152.Create Open 23,46KV  Bus  Switch  Contingencies?").grid(row=320,column=0,sticky = W) 
R152y = Radiobutton(frame2, text='Y', value = 'Y', variable=v152).grid(row=320,column=1,sticky = W)
R152n = Radiobutton(frame2, text='N', value = 'N', variable=v152).grid(row=320,column=2,sticky = W)

v153=StringVar()
v153.set('Y')
L_153=Label(frame2,text="153.Create Open 23,46KV  Line Switch  Contingencies?").grid(row=321,column=0,sticky = W) 
R153y = Radiobutton(frame2, text='Y', value = 'Y', variable=v153).grid(row=321,column=1,sticky = W)
R153n = Radiobutton(frame2, text='N', value = 'N', variable=v153).grid(row=321,column=2,sticky = W)

v154=StringVar()
v154.set('N')
L_154=Label(frame2,text="154.Create Open Low KV  Breaker       Contingencies?").grid(row=322,column=0,sticky = W) 
R154y = Radiobutton(frame2, text='Y', value = 'Y', variable=v154).grid(row=322,column=1,sticky = W)
R154n = Radiobutton(frame2, text='N', value = 'N', variable=v154).grid(row=322,column=2,sticky = W)

v155=StringVar()
v155.set('N')
L_155=Label(frame2,text="155.Create Open Low KV  Bus  Switch   Contingencies?").grid(row=323,column=0,sticky = W) 
R155y = Radiobutton(frame2, text='Y', value = 'Y', variable=v155).grid(row=323,column=1,sticky = W)
R155n = Radiobutton(frame2, text='N', value = 'N', variable=v155).grid(row=323,column=2,sticky = W)

v156=StringVar()
v156.set('Y')
L_156=Label(frame2,text="156.Create Open Low KV  Line Switch   Contingencies?").grid(row=324,column=0,sticky = W) 
R156y = Radiobutton(frame2, text='Y', value = 'Y', variable=v156).grid(row=324,column=1,sticky = W)
R156n = Radiobutton(frame2, text='N', value = 'N', variable=v156).grid(row=324,column=2,sticky = W)

v157=StringVar()
v157.set('S')
L_157=Label(frame2,text="157.Create Ring Bus Breaker Fail-to-Open Contingency Files?").grid(row=325,column=0,sticky = W) 
R157g = Radiobutton(frame2, text='G - Create Group Files', value = 'G', variable=v157).grid(row=326,column=0,sticky = W)
R157s = Radiobutton(frame2, text='S - Create Subgroup Files', value = 'S', variable=v157).grid(row=327,column=0,sticky = W)
R157n = Radiobutton(frame2, text='N - Dont Create Files', value = 'N', variable=v157).grid(row=328,column=0,sticky = W)

v158 = DoubleVar(frame2,value = -1.0)
E_v158= Entry(frame2,textvariable=v158,width=10)
E_v158.grid(row=329, column = 2, sticky = W)
L158=Label(frame2,text="158.Override Ring Bus Breaker Fail-to-Open Outage Rate").grid(row=330,column=0,columnspan = 2,sticky = W)

v159=StringVar()
v159.set('Y')
L_159=Label(frame2,text="159.Create Buses Which Must Not Be Shed File and Fast?").grid(row=331,column=0,sticky = W) 
R159y = Radiobutton(frame2, text='Y', value = 'Y', variable=v159).grid(row=331,column=1,sticky = W)
R159n = Radiobutton(frame2, text='N', value = 'N', variable=v159).grid(row=331,column=2,sticky = W)


Label(frame2,text="            Sectionalizing Equipment File?").grid(row=332,column=0,columnspan=3,sticky = W)


v160=StringVar()
v160.set('Y')
L_160=Label(frame2,text="160.Shed Interchange (INT) Buses?").grid(row=333,column=0,sticky = W) 
R160y = Radiobutton(frame2, text='Y', value = 'Y', variable=v160).grid(row=333,column=1,sticky = W)
R160n = Radiobutton(frame2, text='N', value = 'N', variable=v160).grid(row=333,column=2,sticky = W)

v161=StringVar()
v161.set('Y')
L_161=Label(frame2,text="161.Shed Wholesale Power (WHSP) Buses?").grid(row=334,column=0,sticky = W) 
R161y = Radiobutton(frame2, text='Y', value = 'Y', variable=v161).grid(row=334,column=1,sticky = W)
R161n = Radiobutton(frame2, text='N', value = 'N', variable=v161).grid(row=334,column=2,sticky = W)

v162=StringVar()
v162.set('Y')
L_162=Label(frame2,text="162.Shed Wholesale Transmission (WHST) Buses?").grid(row=335,column=0,sticky = W) 
R162y = Radiobutton(frame2, text='Y', value = 'Y', variable=v162).grid(row=335,column=1,sticky = W)
R162n = Radiobutton(frame2, text='N', value = 'N', variable=v162).grid(row=335,column=2,sticky = W)

v163=StringVar()
v163.set('Y')
L_163=Label(frame2,text="163.Shed SEC (SEC) Buses?").grid(row=336,column=0,sticky = W) 
R163y = Radiobutton(frame2, text='Y', value = 'Y', variable=v163).grid(row=336,column=1,sticky = W)
R163n = Radiobutton(frame2, text='N', value = 'N', variable=v163).grid(row=336,column=2,sticky = W)

v164=StringVar()
v164.set('Y')
L_164=Label(frame2,text="164.Shed Generator (GEN) Buses?").grid(row=337,column=0,sticky = W) 
R164y = Radiobutton(frame2, text='Y', value = 'Y', variable=v164).grid(row=337,column=1,sticky = W)
R164n = Radiobutton(frame2, text='N', value = 'N', variable=v164).grid(row=337,column=2,sticky = W)

v165=StringVar()
v165.set('Y')
L_165=Label(frame2,text="165.Shed Consumers Energy HQ (HEAD) Buses?").grid(row=338,column=0,sticky = W) 
R165y = Radiobutton(frame2, text='Y', value = 'Y', variable=v165).grid(row=338,column=1,sticky = W)
R165n = Radiobutton(frame2, text='N', value = 'N', variable=v165).grid(row=338,column=2,sticky = W)

v166=StringVar()
v166.set('Y')
L_166=Label(frame2,text="166.Shed Hospital (HOSP) Buses?").grid(row=339,column=0,sticky = W) 
R166y = Radiobutton(frame2, text='Y', value = 'Y', variable=v166).grid(row=339,column=1,sticky = W)
R166n = Radiobutton(frame2, text='N', value = 'N', variable=v166).grid(row=339,column=2,sticky = W)

v167=StringVar()
v167.set('Y')
L_167=Label(frame2,text="167.Shed Not-to-Be-Shed (SHED) Buses?").grid(row=340,column=0,sticky = W) 
R167y = Radiobutton(frame2, text='Y', value = 'Y', variable=v167).grid(row=340,column=1,sticky = W)
R167n = Radiobutton(frame2, text='N', value = 'N', variable=v167).grid(row=340,column=2,sticky = W)

v168=StringVar()
v168.set('Y')
L_168=Label(frame2,text="168.Shed Customer Sub - Not Regulated (CSNR) Buses?").grid(row=341,column=0,sticky = W) 
R168y = Radiobutton(frame2, text='Y', value = 'Y', variable=v168).grid(row=341,column=1,sticky = W)
R168n = Radiobutton(frame2, text='N', value = 'N', variable=v168).grid(row=341,column=2,sticky = W)

v169=StringVar()
v169.set('Y')
L_169=Label(frame2,text="169.Shed Welder Sub (WELD) Buses?").grid(row=342,column=0,sticky = W) 
R169y = Radiobutton(frame2, text='Y', value = 'Y', variable=v169).grid(row=342,column=1,sticky = W)
R169n = Radiobutton(frame2, text='N', value = 'N', variable=v169).grid(row=342,column=2,sticky = W)

v170=StringVar()
v170.set('Y')
L_170=Label(frame2,text="170.Create Contingency Analysis Auxiliary Data Base?").grid(row=343,column=0,sticky = W) 
R170y = Radiobutton(frame2, text='Y', value = 'Y', variable=v170).grid(row=343,column=1,sticky = W)
R170n = Radiobutton(frame2, text='N', value = 'N', variable=v170).grid(row=343,column=2,sticky = W)

v171=StringVar()
v171.set('Y')
L_171=Label(frame2,text="171.Create BTF Database Files?").grid(row=344,column=0,sticky = W) 
R171y = Radiobutton(frame2, text='Y', value = 'Y', variable=v171).grid(row=344,column=1,sticky = W)
R171n = Radiobutton(frame2, text='N', value = 'N', variable=v171).grid(row=344,column=2,sticky = W)

v172=StringVar()
v172.set('Y')
L_172=Label(frame2,text="172.Create Breaker Duty Files?").grid(row=345,column=0,sticky = W) 
R172y = Radiobutton(frame2, text='Y', value = 'Y', variable=v172).grid(row=345,column=1,sticky = W)
R172n = Radiobutton(frame2, text='N', value = 'N', variable=v172).grid(row=345,column=2,sticky = W)

v173=StringVar()
v173.set('Y')
L_173=Label(frame2,text="173.Create Equipment Listing?").grid(row=346,column=0,sticky = W) 
R173y = Radiobutton(frame2, text='Y', value = 'Y', variable=v173).grid(row=346,column=1,sticky = W)
R173n = Radiobutton(frame2, text='N', value = 'N', variable=v173).grid(row=346,column=2,sticky = W)

v174=StringVar()
v174.set('Y')
L_174=Label(frame2,text="174.Create p1145 PSSE File?").grid(row=347,column=0,sticky = W) 
R174y = Radiobutton(frame2, text='Y', value = 'Y', variable=v174).grid(row=347,column=1,sticky = W)
R174n = Radiobutton(frame2, text='N', value = 'N', variable=v174).grid(row=347,column=2,sticky = W)

v175=StringVar()
v175.set('Y')
L_175=Label(frame2,text="175.Create Relay Loadability Data Listing?").grid(row=348,column=0,sticky = W) 
R175y = Radiobutton(frame2, text='Y', value = 'Y', variable=v175).grid(row=348,column=1,sticky = W)
R175n = Radiobutton(frame2, text='N', value = 'N', variable=v175).grid(row=348,column=2,sticky = W)

v176=StringVar()
v176.set('Y')
L_176=Label(frame2,text="176.Create Load Search Station Data File?").grid(row=349,column=0,sticky = W) 
R176y = Radiobutton(frame2, text='N - No Output', value = 'N', variable=v176).grid(row=350,column=0,sticky = W)
R176c = Radiobutton(frame2, text='C - Create with No Station Name / Bus Name Cross Reference', value = 'C', variable=v176).grid(row=351,column=0,sticky = W)
R176n = Radiobutton(frame2, text='Y - Create with With Station Name / Bus Name Cross Reference', value = 'Y', variable=v176).grid(row=352,column=0,sticky = W)


varib_list=[v176,v175,v174,v173,v172,v171,v170,v169,v168,v167,v166,v165,v164,v163,v162,v161,v160,v159,v158,v157,v156,v155,v154,v153,v152,v151,v150,v149,v148,v147,v146,v145,v144,v143,v142,v141,v140,v139,v138,v137,v136,v135,v134,v133,v132,v131,v130,v129,v128,v127,v126,v125,v124,v123,v122,v121,v120,v119,v118,v117,v116,v115,v114,v113,v112,v111,v110,v109,v108,v107,v106,v105,v104,v103,v102,v101,v100,v99,v98,v97,v96,v95,v94,v93,v92,v91,v90,v89,v88,v87,v86,v85,v84,v83,v82,v81,v80,v79,v78,v77,v76,v75,v74,v73,v72,v71,v70,v69,v68,v67,v66,v65,v64,v63,v62,v61,v60,v59,v58,v57,v56,v55,v54,v53,v52,v51,v50,v49,v48,v47,v46,v45,v44,v43,v42,v41,v40,v39,v38,v37,v36,v35,v34,v33,v32,v31,v30,v29,v28,v27,v26,v25,v24,v23,v22,v21,v20,v19,v18,v17,v16,v15,v14,v13,v12,v11,v10,v9,v8,v7,v6,v5,v4,v3,v1,v2
]
#----------------------output folder of files in frame2--------------------------------------
op_dir2 = StringVar()


def browse_folder2(): 
    folder_op = filedialog.askdirectory()
    op_dir2.set(Path(folder_op))
    entry_op2.delete(0, END)
    entry_op2.insert(0, folder_op)                                  
    return    
 
 

             
Button(frame2,text = "Output Folder", width=15,command = browse_folder2).grid(row=355, column=1, columnspan=2,sticky = W, padx=5, pady = 2)
entry_op2=Entry(frame2,width = 40)

entry_op2.delete(0, END)
entry_op2.insert(0, Path(op_dir2.get()))
entry_op2.grid(row=355, column = 0, sticky = W, pady = 2)

########### select the database (tab2)#####################
db_dir2 = StringVar()

def browse_dbs2(): 
    filename2 = filedialog.askopenfilename(initialdir = "",title = "Select Database",filetypes=(("access 2000","*.mdb"),("access 2010","*.accdb"))) 
    db_dir2.set(Path(filename2))
    entry_db2.delete(0, END)
    entry_db2.insert(0, filename2)                                  
    return                     
   

   
Button(frame2,text = "Browse Database", width=15,command = browse_dbs2).grid(row=356,column = 1, columnspan=2,sticky = W, padx=5, pady = 2)    

entry_db2 = Entry(frame2,width = 40)
entry_db2.grid(row=356, column = 0, sticky = W, pady = 2)

entry_db2.delete(0, END)
entry_db2.insert(0, Path(db_dir2.get()))


#-------------------------------------------------------------------------------------

def create_configuration_file():
    config_file= op_dir2.get()+'\\temp.config'
    ConfigFile = open(config_file, 'w')
    ConfigFile.write("P1120 Program - Check Database Runscript                         \n")
    ConfigFile.write("\n")
    ConfigFile.write(" {} - Read Table BRANCHid           Data? (Y/N)\n".format(v1.get()))
    ConfigFile.write(" {} - Read Table SEGMENTdata        Data? (Y/N)\n".format(v2.get()))
    ConfigFile.write(" {} - Read Table CONDUCTOR          Data? (Y/N)\n".format(v3.get()))
    ConfigFile.write(" {} - Read Table STRUCTURE          Data? (Y/N)\n".format(v4.get()))
    ConfigFile.write(" {} - Read Table SIXwire            Data? (Y/N)\n".format(v5.get()))
    ConfigFile.write(" {} - Read Table TRANSFORMER        Data? (Y/N)\n".format(v6.get()))
    ConfigFile.write(" {} - Read Table TRANSFORMERdata    Data? (Y/N)\n".format(v7.get()))
    ConfigFile.write(" {} - Read Table TRANSFORMERtest    Data? (Y/N)\n".format(v8.get()))
    ConfigFile.write(" {} - Read Table BREAKERdata        Data? (Y/N)\n".format(v9.get()))
    ConfigFile.write(" {} - Read Table BREAKERconnection  Data? (Y/N)\n".format(v10.get()))
    ConfigFile.write(" {} - Read Table SWITCHdata         Data? (Y/N)\n".format(v11.get()))
    ConfigFile.write(" {} - Read Table SWITCHconnection   Data? (Y/N)\n".format(v12.get()))
    ConfigFile.write(" {} - Read Table NONSECTdata        Data? (Y/N)\n".format(v13.get()))
    ConfigFile.write(" {} - Read Table BUSlist            Data? (Y/N)\n".format(v14.get()))
    ConfigFile.write(" {} - Read Table COMPOSITEdata      Data? (Y/N)\n".format(v15.get()))
    ConfigFile.write(" {} - Read Table BUSTIEdata         Data? (Y/N)\n".format(v16.get()))
    ConfigFile.write(" {} - Read Table DISTcircuit        Data? (Y/N)\n".format(v17.get()))
    ConfigFile.write(" {} - Read Table DISTcapacitors     Data? (Y/N)\n".format(v18.get()))
    ConfigFile.write(" {} - Read Table GENERATOR          Data? (Y/N)\n".format(v19.get()))
    ConfigFile.write(" {} - Read Table BULKcapacitors     Data? (Y/N)\n".format(v20.get()))
    ConfigFile.write(" {} - Read Table REACTOR            Data? (Y/N)\n".format(v21.get()))
    ConfigFile.write(" {} - Read Table WDNAME             Data? (Y/N)\n".format(v22.get()))
    ConfigFile.write(" {} - Read Table GROUPdata          Data? (Y/N)\n".format(v23.get()))
    ConfigFile.write(" {} - Read Table AREAdata           Data? (Y/N)\n".format(v24.get()))
    ConfigFile.write(" {} - Read Table GENERICequip       Data? (Y/N)\n".format(v25.get()))
    ConfigFile.write(" {} - Read Table GENERICbus         Data? (Y/N)\n".format(v26.get()))
    ConfigFile.write(" {} - Read Table GENERICgenerator   Data? (Y/N)\n".format(v27.get()))
    ConfigFile.write(" {} - Read Table GENERICsegment     Data? (Y/N)\n".format(v28.get()))
    ConfigFile.write(" {} - Read Table GENERICtransformer Data? (Y/N)\n".format(v29.get()))
    ConfigFile.write(" {} - Read Table STATION            Data? (Y/N)\n".format(v30.get()))
    ConfigFile.write("\n")
    ConfigFile.write("# Bus Elimination Options: ------------------------------------------------------\n")
    ConfigFile.write(" {} - Delete Xfmr Terminal Buses with 'U' in Col 8 of Name? (Y/N) \n".format(v31.get()))
    ConfigFile.write(" {} - Delete Xfmr Terminal Buses with 'L' in Col 8 of Name? (Y/N) \n".format(v32.get()))
    ConfigFile.write("#--------------------------------------------------------------------------------\n")
    ConfigFile.write("\n")
    ConfigFile.write("# Low Impedance Line Tap Branch Elimination Options: ----------------------------\n")
    ConfigFile.write(" {} - Low Impedance Cutoff (PU) (Zero - Delete No Lines)    \n".format(str.format('{0:.5f}', v33.get())))
    ConfigFile.write(" {} - Allow Fast & Slow Sectionalizing Equip to be Deleted? (Y/N) \n".format(v34.get()))
    ConfigFile.write(" {} - Allow Double Circuit Branch Segments to be Deleted? (Y/N)   \n".format(v35.get()))
    ConfigFile.write("#--------------------------------------------------------------------------------\n")
    ConfigFile.write("\n")
    ConfigFile.write("# Area and Zone Reset Option: ---------------------------------------------------\n")
    ConfigFile.write(" {} - Reset Area 23 Zone 64 to Area 1 Zone 2? (Y/N)               \n".format(v36.get()))
    ConfigFile.write("#--------------------------------------------------------------------------------\n")
    ConfigFile.write("\n")
    ConfigFile.write("# Input Data Check Option: ------------------------------------------------------\n")
    ConfigFile.write(" {} - Check for the Following? (Y/N)                              \n".format(v37.get()))
    ConfigFile.write("#          1) Inconsistent Short Circuit Capability\n")
    ConfigFile.write("#          2) Zero Breaker Short Circuit Capability\n")
    ConfigFile.write("#          3) Missing Equipment Amp Ratings\n")
    ConfigFile.write("#          4) Zero MW bus loads\n")
    ConfigFile.write("#          5) Inconsistent Operating Capability\n")
    ConfigFile.write("#--------------------------------------------------------------------------------\n")
    ConfigFile.write("\n")
    ConfigFile.write("# Generator Probability Data Option: --------------------------------------------\n")
    ConfigFile.write(" {} - Generator Probability Type (F-Forced, T-Total)              \n".format(v38.get()))
    ConfigFile.write("#--------------------------------------------------------------------------------\n")
    ConfigFile.write("\n")
    ConfigFile.write("# Generator Maximum MW Output Option: -------------------------------------------\n")
    ConfigFile.write(" {} - Generator Maximum MW Output Type (S-Summer, W-Winter)       \n".format(v39.get()))
    ConfigFile.write("#--------------------------------------------------------------------------------\n")
    ConfigFile.write("\n")
    ConfigFile.write("# 3-Winder Xfmr Conversion Option: ----------------------------------------------\n")
    ConfigFile.write(" {} - Replace 3-Winder Xfmrs with 2-Winder Xfmrs? (Y/N)           \n".format(v40.get()))
    ConfigFile.write("#--------------------------------------------------------------------------------\n")
    ConfigFile.write("\n")
    ConfigFile.write("# Distribution Capacitor Output Options: ----------------------------------------\n")
    ConfigFile.write("#\n")
    ConfigFile.write("# CALENDAR TYPES:\n")
    ConfigFile.write("# 1) KRY - KEARNEY ELECTRONIC TIME CLOCK STANDARD SCHEDULE\n")
    ConfigFile.write("#             SWITCHES ON MON-FRI, 6:00AM-11:00PM, JAN-DEC\n")
    ConfigFile.write("#             DOESNT SWITCH ON HOLIDAY\n")
    ConfigFile.write("#             VOLTAGE CONTROL\n")
    ConfigFile.write("# 2) NTH - ELECTRONIC TIME CLOCK SWITCH ON WEEKENDS - NORTHERN AREA\n")
    ConfigFile.write("#             SWITCHES ON SAT-SUN, 6:00AM-11:00PM, JAN-DEC\n")
    ConfigFile.write("#             DOESNT SWITCH ON HOLIDAY\n")
    ConfigFile.write("# 3) SMR - ELECTRONIC TIME CLOCK SUMMER SWITCHING ONLY\n")
    ConfigFile.write("#             SWITCHES ON MON-FRI, 6:00AM-11:00PM, MAY-SEPT\n")
    ConfigFile.write("#             DOESNT SWITCH ON HOLIDAY\n")
    ConfigFile.write("# 4) STD - ELECTRONIC TIME CLOCK SWITCH MON-FRI\n")
    ConfigFile.write("#             SWITCHES ON MON-FRI, 6:00AM-11:00PM, JAN-DEC\n")
    ConfigFile.write("#             DOESNT SWITCH ON HOLIDAY\n")
    ConfigFile.write("# 5) ERR - DATA IN ERROR\n")
    ConfigFile.write("# HOLIDAYS:\n")
    ConfigFile.write("# 1) NEW YEARS DAY\n")
    ConfigFile.write("# 2) MEMORIAL DAY\n")
    ConfigFile.write("# 3) INDEPENDENCE DAY\n")
    ConfigFile.write("# 4) LABOR DAY\n")
    ConfigFile.write("# 5) THANKSGIVING AND DAY AFTER\n")
    ConfigFile.write("# 6) CHRISTMAS EVE AND CHRISTMAS\n")
    ConfigFile.write("# 7) NEW YEARS EVE\n")
    ConfigFile.write("#\n")
    ConfigFile.write(" {} - Output Unswitched Caps?                                (Y/N)\n".format(v41.get()))
    ConfigFile.write(" {} - Output KRY Calendar Electronic Time Clock Caps?        (Y/N)\n".format(v42.get()))
    ConfigFile.write(" {} - Output NTH Calendar Electronic Time Clock Caps?        (Y/N)\n".format(v43.get()))
    ConfigFile.write(" {} - Output SMR Calendar Electronic Time Clock Caps?        (Y/N)\n".format(v44.get()))
    ConfigFile.write(" {} - Output STD Calendar Electronic Time Clock Caps?        (Y/N)\n".format(v45.get()))
    ConfigFile.write(" {} - Output ERR Calendar Electronic Time Clock Caps?        (Y/N)\n".format(v46.get()))
    ConfigFile.write(" {} - Output Voltage Controlled Caps?                        (Y/N)\n".format(v47.get()))
    ConfigFile.write(" {} - Output In-Service and Repaired In-Service Caps?        (Y/N)\n".format(v48.get()))
    ConfigFile.write(" {} - Output Intentional Out-of-Service Caps?                (Y/N)\n".format(v49.get()))
    ConfigFile.write(" {} - Output Problem     Out-of-Service Caps?                (Y/N)\n".format(v50.get()))
    ConfigFile.write("#PRI  ----------Radio Control Tone Group Output? (Y/N)-----------\n")
    ConfigFile.write("#XMT  01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20\n")
    ConfigFile.write("#---  -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --\n")
    d_c={1:" Y ",0:" N "}
    adr=''.join([d_c[v.get()] for v in v_list[0]])
    alg=''.join([d_c[v.get()] for v in v_list[1]])
    bck=''.join([d_c[v.get()] for v in v_list[2]])
    fen=''.join([d_c[v.get()] for v in v_list[3]])
    fli=''.join([d_c[v.get()] for v in v_list[4]])
    gra=''.join([d_c[v.get()] for v in v_list[5]])
    ion=''.join([d_c[v.get()] for v in v_list[6]])
    jac=''.join([d_c[v.get()] for v in v_list[7]])
    kal=''.join([d_c[v.get()] for v in v_list[8]])
    lan=''.join([d_c[v.get()] for v in v_list[9]])
    mus=''.join([d_c[v.get()] for v in v_list[10]])
    ows=''.join([d_c[v.get()] for v in v_list[11]])
    sag=''.join([d_c[v.get()] for v in v_list[12]])
    unk=''.join([d_c[v.get()] for v in v_list[13]]) 
    ConfigFile.write(" ADR -{}\n".format(adr))
    ConfigFile.write(" ALG -{}\n".format(alg))
    ConfigFile.write(" BCK -{}\n".format(bck))
    ConfigFile.write(" FEN -{}\n".format(fen))
    ConfigFile.write(" FLI -{}\n".format(fli))
    ConfigFile.write(" GRA -{}\n".format(gra))
    ConfigFile.write(" ION -{}\n".format(ion))
    ConfigFile.write(" JAC -{}\n".format(jac))
    ConfigFile.write(" KAL -{}\n".format(kal))
    ConfigFile.write(" LAN -{}\n".format(lan))
    ConfigFile.write(" MUS -{}\n".format(mus))
    ConfigFile.write(" OWS -{}\n".format(ows))
    ConfigFile.write(" SAG -{}\n".format(sag))
    ConfigFile.write(" UNK -{}\n".format(unk))
    ConfigFile.write("#-----------Pager Control Tone Group Output? (Y/N)---------------\n")
    ConfigFile.write("#     01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20\n")
    ConfigFile.write("#     -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --\n")
    page_c=''.join([d_c[v.get()] for v in v_list2])
    ConfigFile.write("      {}\n".format(page_c))
    ConfigFile.write("{} - Flow Control Pager Line SS#, Last Sequence # On     \n".format(v51.get()))
    ConfigFile.write("#                  (For All Flow Controlled Pagers Enter '9999  9999')\n")
    ConfigFile.write("#                  (When Entering Individual SS#, Last Entry is '   0     0')\n")
    ConfigFile.write("{} - Capacitance Multiplier                                   \n".format(str.format('{0:.3f}', v52.get())))
    ConfigFile.write("#--------------------------------------------------------------------------------\n")
    ConfigFile.write("\n")
    ConfigFile.write("# Bus and Bulk Power Capacitor Output Options: ----------------------------------\n")
    ConfigFile.write(" {} - Time (hhmm)                                              \n".format(v53.get()))
    ConfigFile.write(" {} - Day Code (0-Weekday, 1-Saturday, 2-Sunday, 3-Holiday)       \n".format(v54.get()))
    ConfigFile.write(" {} - Initial Capacitance Option                                  \n".format(v55.get()))
    ConfigFile.write("#            0 - Zero\n")
    ConfigFile.write("#            1 - Total Installed Value\n")
    ConfigFile.write("#            2 - Total On Value\n")
    ConfigFile.write(" {} - Voltage On Limit Option                                     \n".format(v56.get()))
    ConfigFile.write("#            1 - Use Minimum On Voltage Limit for Switching On\n")
    ConfigFile.write("#            2 - Use Maximum On Voltage Limit for Switching On\n")
    ConfigFile.write("#            3 - Use Average On Voltage Limit for Switching On\n")
    ConfigFile.write(" {} - Voltage Off Limit Option                                    \n".format(v57.get()))
    ConfigFile.write("#            1 - Use Minimum Off Voltage Limit for Switching Off\n")
    ConfigFile.write("#            2 - Use Maximum Off Voltage Limit for Switching Off\n")
    ConfigFile.write("#            3 - Use Average Off Voltage Limit for Switching Off\n")
    ConfigFile.write(" {} - Capacitance Multiplier                                 \n".format(str.format('{0:.4f}', v58.get())))
    ConfigFile.write("#--------------------------------------------------------------------------------\n")
    ConfigFile.write("\n")
    ConfigFile.write("# Transmission Rating Options: --------------------------------------------------\n")
    ConfigFile.write(" {} - Output Rating Type (S-Summer, W-Winter)                     \n".format(v59.get()))
    ConfigFile.write(" {} - Check Conductor?                                 (Y/Z/N)    \n".format(v60.get()))
    ConfigFile.write(" {} - Check Transformer?                               (Y/Z/N)    \n".format(v61.get()))
    ConfigFile.write(" {} - Check Breaker?                                   (Y/Z/A/B/N)\n".format(v62.get()))
    ConfigFile.write(" {} - Check Disc   Switch?                             (Y/Z/A/B/N)\n".format(v63.get()))
    ConfigFile.write(" {} - Check Bypass Switch?                             (Y/Z/A/B/N)\n".format(v64.get()))
    ConfigFile.write(" {} - Check Dual   Switch?                             (Y/Z/A/B/N)\n".format(v65.get()))
    ConfigFile.write(" {} - Check Bus    Switch?                             (Y/Z/A/B/N)\n".format(v66.get()))
    ConfigFile.write(" {} - Check Line   Switch?                             (Y/Z/A/B/N)\n".format(v67.get()))
    ConfigFile.write(" {} - Check Current Transformer?                       (Y/Z/A/B/N)\n".format(v68.get()))
    ConfigFile.write(" {} - Check Wavetrap?                                  (Y/Z/A/B/N)\n".format(v69.get()))
    ConfigFile.write(" {} - Check Circuit Connector?                         (Y/Z/A/B/N)\n".format(v70.get()))
    ConfigFile.write(" {} - Check Buswork?                                   (Y/Z/A/B/N)\n".format(v71.get()))
    ConfigFile.write(" {} - Check Sag Limit?                                 (Y/Z/N)    \n".format(v72.get()))
    ConfigFile.write(" {} - Check MISO Base Model Rating?                    (Y/Z/N)    \n".format(v73.get()))
    ConfigFile.write(" {} - Check Interconnection Limit?                     (Y/Z/N)    \n".format(v74.get()))
    ConfigFile.write("#            Y - Yes, Use Rating Data\n")
    ConfigFile.write("#            Z - Yes, Use Rating Data, Don't Use to Calculate Minimum\n")
    ConfigFile.write("#            A - Yes, Use Nameplate Amp Data\n")
    ConfigFile.write("#            B - Yes, Use Nameplate Amp Data, Don't Use to Calculate Minimum\n")
    ConfigFile.write("#            N - No\n")
    ConfigFile.write(" {} - Check Time Over Current Relay Loadability Limit? (N/P/R/O/Q)\n".format(v75.get()))
    ConfigFile.write(" {} - Check Impedance Relay Loadability Limit?         (N/P/R/O/Q)\n".format(v76.get()))
    ConfigFile.write("#            N - Don't Check\n")
    ConfigFile.write("#            P - Check Using Rating Multiplier of 1.0\n")
    ConfigFile.write("#            R - Check Using Rating Multiplier of 1.0,\n")
    ConfigFile.write("#                  Don't Use to Calculate Minimum\n")
    ConfigFile.write("#            O - Check Using Rating Multiplier of 1.2\n")
    ConfigFile.write("#            Q - Check Using Rating Multiplier of 1.2,\n")
    ConfigFile.write("#                  Don't Use to Calculate Minimum\n")
    ConfigFile.write(" {} - Output Branch Mileage in Place of Rating?        ( /N/L/S)  \n".format(v77.get()))
    ConfigFile.write("#            Blank - Output Ratings\n")
    ConfigFile.write("#            N - Output Mileage in Place of Normal Rating\n")
    ConfigFile.write("#            L - Output Mileage in Place of LTE    Rating\n")
    ConfigFile.write("#            S - Output Mileage in Place of STE    Rating\n")
    ConfigFile.write(" {} - Overwrite Emergency Ratings?                     (N/L/S)    \n".format(v78.get()))
    ConfigFile.write("#            N - No Change (Rate B = LTE; Rate C = STE)\n")
    ConfigFile.write("#            L - Output LTE in Place of STE Rating (Rate B = Rate C = LTE)\n")
    ConfigFile.write("#            S - Output STE in Place of LTE Rating (Rate B = Rate C = STE)\n")
    ConfigFile.write(" {} - Psse branch rating file output code              (Y/N)      \n".format(v79.get()))
    ConfigFile.write("#            Y - If none of the three ratings are set, output branch entry\n")
    ConfigFile.write("#            N - If none of the three ratings are set, dont output branch entry\n")
    ConfigFile.write(" {} - Check Ring Bus Breakers?                         (Y/N)      \n".format(v80.get()))
    ConfigFile.write(" {} - Check Ring Bus Disc   Switch?                    (Y/N)      \n".format(v81.get()))
    ConfigFile.write(" {} - Check Ring Bus Bypass Switch?                    (Y/N)      \n".format(v82.get()))
    ConfigFile.write(" {} - Check Ring Bus Dual   Switch?                    (Y/N)      \n".format(v83.get()))
    ConfigFile.write(" {} - Check Ring Bus Bus    Switch?                    (Y/N)      \n".format(v84.get()))
    ConfigFile.write(" {} - Check Ring Bus Line   Switch?                    (Y/N)      \n".format(v85.get()))
    ConfigFile.write(" {} - Check Ring Bus Current Transformers?             (Y/N)      \n".format(v86.get()))
    ConfigFile.write(" {} - Check Ring Bus Wavetraps?                        (Y/N)      \n".format(v87.get()))
    ConfigFile.write(" {} - Check Ring Bus Circuit Connectors?               (Y/N)      \n".format(v88.get()))
    ConfigFile.write(" {} - Check Ring Bus Buswork?                          (Y/N)      \n".format(v89.get()))
    ConfigFile.write("#--------------------------------------------------------------------------------\n")
    ConfigFile.write("\n")
    ConfigFile.write("# High-Voltage Distribution Rating Options: -------------------------------------\n")
    ConfigFile.write(" {} - Output Rating Type (S-Summer, W-Winter)                     \n".format(v90.get()))
    ConfigFile.write(" {} - Check Conductor?                                 (Y/Z/N)    \n".format(v91.get()))
    ConfigFile.write(" {} - Check Transformer?                               (Y/Z/N)    \n".format(v92.get()))
    ConfigFile.write(" {} - Check Breaker?                                   (Y/Z/A/B/N)\n".format(v93.get()))
    ConfigFile.write(" {} - Check Disc   Switch?                             (Y/Z/A/B/N)\n".format(v94.get()))
    ConfigFile.write(" {} - Check Bypass Switch?                             (Y/Z/A/B/N)\n".format(v95.get()))
    ConfigFile.write(" {} - Check Dual   Switch?                             (Y/Z/A/B/N)\n".format(v96.get()))
    ConfigFile.write(" {} - Check Bus    Switch?                             (Y/Z/A/B/N)\n".format(v97.get()))
    ConfigFile.write(" {} - Check Line   Switch?                             (Y/Z/A/B/N)\n".format(v98.get()))
    ConfigFile.write(" {} - Check Current Transformer?                       (Y/Z/A/B/N)\n".format(v99.get()))
    ConfigFile.write(" {} - Check Wavetrap?                                  (Y/Z/A/B/N)\n".format(v100.get()))
    ConfigFile.write(" {} - Check Circuit Connector?                         (Y/Z/A/B/N)\n".format(v101.get()))
    ConfigFile.write(" {} - Check Buswork?                                   (Y/Z/A/B/N)\n".format(v102.get()))
    ConfigFile.write(" {} - Check Sag Limit?                                 (Y/Z/N)    \n".format(v103.get()))
    ConfigFile.write(" {} - Check MISO Base Model Rating?                    (Y/Z/N)    \n".format(v104.get()))
    ConfigFile.write(" {} - Check Interconnection Limit?                     (Y/Z/N)    \n".format(v105.get()))
    ConfigFile.write("#            Y - Yes, Use Rating Data\n")
    ConfigFile.write("#            Z - Yes, Use Rating Data, Don't Use to Calculate Minimum\n")
    ConfigFile.write("#            A - Yes, Use Nameplate Amp Data\n")
    ConfigFile.write("#            B - Yes, Use Nameplate Amp Data, Don't Use to Calculate Minimum\n")
    ConfigFile.write("#            N - No\n")
    ConfigFile.write(" {} - Check Time Over Current Relay Loadability Limit? (N/P/R/O/Q)\n".format(v106.get()))
    ConfigFile.write(" {} - Check Impedance Relay Loadability Limit?         (N/P/R/O/Q)\n".format(v107.get()))
    ConfigFile.write("#            N - Don't Check\n")
    ConfigFile.write("#            P - Check Using Rating Multiplier of 1.0\n")
    ConfigFile.write("#            R - Check Using Rating Multiplier of 1.0,\n")
    ConfigFile.write("#                  Don't Use to Calculate Minimum\n")
    ConfigFile.write("#            O - Check Using Rating Multiplier of 1.2\n")
    ConfigFile.write("#            Q - Check Using Rating Multiplier of 1.2,\n")
    ConfigFile.write("#                  Don't Use to Calculate Minimum\n")
    ConfigFile.write(" {} - Output Branch Mileage in Place of Rating?        ( /N/L/S)  \n".format(v108.get()))
    ConfigFile.write("#            Blank - Output Ratings\n")
    ConfigFile.write("#            N - Output Mileage in Place of Normal Rating\n")
    ConfigFile.write("#            L - Output Mileage in Place of LTE    Rating\n")
    ConfigFile.write("#            S - Output Mileage in Place of STE    Rating\n")
    ConfigFile.write(" {} - Overwrite Emergency Ratings?                     (N/L/S)    \n".format(v109.get()))
    ConfigFile.write("#            N - No Change (Rate B = LTE; Rate C = STE)\n")
    ConfigFile.write("#            L - Output LTE in Place of STE Rating (Rate B = Rate C = LTE)\n")
    ConfigFile.write("#            S - Output STE in Place of LTE Rating (Rate B = Rate C = STE)\n")
    ConfigFile.write(" {} - Psse branch rating file output code              (Y/N)      \n".format(v110.get()))
    ConfigFile.write("#            Y - If none of the three ratings are set, output branch entry\n")
    ConfigFile.write("#            N - If none of the three ratings are set, dont output branch entry\n")
    ConfigFile.write(" {} - Check Ring Bus Breakers?                         (Y/N)      \n".format(v111.get()))
    ConfigFile.write(" {} - Check Ring Bus Disc   Switch?                    (Y/N)      \n".format(v112.get()))
    ConfigFile.write(" {} - Check Ring Bus Bypass Switch?                    (Y/N)      \n".format(v113.get()))
    ConfigFile.write(" {} - Check Ring Bus Dual   Switch?                    (Y/N)      \n".format(v114.get()))
    ConfigFile.write(" {} - Check Ring Bus Bus    Switch?                    (Y/N)      \n".format(v115.get()))
    ConfigFile.write(" {} - Check Ring Bus Line   Switch?                    (Y/N)      \n".format(v116.get()))
    ConfigFile.write(" {} - Check Ring Bus Current Transformers?             (Y/N)      \n".format(v117.get()))
    ConfigFile.write(" {} - Check Ring Bus Wavetraps?                        (Y/N)      \n".format(v118.get()))
    ConfigFile.write(" {} - Check Ring Bus Circuit Connectors?               (Y/N)      \n".format(v119.get()))
    ConfigFile.write(" {} - Check Ring Bus Buswork?                          (Y/N)      \n".format(v120.get()))
    ConfigFile.write("#--------------------------------------------------------------------------------\n")
    ConfigFile.write("\n")
    ConfigFile.write("# PSSE and SSAM Output Options: -------------------------------------------------\n")
    ConfigFile.write("#\n")
    ConfigFile.write("# Transformer Delta/Wye 30 Degree Angular Shift:\n")
    ConfigFile.write(" {} - Create Delta/Wye 30 Degree Angular Shift? (Y/N)             \n".format(v121.get()))
    ConfigFile.write("#\n")
    ConfigFile.write("# Line Branch Impedance:\n")
    ConfigFile.write("#   If line branch impedance < Line Branch Minimum Impedance Allowed,\n")
    ConfigFile.write("#     reset resistance = 0\n")
    ConfigFile.write("#           reactance  = Line Branch Zero Reactance Value\n")
    ConfigFile.write("#           charging   = 0\n")
    ConfigFile.write("#   When creating SSAM files, a branch impedance will not equal the total\n")
    ConfigFile.write("#     of its segment impedances if the branch impedance is reset\n")
    ConfigFile.write(" {} - Line Branch Zero Reactive Value (PU)                  \n".format(str.format('{0:.5f}', v122.get())))
    ConfigFile.write(" {} - Line Branch Minimum Impedance Allowed (PU)            \n".format(str.format('{0:.5f}', v123.get())))
    ConfigFile.write("#\n")
    ConfigFile.write("# Tie Branch Impedance:\n")
    ConfigFile.write("#   If a tie branch connects two buses with bulk power capacitors,\n")
    ConfigFile.write("#     set  resistance = 0\n")
    ConfigFile.write("#          reactance  = Tie Branch Zero Reactance Value\n")
    ConfigFile.write("#          charging   = 0\n")
    ConfigFile.write("#     else resistance = charging = 0, reactance = .00001\n")
    ConfigFile.write(" {} - Tie Branch Zero Reactive Value (PU)                   \n".format(str.format('{0:.5f}', v124.get())))
    ConfigFile.write("#\n")
    ConfigFile.write("# Distribution Circuit:\n")
    ConfigFile.write(" {} - Allocate Bus Load to Distribution Circuits? (Y/N)           \n".format(v125.get()))
    ConfigFile.write("#\n")
    ConfigFile.write("# Distribution Capacitor:\n")
    ConfigFile.write(" {} - Distribution Capacitor Load Model Code (S/M)                \n".format(v126.get()))
    ConfigFile.write("#            S - Model Total of All Capacitors as Load ID 2\n")
    ConfigFile.write("#            M - Model Capacitors as Multiple Load ID Entries as Follows:\n")
    ConfigFile.write("#                  Distribution Circuit Number < 40    - PSS/E Load ID = 2\n")
    ConfigFile.write("#                  Distribution Circuit Number = 40-49 - PSS/E Load ID = 3\n")
    ConfigFile.write("#                  Distribution Circuit Number = 50-59 - PSS/E Load ID = 4\n")
    ConfigFile.write("#                  Distribution Circuit Number = 60-69 - PSS/E Load ID = 5\n")
    ConfigFile.write("#                  Distribution Circuit Number = 70-79 - PSS/E Load ID = 6\n")
    ConfigFile.write("#                  Distribution Circuit Number = 80-89 - PSS/E Load ID = 7\n")
    ConfigFile.write("#\n")
    ConfigFile.write("# 138/46kv and 138/ind Transformer Meter Move:\n")
    ConfigFile.write(" {} - Move 138/46kv and 138/ind Xfmrs to 138kv Area? (Y/N)        \n".format(v127.get()))
    ConfigFile.write("#            This option will reset the midpoint and tertiary of all 138/46kv\n")
    ConfigFile.write("#            and 138/industrial 3-winder transformers to the 138kv area\n")
    ConfigFile.write("#            (area 1 or 23). It will also move the meter end of all 138/46kv\n")
    ConfigFile.write("#            and 138/industrial 2-winder transformers to the 46kv bus.\n")
    ConfigFile.write("#\n")
    ConfigFile.write("#--------------------------------------------------------------------------------\n")
    ConfigFile.write("\n")
    ConfigFile.write("# Output Options: ---------------------------------------------------------------\n")
    ConfigFile.write(" {} - Create Table Data Dump?                                (Y/N)\n".format(v128.get()))
    ConfigFile.write(" {} - Create Branch Rating Listing                                \n".format(v129.get()))
    ConfigFile.write("#            N - No Output\n")
    ConfigFile.write("#            A - Output Amp Ratings\n")
    ConfigFile.write("#            M - Output MVA Ratings\n")
    ConfigFile.write(" {} - Create SSAM Files                                           \n".format(v130.get()))
    ConfigFile.write("#            N - No Output\n")
    ConfigFile.write("#            I - Create with Interchange Load Set to Zero\n")
    ConfigFile.write("#            Y - Create with Interchange Load Not Set to Zero\n")
    ConfigFile.write(" N - Use PSSE Three Winder Card (Elim Midpnt Bus)                \n")
    ConfigFile.write(" {} - Create PSSE Loadflow File                                   \n".format(v131.get()))
    ConfigFile.write("#            N  - No Output\n")
    ConfigFile.write("#            34 - Version 34 Format\n")
    ConfigFile.write("#            33 - Version 33 Format\n")
    ConfigFile.write("#            32 - Version 32 Format\n")
    ConfigFile.write("#            30 - Version 30 Format\n")
    ConfigFile.write(" {} - Create PSSE Sequence File                                   \n".format(v132.get()))
    ConfigFile.write("#            N  - No Output\n")
    ConfigFile.write("#            33 - Version 33 Format\n")
    ConfigFile.write("#            32 - Version 32 Format\n")
    ConfigFile.write("#            30 - Version 30 Format\n")
    ConfigFile.write(" {} - Create PSSE Branch Ratings File                             \n".format(v133.get()))
    ConfigFile.write("#            N  - No Output\n")
    ConfigFile.write("#            34 - Version 34 Format\n")
    ConfigFile.write("#            33 - Version 33 Format\n")
    ConfigFile.write("#            32 - Version 32 Format\n")
    ConfigFile.write("#            30 - Version 30 Format\n")
    ConfigFile.write(" {} - Create PSSE Distribution Capacitor File                     \n".format(v134.get()))
    ConfigFile.write("#            N  - No Output\n")
    ConfigFile.write("#            33 - Version 33 Format\n")
    ConfigFile.write("#            32 - Version 32 Format\n")
    ConfigFile.write("#            30 - Version 30 Format\n")
    ConfigFile.write(" {} - Create DCM  Capacitor File?                            (Y/N)\n".format(v135.get()))
    ConfigFile.write(" {} - Create DCM  Capacitor Data Dump File?                  (Y/N)\n".format(v136.get()))
    ConfigFile.write(" {} - Create MAV  File?                                      (Y/N)\n".format(v137.get()))
    ConfigFile.write(" {} - Create 1147 File?                                      (Y/N)\n".format(v138.get()))
    ConfigFile.write("     Database          Data Label - 'PREVIOUS YR '               \n")
    ConfigFile.write("     PSSE Summary File Data Label - 'LOAD SEARCH '               \n")
    ConfigFile.write("     Max Load Sum File - 'maxloadsummary                  '      \n")
    ConfigFile.write("     PSSE Summary File - 'pssesummary                     '      \n")
    ConfigFile.write("     Area   2 - User - ALR  (ADRIAN)                             \n")
    ConfigFile.write("     Area   3 - User - ERM  (ALMA)                               \n")
    ConfigFile.write("     Area   4 - User - ERM  (AU SABLE)                           \n")
    ConfigFile.write("     Area   5 - User - WEE  (BAY CITY)                           \n")
    ConfigFile.write("     Area   6 - User - ALR  (BATTLE CREEK)                       \n")
    ConfigFile.write("     Area   7 - User - DAL  (BELDING)                            \n")
    ConfigFile.write("     Area   8 - User - WEE  (FLINT)                              \n")
    ConfigFile.write("     Area   9 - User - DAL  (GRAND RAPIDS RURAL)                 \n")
    ConfigFile.write("     Area  10 - User - DAL  (GRAND RAPIDS URBAN)                 \n")
    ConfigFile.write("     Area  11 - User - ERM  (HIGGINS)                            \n")
    ConfigFile.write("     Area  12 - User - ALR  (JACKSON)                            \n")
    ConfigFile.write("     Area  13 - User - DAL  (KALAMAZOO)                          \n")
    ConfigFile.write("     Area  14 - User - ALR  (LANSING)                            \n")
    ConfigFile.write("     Area  15 - User - DAL  (MECOSTA)                            \n")
    ConfigFile.write("     Area  16 - User - ERM  (MIDLAND)                            \n")
    ConfigFile.write("     Area  17 - User - DAL  (MUSKEGON)                           \n")
    ConfigFile.write("     Area  18 - User - DAL  (NORTHWEST)                          \n")
    ConfigFile.write("     Area  19 - User - ALR  (OWOSSO)                             \n")
    ConfigFile.write("     Area  20 - User - ERM  (PETOSKEY)                           \n")
    ConfigFile.write("     Area  21 - User - WEE  (SAGINAW)                            \n")
    ConfigFile.write(" {} - Create Group/Subgroup Contingency Files?               (Y/N)\n".format(v139.get()))
    ConfigFile.write(" {} - Create Generator Contingency Files?                    (Y/N)\n".format(v140.get()))
    ConfigFile.write(" {} - Create Capacitor Contingency Files?                    (Y/N)\n".format(v141.get()))
    ConfigFile.write(" {} - Create Plant     Contingency Files?                    (Y/N)\n".format(v142.get()))
    ConfigFile.write(" {} - Create Open Sectionalizing Device Contingency Files?   (Y/N)\n".format(v143.get()))
    ConfigFile.write("     {} - Contingency Output Code                                 \n".format(v144.get()))
    ConfigFile.write("#              Y - Output Fast, Slow, Manual and Rating Only Devices\n")
    ConfigFile.write("#              N - Output Only Fast, Slow, and Manual Devices\n")
    ConfigFile.write("     {} - Create Open 345KV Breaker         Contingencies?   (Y/N)\n".format(v145.get()))
    ConfigFile.write("     {} - Create Open 345KV Bus  Switch     Contingencies?   (Y/N)\n".format(v146.get()))
    ConfigFile.write("     {} - Create Open 345KV Line Switch     Contingencies?   (Y/N)\n".format(v147.get()))
    ConfigFile.write("     {} - Create Open 69-138KV Breaker      Contingencies?   (Y/N)\n".format(v148.get()))
    ConfigFile.write("     {} - Create Open 69-138KV Bus  Switch  Contingencies?   (Y/N)\n".format(v149.get()))
    ConfigFile.write("     {} - Create Open 69-138KV Line Switch  Contingencies?   (Y/N)\n".format(v150.get()))
    ConfigFile.write("     {} - Create Open 23,46KV  Breaker      Contingencies?   (Y/N)\n".format(v151.get()))
    ConfigFile.write("     {} - Create Open 23,46KV  Bus  Switch  Contingencies?   (Y/N)\n".format(v152.get()))
    ConfigFile.write("     {} - Create Open 23,46KV  Line Switch  Contingencies?   (Y/N)\n".format(v153.get()))
    ConfigFile.write("     {} - Create Open Low KV  Breaker       Contingencies?   (Y/N)\n".format(v154.get()))
    ConfigFile.write("     {} - Create Open Low KV  Bus  Switch   Contingencies?   (Y/N)\n".format(v155.get()))
    ConfigFile.write("     {} - Create Open Low KV  Line Switch   Contingencies?   (Y/N)\n".format(v156.get()))
    ConfigFile.write(" {} - Create Ring Bus Breaker Fail-to-Open Contingency  \n".format(v157.get()))
    ConfigFile.write("#            Files?                                             (G/S/N)\n")
    ConfigFile.write("#          G - Create Group Files\n")
    ConfigFile.write("#          S - Create Subgroup Files\n")
    ConfigFile.write("#          N - Dont Create Files\n")
    ConfigFile.write(" {} - Override Ring Bus Breaker Fail-to-Open Outage Rate (-1.0 - Do not override)\n".format(str.format('{0:.5f}', v158.get())))
    ConfigFile.write(" {} - Create Buses Which Must Not Be Shed File and Fast           \n".format(v159.get()))
    ConfigFile.write("#            Sectionalizing Equipment File?                       (Y/N)\n")
    ConfigFile.write("     {} - Shed Interchange (INT) Buses?                      (Y/N)\n".format(v160.get()))
    ConfigFile.write("     {} - Shed Wholesale Power (WHSP) Buses?                 (Y/N)\n".format(v161.get()))
    ConfigFile.write("     {} - Shed Wholesale Transmission (WHST) Buses?          (Y/N)\n".format(v162.get()))
    ConfigFile.write("     {} - Shed SEC (SEC) Buses?                              (Y/N)\n".format(v163.get()))
    ConfigFile.write("     {} - Shed Generator (GEN) Buses?                        (Y/N)\n".format(v164.get()))
    ConfigFile.write("     {} - Shed Consumers Energy HQ (HEAD) Buses?             (Y/N)\n".format(v165.get()))
    ConfigFile.write("     {} - Shed Hospital (HOSP) Buses?                        (Y/N)\n".format(v166.get()))
    ConfigFile.write("     {} - Shed Not-to-Be-Shed (SHED) Buses?                  (Y/N)\n".format(v167.get()))
    ConfigFile.write("     {} - Shed Customer Sub - Not Regulated (CSNR) Buses?    (Y/N)\n".format(v168.get()))
    ConfigFile.write("     {} - Shed Welder Sub (WELD) Buses?                      (Y/N)\n".format(v169.get()))
    ConfigFile.write(" {} - Create Contingency Analysis Auxiliary Data Base?       (Y/N)\n".format(v170.get()))
    ConfigFile.write(" {} - Create BTF Database Files?                             (Y/N)\n".format(v171.get()))
    ConfigFile.write(" {} - Create Breaker Duty Files?                             (Y/N)\n".format(v172.get()))
    ConfigFile.write(" {} - Create Equipment Listing?                              (Y/N)\n".format(v173.get()))
    ConfigFile.write(" {} - Create p1145 PSSE File?                                (Y/N)\n".format(v174.get()))
    ConfigFile.write(" {} - Create Relay Loadability Data Listing?                 (Y/N)\n".format(v175.get()))
    ConfigFile.write(" {} - Create Load Search Station Data File?                (Y/C/N)\n".format(v176.get()))
    ConfigFile.write("#            N - No Output\n")
    ConfigFile.write("#            C - Create with No Station Name / Bus Name Cross Reference\n")
    ConfigFile.write("#            Y - Create with With Station Name / Bus Name Cross Reference\n")
    ConfigFile.write("#--------------------------------------------------------------------------------\n")



def py1120():
    create_configuration_file()
    s1=db_dir2.get()
    s2=op_dir2.get()+'\\temp.config'
    s3=op_dir2.get()
    os.chdir(s3)  
    os.system('setlocal')
    command_bash='python K:\\ModelsResource\\bin\\p1120.py -d "'+s1+'"  -o "'+s2+'" > p1120.logfile'
    #print(command_bash)
    os.system(command_bash)
    return

    
Button(frame2,text = "run p1120",width=15,command = py1120).grid(row=357, column=1, columnspan=2, sticky = W, padx=5, pady = 2)
    
    

root.mainloop()  


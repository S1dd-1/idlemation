# import modules
import os
import sys

import csv
import subprocess

import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
from tkinter import colorchooser

import converter   # converter.py module

# path for icon
def resource_path(relative):
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), relative)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative)

# path for other stuff like Animations folder, config.csv
def get_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)   # folder where the EXE is
    else:
        return os.path.dirname(os.path.abspath(__file__))

# creates the config file
# -> b! indicates the field is a button
# -> d! indicates the field is a drop down list
# -> s! indicates the field is a slider
# -> c! indicates the field is a colour picker
# -> # indicates the field is a comment
# -> ! indicates the field is an internal flag
def config_initialize():

    with open(config_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        Config = [
            ["b!run_on_startup", "Y"],
            ["d!animation_module", "ANIM_default"],
            ["b!random_animation", "N"],
            ["ms_delay", "100"],
            ["horizontal_offset", "0"],
            ["horizontal_fraction", "3"],
            ["vertical_offset", "0"],
            ["vertical_fraction", "1"],
            ["b!borderless", "Y"],
            ["s!opacity", "1.0"],
            ["c!background_colour", "#000000"],
            ["font", "Consolas"],
            ["font_size", "5"],
            ["c!font_colour", "#FFFFFF"],
            ["taskbar_height", "48"],
            ["!run","N"],
            ["!bg_dark","Y"],
            ["!scale","5"]
        ]
        writer.writerows(Config)
        
base_dir = get_path()

# calls config file creation if it doesn't exist
try:
    config_path = os.path.join(base_dir, "config.csv")
    f = open(config_path, "r")
    f.close()
except FileNotFoundError:
    config_initialize()

with open(config_path, 'r') as configfile:
    reader = csv.reader(configfile)
    config_dict = {row[0]: row[1] for row in reader if len(row) == 2}

# main()

# entry creation with placeholder handler
def entry_handler(key, r, c):
    placeholder = config_dict[key]

    en = tk.Entry(root)
    en.grid(row=r, column=c, padx=5, pady=5, sticky="ew")
    en.insert(0,placeholder)
    en.config(fg = "#808080")
    
    def click(event):
        en.delete(0,'end')
        en.config(fg = "#FFFFFF" if config_dict["!bg_dark"] == "Y" else "#000000")

    def change(event):
        config_dict[key] = placeholder = en.get()
        save_config()
        en.delete(0,'end')
        en.insert(0,placeholder)
        en.config(fg = "#808080")
        root.focus()
    
    en.bind("<Button-1>", click)
    en.bind("<Return>", change)
    en.bind("<FocusOut>", change)

# save changes to the config file
def save_config():
    rows = [[k,v] for k,v in config_dict.items()]

    with open(config_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

# run and stop animation
def run_an():
    run_b.config(text = "Stop")
    run_b.config(bg = "#E93030")
    run_b.config(command = stop_an)
    config_dict["!run"] = "Y"
    save_config()

    base_dir = get_path()

    engine_path = os.path.join(base_dir, "engine.exe")

    # runs engine.exe independantly from idlemation.exe
    subprocess.Popen([engine_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False)
def stop_an():
    run_b.config(text = "Run")
    run_b.config(bg = "#2ABD42")
    run_b.config(command = run_an)
    config_dict["!run"] = "N"
    save_config()

# import animation video and turn it into a module
def import_mod():

    # open file explorer
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Video files", "*.mp4 *.avi"), ("All files", "*.*")]
    )
    if not file_path:
        return

    anim_names.append(os.path.splitext(os.path.basename(file_path))[0])
    refresh_dropdown(col_drop, selected, anim_names)

    # calls converter.py which turns it into ASCII module
    converter.import_vid(file_path, config_dict["!scale"])

# button ON / OFF handler
def but_n(k, btn):
    btn.config(text="Off", command=lambda: but_y(k, btn))
    btn.config(bg = "#E93030")
    config_dict[k] = "N"
    save_config()
def but_y(k, btn):
    btn.config(text="On", command=lambda: but_n(k, btn))
    btn.config(bg = "#2ABD42")
    config_dict[k] = "Y"
    save_config()

# slider handler
def update_scale(key, var):
    config_dict[key] = str(round(var.get(), 2))
    save_config()

# dark mode / light mode handler
def change_mode(bg, fg):
    root.config(bg=bg)
    for w in root.winfo_children():
        if w in n_buttons.values():
            continue
        elif w in c_buttons.values():
            continue
        elif w == run_b:
            continue
        elif isinstance(w, tk.Entry):
            w.config(bg=bg)
        elif isinstance(w, tk.OptionMenu):
            w.config(bg=bg, fg=fg)
            w["menu"].config(bg=bg, fg=fg)
        else:
            try:
                w.config(bg=bg, fg=fg)
            except:
                pass

    save_config()
def light_mode():
    config_dict["!bg_dark"] = "N"
    bg = "#FFFFFF"
    fg = "#000000"
    but_d.config(text="dark mode")
    but_d.config(command = dark_mode)
    but_d.config(activebackground="#D6D6D6", activeforeground="#000000")
    col_drop.config(activebackground="#D6D6D6", activeforeground="#000000")
    imp_b.config(activebackground="#D6D6D6", activeforeground="#000000")
    
    change_mode(bg,fg)
def dark_mode():
    config_dict["!bg_dark"] = "Y"
    bg = "#353535"
    fg = "#FFFFFF"
    but_d.config(text="light mode")
    but_d.config(command = light_mode)
    but_d.config(activebackground="#545454", activeforeground="#FFFFFF")
    col_drop.config(activebackground="#545454", activeforeground="#FFFFFF")
    imp_b.config(activebackground="#545454", activeforeground="#FFFFFF")
    
    change_mode(bg,fg)

# changes the animation from drop down input
def set_animation(value):
    config_dict["d!animation_module"] = "ANIM_" + value
    save_config()

# colour picker handler
def colour_chooser(k):
    colour = colorchooser.askcolor(title="Pick a colour")
    if colour[1]:
        config_dict[k] = colour[1]
        save_config()
        c_buttons[k].config(bg=colour[1])

# drop down handler
def refresh_dropdown(optionmenu, variable, items):
    menu = optionmenu["menu"]
    menu.delete(0, "end")

    for item in items:
        def callback(value=item):
            variable.set(value)
            set_animation(value)

        menu.add_command(label=item, command=callback)

# main() 2: electric boogaloo
root = tk.Tk()
root.iconbitmap(resource_path("idlemation_icon.ico"))
root.title("Idlemation")

default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=11, family="Courier")
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(4, weight=1)

# phantom spacer columns
phantom1 = tk.Label(root, text = "  ")
phantom1.grid(row=0, column=1, padx = 15)
phantom2 = tk.Label(root, text = "  ")
phantom2.grid(row=0, column=3, padx = 15)
phantom3 = tk.Label(root, text = "  ")
phantom3.grid(row=0, column=5, padx = 15)

C1 = list(config_dict.keys())
n_buttons = {} # normal buttons
c_buttons = {} # colour buttons

for i in range(len(C1)):
    key = C1[i]

    # ignore internal flags
    if key.startswith("!"):
        continue
    
    # normal button initialize
    elif key.startswith("b!"):
        tk.Label(root, text=key[2:].replace("_"," ")).grid(row=i, column=0, padx=5, pady=5)

        txt = "ON" if config_dict[key] == "Y" else "OFF"
        col = "#2ABD42" if config_dict[key] == "Y" else "#E93030"
        btn = tk.Button(root, text=txt, bg = col)

        if config_dict[key] == "Y":
            btn.config(command=lambda k=key, b=btn: but_n(k, b))
        else:
            btn.config(command=lambda k=key, b=btn: but_y(k, b))

        n_buttons[key] = btn
        btn.grid(row=i, column=2, padx=5, pady=5, sticky="ew")

    # slider initialize
    elif key.startswith("s!"):
        tk.Label(root, text=key[2:].replace("_"," ")).grid(row=i, column=0, padx=5, pady=5)

        vs = tk.DoubleVar(value=float(config_dict[key]))

        scale = tk.Scale(root, from_=0, to=1, orient="horizontal", resolution=0.01, variable=vs, highlightthickness=0)
        scale.grid(row=i, column=2, padx=5, pady=5, sticky="ew")

        scale.bind("<ButtonRelease-1>", lambda e, k=key, v=vs: update_scale(k, v))
    
    # drop down initialize
    elif key.startswith("d!"):
        tk.Label(root, text=key[2:].replace("_"," ")).grid(row=i, column=0, padx=5, pady=5)
        selected = tk.StringVar(value="select module")
            
        animations_path = os.path.join(base_dir, "Animations")
        anim_files = [
            f for f in os.listdir(animations_path)
            if f.startswith("ANIM_") and f.endswith(".txt")
        ]

        anim_names = [i.split("ANIM_")[1][:-4] for i in anim_files]
        if not anim_names:  
            anim_names = ["default"]

        current = config_dict.get("d!animation_module", "ANIM_default")[5:]
        selected.set(current)

        col_drop = tk.OptionMenu(root, selected, *anim_names, command=set_animation)
        col_drop.grid(row=i, column=2, padx=5, pady=5, sticky="ew")

    # colour picker initialize
    elif key.startswith("c!"):
        tk.Label(root, text=key[2:].replace("_"," ")).grid(row=i, column=0, padx=5, pady=5)
        c_buttons[key] = tk.Button(root, text="", bg=config_dict[key], command=lambda k=key: colour_chooser(k))
        c_buttons[key].grid(row=i, column=2, padx=5, pady=5, sticky="ew")

    # entry initialize
    else:
        tk.Label(root, text=key.replace("_"," ")).grid(row=i, column=0, padx=5, pady=5)

        entry_handler(key, i, 2)

# run/stop animation button initialize
txt = "Stop" if config_dict["!run"] == "Y" else "Run"
cmd  = stop_an if config_dict["!run"] == "Y" else run_an
col1 = "#E93030" if config_dict["!run"] == "Y" else "#2ABD42"
run_b = tk.Button(root, text=txt, command=cmd, bg = col1)
run_b.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

# import video button and scale specifier initialize
tk.Label(root, text="import video").grid(row=2, column=4, padx=5, pady=5)
tk.Label(root, text="resolution factor").grid(row=3, column=4, padx=5, pady=5)
entry_handler("!scale", 4, 4)
imp_b = tk.Button(root,text = "select video", command = import_mod)
imp_b.grid(row=5, column=4, padx=5, pady=5, sticky="ew")

# extra info initialize
text = '''
        COMMENTS        

1. Press ESCAPE when an-
-mation is in focus to  
stop it                 

2. When specifying reso-
-lution, you will have  
to manually adjust the  
font size or window size
so it looks ok          

3. Horizontal offset st-
-arts from the right si-
-de rather than the left

4. Random animation ove-
-rrides animation module

5. Higher resolution fa-
ctor affects video fps  

6. The taskbar can some-
-times hide part of the 
animation, adjust taskb-
-ar height to accomodate
'''
tk.Label(root, text=text).grid(row=1, column=6, rowspan=10, padx=5, pady=5)

# dark mode / light mode button initialize
txt = "light mode" if config_dict["!bg_dark"] == "Y" else "dark mode"
cmd  = dark_mode if config_dict["!bg_dark"] == "Y" else light_mode
but_d = tk.Button(root, text=txt, command=cmd)
but_d.grid(row=len(C1)-4, column=4, padx=5, pady=5, sticky="ew")
if config_dict["!bg_dark"] == "Y":
    dark_mode()
else:
    light_mode()

# keeps the tkinter window alive
root.mainloop()
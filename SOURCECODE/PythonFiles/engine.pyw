# import modules
import os
import sys

import csv
from random import choice
from pyshortcuts import make_shortcut

import tkinter as tk
import itertools

# path for other stuff like Animations folder, config.csv
def get_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)   # folder where the EXE is
    else:
        return os.path.dirname(os.path.abspath(__file__))
    
# path for icon
def resource_path(relative):
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        return os.path.join(exe_dir, relative)
    else:
        return os.path.join(os.path.dirname(__file__), relative)
    
# create shortcut in startup folder
def shortcut_create():
    exe_dir = get_path()
    target_exe = os.path.join(exe_dir, "engine.exe")

    # startup folder
    shortcut_folder = os.path.join(
        os.environ['APPDATA'],
        "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
    )

    make_shortcut(
        script=target_exe,
        name="idlemation-shortcut",
        folder=shortcut_folder,
        icon=os.path.join(exe_dir, "idlemation_icon.ico"),
        terminal=False
    )
    
# reads config file
def get_config():
    config_path = resource_path("config.csv")
    with open(config_path, 'r') as configfile:
        reader = csv.reader(configfile)
        return {row[0]: row[1] for row in reader if len(row) == 2}

# saves config changes
def save_config(config_dict):
    config_path = resource_path("config.csv")
    rows = [[k, v] for k, v in config_dict.items()]
    with open(config_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

# kills animation
def kill_anim(config_dict):
    config_dict["!run"] = "N"
    save_config(config_dict)

# main() part I
def run_anim():

    config_dict = get_config()

    # gets animation.txt file
    animations_path = resource_path("Animations")
    anim_files = [
        f for f in os.listdir(animations_path)
        if f.startswith("ANIM_") and f.endswith(".txt")
    ]

    # random animation check
    if config_dict["b!random_animation"] == "Y" and anim_files:
        filename = choice(anim_files)
    else:
        expected = config_dict["d!animation_module"] + ".txt"
        filename = expected if expected in anim_files else "ANIM_default.txt"

    anim_path = os.path.join(animations_path, filename)

    # load frames
    try:
        with open(anim_path, "r") as f:
            data = f.read()
        frames = [frame for frame in data.split("\n===FRAME===\n") if frame.strip()]
    except:
        frames = ["NO ANIMATION FOUND"]

    # main() part II
    if config_dict["b!run_on_startup"] == "Y" or config_dict["!run"] == "Y":

        global root
        root = tk.Tk()

        config_dict["!run"] = "Y"
        save_config(config_dict)

        # escape to kill animation
        root.bind("<Escape>", lambda e: kill_anim(get_config()))

        # borderless check
        if config_dict["b!borderless"] == "Y":
            root.overrideredirect(True)

        # opacity check
        root.attributes("-alpha", float(config_dict["s!opacity"]))
        root.configure(bg=config_dict["c!background_colour"])

        # window size handler
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        width = screen_w // int(config_dict["horizontal_fraction"])
        height = screen_h // int(config_dict["vertical_fraction"]) - int(config_dict["taskbar_height"])
        x = screen_w - int(config_dict["horizontal_offset"]) - width
        y = int(config_dict["vertical_offset"])
        root.geometry(f"{width}x{height}+{x}+{y}")

        # keep at bottom
        root.lower()
        root.bind("<FocusIn>", lambda e: root.lower())
        
        # actual animation handler
        label = tk.Label(
            root,
            font=(config_dict["font"], config_dict["font_size"]),
            bg=config_dict["c!background_colour"],
            fg=config_dict["c!font_colour"]
        )
        label.pack()

        def update():
            config = get_config()
            if config["!run"] == "N":
                root.after(1, root.destroy)
                return

            label.config(text=next(cycle))
            root.after(int(config["ms_delay"]), update)

        cycle = itertools.cycle(frames)
        update()

        # keeps window alive
        root.mainloop()

# run
if __name__ == "__main__":
    run_anim()

# create shortcut after animation runs once because windows is weird
shortcut_create()
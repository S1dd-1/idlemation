# idlemation

Idlemation is a lightweight, customizable and easy-to-modify ASCII animation engine for Windows that plays frame-by-frame animations on top of the desktop.

NOTE : IDLEMATION creates a startup shortcut so your animations can run when your computer boots. Because it modifies the Windows Startup folder, Windows Defender may flag it as an unfamiliar app. This is expected behavior, IDLEMATION does not access the internet, install services, or modify system files. It only creates a single .lnk shortcut.

If Windows blocks it the first time:
1. Run idlemation.exe once
2. When the Windows Defender prompt appears, click More info → Run anyway.
3. Run the animation once through idlemation.exe or engine.exe.
4. Press Win + R and type shell:startup. You should see idlemation-shortcut.lnk.
5. Double-click the shortcut; if Windows prompts again, choose More info → Run anyway.
6. After this, Windows will trust the shortcut and IDLEMATION will launch normally on startup.

## Features
1. Runs a frame-by-frame ASCII art animation on the desktop (Well. Above it, but below all other programs)
2. Allows a wide array of customization options such as choosing and importing animations, changing colours, opacity and more
3. Dual executable system: engine.exe runs the animation and can be run independantly from the idlemation.exe GUI handler
4. Easy to save and share assets such as animations and config settings
5. Easy to modify source code alongside exe app building

## How to Run
1. Download IDLEMATION from latest release
2. Go to IDLEMATION/dist/engine
3. There you can find two executable files: idlemation.exe and engine.exe
4. idlemation.exe includes the GUI, which allows you to change config settings easily
5. engine.exe just runs the animation
6. idlemation-shortcut.lnk is created in the startup folder and turning run_on_startup on results in the animation being run soon after the computer is opened
7. PRECAUTION : you must run the animation through idlemation.exe or engine.exe once before idlemation-shortcut.lnk is created

## How to Modify the Source Code
1. Download SOURCECODE from github repository
2. There you can see two folders, ASSETS and PYTHONFILES
3. Inside PYTHONFILES, you can edit idlemation.py, converter.py, and engine.pyw
4. idlemation.py controls the GUI and config file initialization
5. converter.py controls the conversion of .mp4 files to ASCII animation .txt files
6. engine.pyw controls the running of the animation and startup shortcut initialization

Original made by S1dd-1 on github -> https://github.com/S1dd-1/idlemation

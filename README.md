# redide

### red.py

red-lang ide made in Python

- Basic Syntax Highlight


Depends: `bash, Python3, tkinter, tcl/tk` Linux environment [Windows under a VM] ;)

`Bash` is required if you wan access to the internal shell. *You can edit the subprocess code in the file to your shell of preference.* `sed -i 's|"/bin/bash"|"/your/shell"|g' red.py`

# HOWTO

`python3 red.py` Launch app

*Ctrl-R* Creates new workarea. Watch for the dark bar appear on the right. Dual side arrow cursor appears clik and drag to pane window.

Internal Commands are singel character:  `d o w s` 

*Return* execute internal commands like a normal shell

`d` clear all

`o [filename]` opens a file in current path

`w [filename]` writes a file to current path

`s [linux command]` runs shell `s ls -t` (Shell does not maintain state, so `s cd dir; [do stuff]`) Its just a subprocess for you to get text manipulation access using linux commands `s cat file | sed this | grep that`. I just edit files like that instead of using vim or emacs. Call me a [purist](https://adamdrake.com/command-line-tools-can-be-235x-faster-than-your-hadoop-cluster.html).

*Escape* removes shell window. 


*Escape* clear command line 

*Escape* Focus command line if not focused

*Middle Button Click* Paste the Yank [Yanking and Copying text are 2 different things. To Yank: Highlight text anywhere outside of app or a different pad *(Ctrl-R)* and with Mouse Scroll-wheel click it and you will "Paste" the text [yank].)

*Wheel Click Drag* Scrolls Up/Down

_**Ctrl**-a,e,d,t,n,p,i,b,f,c,v,x,/_ Default POSIX Bindings by Tkinter: move to begin line, line end, delete, transpose, next parg, prev parg, insert tab, back char, fwd char, copy, paste, cut, select all, respectively.

[quirk: move/place cursor on the last line first before entering commands into the Red interpreter window]

I can fix all the hacks as I get better with Python.

---

Get Red: https://github.com/red/red

Get pnk.lang: https://github.com/dislux-hapfyl/shimky

#allerrorsmatter

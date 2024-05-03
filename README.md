# redide

### red.py

red-lang ide made in Python

- Basic Syntax Highlight

- Compiles

- Interpreter

Depends: `red, redc, bash, Python3, tkinter, tcl/tk` Linux environment [Windows under a VM] ;)

The red interpreter and compiler should be in your path named `red` and `redc`. Mine is in `/usr/local/bin/` and also `Bash` is required if you wan access to the internal shell. *You can edit the subprocess code in the file to your shell of preference.* `sed -i 's|"/bin/bash"|"/your/shell"|g' red.py`

# HOWTO

`python3 red.py` Launch app

*Ctrl-R* Creates new workarea. Watch for the dark bar appear on the right. Dual side arrow cursor appears clik and drag to pane window.

Internal Commands are singel character:  `d c o w s` 

*Return* execute internal commands

`d` clear all

`c` compile opened or saved file

`o [filename]` opens a file in current path

`w [filename]` writes a file to current path

`s [linux command]` runs shell `s ls -t` (Shell does not maintain state, so `cd dir; [do stuff]`) Its just a subprocess for you to get text manipulation access using linux commands `awk,sed,grep`. I just edit files like that instead of using vim or emacs. Call me a purist.

*Escape* removes shell window. 


*Escape* clear command line 

*Escape* Focus command line if not focused

*Middle Button Click* Paste the Yank [Yanking and Copying text are 2 different things. To Yank: Highlight text anywhere outside of app or a different pad *(Ctrl-R)* and with Mouse Scroll-wheel click it and you will "Paste" the text [yank].)

*Middle Button Click Drag* Scrolls Up/Down

_**Ctrl**-a,e,d,t,n,p,i,b,f,c,v,x,/_ Default POSIX Bindings by Tkinter: move to begin line, line end, delete, transpose, next parg, prev parg, insert tab, back char, fwd char, copy, paste, cut, select all, respectively.

---

Get Red: https://github.com/red/red

Get pnk.lang: https://github.com/dislux-hapfyl/shimky

#allerrorsmatter

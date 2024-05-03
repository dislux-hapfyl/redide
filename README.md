# redide

### red.py

red-lang ide made in Python

- Basic Syntax Highlight

- Compiles

- Interpreter

Depends: red, redc, bash

The red interpreter and compiler should be in your path named `red` and `redc`. Mine is in `/usr/local/bin/` and also `Bash` is required if you wan access to the internal shell. *You can edit the subprocess code in the file to your shell of preference.* `sed -i 's|"/bin/bash"|"/your/shell"|g' red.py`

#HOWTO

`python3 red.py` Launch app

*Ctrl-R* Creates new workarea. Watch for the dark bar appear on the right. Dual side arrow appears clik and drag. Resizable workspace.

Internal Commands are singel character:  `o w c s d`

`c` compile opened or saved file

`s [linux command]` runs shell `s ls -t`

*Escape* removes shell window. 

`o [file in present path]` opens file in current path

`w [filename]` writes a filename to current path

`d` deletes all inside the text pad above command line

*Return* execute command

*Escape* clear command line 

*Escape* Focus command line if not focused

*Middle Button Click* Paste the Yank [Yanking and Copying text are 2 different things. To Yank: Highlight text anywhere outside of app or a different pad *(Ctrl-R)* and with Mouse Scroll-wheel click it and you will "Paste" the text [yank].)

*Middle Button Click Drag* Scrolls Up/Down

_**Ctrl**-a,e,d,t,n,p,i,b,f,c,v,x,/_ Default POSIX Bindings by Tkinter: move to begin line, line end, delete, transpose, next parg, prev parg, insert tab, back char, fwd char, copy, paste, cut, select all, respectively.

---

Get Red: https://github.com/red/red

Get pnk.lang: https://github.com/dislux-hapfyl/shimky

#allerrorsmatter

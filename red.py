#!/usr/bin/env python3
#pnk.lang.gen;
from tkinter import Tk,Frame,Text,Entry,PanedWindow
from re import finditer,match
from threading import Thread
import queue
import subprocess
import datetime


class Red(Tk):

    def __init__(self):
        super().__init__()
        self.configure(bg="#202124")
        self.pw = PanedWindow(self,orient="horizontal",sashwidth=2,relief="flat",showhandle=True,sashpad=1,bg="#111")
        self.pw.pack(expand=1,fill="both",padx=5,pady=5,)
        self.pw.pack(expand=1,fill="both",padx=5,pady=5,)
        self.run()
        self.bind_all("<Control-R>", self.run)

    def run(self,e=None):
        self.app = App(self,)
        self.pw.add(self.app)


class App(Frame):

    def __init__(self,parent,):
        super().__init__(parent,)
        self.master = parent
        self.configure(bg="#202124")
        self.iSrcPad = SrcPad(self,)
        self.iSrcPad.pack(expand=1,fill="both",padx=5,pady=5,)
        self.iConsole = Console(self,"red")
        self.iConsole.pack(expand=1,fill="both",padx=5,pady=5,)


class Console(Frame):

    def __init__(self, parent, com):
        super().__init__(parent, )
        self.master = parent
        self.configure(bg="#202124")

        self.ttyText = Text(self,fg="#DDD",blockcursor=True,bg="#222",cursor="pencil",
                            font=("VictorMono",16),highlightbackground="#444",highlightcolor="#2BCDBB",
                            insertbackground="red",relief="flat",padx=20,pady=20,wrap="word",height=18)
        self.tagConf()
        self.ttyText.bind("<Return>", self.enter)
        self.ttyText.bind("<KeyRelease>", self.doSyntax)
        self.ttyText.pack(expand=1,fill="both",padx=3,pady=3,)
        self.p = subprocess.Popen(com,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        self.outQueue = queue.Queue()
        self.errQueue = queue.Queue()
        self.linestart = 0
        self.alive = True
        Thread(target=self.readFromProccessOut,daemon=True).start()
        Thread(target=self.readFromProccessErr,daemon=True).start()
        self.writeLoop()

    def destroy(self,event=None):
        self.alive = False
        self.p.stdin.write("exit()\n".encode())
        self.p.stdin.flush()
        self.ttyText.destroy()
        Frame.destroy(self)

    def enter(self,e):
        string = self.ttyText.get(1.0,"end")[self.linestart:]
        self.linestart += len(string)
        self.p.stdin.write(string.encode())
        self.p.stdin.flush()

    def readFromProccessOut(self,):
        while self.alive:
           data = self.p.stdout.raw.read(1024).decode()
           self.outQueue.put(data)
    
    def readFromProccessErr(self,):
        while self.alive:
           data = self.p.stderr.raw.read(1024).decode()
           self.errQueue.put(data)

    def writeLoop(self,):
        if not self.errQueue.empty():
           self.write(self.errQueue.get())
        if not self.outQueue.empty():
           self.write(self.outQueue.get())
        if self.alive:
           self.after(10,self.writeLoop)


    def write(self,string):
        self.ttyText.insert("end", f"{string}")
        self.ttyText.see("end")
        self.linestart += len(string)

    def doSyntax(self,e=None):
        self.syntax(self.ttyText)

    def tagConf(self,e=None):
        d = { "arg": ("#333", "#eccca2"), "args": ("#444", "#eccca2"), "brc": ("#222", "red"), "brcc": ("#222", "blue"), "paren": ("#222", "orange"), "slash": ("#222", "green"), "parenn": ("#222", "yellow"), "crlb": ("#444", "#eccca2"), "hash": ("#222", "magenta"), "col": ("#222", "#00ffff"), "eql": ("#222", "#00ffff"),"dash": ("#222", "#00ffff"), "pls": ("#222", "yellow"), "star": ("#222", "#bfff00"), "qs": ("#222", "#bfff00"), "dol": ("#222", "green"), "exc": ("#222", "orange"), "nnn": ("#222","orange"),"pct": ("#222","purple"),}
        for key,value in d.items():
            self.ttyText.tag_configure(key,background=value[0],foreground=value[1])

    def tagg(self,x,y,a,b,e=None):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.x.tag_add(y,f"1.0+{a}c",f"1.0+{b}c")

    def syntax(self,xx,e=None):
        self.xx = xx
        data = self.xx.get("1.0","end-1c")
        args_idx = [(m.start(),m.end()) for m in finditer(r'\"(.*?)\"', data)]
        for start,end in args_idx:
            self.tagg(xx,"args",start,end)
        arg_idx = [(m.start(),m.end()) for m in finditer(r'\'', data)]
        for start,end in arg_idx:
            self.tagg(xx,"arg",start,end)
        crlb_idx = [(m.start(),m.end()) for m in finditer(r'\{(.*?)\}', data)]
        for start,end in crlb_idx:
            self.tagg(xx,"crlb",start,end)
        brc_idx = [(m.start(),m.end()) for m in finditer(r'\[', data)]
        for start,end in brc_idx:
            self.tagg(xx,"brc",start,end)
        paren_idx = [(m.start(),m.end()) for m in finditer(r'\(', data)]
        for start,end in paren_idx:
            self.tagg(xx,"paren",start,end)
        parenn_idx = [(m.start(),m.end()) for m in finditer(r'\)', data)]
        for start,end in parenn_idx:
            self.tagg(xx,"parenn",start,end)
        slash_idx = [(m.start(),m.end()) for m in finditer(r'\/', data)]
        for start,end in slash_idx:
            self.tagg(xx,"slash",start,end)
        brcc_idx = [(m.start(),m.end()) for m in finditer(r'\]', data)]
        for start,end in brcc_idx:
            self.tagg(xx,"brcc",start,end)
        hash_idx = [(m.start(),m.end()) for m in finditer(r'#', data)]
        for start,end in hash_idx:
            self.tagg(xx,"hash",start,end)
        col_idx = [(m.start(),m.end()) for m in finditer(r':', data)]
        for start,end in col_idx:
            self.tagg(xx,"col",start,end)
        dash_idx = [(m.start(),m.end()) for m in finditer(r'-', data)]
        for start,end in dash_idx:
            self.tagg(xx,"dash",start,end)
        eql_idx = [(m.start(),m.end()) for m in finditer(r'=', data)]
        for start,end in eql_idx:
            self.tagg(xx,"eql",start,end)
        pls_idx = [(m.start(),m.end()) for m in finditer(r'\+', data)]
        for start,end in pls_idx:
            self.tagg(xx,"pls",start,end)
        star_idx = [(m.start(),m.end()) for m in finditer(r'\*', data)]
        for start,end in star_idx:
            self.tagg(xx,"star",start,end)
        qs_idx = [(m.start(),m.end()) for m in finditer(r'\?', data)]
        for start,end in qs_idx:
            self.tagg(xx,"qs",start,end)
        dol_idx = [(m.start(),m.end()) for m in finditer(r'\$', data)]
        for start,end in dol_idx:
            self.tagg(xx,"dol",start,end)
        exc_idx = [(m.start(),m.end()) for m in finditer(r'!', data)]
        for start,end in exc_idx:
            self.tagg(xx,"exc",start,end)
        nnn_idx = [(m.start(),m.end()) for m in finditer(r'~', data)]
        for start,end in nnn_idx:
            self.tagg(xx,"nnn",start,end)
        pct_idx = [(m.start(),m.end()) for m in finditer(r'%', data)]
        for start,end in pct_idx:
            self.tagg(xx,"pct",start,end)

class SrcPad(Frame):
    def __init__(self,parent,):
        super().__init__(parent,)
        self.master = parent
        self.configure(bg="#202124")

        self.srcTxt = Text(self,fg="#DDD",blockcursor=True,bg="#222",cursor="pencil",
                           font=("VictorMono",16),highlightbackground="#444",highlightcolor="#2BCDBB",
                           insertbackground="red",relief="flat",padx=20,pady=20,undo=True,wrap="word")
        self.srcTxt.pack(expand=1,fill="both",padx=5,pady=5,)

        self.srcTxt.bind("<Shift_R>", self.synThd)
        self.srcTxt.bind("<Shift-Return>", self.add_indent)
        self.srcTxt.bind("<Control-Return>", self.stay_indent)
        self.srcTxt.bind("<Control-l>", self.cleartxt)
        self.srcTxt.bind("<Escape>", self.myExit)

        self.comEntry = Entry(self,fg="#DDD",bg="#202124",cursor="shuttle",font=("VictorMono",16),
                              highlightbackground="#444",highlightcolor="#222",insertbackground="red",relief="flat")
        self.comEntry.pack(expand=0,fill="x",padx=5,pady=5,)

        self.comEntry.bind("<Return>", self.cliSh)
        self.comEntry.bind("<Escape>", self.cliclr)
        self.tagConf()
        self.myExit()

    def add_indent(self, event):
        text = self.srcTxt
        line = text.get("insert linestart", "insert")
        m = match(r"^(\s+)", line)
        whitespace = m.group(0) if m else ""
        text.insert("insert", f"\n    {whitespace}")
        return "break"

    def stay_indent(self, event):
        text = self.srcTxt
        line = text.get("insert linestart", "insert")
        m = match(r"^(\s+)", line)
        whitespace = m.group(0) if m else ""
        text.insert("insert", f"\n{whitespace}")
        return "break"

    def thdStart(self,x,e=None):
        self.x = x
        thd = Thread(target=x,daemon=True)
        thd.start()

    def cliclr(self,e=None):
        self.comEntry.delete(0,"end")

    def myExit(self,e=None):
        self.comEntry.focus()

    def cliSh(self,e=None):
        line = self.comEntry.get()
        tt = line.split()
        if not tt:
            pass
        elif tt[0] == "o":
            self.openfile()
        elif tt[0] == "w":
            self.savefile()
        elif tt[0] == "d":
            self.cleartxt()
            self.cliclr()
        elif tt[0] == "c":
            self.compile()
        elif tt[0] == "s":
            self.mapitOut()

    def clearOut(self,e=None):
        self.iShOut.destroy()
        self.comEntry.focus()

    def compile(self,e=None):
        self.thdStart(self.redc)

    def mapitOut(self,e=None):
        self.thdStart(self.shell)

    def shell(self,e=None):
        line = self.comEntry.get()
        tt = line.split()
        cmd = " ".join( str(i) for i in tt[1:])
        self.iShOut = ShOut(self,)
        self.iShOut.place(x=30,y=30)
        self.iShOut.txt.bind("<Escape>", self.clearOut)
        self.iShOut.txt.focus()
        try:
            result = subprocess.run(f"{cmd}",shell=True,executable="/bin/bash",stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            if result.returncode == 0:
                self.iShOut.txt.insert("1.0",f"\n\n{result.stdout}\n")
            else:
                self.iShOut.txt.insert("1.0",f"#$%&*^ #$%&*^ {datetime.datetime.now().strftime('<%m.%d.%Y.%H:%M>')} {result.stderr}\n")
        except Exception as e:
            self.iShOut.txt.insert("1.0",f"#$%&*^ #$%&*^ {datetime.datetime.now().strftime('<%m.%d.%Y.%H:%M>')} {str(e)}\n")

    def redc(self,e=None):
        self.cliclr()
        self.iShOut = ShOut(self,)
        self.iShOut.place(x=30,y=30)
        self.iShOut.txt.insert("1.0",f"{datetime.datetime.now().strftime('<%m.%d.%Y.%H:%M>')} Compiling...Please Wait!\n")
        self.iShOut.txt.bind("<Escape>", self.clearOut)
        self.iShOut.txt.focus()
        try:
            result = subprocess.run(f"redc -c {self.file} > .out ; cat .out",
                                    shell=True,executable="/bin/bash",stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            if result.returncode == 0:
                self.iShOut.txt.insert("end",f"\n\n{result.stdout}\n")
            else:
                self.iShOut.txt.insert("end",f"#$%&*^ #$%&*^ {datetime.datetime.now().strftime('<%m.%d.%Y.%H:%M>')} {result.stderr}\n")
        except Exception as e:
            self.iShOut.txt.insert("end",f"#$%&*^ #$%&*^ {datetime.datetime.now().strftime('<%m.%d.%Y.%H:%M>')} {str(e)}\n")
        self.iShOut.txt.insert("end",f"{datetime.datetime.now().strftime('<%m.%d.%Y.%H:%M>')} Done!\n")

    def openfile(self,e=None):
        line = self.comEntry.get()
        f = line.split()
        self.file = f[1]
        self.cleartxt()
        f = open(f[1], "r")
        thefile = f.read()
        self.srcTxt.insert("1.0", thefile)
        self.synThd()

    def savefile(self,e=None):
        line = self.comEntry.get()
        f = line.split()
        self.file = f[1]
        data = self.srcTxt.get("1.0","end-1c")
        with open(f[1], "w") as file:
            file.write(data)
        self.synThd()

    def cleartxt(self,e=None):
        self.srcTxt.delete("1.0","end")

    def remTag(self,e=None):
        for tag in self.srcTxt.tag_names():
            self.srcTxt.tag_remove(tag, "1.0", "end")
        self.tagConf()

    def synThd(self,e=None):
        self.remTag()
        self.thdStart(self.doSyntax)

    def doSyntax(self,e=None):
        self.syntax(self.srcTxt)

    def tagConf(self,e=None):
        d = { "arg": ("#333", "#eccca2"), "args": ("#444", "#eccca2"), "brc": ("#222", "red"), "brcc": ("#222", "blue"), "paren": ("#222", "orange"), "slash": ("#222", "green"), "parenn": ("#222", "yellow"), "crlb": ("#444", "#eccca2"), "hash": ("#222", "magenta"), "col": ("#222", "#00ffff"), "eql": ("#222", "#00ffff"),"dash": ("#222", "#00ffff"),"larr": ("#222", "red"),"rarr": ("#222", "blue"), "pls": ("#222", "#bfff00"), "star": ("#222", "#bfff00"), "qs": ("#222", "#bfff00"), "dol": ("#222", "green"), "exc": ("#222", "orange"), "nnn": ("#222","orange"), "pct": ("#222","purple"), "smcl": ("#222", "#bfff00"), "dot": ("#222", "pink"), "cm": ("#222", "cyan"), "upar": ("#222", "cyan"), "spc": ("#333", "#333"),}
        for key,value in d.items():
            self.srcTxt.tag_configure(key,background=value[0],foreground=value[1])

    def tagg(self,x,y,a,b,e=None):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.x.tag_add(y,f"1.0+{a}c",f"1.0+{b}c")

    def syntax(self,xx,e=None):
        self.xx = xx
        data = self.xx.get("1.0","end-1c")
        args_idx = [(m.start(),m.end()) for m in finditer(r'\"(.*?)\"', data)]
        for start,end in args_idx:
            self.tagg(xx,"args",start,end)
        arg_idx = [(m.start(),m.end()) for m in finditer(r'\'', data)]
        for start,end in arg_idx:
            self.tagg(xx,"arg",start,end)
        crlb_idx = [(m.start(),m.end()) for m in finditer(r'\{(.*?)\}', data)]
        for start,end in crlb_idx:
            self.tagg(xx,"crlb",start,end)
        brc_idx = [(m.start(),m.end()) for m in finditer(r'\[', data)]
        for start,end in brc_idx:
            self.tagg(xx,"brc",start,end)
        paren_idx = [(m.start(),m.end()) for m in finditer(r'\(', data)]
        for start,end in paren_idx:
            self.tagg(xx,"paren",start,end)
        parenn_idx = [(m.start(),m.end()) for m in finditer(r'\)', data)]
        for start,end in parenn_idx:
            self.tagg(xx,"parenn",start,end)
        slash_idx = [(m.start(),m.end()) for m in finditer(r'\/', data)]
        for start,end in slash_idx:
            self.tagg(xx,"slash",start,end)
        brcc_idx = [(m.start(),m.end()) for m in finditer(r'\]', data)]
        for start,end in brcc_idx:
            self.tagg(xx,"brcc",start,end)
        hash_idx = [(m.start(),m.end()) for m in finditer(r'#', data)]
        for start,end in hash_idx:
            self.tagg(xx,"hash",start,end)
        col_idx = [(m.start(),m.end()) for m in finditer(r':', data)]
        for start,end in col_idx:
            self.tagg(xx,"col",start,end)
        dash_idx = [(m.start(),m.end()) for m in finditer(r'-', data)]
        for start,end in dash_idx:
            self.tagg(xx,"dash",start,end)
        eql_idx = [(m.start(),m.end()) for m in finditer(r'=', data)]
        for start,end in eql_idx:
            self.tagg(xx,"eql",start,end)
        pls_idx = [(m.start(),m.end()) for m in finditer(r'\+', data)]
        for start,end in pls_idx:
            self.tagg(xx,"pls",start,end)
        star_idx = [(m.start(),m.end()) for m in finditer(r'\*', data)]
        for start,end in star_idx:
            self.tagg(xx,"star",start,end)
        dot_idx = [(m.start(),m.end()) for m in finditer(r'\.', data)]
        for start,end in dot_idx:
            self.tagg(xx,"dot",start,end)
        qs_idx = [(m.start(),m.end()) for m in finditer(r'\?', data)]
        for start,end in qs_idx:
            self.tagg(xx,"qs",start,end)
        dol_idx = [(m.start(),m.end()) for m in finditer(r'\$', data)]
        for start,end in dol_idx:
            self.tagg(xx,"dol",start,end)
        exc_idx = [(m.start(),m.end()) for m in finditer(r'!', data)]
        for start,end in exc_idx:
            self.tagg(xx,"exc",start,end)
        nnn_idx = [(m.start(),m.end()) for m in finditer(r'~', data)]
        for start,end in nnn_idx:
            self.tagg(xx,"nnn",start,end)
        pct_idx = [(m.start(),m.end()) for m in finditer(r'%', data)]
        for start,end in pct_idx:
            self.tagg(xx,"pct",start,end)
        larr_idx = [(m.start(),m.end()) for m in finditer(r'<', data)]
        for start,end in larr_idx:
            self.tagg(xx,"larr",start,end)
        rarr_idx = [(m.start(),m.end()) for m in finditer(r'>', data)]
        for start,end in rarr_idx:
            self.tagg(xx,"rarr",start,end)
        smcl_idx = [(m.start(),m.end()) for m in finditer(r';', data)]
        for start,end in smcl_idx:
            self.tagg(xx,"smcl",start,end)
        dot_idx = [(m.start(),m.end()) for m in finditer(r'\.', data)]
        for start,end in dot_idx:
            self.tagg(xx,"dot",start,end)
        cm_idx = [(m.start(),m.end()) for m in finditer(r'\,', data)]
        for start,end in cm_idx:
            self.tagg(xx,"cm",start,end)
        upar_idx = [(m.start(),m.end()) for m in finditer(r'\^', data)]
        for start,end in upar_idx:
            self.tagg(xx,"upar",start,end)
        spc_idx = [(m.start(),m.end()) for m in finditer(r' ', data)]
        for start,end in spc_idx:
            self.tagg(xx,"spc",start,end)

class ShOut(Frame):
    def __init__(self,parent,):
        super().__init__(parent,)
        self.master = parent
        self.configure(bg="#202124")

        self.txt = Text(self,fg="#DDD",blockcursor=True,bg="#222",cursor="pencil",font=("VictorMono",16),highlightbackground="#444",highlightcolor="#2BCDBB",insertbackground="red",relief="flat",padx=20,pady=20,undo=True,wrap="word")
        self.txt.pack(expand=0,fill="none",padx=5,pady=5,)

if __name__ == '__main__':
    go = Red()
    go.title("red-ide")
    go.mainloop()


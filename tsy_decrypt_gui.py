#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tsy 解密工具 - 图形界面版
依赖: Python 3 + tkinter（标准库，无需额外安装）
用法: python3 tsy_decrypt_gui.py
"""
import struct, os, base64, threading
from tkinter import *
from tkinter import ttk, filedialog, messagebox

_B64 = """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"""

d = base64.b64decode(_B64)
_T = [list(struct.unpack("<256I", d[i:i+1024])) for i in range(0,4096,1024)]
_S = list(d[4096:4352])
_R = [list(struct.unpack("<4I", d[4352+i*16:4352+i*16+16])) for i in range(16)]
T0,T1,T2,T3 = _T; S=_S; RK=_R

def _h(s, d, k):
    a,b,c,e=s; k0,k1,k2,k3=k
    d[0]=T3[(a>>24)&255]^T2[(e>>16)&255]^T1[(c>>8)&255]^T0[b&255]^k0
    d[1]=T3[(b>>24)&255]^T2[(a>>16)&255]^T1[(e>>8)&255]^T0[c&255]^k1
    d[2]=T3[(c>>24)&255]^T2[(b>>16)&255]^T1[(a>>8)&255]^T0[e&255]^k2
    d[3]=T3[(e>>24)&255]^T2[(c>>16)&255]^T1[(b>>8)&255]^T0[a&255]^k3

def _l(s, d, k):
    w0,w1,w2,w3=s; k0,k1,k2,k3=k
    d[0]=((S[(w0>>24)&255]<<24)|(S[(w3>>16)&255]<<16)|(S[(w2>>8)&255]<<8)|S[w1&255])^k0
    d[1]=((S[(w1>>24)&255]<<24)|(S[(w0>>16)&255]<<16)|(S[(w3>>8)&255]<<8)|S[w2&255])^k1
    d[2]=((S[(w2>>24)&255]<<24)|(S[(w1>>16)&255]<<16)|(S[(w0>>8)&255]<<8)|S[w3&255])^k2
    d[3]=((S[(w3>>24)&255]<<24)|(S[(w2>>16)&255]<<16)|(S[(w1>>8)&255]<<8)|S[w0&255])^k3

def decrypt_block(data):
    s=list(struct.unpack(">4I",data)); w=[0,0,0,0]
    for i in range(4): s[i]^=RK[0][i]
    for i in range(6): _h(s,w,RK[i*2+1]); _h(w,s,RK[i*2+2])
    _h(s,w,RK[13]); _l(w,s,RK[14])
    return struct.pack(">IIII",*s)

def decrypt_bytes(data):
    r=bytearray()
    for i in range(0,len(data),16):
        r.extend(decrypt_block(data[i:i+16].ljust(16,b"\x00")))
    r=bytes(r); n=len(data)-7032
    return r[:n] if 0<n<len(r) else r

KNOWN = {b"PK\x03\x04":"DOCX/XLSX", b"\xd0\xcf\x11\xe0":"XLS", b"%PDF":"PDF"}
def check_file(path):
    try:
        data = open(path,"rb").read()
    except:
        return False, "", "\u65e0\u6cd5\u8bfb\u53d6"
    if len(data) < 7032+16:
        return False, "", "\u6587\u4ef6\u592a\u5c0f"
    dec = decrypt_block(data[:16])
    for m,f in KNOWN.items():
        if dec[:len(m)]==m: return True, f, "\u5df2\u68c0\u6d4b:"+f
    return False, "", "\u672a\u68c0\u6d4b\u5230"

class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("tsy\u89e3\u5bc6\u5de5\u5177")
        self.root.geometry("700x520")
        self.root.resizable(False, False)
        self.files = []
        self._build()
    
    def _add_file(self, path):
        if path in [f[0] for f in self.files]: return
        is_enc, fmt, status = check_file(path)
        self.files.append((path, os.path.basename(path), is_enc))
        self.tree.insert("", END, values=(len(self.files), path, status))
    
    def _build(self):
        top = ttk.Frame(self.root, padding=8)
        top.pack(fill=X)
        ttk.Label(top, text="\u70b9\u51fb\u201c\u6dfb\u52a0\u6587\u4ef6\u201d\u9009\u62e9\u9700\u8981\u89e3\u5bc6\u7684\u6587\u4ef6\uff08\u652f\u6301\u591a\u9009\uff09").pack(anchor=W)
        bf = ttk.Frame(top)
        bf.pack(fill=X, pady=4)
        ttk.Button(bf, text="\u6dfb\u52a0\u6587\u4ef6", command=self._add_dialog).pack(side=LEFT, padx=2)
        ttk.Button(bf, text="\u5220\u9664\u9009\u4e2d", command=self._remove_sel).pack(side=LEFT, padx=2)
        ttk.Button(bf, text="\u6e05\u7a7a\u5217\u8868", command=self._clear).pack(side=LEFT, padx=2)
        
        tf = ttk.Frame(self.root, padding=8)
        tf.pack(fill=BOTH, expand=True)
        self.tree = ttk.Treeview(tf, columns=("#","path","status"), show="headings", height=10)
        self.tree.heading("#", text="\u5e8f\u53f7")
        self.tree.heading("path", text="\u6587\u4ef6\u8def\u5f84")
        self.tree.heading("status", text="\u5904\u7406\u7ed3\u679c")
        self.tree.column("#", width=50, anchor=CENTER)
        self.tree.column("path", width=430)
        self.tree.column("status", width=130, anchor=CENTER)
        sb = ttk.Scrollbar(tf, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        sb.pack(side=RIGHT, fill=Y)
        self.tree.bind("<Delete>", lambda e: self._remove_sel())
        
        mid = ttk.LabelFrame(self.root, text="\u8f93\u51fa\u4f4d\u7f6e\u8bbe\u7f6e", padding=8)
        mid.pack(fill=X, padx=8)
        self.out_var = StringVar(value="original")
        ttk.Radiobutton(mid, text="\u539f\u76ee\u5f55\u8f93\u51fa", variable=self.out_var, value="original").pack(anchor=W)
        nf = ttk.Frame(mid)
        nf.pack(fill=X)
        ttk.Radiobutton(nf, text="\u65b0\u76ee\u5f55\u8f93\u51fa", variable=self.out_var, value="new").pack(side=LEFT)
        self.out_path = StringVar()
        ttk.Entry(nf, textvariable=self.out_path, width=40).pack(side=LEFT, padx=4)
        ttk.Button(nf, text="\u6d4f\u89c8...", command=self._browse).pack(side=LEFT)
        nf2 = ttk.Frame(mid)
        nf2.pack(fill=X, pady=2)
        self.name_var = StringVar(value="prefix")
        ttk.Radiobutton(nf2, text="\u52a0\u524d\u7f00", variable=self.name_var, value="prefix").pack(side=LEFT, padx=2)
        self.pre = StringVar(value="dec_")
        ttk.Entry(nf2, textvariable=self.pre, width=10).pack(side=LEFT, padx=2)
        ttk.Radiobutton(nf2, text="\u52a0\u540e\u7f00", variable=self.name_var, value="suffix").pack(side=LEFT, padx=2)
        self.suf = StringVar(value="_dec")
        ttk.Entry(nf2, textvariable=self.suf, width=10).pack(side=LEFT, padx=2)
        
        bot = ttk.Frame(self.root, padding=8)
        bot.pack(fill=X)
        self.top_var = IntVar(value=1)
        ttk.Checkbutton(bot, text="\u7a97\u53e3\u7f6e\u9876", variable=self.top_var, command=self._top).pack(side=LEFT)
        ttk.Label(bot, text="\u89e3\u5bc6\u5f15\u64ce: \u5c31\u7eea", foreground="green").pack(side=LEFT, padx=20)
        ttk.Button(bot, text="\u5f00\u59cb\u89e3\u5bc6", command=self._start).pack(side=RIGHT, padx=2)
        ttk.Button(bot, text="\u6253\u5f00\u8f93\u51fa\u76ee\u5f55", command=self._openout).pack(side=RIGHT, padx=2)
        ttk.Button(bot, text="\u9000\u51fa\u7a0b\u5e8f", command=self.root.quit).pack(side=RIGHT, padx=2)
    
    def _add_dialog(self):
        ps = filedialog.askopenfilenames(title="\u9009\u62e9\u6587\u4ef6")
        for p in ps: self._add_file(p)
    
    def _remove_sel(self):
        sel = self.tree.selection()
        if not sel: return
        for item in sel:
            idx = self.tree.index(item)
            self.files.pop(idx)
            self.tree.delete(item)
        for i, item in enumerate(self.tree.get_children()):
            self.tree.set(item, "#", i+1)
    
    def _clear(self):
        self.files.clear()
        for i in self.tree.get_children(): self.tree.delete(i)
    
    def _browse(self):
        d = filedialog.askdirectory()
        if d: self.out_path.set(d)
    
    def _top(self):
        self.root.attributes("-topmost", self.top_var.get()==1)
    
    def _openout(self):
        d = self.out_path.get() if self.out_var.get()=="new" else (os.path.dirname(self.files[0][0]) if self.files else "")
        if d: os.startfile(d)
    
    def _start(self):
        if not self.files:
            messagebox.showwarning("\u63d0\u793a", "\u8bf7\u5148\u6dfb\u52a0\u6587\u4ef6")
            return
        valid = [(i,f) for i,f in enumerate(self.files) if f[2]]
        if not valid:
            messagebox.showwarning("\u63d0\u793a", "\u6ca1\u6709\u68c0\u6d4b\u5230\u53ef\u89e3\u5bc6\u7684\u6587\u4ef6")
            return
        threading.Thread(target=self._proc, daemon=True).start()
    
    def _proc(self):
        items = self.tree.get_children()
        for i, item in enumerate(items):
            path, name, is_enc = self.files[i]
            if not is_enc:
                self.root.after(0, lambda it=item: self.tree.set(it, "status", "\u8df3\u8fc7"))
                continue
            self.root.after(0, lambda it=item: self.tree.set(it, "status", "\u89e3\u5bc6\u4e2d..."))
            try:
                res = decrypt_bytes(open(path,"rb").read())
                base, ext = os.path.splitext(name)
                new_name = (self.pre.get()+name) if self.name_var.get()=="prefix" else base+self.suf.get()+ext
                out_dir = self.out_path.get() if (self.out_var.get()=="new" and self.out_path.get()) else os.path.dirname(path)
                os.makedirs(out_dir, exist_ok=True)
                open(os.path.join(out_dir, new_name),"wb").write(res)
                self.root.after(0, lambda it=item, s=len(res): self.tree.set(it, "status", f"OK {s:,}B"))
            except Exception as e:
                self.root.after(0, lambda it=item, m=str(e)[:30]: self.tree.set(it, "status", f"\u5931\u8d25:{m}"))
        self.root.after(0, lambda: messagebox.showinfo("\u5b8c\u6210", f"\u5904\u7406\u5b8c\u6210: {len(self.files)}\u4e2a\u6587\u4ef6"))

if __name__ == "__main__":
    App().root.mainloop()

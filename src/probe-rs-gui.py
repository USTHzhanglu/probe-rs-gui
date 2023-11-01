#!/usr/bin/env python
# coding: utf-8

import pathlib
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.pathchooserinput import PathChooserInput
import threading
import os,sys
import webbrowser
import yaml

import os
import sys
#生成资源文件目录访问路径
def app_path():
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return base_path

version = '0.0.1'
author = 'USTHzhanglu@outlook.com'
copyright = 'USTHzhanglu'
show_about = (
'probe-rs-gui\r\n'+
'Version:%s\r\n'%version+
'Author:%s\r\n'%author+
'Copyright@%s'%copyright
)
class Cfg:
    def __init__(self):
        self.bin_path = ''
        self.config_path = ''
        self.format = "bin"
        self.pack_yaml = ""
        self.speed = "16000"
        self.chip = ""
        self.configure = None
        self.status = False
        self.error = ''
    def upload(self):
        try:
            with open(self.config_path,'r') as f:
                self.configure = yaml.load(f,Loader=yaml.FullLoader)
                self.pack_yaml = self.configure.get("pack_yaml")
                self.speed = self.configure.get("speed")
                self.chip = self.configure.get("chip")

                if(os.path.isabs(self.pack_yaml) == False):
                    self.pack_yaml = os.path.dirname(os.path.abspath(self.config_path)) +'\\' + self.pack_yaml
                print("chip: " + self.chip)
                print("pack path: " + self.pack_yaml)
                print("speed: " + self.speed)
                self.status = True

        except Exception as e:
            self.status = False
            self.error = e



def download_bin(ui):
    is_err_download = False
    try:
        ret = ''
        #probe-rs download --chip HC32F4A0PIHB --chip-description-path .\HC32F4A0-Series.yaml  --format bin --speed 16000 bootloader.bin
        cmd = app_path() + '\probe-rs download ' + \
                '--chip %s '%cfg.chip + '--chip-description-path %s '%cfg.pack_yaml + \
                '--speed %s '%cfg.speed + '--format %s '%cfg.format + cfg.bin_path
        # print(cmd)
        ret = os.popen(cmd).read()
        print(ret)
    except Exception as r:
        ui.messagebox.showerror('Flash error',r)
        is_err_download = True
    finally:
        if is_err_download == False:
            ui.messagebox.showinfo('Flash','Download success')
        else:
            ui.messagebox.showerror('Flash error','download fail')
        ui.out.edit_undo()
        ui.out.insert('end','----------Download Finish----------')

        
def erase_bin(ui):
    is_err_erase= False
    try:
        ret = ''
        #probe-rs erase --chip HC32F4A0PIHB --chip-description-path .\HC32F4A0-Series.yaml
        cmd = app_path() + '\probe-rs erase ' + \
                '--chip %s '%cfg.chip + '--chip-description-path %s '%cfg.pack_yaml
        # print(cmd)
        ret = os.popen(cmd).read()
    except Exception as r:
        is_err_erase = True
        ui.messagebox.showerror('Flash error',r)
    finally:
        if is_err_erase == False:
            ui.messagebox.showinfo('Flash','Erase success')
        else:
            ui.messagebox.showerror('Flash error','erase fail')
        ui.out.edit_undo()
        ui.out.insert('end','-----------Erase Finish-----------')


class std2tk(object): 
    def __init__(self,tk):
        self._buff = ""
        self.tk = tk
    def write(self, out_stream): 
        self.tk.out.insert('end',out_stream)
    def flush(self): 
        pass

class PyocdApp:
    def __init__(self, master=None):
        # pragrm
        self.messagebox = tk.messagebox
        
        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        #menu
        self.menu1 = tk.Menu(self.toplevel1,tearoff = True)

        self.mi_download = 1
        self.menu1.add('command', font='{宋体} 9 {}', label='Update')
        _wcmd = lambda itemid="download": self.menucallback(itemid)
        self.menu1.entryconfigure(self.mi_download, command=_wcmd)
        self.toplevel1.configure(menu=self.menu1)
        
        self.mi_help = 2
        self.menu1.add('command', font='{宋体} 9 {}', label='Help')
        _wcmd = lambda itemid="help": self.menucallback(itemid)
        self.menu1.entryconfigure(self.mi_help, command=_wcmd)
        
        self.mi_about = 3
        self.menu1.add('command', font='{宋体} 9 {}', label='About')
        _wcmd = lambda itemid="about": self.menucallback(itemid)
        self.menu1.entryconfigure(self.mi_about, command=_wcmd)
        self.toplevel1.configure(menu=self.menu1)
        
        
        self.gui = ttk.Frame(self.toplevel1)
        self.labelframe1 = ttk.Labelframe(self.gui)
        self.binchooserinput = PathChooserInput(self.labelframe1)
        self.binchooserinput.configure(state='normal', title='file', type='file')
        self.binchooserinput.configure(filetypes=[('bin files', ['.bin','.hex','.elf'])])
        self.binchooserinput.pack(fill='x', side='top')
        self.labelframe1.configure(text='Select Bin')
        self.labelframe1.pack(fill='x', side='top')
        
        self.labelframe2 = ttk.Labelframe(self.gui)
        self.binchooserinput2 = PathChooserInput(self.labelframe2)
        self.binchooserinput2.configure(state='normal', title='config', type='file')
        self.binchooserinput2.configure(filetypes=[('yaml file','.yaml')])
        self.binchooserinput2.pack(fill='x', side='top')
        self.labelframe2.configure(text='Select Config')
        self.labelframe2.pack(fill='x', side='top')
        self.frame1 = ttk.Frame(self.gui)

        self.out = tk.Text(self.frame1,undo=True,maxundo = 1)
        self.out.configure(background='#000000',font='{宋体} 10 {}', foreground='#00ff00', height='9', relief='groove')
        self.out.configure(width='50')
        self.out.pack(anchor='center', expand='true', fill='both', side='top')
        
        self.erase = tk.Button(self.frame1)
        self.erase.configure(relief='groove', text='Erase Chip')
        self.erase.pack(anchor='center', ipadx='15', padx='20', pady='10', side='left')
        self.erase.configure(command=self.erasechip)
        self.start = tk.Button(self.frame1)
        self.start.configure(relief='groove', text='Download')
        self.start.pack(anchor='center', ipadx='15', padx='20', pady='10', side='right')
        self.start.configure(command=self.download)
        
        self.frame1.pack(anchor='center', expand='true', fill='both', side='bottom')
        self.gui.configure(height='480', relief='flat', width='320')
        self.gui.pack(anchor='center', side='top')
        self.gui.pack_propagate(0)
        self.toplevel1.configure(height='480', width='320')
#        self.toplevel1.geometry('320x480')
#自适应屏幕居中
        self.toplevel1.geometry('320x480' + '+'
                            + str((self.toplevel1.winfo_screenwidth() - 320) // 2) + '+'
                            + str((self.toplevel1.winfo_screenheight() - 480) // 2 - 18))

        self.toplevel1.title('probe-rs-GUI')
        self.toplevel1.resizable(False, False)
        self.toplevel1.attributes('-alpha',0.95)        
        
        # Main widget
        self.mainwindow = self.toplevel1
        self.mainwindow.attributes('-topmost', 1)#强制前台
        self.mainwindow.after_idle(self.mainwindow.attributes,'-topmost',False)
        self.mainwindow.focus_force()
        self.mainwindow.bind('<Key>',self.press_key)
    def run(self):
        self.mainwindow.mainloop()
        
        
    def menucallback(self, itemid):
        if itemid == 'about':
            tk.messagebox.showinfo(title="About",message = show_about)
        elif itemid =='help':
            webbrowser.open('https://github.com/USTHzhanglu/probe-rs-gui/readme.md',new=0)
        elif itemid =='download':  
            if tk.messagebox.askokcancel("Download", "Go to Github?"):
                webbrowser.open('https://github.com/USTHzhanglu/probe-rs-gui',new=0)      

    def download(self):
        cfg.bin_path = self.binchooserinput.cget('path')
        cfg.config_path = self.binchooserinput2.cget('path')
        if (cfg.bin_path and cfg.config_path):
            self.out.delete('1.0','end')
            self.out.insert('end',"bin:%s"%(cfg.bin_path))
            self.out.insert('end','\r\n')
            self.out.insert('end',"yaml:%s"%(cfg.config_path))
            self.out.insert('end','\r\n')
            cfg.upload()
            if(cfg.status == False):
                tk.messagebox.showerror('Config error',cfg.error)
            # os.chdir(config_path)
            self.out.edit_separator()
            self.out.insert('end','-----------Downloading-------------\r\n')

            download = threading.Thread(target=download_bin,args=(app,))
            if download.is_alive() is False:
                download.start() 
            else:
                tk.messagebox.showerror('Flash error','download fail')
        else :
            tk.messagebox.showerror('Path error','please select a valid file')
            
    def erasechip(self):
        cfg.config_path = self.binchooserinput2.cget('path')
        if cfg.config_path:
            self.out.delete('1.0','end')
            self.out.insert('end',"dir:%s"%(cfg.config_path))
            self.out.insert('end','\r\n')
            # os.chdir(config_path)
            self.out.edit_separator()
            if tk.messagebox.askokcancel("Erase", "erase chip?"):
                self.out.insert('end','-----------Start Erase-------------\r\n')
                erase = threading.Thread(target=erase_bin,args=(app,))
                if erase.is_alive() is False:
                    erase.start() 
                else:
                    tk.messagebox.showerror('Flash error','erase fail')
        else :
            tk.messagebox.showerror('Path error','please select a valid config')
    
            
    def press_key(self,event):
        key_index = event.keycode
        if key_index in [13,32]:
            self.download()
        elif key_index == 27:
            if tk.messagebox.askokcancel("Quit", "do you wait exit?"):
                self.mainwindow.destroy()


if __name__ == '__main__':
    app = PyocdApp()
    cfg = Cfg()
    _std = std2tk(app)
    # sys.stdout = _std
    app.run()


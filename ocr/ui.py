import tkinter as tk
from tkinter import messagebox
from tkinter import ttk,Listbox


class MyUI:
    def __init__(self, root: tk.Tk):
        # 东 East
        # 南 South
        # 西 West
        # 北 North
        self.root = root
        self.setmid(root)
        root.title("字符提取工具")
        self.btn_open = ttk.Button(root, text='读取文件', width=60)
        self.btn_open.grid(row=0, column=0, columnspan=3, sticky='w', padx=10, pady=10)
        self.cmb_allalog = ttk.Combobox(root, width=18)
        self.cmb_allalog.grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.txt_config = tk.Text(root, width=20,height=15)
        self.txt_config.grid(row=2, rowspan=2, column=0, sticky='w', padx=10)
        self.btn_add = ttk.Button(root, text=">>")
        self.btn_add.grid(row=1, column=1,rowspan=3,sticky='w', padx=10, pady=10)
        self.list_selectalog = tk.Listbox(root,width=20,height=10)
        self.list_selectalog.insert(tk.END,"123")
        self.list_selectalog.grid(row=2, column=2, rowspan=3, sticky='w', padx=10, pady=10)

    def setmid(self, root):
        window_width = 500
        window_height = 300
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")


if __name__ == '__main__':
    root = tk.Tk()
    ui = MyUI(root)
    root.mainloop()

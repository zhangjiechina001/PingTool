import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("C语言中文网")

root.resizable(300,200)
root.geometry('500x350+300+300')

tk.Label(root, text="用户名").grid(row=0, sticky="w")
tk.Label(root, text="密码").grid(row=1, sticky="w")

tk.Entry(root).grid(row=0, column=1)
tk.Entry(root, show="*").grid(row=1, column=1)
# 加载图片LOGO,注意这里是gif格式的图片
# photo = tk.PhotoImage(file="C:/Users/Administrator/Desktop/1.gif")

tk.Label(root).grid(row=0, column=2, rowspan=2, padx='4px', pady='5px')

# 编写一个简单的回调函数
def login():
    messagebox.showinfo('欢迎来到C语言中文网')

# 使用grid()函数来布局，并控制按钮的显示位置
tk.Button(root, text="登录", width=10, command=login).grid(row=3, column=0, columnspan=2,sticky="w", padx=10, pady=5)
tk.Button(root, text="退出", width=10, command=root.quit).grid(row=3, column=1, columnspan=2,sticky="e", padx=10, pady=5)
# 开启事件主循环
root.mainloop()
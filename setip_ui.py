import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess


class NetAdapter:
    def __init__(self, lines):
        self.EnableDHCP = '是' in lines[1]
        self.IPAddr = lines[2].split(':')[1].strip()
        # 接口 "net1" 的配置
        # DHCP 已启用:                          是
        # IP 地址:                           192.168.1.3
        # 子网前缀:                        192.168.1.0/24 (掩码 255.255.255.0)
        # 默认网关:                         192.168.1.1
        # 网关跃点数:                       0
        # InterfaceMetric:                      35


class SetIPUI:
    def __init__(self, root):
        root.title("网卡设置工具")
        root.geometry('250x250')

        tk.Label(root, text="网卡类型").grid(row=0, padx='2px', pady='3px')
        self.cmb = ttk.Combobox(root)
        self.cmb.grid(row=0, column=1, columnspan=1, padx='2px', pady='3px')
        self.cmb['values'] = self.getAllNames()
        self.cmb.bind("<<ComboboxSelected>>", self.getAdapterInfo)

        rowIndex = 1
        entry_vars = []

        for title in ['ip', '子网掩码', '默认网关', '首选dns', '备用dns']:
            tk.Label(root, text=title).grid(row=rowIndex, column=0, padx='2px', pady='3px')
            entry_var = tk.StringVar()
            tk.Entry(root, textvariable=entry_var).grid(row=rowIndex, column=1, padx='2px', pady='3px')
            entry_vars.append(entry_var)
            rowIndex += 1

        # Function to get values from Entry widgets
        def get_values():
            values = [var.get() for var in entry_vars]
            messagebox.showinfo('Entered Values', ', '.join(values))

        tk.Button(root, text="动态ip", width=10, command=self.setDynamicIp).grid(row=rowIndex, column=0, columnspan=2,
                                                                               sticky="w", padx=10, pady=5)
        tk.Button(root, text="静态ip", width=10, command=root.quit).grid(row=rowIndex, column=1, columnspan=2, sticky="e",
                                                                       padx=10, pady=5)

    def getAllNames(self):
        command = "netsh interface show interface"
        output = subprocess.check_output(command, shell=True, text=True)
        adapters = []
        lines = output.splitlines()
        lines = [l for l in lines if "连接" in l]
        for line in lines:  # 从第四行开始解析
            parts = line.split()
            if len(parts) > 1:
                adapter_name = parts[3]
                adapters.append(adapter_name)
                print(adapter_name)
        return adapters

    def getAdapterInfo(self, event):
        adapter = self.cmb.get()  # 网卡名称
        # 使用 netsh 命令获取特定适配器的 IP 地址状态
        command = f"netsh interface ip show address \"{adapter}\""
        output = subprocess.check_output(command, shell=True, text=True)

        # 解析输出以获取 IP 地址状态
        lines = output.splitlines()
        myAda = NetAdapter(lines)
        for line in lines:
            if "IP 地址" in line:
                print(f"IP 地址状态: {line}")

    def setDynamicIp(self):
        adapter = self.cmb.get()  # 网卡名称
        # 使用netsh设置为动态IP地址（DHCP）
        try:
            ipCmd = f"netsh interface ipv4 set address name={adapter} source=dhcp"
            result = subprocess.run(ipCmd, shell=True, check=True, encoding='utf-8')
            subprocess.run(f"netsh interface ipv4 set dns name={adapter} source=dhcp", shell=True, check=True,
                           encoding='utf-8')
            messagebox.showinfo("完成", "已设置为动态IP地址（DHCP）")
        except subprocess.CalledProcessError as err:
            messagebox.showerror("错误", err.output)

    def setStaticIp(self):
        adapter = self.cmb.get()  # 网卡名称


if __name__ == '__main__':
    root = tk.Tk()
    myUI = SetIPUI(root)
    root.mainloop()

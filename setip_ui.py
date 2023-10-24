# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import re
from re import search
import os
import json


class NetAdapter:
    def __init__(self, lines):
        self.EnableDHCP = '是' in lines[0]
        self.IPAddr = lines[1].split(':')[1].strip()
        input_string = lines[2]
        pattern = r'掩码 (\d+\.\d+\.\d+\.\d+)'
        match = re.search(pattern, input_string)
        self.Mask = "255.255.255.0"
        if (match):
            self.Mask = match.group(1)
        # 接口 "net1" 的配置
        # DHCP 已启用:                          是
        # IP 地址:                           192.168.1.3
        # 子网前缀:                        192.168.1.0/24 (掩码 255.255.255.0)
        # 默认网关:                         192.168.1.1
        # 网关跃点数:                       0
        # InterfaceMetric:                      35

    def EnableDHCPStr(self):
        return '动态IP' if self.EnableDHCP else '静态IP'


class SetIPUI:
    def __init__(self, root):
        root.title("网卡设置工具")
        self.setmid(root)

        tk.Label(root, text="网卡类型").grid(row=0, padx='2px', pady='3px')
        self.configDic = self.initConfig()

        self.cmb = ttk.Combobox(root)
        self.cmb.grid(row=0, column=1, columnspan=1, padx='2px', pady='3px')
        self.cmb['values'] = list(self.configDic.keys())
        self.cmb.bind("<<ComboboxSelected>>", self.getAdapterInfo)

        rowIndex = 1
        self.entry_vars = []
        for title in ['类型', 'ip', '子网掩码']:
            tk.Label(root, text=title).grid(row=rowIndex, column=0, padx='2px', pady='3px')
            entry_var = tk.StringVar()
            entry = tk.Entry(root, textvariable=entry_var)
            entry.grid(row=rowIndex, column=1, padx='2px', pady='3px')
            self.entry_vars.append(entry_var)
            rowIndex += 1

        tk.Button(root, text="动态ip", width=10, command=self.setDynamicIp).grid(row=rowIndex, column=0, columnspan=1,
                                                                                 sticky="w", padx=10, pady=5)
        tk.Button(root, text="静态ip", width=10, command=self.setStaticIp).grid(row=rowIndex, column=1, columnspan=1,
                                                                                sticky="e", padx=10, pady=5)

        text = tk.Text(root, height=20, width=40)
        text.grid(row=0, column=2, rowspan=rowIndex + 1, columnspan=3, sticky="e", padx=10, pady=5)
        self.setExplain(text)

    def setExplain(self, text: tk.Text):
        context = "说明:\n" \
                  "1.启动程序读取config.json文件\n" \
                  "2.如果没有该文件则创建，写入当前网卡信息\n" \
                  "3.通过配置信息进行网卡状态修改\n" \
                  "4.更新文件状态，删除或修改当前config.json即可"
        text.insert('1.0', context)

    def setmid(self, root):
        window_width = 580
        window_height = 280
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def initConfig(self) -> dict:
        fn = 'config.json'
        if not os.path.exists(fn):
            self.createConfig()
        with open(fn, "r", encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data

    def createConfig(self):
        names = self.getAllNames()
        data = {}
        for name in names:
            myAda = self.getAdapterInfoImpl(name)
            if myAda is None:
                continue
            data[name] = {'dhcp': myAda.EnableDHCP, 'ip': myAda.IPAddr, 'mask': myAda.Mask}
        # 写回JSON文件
        fn = 'config.json'
        with open(fn, "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def getAllNames(self):
        command = "netsh interface show interface"
        output = subprocess.check_output(command, shell=True, text=True)
        adapters = []
        lines = output.splitlines()
        lines = [l for l in lines if "连接" in l]
        for line in lines:  # 从第四行开始解析
            parts = line.split('   ')
            if len(parts) > 1:
                adapter_name = parts[-1]
                adapters.append(adapter_name)
                print(adapter_name)
        return adapters

    def getAdapterInfo(self, event):
        key = self.cmb.get()
        adapter = self.configDic[key]
        if adapter is None:
            messagebox.showerror("错误", f"{self.cmb.get()}未连接或未启用")
            return

        dhcp = self.getAdapterInfoImpl(key).EnableDHCPStr()
        self.entry_vars[0].set(dhcp)
        self.entry_vars[1].set(adapter['ip'])
        self.entry_vars[2].set(adapter['mask'])

    def getAdapterInfoImpl(self, adapter):
        command = f"netsh interface ip show address \"{adapter}\""
        output = subprocess.check_output(command, shell=True, text=True)

        # 解析输出以获取 IP 地址状态
        lines = output.splitlines()
        if not any('IP 地址' in line for line in lines):
            return

        myAda = NetAdapter(lines[2:])
        return myAda

    def setDynamicIp(self):
        adapter = self.cmb.get()  # 网卡名称
        # 使用netsh设置为动态IP地址（DHCP）
        try:
            ipCmd = f"netsh interface ipv4 set address name=\"{adapter}\" source=dhcp"
            subprocess.run(ipCmd, shell=True, check=True, encoding='utf-8')
            subprocess.run(f"netsh interface ipv4 set dns name=\"{adapter}\" source=dhcp", shell=True, check=True,
                           encoding='utf-8')
            messagebox.showinfo("完成", "已设置为动态IP地址(DHCP)")
        except subprocess.CalledProcessError as err:
            messagebox.showerror("错误", err.output)

    def setStaticIp(self):
        interface_name = self.cmb.get()  # 网卡名称
        # 请根据你的网络配置进行适当的替换
        ip_address = self.entry_vars[1].get()
        subnet_mask = self.entry_vars[2].get()

        try:
            command = f"netsh interface ipv4 set address name=\"{interface_name}\" static {ip_address} {subnet_mask}"
            # 使用netsh设置静态IP地址
            subprocess.run(command, shell=True,encoding='utf-8',check=True)
            messagebox.showinfo("完成", "已设置为静态IP地址")
        except subprocess.CalledProcessError as err:
            messagebox.showerror("错误", err.output)


if __name__ == '__main__':
    # pyinstaller -F -w --uac-admin -i .\img\network_web_icon.ico -n IPTool .\setip_ui.py
    root = tk.Tk()
    myUI = SetIPUI(root)
    root.mainloop()

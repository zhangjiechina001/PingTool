# import subprocess
#
# # 定义要设置为动态 IP 的网络适配器名称
# adapter_name = "以太网"
#
# # 使用 netsh 命令设置网络适配器的 IP 为动态分配
# command = f"netsh interface ip set address name=\"{adapter_name}\" source=dhcp"
# subprocess.run(command, shell=True, check=True)
import subprocess

# 使用 netsh 命令获取网络适配器信息
command = "netsh interface show interface"
output = subprocess.check_output(command, shell=True, text=True)

# 解析输出以获取适配器信息
adapters = []
lines = output.splitlines()
lines = [l for l in lines if "连接" in l]
for line in lines:  # 从第四行开始解析
    parts = line.split()
    if len(parts) > 1:
        adapter_name = parts[3]
        adapters.append(adapter_name)

# 打印网络适配器列表
for adapter in adapters:
    print(f"Adapter Name: {adapter}")





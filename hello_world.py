name = "Python教程"
def demo ():
    #通过 globals() 函数访问甚至修改全局变量
    print(globals()['name'])
    globals()['name']="Java教程"
    #定义局部变量
    name = "shell教程"
demo()
print(name)
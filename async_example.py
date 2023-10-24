import tkinter as tk
import asyncio

def start_async_task():
    asyncio.ensure_future(async_task())

async def async_task():
    result_label.config(text="Running async task...")
    await asyncio.sleep(2)  # 模拟耗时的异步操作
    result_label.config(text="Async task completed")

root = tk.Tk()
root.title("Async Task with Tkinter")
start_button = tk.Button(root, text="Start Async Task", command=start_async_task)
start_button.pack()

result_label = tk.Label(root, text="1234")
result_label.pack()

def setmid( root):
    window_width = 580
    window_height = 280
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

setmid(root)
root.mainloop()

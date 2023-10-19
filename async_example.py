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

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()

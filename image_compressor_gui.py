import os
import zipfile
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def get_sort_key(file_path, sort_by):
    if sort_by == "name":
        return natural_sort_key(os.path.basename(file_path))
    elif sort_by == "ctime":
        return os.path.getctime(file_path)
    elif sort_by == "mtime":
        return os.path.getmtime(file_path)
    elif sort_by == "size":
        return os.path.getsize(file_path)
    return 0

class ImageCompressorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("图片分组压缩工具")
        self.geometry("600x450")
        self.resizable(False, False)

        self.folder_path = tk.StringVar()
        self.group_size = tk.IntVar(value=20)
        self.sort_by = tk.StringVar(value="name")

        self.create_widgets()

    def create_widgets(self):
        # 文件夹选择
        folder_frame = tk.LabelFrame(self, text="选择图片文件夹", padx=10, pady=5)
        folder_frame.pack(fill="x", padx=10, pady=5)

        tk.Entry(folder_frame, textvariable=self.folder_path, width=50).pack(side="left", padx=(0, 5))
        tk.Button(folder_frame, text="浏览", command=self.browse_folder).pack(side="left")

        # 参数设置
        param_frame = tk.LabelFrame(self, text="压缩设置", padx=10, pady=5)
        param_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(param_frame, text="每组图片数量：").grid(row=0, column=0, sticky="e")
        tk.Spinbox(param_frame, from_=1, to=100, textvariable=self.group_size, width=5).grid(row=0, column=1, sticky="w")

        tk.Label(param_frame, text="排序方式：").grid(row=0, column=2, sticky="e", padx=(20, 0))
        sort_options = ["name", "ctime", "mtime", "size", "none"]
        ttk.Combobox(param_frame, textvariable=self.sort_by, values=sort_options, state="readonly", width=10).grid(row=0, column=3, sticky="w")

        # 压缩按钮
        tk.Button(self, text="开始压缩", command=self.start_compression).pack(pady=10)

        # 日志输出
        log_frame = tk.LabelFrame(self, text="输出日志", padx=10, pady=5)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = tk.Text(log_frame, height=15, wrap="word", state="disabled")
        self.log_text.pack(fill="both", expand=True)

        # 状态栏
        self.status = tk.StringVar(value="准备就绪")
        tk.Label(self, textvariable=self.status, anchor="w").pack(fill="x", padx=10, pady=(0, 5))

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)

    def start_compression(self):
        folder = self.folder_path.get()
        size = self.group_size.get()
        order = self.sort_by.get()

        if not os.path.exists(folder):
            messagebox.showerror("错误", "文件夹路径无效")
            return
        if size < 1:
            messagebox.showerror("错误", "分组大小必须大于0")
            return

        threading.Thread(target=self.compress_images,
                         args=(folder, size, order),
                         daemon=True).start()

    def compress_images(self, folder_path, group_size, sort_by):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        self.log("开始压缩...")
        self.status.set("处理中...")

        try:
            all_files = os.listdir(folder_path)
        except Exception as e:
            self.log(f"错误: 无法读取文件夹 - {e}")
            return

        image_files = []
        for f in all_files:
            file_path = os.path.join(folder_path, f)
            if os.path.isfile(file_path) and os.path.splitext(f)[1].lower() in image_extensions:
                image_files.append(file_path)

        if not image_files:
            self.log("未找到图片文件")
            return

        self.log(f"共找到 {len(image_files)} 张图片")

        if sort_by != "none":
            self.log(f"按 {sort_by} 排序...")
            image_files.sort(key=lambda x: get_sort_key(x, sort_by))

        groups = [image_files[i:i + group_size] for i in range(0, len(image_files), group_size)]
        self.log(f"将创建 {len(groups)} 个压缩包")

        for idx, group in enumerate(groups, 1):
            zip_name = os.path.join(folder_path, f"图片组_{idx:03d}.zip")
            try:
                with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for image_path in group:
                        zipf.write(image_path, arcname=os.path.basename(image_path))
                self.log(f"✓ 创建: {os.path.basename(zip_name)}（{len(group)} 张）")
            except Exception as e:
                self.log(f"✗ 失败: {os.path.basename(zip_name)} - {e}")

        self.status.set("完成")
        self.log("所有压缩包创建完成！")
        messagebox.showinfo("完成", "图片分组压缩完成！")

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"{datetime.now():%H:%M:%S} - {message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

if __name__ == "__main__":
    app = ImageCompressorApp()
    app.mainloop()

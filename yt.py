import subprocess
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading
import time

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube 1080p 下載器")
        self.root.geometry("650x750")
        self.root.resizable(False, False)
        
        # 設定樣式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 標題
        title_label = ttk.Label(
            root, 
            text="YouTube 1080p 下載器",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=15)
        
        # YouTube URL 輸入區
        url_label = ttk.Label(root, text="YouTube 影片網址:", font=("Arial", 10))
        url_label.pack(anchor="w", padx=20, pady=(10, 0))
        
        self.url_entry = ttk.Entry(root, width=70, font=("Arial", 10))
        self.url_entry.pack(padx=20, pady=8)
        
        # 儲存路徑選擇區
        path_label = ttk.Label(root, text="儲存路徑:", font=("Arial", 10))
        path_label.pack(anchor="w", padx=20, pady=(10, 0))
        
        path_frame = ttk.Frame(root)
        path_frame.pack(padx=20, pady=8, fill="x")
        
        self.path_entry = ttk.Entry(path_frame, width=55, font=("Arial", 10))
        self.path_entry.pack(side="left", fill="x", expand=True)
        self.path_entry.insert(0, str(Path.home() / "Downloads"))
        
        browse_btn = ttk.Button(path_frame, text="選擇...", command=self.select_path, width=8)
        browse_btn.pack(side="left", padx=(8, 0))
        
        # 下載類型選擇
        type_label = ttk.Label(root, text="下載類型:", font=("Arial", 10))
        type_label.pack(anchor="w", padx=20, pady=(15, 8))
        
        self.download_type = tk.StringVar(value="best")
        
        type_frame = ttk.Frame(root)
        type_frame.pack(padx=40, pady=0, anchor="w")
        
        tk.Radiobutton(type_frame, text="1080p 影片", variable=self.download_type, value="1080p", font=("Arial", 10), bg="white").pack(anchor="w", pady=3)
        tk.Radiobutton(type_frame, text="最高畫質影片", variable=self.download_type, value="best", font=("Arial", 10), bg="white").pack(anchor="w", pady=3)
        tk.Radiobutton(type_frame, text="音聲 (MP3)", variable=self.download_type, value="mp3", font=("Arial", 10), bg="white").pack(anchor="w", pady=3)
        
        # 選項框架
        options_frame = ttk.Frame(root)
        options_frame.pack(anchor="w", padx=40, pady=5)
        
        self.overwrite_var = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="覆蓋已存在的檔案", variable=self.overwrite_var, font=("Arial", 9), bg="white").pack(anchor="w")
        
        # 穩定模式
        self.stable_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="穩定模式（推薦，確保完整下載）", variable=self.stable_var, font=("Arial", 9), bg="white").pack(anchor="w", pady=(3, 0))
        
        # 進度條
        self.progress_label = ttk.Label(root, text="準備就緒", foreground="green", font=("Arial", 9))
        self.progress_label.pack(pady=(10, 5))
        
        self.progress_bar = ttk.Progressbar(root, length=550, mode='indeterminate')
        self.progress_bar.pack(pady=5)
        
        # 日誌文本框
        log_label = ttk.Label(root, text="下載日誌:", font=("Arial", 9))
        log_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        # 框架用於文本框和滾動條
        log_frame = ttk.Frame(root)
        log_frame.pack(padx=20, pady=5, fill="both", expand=True)
        
        self.log_text = tk.Text(log_frame, height=6, width=75, font=("Courier", 7), bg="#f0f0f0")
        self.log_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # 下載按鈕和取消按鈕
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=12)
        
        self.download_btn = ttk.Button(
            button_frame,
            text="▶ 開始下載",
            command=self.start_download,
            width=20
        )
        self.download_btn.pack(side="left", padx=5)
        
        self.cancel_btn = ttk.Button(
            button_frame,
            text="✕ 取消",
            command=self.cancel_download,
            width=20,
            state='disabled'
        )
        self.cancel_btn.pack(side="left", padx=5)
        
        # 狀態文字
        self.status_label = ttk.Label(root, text="", foreground="green", font=("Arial", 9))
        self.status_label.pack(pady=3)
        
        self.is_downloading = False
        self.download_process = None
        self.download_thread = None
    
    def log(self, message):
        """添加日誌訊息"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def select_path(self):
        """選擇儲存路徑"""
        folder = filedialog.askdirectory(title="選擇儲存資料夾")
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
    
    def update_status(self, message, color="black"):
        """更新狀態訊息"""
        self.status_label.config(text=message, foreground=color)
        self.root.update()
    
    def enable_buttons(self, enable=True):
        """啟用或禁用按鈕"""
        if enable:
            self.download_btn.config(state='normal')
            self.cancel_btn.config(state='disabled')
        else:
            self.download_btn.config(state='disabled')
            self.cancel_btn.config(state='normal')
        self.root.update()
    
    def cancel_download(self):
        """取消下載"""
        self.is_downloading = False
        
        if self.download_process is not None:
            try:
                self.log("⚠️  正在終止下載...")
                if os.name == 'nt':
                    self.download_process.terminate()
                    try:
                        self.download_process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        self.download_process.kill()
                else:
                    self.download_process.terminate()
                    try:
                        self.download_process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        self.download_process.kill()
            except:
                pass
        
        self.log("✓ 已取消")
        self.progress_bar.stop()
        self.update_status("已取消", "orange")
        self.enable_buttons(enable=True)
    
    def start_download(self):
        """開始下載"""
        url = self.url_entry.get().strip()
        save_path = self.path_entry.get().strip()
        download_type = self.download_type.get()
        
        if not url:
            messagebox.showerror("錯誤", "請輸入 YouTube 網址")
            return
        
        if not save_path:
            messagebox.showerror("錯誤", "請選擇儲存路徑")
            return
        
        self.log_text.delete(1.0, tk.END)
        self.log(f"🔍 開始下載")
        self.log(f"📌 類型: {self._get_type_name(download_type)}")
        self.log(f"💾 路徑: {save_path}")
        self.log("-" * 60)
        
        save_path = save_path.strip('"').strip("'")
        
        self.is_downloading = True
        self.enable_buttons(enable=False)
        
        self.download_thread = threading.Thread(
            target=self.download_video,
            args=(url, save_path, download_type),
            daemon=True
        )
        self.download_thread.start()
    
    def _get_type_name(self, download_type):
        """取得下載類型名稱"""
        if download_type == "1080p":
            return "1080p 影片"
        elif download_type == "best":
            return "最高畫質影片"
        else:
            return "音聲 (MP3)"
    
    def open_folder(self, path):
        """打開資料夾"""
        try:
            if os.name == 'nt':
                os.startfile(path)
            else:
                import subprocess as sp
                sp.Popen(['xdg-open', path])
        except:
            pass
    
    def find_latest_video(self, directory):
        """找到最大的視頻/音頻檔案"""
        video_extensions = ('.mp4', '.mkv', '.webm', '.avi', '.mov', '.flv', '.mp3', '.m4a', '.aac', '.wav')
        
        try:
            largest_file = None
            largest_size = 0
            
            for f in os.listdir(directory):
                filepath = os.path.join(directory, f)
                
                if os.path.isfile(filepath) and f.lower().endswith(video_extensions):
                    try:
                        file_size = os.path.getsize(filepath)
                        
                        # 排除太小的檔案（臨時檔案通常很小）
                        if file_size > 1024 * 1024:  # 至少 1MB
                            if file_size > largest_size:
                                largest_size = file_size
                                largest_file = (f, filepath, file_size)
                    except:
                        pass
            
            return largest_file
        except:
            return None
    
    def download_video(self, url, save_path, download_type):
        """執行下載"""
        try:
            Path(save_path).mkdir(parents=True, exist_ok=True)
            self.log("✓ 資料夾已準備")
            
            # 建立 yt-dlp 命令
            cmd = ['yt-dlp']
            
            # 格式選擇 - 排除 Opus 編碼
            if download_type == "1080p":
                cmd.extend(['-f', 'bestvideo[height<=1080][vcodec!=av01][acodec!=opus]+bestaudio[acodec!=opus]/best[acodec!=opus]'])
                self.update_status("⏳ 下載中 (1080p)...", "blue")
                self.log("格式: 1080p + AAC音聲")
            elif download_type == "best":
                cmd.extend(['-f', 'bestvideo[vcodec!=av01][acodec!=opus]+bestaudio[acodec!=opus]/best[acodec!=opus]'])
                self.update_status("⏳ 下載中 (最高畫質)...", "blue")
                self.log("格式: 最高畫質 + AAC音聲")
            else:
                cmd.extend(['-f', 'bestaudio[acodec!=opus]/best'])
                self.update_status("⏳ 下載中 (MP3)...", "blue")
                self.log("格式: MP3")
            
            # 輸出設定
            cmd.extend([
                '-o', os.path.join(save_path, '%(title)s.%(ext)s'),
                '--progress',
                '--no-warnings',
                '--socket-timeout', '30',  # 30 秒超時
            ])
            
            # 穩定模式 - 不使用有問題的並列下載
            if self.stable_var.get():
                # 穩定設定：單線程下載，但有重試機制
                cmd.extend([
                    '--retries', '5',  # 重試 5 次
                    '--fragment-retries', '5',  # 片段重試 5 次
                ])
                self.log("✓ 穩定模式: 確保完整下載")
            
            # 覆蓋選項
            if self.overwrite_var.get():
                cmd.append('--force-overwrites')
                self.log("✓ 覆蓋模式")
            else:
                cmd.append('--no-overwrites')
                self.log("✓ 保留模式")
            
            # MP3 特殊處理
            if download_type == "mp3":
                cmd.extend([
                    '-x',
                    '--audio-format', 'mp3',
                    '--audio-quality', '192',
                ])
            else:
                cmd.extend([
                    '--merge-output-format', 'mp4',
                ])
            
            cmd.append(url)
            
            self.log("🌐 開始下載...")
            self.progress_bar.start()
            
            # 執行 yt-dlp
            self.download_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # 讀取輸出
            for line in self.download_process.stdout:
                if not self.is_downloading:
                    break
                line = line.strip()
                if line:
                    if any(keyword in line.lower() for keyword in ['download', 'error', 'merging', 'converting']):
                        self.log(line)
            
            # 等待完成
            return_code = self.download_process.wait()
            
            if self.is_downloading:
                if return_code == 0:
                    # 等待檔案寫入完成
                    self.log("⏳ 等待檔案寫入...")
                    time.sleep(2)
                    
                    # 尋找下載的檔案
                    found_file = self.find_latest_video(save_path)
                    
                    if found_file:
                        filename, filepath, size = found_file
                        size_mb = size / (1024 * 1024)
                        
                        self.log(f"✅ 下載完成！")
                        self.log(f"📄 {filename}")
                        self.log(f"📊 {size_mb:.2f} MB")
                        
                        self.progress_bar.stop()
                        self.update_status(f"✅ 完成！", "green")
                        
                        response = messagebox.askyesno(
                            "成功",
                            f"下載完成！\n\n{filename}\n{size_mb:.2f} MB\n\n打開資料夾？"
                        )
                        if response:
                            self.open_folder(save_path)
                        
                        self.log("3 秒後關閉...")
                        self.root.after(3000, self.root.quit)
                    else:
                        self.log("❌ 找不到下載的檔案")
                        self.log("可能原因:")
                        self.log("- 檔案已存在（未勾選覆蓋）")
                        self.log("- 影片太小或被中斷")
                        self.progress_bar.stop()
                        self.update_status("❌ 找不到檔案", "red")
                        self.enable_buttons(enable=True)
                
                else:
                    self.progress_bar.stop()
                    self.update_status(f"❌ 失敗", "red")
                    self.log(f"❌ 返回碼: {return_code}")
                    self.log("請檢查網路連線或 YouTube 網址")
                    self.enable_buttons(enable=True)
        
        except FileNotFoundError:
            self.log("❌ yt-dlp 未安裝")
            self.progress_bar.stop()
            self.update_status(f"❌ yt-dlp 未安裝", "red")
            self.log("請執行: pip install yt-dlp")
            self.enable_buttons(enable=True)
        
        except Exception as e:
            self.log(f"❌ 錯誤: {str(e)}")
            self.progress_bar.stop()
            self.update_status(f"❌ 錯誤", "red")
            self.enable_buttons(enable=True)
        
        finally:
            self.is_downloading = False
            self.download_process = None

# 運行應用
if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()

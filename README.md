# 🎬 YouTube 1080p 下載器

一個簡單易用的 **YouTube 影片下載工具**，用 Python 開發，支援 **1080p 高畫質**、**最高畫質自動選擇**、**MP3 音訊提取**。無需終端指令，完全 GUI 操作！

---

## ✨ 主要特色

| 功能 | 說明 |
|------|------|
| 🎥 **1080p 下載** | 優先下載 1080p，無法時自動降級 |
| 🌟 **最高畫質** | 自動選擇最高可用畫質 |
| 🎵 **MP3 提取** | 將影片音訊轉成 MP3（192kbps） |
| 📁 **自動打開資料夾** | 下載完成後一鍵開啟下載位置 |
| ⚡ **穩定下載** | 自動避開 Opus 編碼問題，確保相容性 |
| 🖱️ **完整 GUI** | 無需命令列，點點滑鼠即可操作 |
| 📦 **獨立執行檔** | 打包成 .exe，分享給沒裝 Python 的人 |

---

## 🚀 快速開始

### 方式 1：直接用 .exe（推薦給一般使用者）

1. **下載** `yt.exe` 檔案
2. **雙擊執行**
3. 貼上 YouTube 網址
4. 選擇儲存位置
5. 點擊「開始下載」
6. 完成！✅

### 方式 2：用 Python 執行（給開發者）

```bash
# 1. 安裝依賴
pip install yt-dlp

# 2. 執行程式
python yt.py
```

---

## 📋 系統需求

| 項目 | 需求 |
|------|------|
| **作業系統** | Windows 10 / 11（或 Mac/Linux 用 Python 執行） |
| **Python 版本** | 3.10 以上（如用原始碼執行） |
| **網路連線** | 必須 ✓ |
| **磁碟空間** | 視影片大小（1080p 通常 100-500MB） |

### 必裝套件

```bash
pip install yt-dlp
```

### 內建模組（無需額外安裝）

- tkinter（GUI）
- subprocess（執行外部程式）
- os, pathlib, threading, time（系統操作）

---

## 📖 使用教學

### 步驟 1：貼上 YouTube 網址

在「YouTube 影片網址」欄位貼上：
- ✅ `https://www.youtube.com/watch?v=xxx`
- ✅ `https://youtu.be/xxx`

### 步驟 2：選擇儲存位置

- 預設為 `C:\Users\[你的帳號]\Downloads`
- 點擊「選擇...」可改為其他位置

### 步驟 3：選擇下載類型

| 選項 | 說明 | 檔案格式 |
|------|------|----------|
| **1080p 影片** | 優先 1080p，無則最高畫質 | MP4 |
| **最高畫質影片** | 自動選最高可用畫質 | MP4 |
| **音聲 (MP3)** | 只下載音訊，轉為 MP3 | MP3 |

### 步驟 4：選擇進階選項

```
□ 覆蓋已存在的檔案
  → 勾選：同名檔案會被替換
  → 不勾選：自動重命名（如 video (1).mp4）

☑ 穩定模式（推薦）
  → 勾選：確保下載完整，速度正常
  → 不勾選：可能更快，但有風險
```

### 步驟 5：開始下載

1. 點擊「▶ 開始下載」
2. 觀看下方日誌區顯示進度
3. 進度條轉動表示正在下載
4. 完成後會彈出提示框，問是否打開資料夾
5. 選「是」會自動打開 Windows 檔案總管 ✓

---

## ❓ 常見問題

### Q1: 下載完成後找不到檔案？

**A:** 
- 勾選「是否打開資料夾」→ 自動開啟下載位置
- 或手動進入你選擇的儲存路徑
- 最新的檔案（檔案大小最大）就是你要的

### Q2: 影片沒有聲音？

**A:** 
- 已自動過濾 Opus 編碼，改用 AAC（相容性更好）
- 用 VLC 或其他播放器試試（Windows 內建播放器有時不支援特殊編碼）

### Q3: 為什麼下載速度很慢？

**A:**
- 「穩定模式」優先完整性，速度會正常但不一定最快
- 檢查網路連線品質
- YouTube 伺服器有時會限流

### Q4: 出現「yt-dlp 未安裝」的錯誤？

**A:** 
執行：
```bash
pip install yt-dlp
```

### Q5: 可以下載播放清單或整個頻道嗎？

**A:** 
目前只支援單一影片。如需此功能可提交 GitHub Issue 或自行修改程式碼。

### Q6: 可以在手機上執行嗎？

**A:** 
不能。`.exe` 只能在 Windows 電腦執行。手機使用者建議用線上工具：
- https://y2mate.com
- https://savefrom.net

---

## 🛠️ 開發資訊

### 技術堆疊

```
Language:  Python 3.13
GUI:       tkinter
Download:  yt-dlp (subprocess)
Package:   PyInstaller
```

### 核心邏輯

1. **GUI 介面**：tkinter 製作友善的圖形介面
2. **下載執行**：使用 `yt-dlp` 命令列工具
3. **進程管理**：`subprocess.Popen()` 監控下載進度
4. **編碼過濾**：自動排除 Opus，優選 AAC / MP3
5. **多線程**：在背景下載，不卡 UI
6. **錯誤處理**：完整的異常捕捉與友善的提示

### 專案結構

```
youtube-downloader/
├── yt.py                    # 主程式（GUI + 下載邏輯）
├── README.md                # 專案說明文件
├── requirements.txt         # 依賴套件清單
└── dist/
    └── yt.exe               # 打包好的執行檔
```

### 打包成 .exe（給沒有 Python 的使用者）

```bash
# 1. 安裝 PyInstaller
pip install pyinstaller

# 2. 打包
pyinstaller --onefile --windowed yt.py

# 3. 產出檔案
dist/yt.exe  ← 可直接分享給別人
```

---

## 📝 requirements.txt

```
yt-dlp>=2024.0.0
```

新使用者可執行：
```bash
pip install -r requirements.txt
```

---

## 🔧 進階使用（開發者）

### 修改預設下載位置

在 `yt.py` 中找到這行：

```python
self.path_entry.insert(0, str(Path.home() / "Downloads"))
```

改為你想要的路徑，例如：

```python
self.path_entry.insert(0, "D:/我的影片")
```

### 修改預設下載類型

在 `yt.py` 中找到：

```python
self.download_type = tk.StringVar(value="best")
```

改為 `"1080p"` 或 `"mp3"`

### 自訂應用程式圖標

```bash
pyinstaller --onefile --windowed --icon=app.ico yt.py
```

（需要一個 `app.ico` 檔案）

---

## 📄 License

MIT License - 自由使用、修改、分發

詳見 LICENSE 檔案（若有的話）

---

## 🙋 支援與回報

- **有 Bug？** 提交 GitHub Issue
- **有想法？** 提交 GitHub Discussion 或 Pull Request
- **不知道怎麼用？** 看上面的「常見問題」區塊 😊

---

## 👨‍💻 開發者

**你的名字** （可改成自己的 GitHub 帳號連結）

---

## 💝 感謝

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube 下載核心
- [Python tkinter](https://docs.python.org/3/library/tkinter.html) - GUI 框架
- [PyInstaller](https://pyinstaller.org/) - 打包工具

---

## 🚦 版本歷史

| 版本 | 日期 | 更新內容 |
|------|------|----------|
| v1.0 | 2026-01-13 | 首次發佈，支援 1080p / 最高畫質 / MP3 |

---

**⭐ 如果有幫助，請給個 Star！感謝！**

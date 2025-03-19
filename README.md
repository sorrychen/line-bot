# LINE Business Chatbot

## 📝 專案簡介
本專案是一個 **LINE Business 聊天機器人**，能夠根據不同模式回應使用者，支援 **規則式回應、GPT-4o 模型 回應、OpenAI Assistant 回應**，並整合 **菜單與營業時間查詢**，適用於咖啡廳、餐飲業等客戶服務應用。

---

## 🏗️ 技術棧
- **後端框架**：Flask
- **LINE Bot API**：`line-bot-sdk`
- **AI 回應**：OpenAI GPT-4, OpenAI Assistant
- **Function Calling**：OpenAI Assistant Tool Calling
- **Webhook 服務**：Ngrok（本地測試）
- **部署**：Render + Gunicorn

  
---

## 📌 功能
- **Echo 回應**（`app_rule_base.py`）：簡單回傳使用者的訊息 (只會回覆和使用者一樣句子)
- **GPT-4 回應**（`app_gpt_basic.py`）：使用 GPT-4 進行對話 (不會記住前面內容)
- **OpenAI Assistant 回應**（`app.py`）：更智能的 AI 助手回應 (可記住前面內容對之後問題作回答)
- **查詢咖啡廳菜單**（`menu.txt`）：提供咖啡廳完整菜單
- **查詢咖啡廳營業時間**（`open_hour.txt`）：提供店家營業時間資訊
- **Function Calling 支援**（`tools_list.py`）：
    - 查詢今日日期
    - 查詢營業時間
    - 呼叫使用者名字

---

## 🛠️ 環境設置

### 1️⃣ 安裝環境與相依套件
```bash
# 創建虛擬環境
python -m venv .venv

# 啟動虛擬環境 (Windows)
.venv\Scripts\activate

# 安裝必要套件
pip install -r requirements.txt
```

### 2️⃣ 設定 `.env` 環境變數
請根據 `.env.example` 設定你的 **LINE API Key、OpenAI API Key**。
```plaintext
CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
CHANNEL_SECRET=your_line_channel_secret
LINE_BOT_API_KEY=your_openai_api_key
GPT_FILE_VECTOR_STORE_ID=your_openai_vector_store_id
```

---

## 🚀 運行專案

### 1️⃣ 啟動 Ngrok（本地測試用）
```bash
# 執行 ngrok
ngrok http 5000
```
> **Ngrok 會生成一個公開網址**，將此網址填入 **LINE Webhook URL**。

### 2️⃣ 運行 Flask 伺服器
```bash
python app.py  # 或選擇 app_gpt_basic.py / app_rule_base.py
```

> 測試方式：打開 LINE 聊天機器人，傳送訊息測試回應。

---

## 🌍 部署到 Render

### 1️⃣ 安裝 `gunicorn`
```bash
pip install gunicorn
```

---

## 📂 專案目錄結構
```plaintext
LINE-BOT/
├── .env.example            # 環境變數範例
├── app.py                  # OpenAI Assistant 版本 
├── app_gpt_basic.py        # GPT-4o 版本
├── app_rule_base.py        # Echo 回應版本
├── gpt_funcs.py            # OpenAI Assistant 相關函數
├── menu.txt               
├── open_hour.txt          
├── requirements.txt       
└── tools_list.py           # Function Calling 設定
```

---

## 📜 其他說明
- `gpt_funcs.py`：負責 OpenAI Assistant 互動
- `tools_list.py`：Function Calling 設定
- `menu.txt` / `open_hour.txt`：提供菜單與營業時間資訊

---

<img src="https://github.com/user-attachments/assets/ca515c23-675f-4e04-833d-e03045cc388a" width="300">



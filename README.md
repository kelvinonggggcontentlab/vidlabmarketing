# Vidlab Marketing Telegram Bot (Render Cloud Version)

This repo contains the latest production-grade code and cloud deployment setup for the Vidlab Marketing Telegram Bot.

## Features
- **Multilingual (English + Bahasa Malaysia) welcome and operation interface**
- **Asynchronous, non-blocking Google Sheets logging** (auto-record Staff Verify login time)
- **Auto photo (LOGO) reply and robust ID validation**
- **Cloud 24/7 online: Render.com free plan compatible**

---

## 快速指南（中文）

### 1. 必须上传以下文件到根目录：
- `Main_sriptt.py` （主程序）
- `requirements.txt` （依赖清单）
- `vidlab_logo.png`（公司Logo图）
- `vidlab-marketing-460409-f0e918ae72e2.json`（Google服务账号JSON，需已被Google Sheet授权）

### 2. Render.com部署设置
- **Build Command:**  
  `pip install -r requirements.txt`
- **Start Command:**  
  `python Main_sriptt.py`
- **Python version:** 3.11
- **环境变量建议设置：**  
  `BOT_TOKEN=你的Telegram Bot Token`
- 仅允许一处run_polling，勿本地/云端同时跑

### 3. Google Sheet表结构
- A: STAFF ID
- B: STAFF NAME
- C: TELEGRAM USERNAME
- D: TELEGRAM ID
- E: TELEGRAM MESSAGE LINK
- F: ROLE
- G: STATUS
- G:AA: 登录记录

### 4. 常见错误排查
- **API权限/Token冲突/文件名拼写**：参考代码内注释与本项目文档
- **如需Webhook上线或多云互备，联系主开发Kelvin或见本repo FAQ**

---

## English Quick Guide

1. Upload the following to the root:
   - Main_sriptt.py
   - requirements.txt
   - vidlab_logo.png
   - vidlab-marketing-460409-f0e918ae72e2.json (ensure Google Sheet shared to this service account)

2. Render.com settings:
   - Build: `pip install -r requirements.txt`
   - Start: `python Main_sriptt.py`
   - Python: 3.11
   - Set env `BOT_TOKEN` (Telegram Bot Token)
   - Only one process with run_polling at a time!

3. Google Sheet column order:
   - STAFF ID, STAFF NAME, TELEGRAM USERNAME, TELEGRAM ID, ... LOGIN TIME G:AA

4. Troubleshooting:
   - API permissions, file/column name typo, token conflicts -- see code comments.
   - For Webhook/cloud scaling, contact Kelvin or check repo FAQ.

---

### Contact & Maintenance

Project Maintainer: Kelvin Ong  
Telegram: [你的联系方式]  
For business/automation partnership, please open an issue or contact above.

---

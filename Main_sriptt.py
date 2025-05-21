#!/usr/bin/env python3
import os
import logging
import pytz
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
from concurrent.futures import ThreadPoolExecutor

SCOPE = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
JSON_PATH = './vidlab-marketing-460409-f0e918ae72e2.json'
SPREADSHEET_NAME = 'VidLab_Marketing_Tracking_Managed_v1'
STAFF_LIST_SHEET = 'Staff List'
LOGO_PATH = './vidlab_logo.png'

VERIFY, INPUT_STAFF_ID, MAIN_MENU = range(3)

executor = ThreadPoolExecutor()

def get_gsheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_PATH, SCOPE)
    client = gspread.authorize(creds)
    return client

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 先发logo
    if os.path.exists(LOGO_PATH):
        await update.message.reply_photo(photo=InputFile(LOGO_PATH))
    # 双语欢迎信息
    welcome_msg = (
        "Welcome to Vidlab Marketing!\n"
        "I'm Calvin from AI Content Department, and also your Vidlab AI Assistant.\n\n"
        "Selamat datang ke Vidlab Marketing!\n"
        "Saya Calvin dari Jabatan Kandungan AI, juga Pembantu AI Vidlab anda.\n"
    )
    reply_keyboard = [[KeyboardButton("Staff Verify / Pengesahan Staf")]]
    await update.message.reply_text(
        welcome_msg,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return VERIFY

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please enter your Staff ID (e.g. G003):\n"
        "Sila masukkan ID Staf anda (contoh: G003):"
    )
    return INPUT_STAFF_ID

def sync_sheet_update(staff_id, telegram_user):
    try:
        gc = get_gsheet()
        sheet = gc.open(SPREADSHEET_NAME).worksheet(STAFF_LIST_SHEET)
        # 取A列（STAFF ID），去空格大写
        all_staff = [x.strip().upper() for x in sheet.col_values(1) if x.strip()]
        if staff_id not in all_staff:
            return False
        staff_records = sheet.get_all_records()
        staff_row = None
        for idx, record in enumerate(staff_records):
            if str(record['STAFF ID']).strip().upper() == staff_id:
                staff_row = idx + 2
                sheet.update_cell(staff_row, 3, telegram_user.username or "")
                sheet.update_cell(staff_row, 4, str(telegram_user.id))
                break
        # G:AA 登录时间
        if staff_row:
            tz = pytz.timezone('Asia/Kuala_Lumpur')
            now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
            row_values = sheet.row_values(staff_row)
            first_empty_col = 7
            for col in range(7, 28):
                if len(row_values) < col or row_values[col-1] == "":
                    first_empty_col = col
                    break
            sheet.update_cell(staff_row, first_empty_col, now)
            return True
        return False
    except Exception as e:
        print(f"Error in sync_sheet_update: {e}")
        return False

async def input_staff_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    staff_id = update.message.text.strip().upper()
    telegram_user = update.effective_user

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, sync_sheet_update, staff_id, telegram_user)
    if not result:
        await update.message.reply_text(
            "❌ Invalid Staff ID! Please contact admin or re-enter.\n"
            "❌ ID Staf tidak sah! Sila hubungi admin atau masukkan semula."
        )
        return INPUT_STAFF_ID

    await update.message.reply_text(
        "✅ Staff verification successful! Login time recorded.\n"
        "✅ Pengesahan staf berjaya! Masa login telah direkodkan."
    )
    reply_keyboard = [[KeyboardButton("Upload Footage / Muat Naik Footage")]]
    await update.message.reply_text(
        "Please select an option:\nSila pilih operasi:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return MAIN_MENU

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Operation cancelled.\nOperasi dibatalkan."
    )
    return ConversationHandler.END

def main():
    application = Application.builder().token('7624965037:AAF9ZyfK_ZnbGhnwYMtDbGlV23n-SO_59qo').build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            VERIFY: [MessageHandler(filters.Regex("^Staff Verify / Pengesahan Staf$"), verify)],
            INPUT_STAFF_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, input_staff_id)],
            MAIN_MENU: [MessageHandler(filters.Regex("^(Upload Footage / Muat Naik Footage)$"), lambda u, c: u.message.reply_text("...not implemented..."))],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()


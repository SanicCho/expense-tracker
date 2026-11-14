import csv
import os
from datetime import datetime

# 與 Member B 約定的資料檔案名稱與欄位標題
DATA_FILE = "expenses.csv"
HEADERS = ["date", "amount", "category", "notes"]


def initialize_csv(file_path=DATA_FILE):
    """確認資料檔案是否存在，若不存在或為空檔案則自動建立並寫入標題列。"""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

def save_expense(date, amount, category, notes="", file_path=DATA_FILE):
    """將單筆支出附加寫入 CSV 檔案中。"""
    initialize_csv(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date, amount, category, notes])
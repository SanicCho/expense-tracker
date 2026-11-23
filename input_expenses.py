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

def get_valid_date():
    """取得並驗證日期輸入（預設為今日，或符合 YYYY-MM-DD 格式）。"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    while True:
        date_input = input(f"請輸入日期 (YYYY-MM-DD) [直接按 Enter 預設為 {today_str}]: ").strip()
        if not date_input:
            return today_str
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("❌ 日期格式錯誤，請依照 YYYY-MM-DD 格式輸入（例如 2026-11-14）。")

def get_valid_amount():
    """取得並驗證金額輸入（必須為大於 0 的數字）。"""
    while True:
        amount_input = input("請輸入金額: ").strip()
        try:
            amount = float(amount_input)
            if amount <= 0:
                print("❌ 金額必須大於 0，請重新輸入。")
                continue
            return amount
        except ValueError:
            print("❌ 金額格式錯誤，請輸入有效的數字（例如 150 或 99.5）。")


def get_valid_category():
    """取得並驗證類別輸入（不可為空，並統一首字母大寫以利後續圓餅圖分組）。"""
    while True:
        category_input = input("請輸入類別 (例如 Food, Transport, Entertainment): ").strip()
        if category_input:
            # 統一格式化，避免 "food" 與 "Food" 被圓餅圖判定為不同類別
            return category_input.capitalize()
        print("❌ 類別為必填欄位，不可為空。")

def save_expense(date, amount, category, notes="", file_path=DATA_FILE):
    """將單筆支出附加寫入 CSV 檔案中。"""
    initialize_csv(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date, amount, category, notes])

def run_input_module():
    """執行互動式支出輸入迴圈，支援連續新增多筆支出。"""
    print("=== 支出紀錄輸入系統 (Input Module) ===")
    initialize_csv()

    while True:
        print("\n--- 新增一筆支出 ---")
        date = get_valid_date()
        amount = get_valid_amount()
        category = get_valid_category()
        notes = input("請輸入備註 (選填，可直接按 Enter 略過): ").strip()

        save_expense(date, amount, category, notes)
        print(f"✅ 已儲存：{date} | {category} | ${amount:.2f} | 備註: {notes if notes else '無'}")

        cont = input("\n是否繼續新增下一筆支出？(y/n) [預設 y]: ").strip().lower()
        if cont == "n":
            print("結束輸入，所有資料已安全儲存至 expenses.csv。")
            break


if __name__ == "__main__":
    run_input_module()
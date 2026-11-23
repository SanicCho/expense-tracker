import csv
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path


def load_totals(path):
    totals = defaultdict(Decimal)
    skipped = 0
    with Path(path).open(encoding="utf-8-sig", newline="") as source:
        rows = csv.DictReader(source)
        if not {"category", "amount"}.issubset(rows.fieldnames or []):
            raise ValueError("CSV 缺少 category 或 amount 欄位。")
        for row in rows:
            category = (row.get("category") or "").strip()
            try:
                amount = Decimal(row.get("amount") or "")
            except InvalidOperation:
                amount = None
            if not category or amount is None or not amount.is_finite() or amount <= 0:
                skipped += 1
                continue
            totals[category] += amount
    return sorted(totals.items(), key=lambda item: (-item[1], item[0])), skipped


def draw_chart(data):
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    fonts = ["Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC", "Noto Sans CJK JP"]
    available = font_manager.get_font_names()
    plt.rcParams["font.family"] = [f for f in fonts if f in available] + ["DejaVu Sans"]
    labels = [category for category, _ in data]
    amounts = [float(value) for _, value in data]
    fig, ax = plt.subplots()
    ax.pie(amounts, labels=labels, autopct="%.1f%%", startangle=90)
    ax.set_title("支出類別分布")
    return fig


def main():
    import argparse
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(description="依支出類別繪製圓餅圖")
    parser.add_argument("--csv", default="expenses.csv", help="資料檔路徑")
    args = parser.parse_args()
    try:
        data, skipped = load_totals(args.csv)
        if skipped:
            print(f"已略過 {skipped} 筆無效支出。")
        if not data:
            print("目前沒有有效支出，請先執行 input_expenses.py 新增資料。")
            return
        draw_chart(data)
        plt.show()
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"無法產生圖表：{error}\n")


if __name__ == "__main__":
    main()

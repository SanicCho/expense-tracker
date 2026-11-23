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
    paper, ink, muted = "#faf8f2", "#193f38", "#54675f"
    palette = ["#217565", "#d28a44", "#547da4", "#ae6675", "#7d874c", "#9179ab"]
    total = sum(value for _, value in data)
    fractions = [float(value / total) for _, value in data]
    colors = [palette[i % len(palette)] for i in range(len(data))]
    height = max(5, 2 + len(data) * 0.46)
    fig, (ring, detail) = plt.subplots(1, 2, figsize=(10, height),
                                      gridspec_kw={"width_ratios": [1, 1.2]})
    fig.patch.set_facecolor(paper)
    fig.subplots_adjust(left=.04, right=.96, bottom=.09, top=.79, wspace=.12)
    fig.text(.055, .89, "支出類別分布", fontsize=23, weight="bold", color=ink)
    ring.pie(fractions, colors=colors, startangle=90, counterclock=False,
             wedgeprops={"width": .3, "edgecolor": paper, "linewidth": 2})
    ring.text(0, .14, "總支出", ha="center", color=muted, fontsize=11)
    ring.text(0, -.13, f"{total:,.2f}", ha="center", color=ink, fontsize=18)
    detail.set_axis_off()
    detail.set_xlim(0, 1)
    detail.set_ylim(-len(data), 1)
    for x, label, align in [(.055, "類別", "left"), (.78, "金額", "right"), (1, "占比", "right")]:
        detail.text(x, .6, label, ha=align, color=muted, fontsize=10)
    for i, ((label, value), fraction) in enumerate(zip(data, fractions)):
        y = -i - .3
        detail.axhline(y + .48, color="#dedfd5", lw=.8)
        detail.scatter(.015, y, color=colors[i], s=45)
        detail.text(.055, y, label, va="center", color=ink, parse_math=False)
        detail.text(.78, y, f"{value:,.2f}", va="center", ha="right", color=ink)
        detail.text(1, y, f"{fraction:.1%}", va="center", ha="right", color=muted)
    return fig


def main():
    import argparse
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(description="依支出類別繪製圓餅圖")
    parser.add_argument("--csv", default="expenses.csv", help="資料檔路徑")
    parser.add_argument("--output", help="將圖表輸出成 PNG")
    args = parser.parse_args()
    try:
        data, skipped = load_totals(args.csv)
        if skipped:
            print(f"已略過 {skipped} 筆無效支出。")
        if not data:
            print("目前沒有有效支出，請先執行 input_expenses.py 新增資料。")
            return
        fig = draw_chart(data)
        if args.output:
            fig.savefig(args.output, dpi=160, bbox_inches="tight")
            plt.close(fig)
        else:
            plt.show()
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"無法產生圖表：{error}\n")


if __name__ == "__main__":
    main()

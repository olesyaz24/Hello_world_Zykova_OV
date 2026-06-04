import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch

print("Подключение к базе данных...")

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5430",
        user="postgres_user",
        password="postgres_password",
        database="postgres_db"
    )
    print("✓ Подключение установлено")

    # Запрос 1: средняя цена и количество товаров по категориям
    df_categories = pd.read_sql("""
        SELECT
            pr.category,
            ROUND(AVG(p.price)::numeric, 2) AS avg_price,
            COUNT(*) AS total_products
        FROM prices p
        JOIN products pr ON p.product_id = pr.id
        GROUP BY pr.category
        ORDER BY avg_price DESC
    """, connection)

    # Запрос 2: количество товаров по категориям (для круговой диаграммы)
    df_categories_pie = pd.read_sql("""
        SELECT
            pr.category,
            COUNT(*) AS product_count
        FROM prices p
        JOIN products pr ON p.product_id = pr.id
        GROUP BY pr.category
        ORDER BY product_count DESC
    """, connection)

    # Запрос 3: все цены (только столбец price)
    df_prices = pd.read_sql("SELECT price FROM prices", connection)

    # Запрос 4: аномалии — товары с ценой выше Q3 + 1.5*IQR
    df_anomalies = pd.read_sql("""
        WITH price_stats AS (
            SELECT
                PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) as q1,
                PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) as q3
            FROM prices
        )
        SELECT
            pr.name AS product_name,
            pr.category,
            p.price
        FROM prices p
        JOIN products pr ON p.product_id = pr.id
        CROSS JOIN price_stats
        WHERE p.price > q3 + 1.5 * (q3 - q1)
        ORDER BY p.price DESC
    """, connection)

    print(f"Категорий: {len(df_categories)} | Записей: {len(df_prices)} | Аномалий: {len(df_anomalies)}")

except Exception as error:
    print(f"Ошибка: {error}")
    raise SystemExit

finally:
    connection.close()
    print("✓ Соединение закрыто\n")

# Расчёт статистики
mean_price = df_prices["price"].mean()
median_price = df_prices["price"].median()
std_price = df_prices["price"].std()
q1 = df_prices["price"].quantile(0.25)
q3 = df_prices["price"].quantile(0.75)

overall_avg = df_categories["avg_price"].mean()
bar_colors = ["#2ecc71" if val > overall_avg else "#f0ad4e" for val in df_categories["avg_price"]]

# Настройка графиков
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "figure.dpi": 130,
})

fig = plt.figure(figsize=(16, 10))
fig.suptitle("Анализ товарной базы данных", fontsize=15, fontweight="bold", y=1.01)

gs = gridspec.GridSpec(2, 3, figure=fig,
                       height_ratios=[5, 4],
                       width_ratios=[2, 1, 2],
                       hspace=0.45, wspace=0.35)

ax1 = fig.add_subplot(gs[0, 0:2])
ax2 = fig.add_subplot(gs[0, 2])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1:3])

# ГРАФИК 1: Средняя цена по категориям
bars1 = ax1.barh(
    df_categories["category"],
    df_categories["avg_price"],
    color=bar_colors,
    edgecolor="white",
    height=0.6,
)

for bar, val in zip(bars1, df_categories["avg_price"]):
    ax1.text(
        bar.get_width() + 0.04,
        bar.get_y() + bar.get_height() / 2,
        f"{val:.2f}",
        va="center", fontsize=9,
    )

ax1.axvline(overall_avg, color="crimson", linestyle="--",
            linewidth=1.3, label=f"Среднее: {overall_avg:.2f} руб.")
ax1.set_xlim(0, df_categories["avg_price"].max() * 1.1)
ax1.set_xlabel("Средняя цена (руб.)")
ax1.set_title("Средняя цена по категориям", fontweight="bold", pad=8)

legend_patches = [
    Patch(facecolor="#2ecc71", label=f"Выше среднего (≥ {overall_avg:.2f})"),
    Patch(facecolor="#f0ad4e", label="Ниже среднего"),
]
ax1.legend(handles=legend_patches, fontsize=8, loc="lower right")

# ГРАФИК 2: Количество товаров по категориям
bars2 = ax2.bar(
    df_categories["category"],
    df_categories["total_products"],
    color="#5cb85c",
    edgecolor="white",
    width=0.6,
)

for bar in bars2:
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.15,
        str(int(bar.get_height())),
        ha="center", fontsize=9,
    )

ax2.set_ylim(0, df_categories["total_products"].max() + 2.5)
ax2.set_ylabel("Количество товаров")
ax2.set_title("Количество товаров\nпо категориям", fontweight="bold", pad=8)
ax2.set_xticks(range(len(df_categories)))
ax2.set_xticklabels(df_categories["category"], rotation=40, ha="right", fontsize=8)

# ГРАФИК 3: Круговая диаграмма
pie_labels = [f"{row.category} ({row.product_count} шт.)" for _, row in df_categories_pie.iterrows()]
pie_colors = ["#7b68ee", "#4a90d9", "#2ecc71", "#f0ad4e", "#d9534f"]

wedges, texts, autotexts = ax3.pie(
    df_categories_pie["product_count"],
    labels=None,
    autopct="%1.0f%%",
    colors=pie_colors[:len(df_categories_pie)],
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    pctdistance=0.7,
)

for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight("bold")

ax3.set_title("Товары\nпо категориям", fontweight="bold", pad=8)
ax3.legend(
    wedges, pie_labels,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.22),
    fontsize=8,
    frameon=False,
)

# ГРАФИК 4: Гистограмма распределения цен
ax4.hist(df_prices["price"], bins=20, color="#f0ad4e", edgecolor="white", alpha=0.7)
ax4.axvline(median_price, color="crimson", linestyle="--", linewidth=1.5, label=f"Медиана: {median_price:.2f} руб.")
ax4.axvline(mean_price, color="blue", linestyle=":", linewidth=1.5, label=f"Среднее: {mean_price:.2f} руб.")

stats_text = (
    f"Всего: {len(df_prices)}\n"
    f"Среднее: {mean_price:.2f}\n"
    f"Медиана: {median_price:.2f}\n"
    f"Ст.откл.: {std_price:.2f}\n"
    f"Q1: {q1:.2f} | Q3: {q3:.2f}"
)

ax4.text(0.97, 0.95, stats_text,
         transform=ax4.transAxes, va="top", ha="right", fontsize=8,
         bbox={"boxstyle": "round,pad=0.4", "facecolor": "lightyellow",
               "edgecolor": "lightgray", "alpha": 0.8})

if not df_anomalies.empty:
    max_price = df_anomalies["price"].max()
    ax4.annotate(
        f"Аномалия: {len(df_anomalies)} товаров",
        xy=(max_price, 0),
        xytext=(max_price * 0.7, ax4.get_ylim()[1] * 0.7),
        arrowprops={"arrowstyle": "->", "color": "crimson"},
        fontsize=8, color="crimson",
    )

ax4.set_xlabel("Цена (руб.)")
ax4.set_ylabel("Количество товаров")
ax4.set_title("Распределение цен на товары", fontweight="bold", pad=8)
ax4.legend(fontsize=8)

# Подпись об аномалиях
if df_anomalies.empty:
    fig.text(0.5, -0.03, "✅ Аномалий не обнаружено", ha="center", fontsize=9, color="#2ecc71")
else:
    fig.text(0.5, -0.03, f"⚠ Аномалия: {len(df_anomalies)} товаров с аномально высокой ценой",
             ha="center", fontsize=9, color="#8b0000")

# Сохранение
OUTPUT_FILE = "product_analysis_charts.png"
plt.savefig(OUTPUT_FILE, bbox_inches="tight", dpi=150)
print(f"✓ График сохранён: {OUTPUT_FILE}")

plt.show()

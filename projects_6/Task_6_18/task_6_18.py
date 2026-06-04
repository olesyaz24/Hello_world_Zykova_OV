import psycopg2
import pandas as pd

try:
    conn = psycopg2.connect(
        host="localhost",
        port="5430",
        user="postgres_user",
        password="postgres_password",
        database="postgres_db"
    )
    print("Подключение успешно!")

    query = """
      SELECT 
          p.product_id,
          pr.name AS product_name,
          pr.category,
          p.price
      FROM prices p
      JOIN products pr ON p.product_id = pr.id
    """

    df = pd.read_sql(query, conn)
    conn.close()

    print("\nРезультат:")
    print(df)

except Exception as error:
    print(f"Ошибка: {error}")

print("\n=== Значения ===")
metrics = {
    'Среднее (mean)': df['price'].mean(),
    'Медиана (median)': df['price'].median(),
    'Ст. отклонение (std)': df['price'].std(),
    'Минимум (min)': df['price'].min(),
    'Максимум (max)': df['price'].max()
}

for name, val in metrics.items():
    print(f"{name:30s}: {val:.2f} руб.")
print("\n=== Квартили ===")
q1 = df['price'].quantile(0.25)
q2 = df['price'].quantile(0.50)
q3 = df['price'].quantile(0.75)
iqr = q3 - q1

print(f"Q1 (25%): {q1}")
print(f"Q2 (50%): {q2}")
print(f"Q3 (75%): {q3}")
print(f"IQR (Q3-Q1): {iqr}")

expensive = df[df['price'] > q3]
print(f"\nТовары с ценой выше Q3 (выше {q3:} руб.):")
print(expensive[['product_name', 'category', 'price']])

category_stats = df.groupby('category').agg(
    count=('price', 'count'),
    mean_price=('price', 'mean'),
    median_price=('price', 'median'),
    std_price=('price', 'std')
).round(2).sort_values('mean_price', ascending=False)

print("\n" + "=" * 50)
print("СТАТИСТИКА ПО КАТЕГОРИЯМ")
print("=" * 50)
print(category_stats)

price_range = df.groupby('product_name').agg(
    min_price=('price', 'min'),
    max_price=('price', 'max'),
    category=('category', 'first')
)
price_range['price_span'] = price_range['max_price'] - price_range['min_price']
top5 = price_range.nlargest(5, 'price_span')

print("\n" + "=" * 50)
print("ТОП-5 ТОВАРОВ С НАИБОЛЬШИМ РАЗБРОСОМ ЦЕН")
print("=" * 50)
print(top5[['category', 'min_price', 'max_price', 'price_span']])








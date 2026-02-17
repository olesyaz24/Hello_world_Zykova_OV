operator = input("Введите имя оператора: ")
pressure = input("Введите текущее значение давления (Па): ")

with open("sensor_log.txt", "w", encoding="utf-8") as file:
    file.write(f"Введите имя оператора: {operator}\n Введите текущее значение давления (Па): {pressure}\n")

print("Данные успешно сохранены в sensor_log.txt")
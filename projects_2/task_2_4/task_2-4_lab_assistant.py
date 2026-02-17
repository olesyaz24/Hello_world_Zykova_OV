volume = float(input("Введите объем раствора (мл): "))
salt_mass = volume * 0.09
salt_mass_rounded = round(salt_mass, 2)
with open("recipe.txt", "w", encoding="utf-8") as file:
    
    file.write("ОТЧЕТ ПО ПРИГОТОВЛЕНИЮ:\n")
    file.write("-" * 30 + "\n")
    file.write(f"Общий объем: {volume} мл\n")
    file.write(f"Масса соли: {salt_mass_rounded} г\n")
    file.write(f"Объем воды: {volume} мл\n")

print("Рецепт сохранен в файл recipe.txt")

reagent_name = input("название реактива: ")
reagent_quantity = input("количество шт: ")
print(f"Реактив {reagent_name} поступил на склад в количестве {reagent_quantity} шт")
with open("inventory.txt", "w", encoding="utf-8") as file:

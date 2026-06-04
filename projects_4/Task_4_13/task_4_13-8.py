N = int(input("Введите количество элементов массива: "))
count = 0
i = 1

while i <= N:
    a = float(input(f"Введите элемент {i}: "))

    if a > 0:

        count = count + 1

    i = i + 1

print("Количество", count)
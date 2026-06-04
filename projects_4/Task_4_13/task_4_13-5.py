N = int(input("Введите количество чисел: "))
a = int(input("Введите число: "))

max_number = a
i = 2

while i <= N:
    a = int(input(f"Введите число {i}: "))

    if a > max_number:

        max_number = a
    i = i + 1

print(max_number, "Максимальное число:")
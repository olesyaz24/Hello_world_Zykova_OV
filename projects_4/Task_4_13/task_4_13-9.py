N = int(input("Введите количество элементов массива: "))

sum = 0
i = 1

while i <= N:
    a = int(input(f"Введите элемент {i}: "))
    if a % 2 != 0:
        sum = sum + a

    i = i + 1

print("Сумма всех нечетных элементов: ", sum)

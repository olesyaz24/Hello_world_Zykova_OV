N = int(input("Введите количество элементов массива: "))

sum = 0
i = 1

while i <= N:
    a = int(input(f"Введите элемент {i}: "))
    sum = sum + a
    i = i + 1

avg = sum / N

print("Среднее арифметическое:", avg)
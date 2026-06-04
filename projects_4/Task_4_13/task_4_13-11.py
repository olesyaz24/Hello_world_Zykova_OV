N = int(input("Введите количество элементов массива: "))
sum = 0
count = 0
i = 1

while i <= N:
    a = int(input(f"Введите элемент {i}: "))

    if i % 2 == 0:
        sum = sum + a
        count = count + 1
    i = i + 1

avg = sum / count
print("Среднее арифметическое элементов с чётными индексами:", avg)

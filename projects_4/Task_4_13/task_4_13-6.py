N = int(input("Введите N: "))

i = 1
sum = 0

while i <= N:

    sum = sum + (i * i)
    i = i + 1

print(sum, "Сумма квадратов первых", N, "натуральных чисел:")

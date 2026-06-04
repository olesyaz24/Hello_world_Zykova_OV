a = float(input("Введите первое число: "))
b = float(input("Введите второе число: "))
c = float(input("Введите третье число: "))
d = float(input("Введите четвёртое число: "))

min_number = a

if min_number > b:
    min_number = b

if min_number > c:
    min_number = c

if min_number > d:
    min_number = d

print("Минимальное число:", min_number)
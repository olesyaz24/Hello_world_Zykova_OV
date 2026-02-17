dna = input("Введите последовательность ДНК: ")
dna_upper = dna.upper()

a_count = dna_upper.count("A")
t_count = dna_upper.count("T")
g_count = dna_upper.count("G")
c_count = dna_upper.count("C")

total_length = len(dna_upper)

a_percent = (a_count / total_length) * 100
t_percent = (t_count / total_length) * 100
g_percent = (g_count / total_length) * 100
c_percent = (c_count / total_length) * 100

print("\n=== Анализ последовательности ДНК ===\n")
print(f"Последовательность в верхнем регистре: {dna_upper}")
print("\nПодсчёт нуклеотидов:")
print(f"A: {a_count} ({a_percent:.1f}%)")
print(f"T: {t_count} ({t_percent:.1f}%)")
print(f"G: {g_count} ({g_percent:.1f}%)")
print(f"C: {c_count} ({c_percent:.1f}%)")
print(f"\nОбщая длина: {total_length} нуклеотидов")

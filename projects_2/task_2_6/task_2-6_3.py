donor = input("Введите группу крови донора (I, II, III, IV): ").upper()
recipient = input("Введите группу крови реципиента (I, II, III, IV): ").upper()

if donor == "I":
    print("Переливание возможно (I — универсальный донор)")
elif donor == recipient:
    print("Переливание возможно (группы совпадают)")
elif donor == "II" and (recipient == "II" or recipient == "IV"):
    print("Переливание возможно (II можно переливать II и IV)")
elif donor == "III" and (recipient == "III" or recipient == "IV"):
    print("Переливание возможно (III можно переливать III и IV)")
elif donor == "IV" and recipient == "IV":
    print("Переливание возможно (IV можно переливать только IV)")
else:
    print("Переливание невозможно")
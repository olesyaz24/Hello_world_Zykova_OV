read -p "Введите массу(в кг): " WEIGHT
read -p "Введите рост(в м): " HEIGHT
BMI=$((WEIGHT/HEIGHT**2))
echo "ИМТ=$BMI"


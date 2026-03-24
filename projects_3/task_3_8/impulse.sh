#!/bin/bash

read -p "Введите название гена: " gene_name
read -p "Введите уровень экспрессии гена: " expression

if [ -z "$gene_name" ] || [ -z "$expression" ]; then
echo "Ошибка! Недостаточно данных."
exit 1
fi

echo "Экспрессия гена $gene_name составляет $expression единиц"

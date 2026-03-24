#!/bin/bash

for i in {1..10}; do 
touch "test$i.txt"; 
done
echo "Создано 10 файлов"

counter=10
while [ $counter -ge 1 ]; do
rm "test$counter.txt"
counter=$((counter - 1))
done
echo "Удалено 10 файлов"

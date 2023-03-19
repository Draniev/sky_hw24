== Домашка №23 ==

1. Принимает 5 параметров: где 1, 2, 3, 4 - запрос, 5-ый - имя файла. 
2. Метод ищет файлы внутри директории data.
3. Обрабатывает файлы, следуя написанному запросу, и возвращает ответ клиенту

Доступны запросы по GET и POST методам.
примеры команд:
- sort (asc|desc) сортирует по возрастанию, убыванию
- limit (N) выводит только N записей
- map (N) выводит N-ную колонку из записи
- filter (str) ищет записи с содержимым str
- unique ("") возвращает только уникальные строчки

Пример запроса GET
http://127.0.0.1:5000/perform_query?filename=apache_logs.txt&cmd1=filter&value1=216&cmd2=map&value2=0

Пример запроса POST
curl -X 'POST' 127.0.0.1:5000/perform_query \
-d '{"filename":"apache_logs_small.txt", "cmd1":"filter", "value1":"216", "cmd2":"limit", "value2":"5"}' \
-H 'Content-type: application/json'

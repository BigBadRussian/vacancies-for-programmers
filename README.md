# Сравнение зарплат программистов в завивисимости от языка
Программа для терминала. Строит терминальную таблицу, показывающую среднюю зарплату 
для нескольких популярных языков программирования. Данные для расчетов 
запрашиваются от API HeadHunter и SuperJob двумя скриптами соответственно.
Третий скрипт (Build_table) объединяет данные и строит таблицу.

### Как установить
Для получения информации от API HH [пройдите по ссылке](https://dev.hh.ru/admin),
затем выберите "регистрация нового приложения". Когда получите user-agent, запишите 
данные в .env файл:  
```
'USER_AGENT_HH' = 'ваш user-agent'
```
Для получения информации от API SJ [пройдите по ссылке](https://api.superjob.ru/),
поле регистрации вы получите ваш secret_key. Запишите ключ в .env:
```
'APP_SECRET_KEY_SJ' = 'ваш secret_key'
```
Python3 должен быть уже установлен.  
Установите зависимости:
```commandline
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```
### Запуск
```commandline
python3 Build_table.py
```
![](https://github.com/BigBadRussian/vacancies-for-programmers/blob/master/table.jpg)
### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).

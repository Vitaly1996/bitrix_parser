### bitrix_parser
### Описание
Функциональный WEB-парсер для анализа и сбора заявок с портала Битрикс24.
Софт предназначен для обновления списка заявок путем нажатия на кнопку "Лупа".
Временной интервал задается пользователем вручную – это 2 цифры «от» и «до». К примеру, 20 и 40. Софт должен обновлять список заявок каждый раз рандомно в заданном временном интервале. Также софт анализирует текст заявок и исключает автоматическое взятие заявки в случае нахождения "стоп слов".


### Технологии
- python 3.7
- django 3.2.18
- selenium==4.8.3


### Особенности
- для управления браузером была использована библитотека Selenium;
- реализована Django Admin панель для управления лицензиями пользователей;
- использона пользовательская модель, унаследованная от AbstractBaseUser;

### Установка
- склонировать репозиторий
```sh
git clone github.com/Vitaly1996/bitrix_parser
```

- в директории bitrix_parser/bitrix_parser/ создаем файл .env и записываем в него следующие переменные окружения:
```commandline
  PASSWORD=<ваш_пароль>    
  LOGIN=<ваш_логин>  
  ```
- в файле bitrix_parser/bitrix_parser/leads/config.py при необходимости меняем переменные, связанные с настройкой браузера:
```commandline
executable_path=<путь до драйвера вашего_браузера>
user_agent=<меняем user_agent>
```

- создать и активировать виртуальное окружение для проекта
```commandline
python -m venv venv
source venv/scripts/activate (Windows)    
source venv/bin/activate (MacOS/Linux)
python3 -m pip install --upgrade pip
```
- установить зависимости

```commandline
python pip install -r requirements.txt
```
- сделать миграции
```commandline
python manage.py makemigrations
python manage.py migrate
```

- запустить сервер
```commandline
python manage.py runserver
```

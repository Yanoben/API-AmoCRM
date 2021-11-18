# API-AmoCRM
Back-end GET request for API AmoCRM

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Yanoben/API-AmoCRM.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
. env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

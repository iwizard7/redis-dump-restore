# Redis Data Dump Utility ⚙️

## Описание

Этот Python скрипт позволяет сохранять и загружать данные из базы данных Redis в файл JSON и обратно. Он поддерживает функции для:

* Сохранения всех ключей или ключей по маске из выбранной базы данных Redis в файл.
* Загрузки данных из файла JSON в выбранную базу данных Redis.

## Функционал

### Сохранение данных из Redis в файл:

* Выберите базу данных Redis.
* Укажите маску ключа (опционально) для фильтрации ключей.
* Укажите имя файла для сохранения дампа данных.

### Загрузка данных из файла в Redis:

* Укажите имя файла с дампом данных.
* Выберите базу данных Redis для загрузки данных.

## Установка

Убедитесь, что у вас установлен Python 3.6 или выше. Вы можете проверить это с помощью команды:

```bash
python --version
```
Установите необходимые зависимости:
```bash
pip install redis
```
## Использование

Сохранение данных:
Запустите скрипт:
```bash
python redis_dump_util.py
Выберите опцию “1” для сохранения данных в дамп.
Введите номер базы данных Redis.
Укажите маску ключа для фильтрации (оставьте пустым для сохранения всех ключей).
Укажите имя файла для сохранения дампа.
```
Загрузка данных:
Запустите скрипт:
```bash
python redis_dump_util.py
Выберите опцию “2” для загрузки данных.
Введите имя файла с дампом.
Укажите номер базы данных Redis. Дамп будет восстановлен в эту базу.
```

## Пример использования:
Для сохранения данных из базы данных Redis с номером 2 в файл backup.json:
```bash
python redis_dump_util.py
Выберите “1” для сохранения данныхВведите “2” для номера базы данных
Введите маску ключа, если необходимо (или оставьте пустым)
Введите “backup.json” для имени файла
```
Для загрузки данных из файла backup.json в базу данных Redis с номером 2:
```bash
python redis_dump_util.py
Выберите “2” для загрузки данныхВведите “backup.json” для имени файла
Введите “2” для номера базы данных
```
## История изменений
Основные изменения:

#Обработка данных при выгрузке в файл:

smembers теперь преобразуется в список для удобства записи в JSON.
Добавлен параметр default=str в json.dump для обработки нестандартных типов данных.

### Обработка данных при загрузке из файла:
Обработка списков и наборов теперь улучшена для корректной загрузки данных.
Добавлена обработка пустых списков (хотя они не загружаются, это может быть полезно для дальнейших улучшений).

### Устранены потенциальные ошибки:
Преобразование множества в список перед записью в файл.
Убедитесь, что hmset поддерживается вашей версией redis-py, поскольку в новых версиях он может быть заменен на hset.

Обновления:

Обработка ошибок декодирования: При декодировании строковых данных теперь добавлена обработка UnicodeDecodeError. Если данные не могут быть декодированы в UTF-8, они сохраняются как бинарные данные.
Обработка бинарных данных при загрузке: При загрузке данных из файла добавлена возможность сохранения бинарных данных, если они были сохранены в этом формате.

## Требования
Python 3.6 или выше
Библиотека redis (устанавливается с помощью pip)

## Лицензия
Этот проект лицензирован под MIT License. См. LICENSE для подробностей.
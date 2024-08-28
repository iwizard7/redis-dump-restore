import redis
import json
import os


def dump_redis_to_file(redis_client, db_number, key_pattern=None, file_path='dump.json'):
    redis_client.execute_command('SELECT', db_number)
    cursor = 0
    dump = {}
    while True:
        cursor, keys = redis_client.scan(cursor, match=key_pattern or '*', count=1000)
        for key in keys:
            key_type = redis_client.type(key).decode()
            if key_type == 'string':
                dump[key.decode()] = redis_client.get(key).decode()
            elif key_type == 'list':
                dump[key.decode()] = redis_client.lrange(key, 0, -1)
            elif key_type == 'set':
                dump[key.decode()] = redis_client.smembers(key)
            elif key_type == 'zset':
                dump[key.decode()] = redis_client.zrange(key, 0, -1, withscores=True)
            elif key_type == 'hash':
                dump[key.decode()] = redis_client.hgetall(key)
            else:
                dump[key.decode()] = 'Unsupported type'
        if cursor == 0:
            break

    with open(file_path, 'w') as f:
        json.dump(dump, f, indent=4)


def load_file_to_redis(redis_client, file_path, db_number):
    redis_client.execute_command('SELECT', db_number)
    with open(file_path, 'r') as f:
        dump = json.load(f)

    for key, value in dump.items():
        if isinstance(value, list) and value:
            if isinstance(value[0], dict):  # List of hash fields
                redis_client.hmset(key, {k: v for d in value for k, v in d.items()})
            else:  # List or set values
                redis_client.rpush(key, *value)
        elif isinstance(value, set):
            redis_client.sadd(key, *value)
        elif isinstance(value, dict):  # Hash type
            redis_client.hmset(key, value)
        else:  # String or other types
            redis_client.set(key, value)


def main():
    redis_host = 'localhost'
    redis_port = 6379

    redis_client = redis.Redis(host=redis_host, port=redis_port)

    choice = input("Выберите действие (1 - сохранить в файл, 2 - загрузить из файла): ").strip()

    if choice == '1':
        db_number = int(input("Введите номер базы данных Redis: ").strip())
        key_pattern = input("Введите маску ключа (или оставьте пустым для всех ключей): ").strip()
        file_path = input("Введите путь к файлу для сохранения дампа: ").strip()
        dump_redis_to_file(redis_client, db_number, key_pattern, file_path)
        print(f"Дамп сохранен в {file_path}")

    elif choice == '2':
        file_path = input("Введите путь к файлу с дампом: ").strip()
        db_number = int(input("Введите номер базы данных Redis для загрузки дампа: ").strip())
        if not os.path.exists(file_path):
            print("Файл не существует.")
            return
        load_file_to_redis(redis_client, file_path, db_number)
        print(f"Дамп загружен в базу данных Redis номер {db_number}")

    else:
        print("Неверный выбор")


if __name__ == "__main__":
    main()
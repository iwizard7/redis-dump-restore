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
            key = key.decode()
            key_type = redis_client.type(key).decode()
            if key_type == 'string':
                dump[key] = redis_client.get(key).decode()
            elif key_type == 'list':
                dump[key] = [item.decode() for item in redis_client.lrange(key, 0, -1)]
            elif key_type == 'set':
                dump[key] = [item.decode() for item in redis_client.smembers(key)]
            elif key_type == 'zset':
                dump[key] = [(item.decode(), score) for item, score in redis_client.zrange(key, 0, -1, withscores=True)]
            elif key_type == 'hash':
                dump[key] = {k.decode(): v.decode() for k, v in redis_client.hgetall(key).items()}
            else:
                dump[key] = 'Unsupported type'
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
            # Handle lists and sets
            if isinstance(value[0], dict):  # If the value is a list of hashes
                redis_client.hmset(key, {k: v for d in value for k, v in d.items()})
            else:  # List or set values
                redis_client.rpush(key, *value)
        elif isinstance(value, dict):
            # Handle hash type
            redis_client.hmset(key, value)
        elif isinstance(value, str):
            # Handle string type
            redis_client.set(key, value)
        elif isinstance(value, list) and not value:
            # Handle empty lists (usually needs special treatment)
            pass
        else:
            print(f"Unsupported type for key {key}: {type(value)}")


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

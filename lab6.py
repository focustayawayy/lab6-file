import os
import logging
from functools import wraps



class FileNotFound(Exception):
    pass


class FileCorrupted(Exception):
    pass



def logged(exc_type, mode="console"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exc_type as e:
                logger = logging.getLogger(func.__name__)
                logger.setLevel(logging.ERROR)

                # console
                if mode == "console":
                    handler = logging.StreamHandler()
                # file
                elif mode == "file":
                    handler = logging.FileHandler("file_operations.log", encoding="utf-8")
                else:
                    raise ValueError("Невідомий режим логування")

                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)

                logger.addHandler(handler)
                logger.error(str(e))

                logger.removeHandler(handler)

                raise
        return wrapper
    return decorator



class FileManager:
    def __init__(self, filepath: str):
        self.filepath = filepath

        if not filepath.endswith('.csv'):
            raise ValueError("Файл для роботи повинен мати формат .csv")

        if not os.path.exists(filepath):
            raise FileNotFound(f"Файл '{filepath}' не знайдено.")

    @logged(FileCorrupted, mode="console")
    def read(self):
        """Читання файлу."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            raise FileCorrupted("Помилка читання файлу. Можливо файл пошкоджено.")

    @logged(FileCorrupted, mode="file")
    def write(self, data: str):
        """Запис у файл (перезаписує вміст)."""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.write(data)
        except Exception:
            raise FileCorrupted("Помилка запису у файл.")

    @logged(FileCorrupted, mode="file")
    def append(self, data: str):
        """Допис у файл (зберігає попередній вміст)."""
        try:
            with open(self.filepath, 'a', encoding='utf-8') as f:
                f.write(data)
        except Exception:
            raise FileCorrupted("Помилка допису у файл.")


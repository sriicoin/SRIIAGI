import os

class FileHandler:
    @staticmethod
    def read_file(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Target file not found: {file_path}")
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    @staticmethod
    def write_file(file_path, content):
        directory = os.path.dirname(os.path.abspath(file_path))
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
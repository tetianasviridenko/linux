import threading

class FileReaderThread(threading.Thread):
    def __init__(self, file_path):
        threading.Thread.__init__(self)
        self.file_path = file_path
        self.file_content = ""

    def run(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.file_content = file.read()
        except Exception as e:
            self.file_content = f"Помилка при читанні файлу: {e}"

def main():
    file_path = 'example.txt'

    file_reader_thread = FileReaderThread(file_path)

    file_reader_thread.start()

    file_reader_thread.join()

    print("Вміст файлу:")
    print(file_reader_thread.file_content)

if __name__ == "__main__":
    main()


import os
from threading import Thread
from time import perf_counter
import sys
import colorama

colorama.init(autoreset=True)

FILE_EXTENSIONS: list[str] = ['jpg', 'png', 'mp3', 'jpeg', 'mp4', 'bmp', 'gif', 'mkv', 'fif', 'mov', 'm4a']


class Files:
    def __init__(self, folder) -> None:
        self.folder: str = folder
        self.files: list[str] = list(filter(
            lambda file_name: file_name[-3:].lower() in FILE_EXTENSIONS,
            os.listdir(self.folder)))
        self.folder_size: float = self.get_dir_size() / (1024 ** 2)

    def get_dir_size(self):
        total = 0
        path = self.folder
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self.get_dir_size(entry.path)
        return round(total, 1)

    def destroy_file(self, file: str) -> None:
        path: str = f'{self.folder}/{file}'
        file_size: float = round(os.path.getsize(path) / (1024 ** 2), 1)
        with open(path, 'w') as f:
            f.write('')

        print(f'Name: {file} | Size: {file_size} MB\n'
              f"Number: {self.files.index(file) + 1} / {len(self.files)}\n", end='')

    def destroy(self) -> None:
        for file in self.files:
            t = Thread(target=lambda: self.destroy_file(file))
            t.daemon = True
            t.start()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("destroy <path>")
        sys.exit()

    if not os.path.isdir(sys.argv[1]):
        print('That is not a valid path')
        sys.exit()

    files = Files(sys.argv[1])

    start: float = perf_counter()
    files.destroy()
    end: float = perf_counter() - start

    print(f'\n\n{colorama.Fore.GREEN}Destroyed {len(files.files)} files ({files.folder_size} MB) in {round(end * 100, 1)}ms\n', end='')

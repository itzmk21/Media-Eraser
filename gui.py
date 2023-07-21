import os
from threading import Thread
from time import perf_counter
from tkinter.filedialog import Directory


import colorama

colorama.init(autoreset=True)

FILE_EXTENSIONS: list[str] = ['jpg', 'png', 'mp3', 'jpeg', 'mp4', 'bmp', 'gif', 'mkv', 'fif', 'mov', 'm4a']


class ImageDestroyer(Directory):
    def __init__(self) -> None:
        super().__init__()

        self.folder = super().show()
        self.files: list[str] = list(filter(
            lambda file_name: file_name[-3:].lower() in FILE_EXTENSIONS,
            os.listdir(self.folder)))

    def destroy_file(self, file: str) -> None:
        path: str = f'{self.folder}/{file}'
        file_size: float = round(os.path.getsize(path) / (1024 ** 2), 1)
        with open(path, 'w') as f:
            f.write('')

        with open('logs.txt', 'a') as f:
            f.write(f'Name: {file} | Size: {file_size} MB\n')

        print(f"Number: {self.files.index(file) + 1} / {len(self.files)}\n", end='')

    def destroy(self) -> None:
        for file in self.files:
            t = Thread(target=lambda: self.destroy_file(file))
            t.daemon = True
            t.start()


if __name__ == '__main__':
    images = ImageDestroyer()

    start: float = perf_counter()
    images.destroy()
    end: float = perf_counter() - start

    size: float = os.path.getsize(images.folder) / (1024 ** 2)
    print(f'\n\n{colorama.Fore.GREEN}Destroyed {len(images.files)} files ({size} MB) in {round(end * 100, 1)}ms\n', end='')
    input()

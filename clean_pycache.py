import shutil
import os
from rich.console import Console
from rich.progress import track

console = Console()


def main():
    with console.status("正在搜寻可清理之文件"):
        egg_info: list = []
        for file in os.listdir():
            if file.endswith(".egg-info"):
                egg_info.append(file)
                console.print(file)

        pycache: list = []
        for dirpath, dirnames, filenames in os.walk("./"):
            for dirname in dirnames:
                if dirname == "__pycache__":
                    pycache.append(fn := os.path.join(dirpath, dirname))
                    console.print(fn)
    for file in track(
        ["build", "dist", "logs", "log", *egg_info, *pycache], description="正在清理"
    ):
        if os.path.isdir(file) and os.access(file, os.W_OK):
            shutil.rmtree(file)


if __name__ == "__main__":
    main()

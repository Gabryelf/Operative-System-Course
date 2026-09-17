# demo1_whoami.py
import os
import platform
import time


def print_process_info(label=""):
    print(f"\n===== {label} =====")
    print(f"Текущий процесс (PID):       {os.getpid()}")
    print(f"Родительский процесс (PPID): {os.getppid()}")
    print(f"Пользователь:                {os.getlogin() if hasattr(os, 'getlogin') else 'n/a'}")
    print(f"ОС:                          {platform.system()} {platform.release()}")
    print(f"Рабочая директория:          {os.getcwd()}")


if __name__ == "__main__":
    print_process_info("Первый запуск")
    time.sleep(10)

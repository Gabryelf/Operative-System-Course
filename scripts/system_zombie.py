import os
import time

if __name__ == "__main__":
    print(f"Родитель PID={os.getpid()} спит 30 сек, НЕ забирая статус ребёнка...")
    pid = os.fork()

    if pid == 0:
        print(f"Ребёнок PID={os.getpid()} умирает через 2 сек")
        time.sleep(2)
        os.exit(0)
    else:
        time.sleep(30)  # родитель не вызывает wait() → ребёнок станет зомби
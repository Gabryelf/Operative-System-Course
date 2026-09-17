import multiprocessing as mp
import os
import time


def child_work(child_id):
    print(f"Ребёнок #{child_id}: PID={os.getpid()}, родитель PPID={os.getppid()}")
    time.sleep(1)


if __name__ == "__main__":
    print(f"Родитель: PID={os.getpid()}")
    procs = []
    for i in range(3):
        p = mp.Process(target=child_work, args=(i,))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()  # ждём завершения
    print("Все процессы завершены.")
    
# collector.py
import psutil

def collect_process_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)
    return processes

if __name__ == "__main__":
    process_info = collect_process_info()
    print(process_info)

# storage.py
import sqlite3

def init_db():
    conn = sqlite3.connect('edr.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS processes
                 (pid INTEGER, name TEXT, username TEXT, cpu_percent REAL, memory_percent REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS threats
                 (pid INTEGER, name TEXT, username TEXT, cpu_percent REAL, memory_percent REAL)''')
    conn.commit()
    conn.close()

def store_process_info(process_info):
    conn = sqlite3.connect('edr.db')
    c = conn.cursor()
    c.executemany('INSERT INTO processes VALUES (?,?,?,?,?)', process_info)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    from collector import collect_process_info
    process_info = [(proc['pid'], proc['name'], proc['username'], proc['cpu_percent'], proc['memory_percent']) for proc in collect_process_info()]
    store_process_info(process_info)

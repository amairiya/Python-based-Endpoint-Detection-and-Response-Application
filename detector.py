
import sqlite3

# Define your threat detection rules here
THREAT_RULES = {
    "cpu_percent": 80.0,  # Example rule: CPU usage > 80%
    "memory_percent": 80.0,  # Example rule: Memory usage > 80%
    "suspicious_processes": []  # Example rule: Suspicious process names
}

threats = []

def update_suspicious_processes_from_file():
    with open("suspicious_processes.txt", 'r') as file:
        # Read lines from the file and strip any extra whitespace characters
        suspicious_processes = [line.strip() for line in file.readlines()]
    
    # Update the THREAT_RULES dictionary
    THREAT_RULES["suspicious_processes"] = suspicious_processes

def detect_threats():
    update_suspicious_processes_from_file()
    conn = sqlite3.connect('edr.db')
    c = conn.cursor()
    

    # Rule 1: Detect high CPU usage
    c.execute("SELECT * FROM processes WHERE cpu_percent > ?", (THREAT_RULES["cpu_percent"],))
    threats.extend(c.fetchall())
    # high_cpu_processes = c.fetchall()
    # insert_query = """
    #     INSERT INTO threats (pid, name, username, cpu_percent, memory_percent )
    #     VALUES (?,?,?,?,?);
    #     """
    # c.executemany(insert_query, high_cpu_processes)
    
    # Rule 2: Detect high memory usage
    c.execute("SELECT * FROM processes WHERE memory_percent > ?", (THREAT_RULES["memory_percent"],))
    threats.extend(c.fetchall())
    # suspicious_processes_memory_percent = c.fetchall()
    # insert_query = """
    #     INSERT INTO threats (pid, name, username, cpu_percent, memory_percent )
    #     VALUES (?,?,?,?,?);
    #     """
    # c.executemany(insert_query, suspicious_processes_memory_percent)
        
    # Rule 3: Detect suspicious process names
    for proc_name in THREAT_RULES["suspicious_processes"]:
        c.execute("SELECT * FROM processes WHERE name LIKE ?", (proc_name,))
        threats.extend(c.fetchall())
        # suspicious_processes_name = c.fetchall()
        # insert_query = """
        # INSERT INTO threats (pid, name, username, cpu_percent, memory_percent )
        # VALUES (?,?,?,?,?);
        # """
        # c.executemany(insert_query, threats)


    insert_query = """
        INSERT INTO threats (pid, name, username, cpu_percent, memory_percent )
        VALUES (?,?,?,?,?);
        """
    c.executemany(insert_query, threats)
        
    conn.commit()
    conn.close()
    return threats

if __name__ == "__main__":
    threats = detect_threats()
    print("Detected Threats:", threats)
    
    
    
    # # Insert the high CPU processes into the threat table
    # insert_query = """
    # INSERT INTO threats (pid, name, username, cpu_percent, memory_percent )
    # VALUES (?,?,?,?,?);
    # """
    # c.executemany(insert_query, high_cpu_processes)
    
    # high_cpu_processes
    # suspicious_processes_name
    # suspicious_processes_memory_percent

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
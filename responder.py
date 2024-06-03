# responder.py
import os

def respond_to_threats(threats):
    for threat in threats:
        pid = threat[0]
        print(f"Terminating process {pid} due to high CPU usage.")
        try:
            os.kill(pid, 9)
        except Exception as e:
            print(f"Failed to terminate process {pid}: {e}")

if __name__ == "__main__":
    from detector import detect_threats
    threats = detect_threats()
    respond_to_threats(threats)

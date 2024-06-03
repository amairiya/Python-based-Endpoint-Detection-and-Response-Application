# app.py
from flask import Flask, render_template, redirect, url_for
import sqlite3
from collector import collect_process_info
from storage import store_process_info, init_db
from detector import detect_threats
from responder import respond_to_threats

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('edr.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    init_db()
    conn = get_db_connection()
    processes = conn.execute('SELECT * FROM processes').fetchall()
    conn.close()
    return render_template('index.html', processes=processes)


@app.route('/threats_List')
def threats_List():
    conn = get_db_connection()
    threats = conn.execute('SELECT * FROM threats').fetchall()
    conn.close()
    return render_template('threats_List.html', threats=threats)
    
    
    
    
@app.route('/trigger_method_collect')
def trigger_method_collect():
    # Call your method here
    perform_action_collect()
    return redirect(url_for('index'))
# Example method to be triggered
def perform_action_collect():
    process_info = [(proc['pid'], proc['name'], proc['username'], proc['cpu_percent'], proc['memory_percent']) for proc in collect_process_info()]
    store_process_info(process_info)


@app.route('/trigger_method_detect')
def trigger_method_detect():
    # Call your method here
    perform_action_detect()
    return redirect(url_for('threats_List'))
# Example method to be triggered
def perform_action_detect():
        threats = detect_threats()
        print("Detected Threats:", threats)
    

@app.route('/trigger_method_respond')
def trigger_method_respond():
    # Call your method here
    perform_action_respond()
    return redirect(url_for('index'))
# Example method to be triggered
def perform_action_respond():
        threats = detect_threats()
        respond_to_threats(threats)
    

@app.route('/clean_logs')
def clean_logs():
    conn = sqlite3.connect('edr.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS processes")
    c.execute("DROP TABLE IF EXISTS threats")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)


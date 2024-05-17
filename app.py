from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization function
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY,
            date TEXT,
            class1 INTEGER,
            class2 INTEGER,
            class3 INTEGER,
            class4 INTEGER,
            class5 INTEGER,
            class6 INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Route to delete all data
@app.route('/reset')
def reset_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('DELETE FROM attendance')
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to view the calendar
@app.route('/calendar')
def calendar():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM attendance')
    data = c.fetchall()
    conn.close()
    return render_template('calendar.html', data=data)

# Route to update attendance
@app.route('/update', methods=['POST'])
def update():
    date = request.form['date']
    classes = [int(request.form.get(f'class{i}', 0)) for i in range(1, 7)]
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO attendance (date, class1, class2, class3, class4, class5, class6)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (date, *classes))
    conn.commit()
    conn.close()
    return redirect(url_for('calendar'))

# Route to view attendance percentage
# Route to view attendance percentage
@app.route('/attendance')
def attendance():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM attendance')
    data = c.fetchall()
    conn.close()
    
    total_attended_classes = 0
    total_possible_classes = len(data) * 6  # 6 classes per day
    
    for row in data:
        total_attended_classes += sum(row[2:])  # Sum of attended classes for each day
    
    attendance_percentage = (total_attended_classes / total_possible_classes) * 100 if total_possible_classes > 0 else 0
    
    return render_template('attendance.html', percentage=attendance_percentage)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

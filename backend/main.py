from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json

app=Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('db/reports.db')
    cursor = conn.cursor()
    cursor.execute('''  CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            user TEXT,
            videoId TEXT      
                   )''')
    conn.commit()
    conn.close()
    

@app.route('/filter', methods=['POST'])
def filter():
    global data
    comments = list()
    try:
        data = request.get_json()

        print(data)
        if not isinstance(data,list)or not all(isinstance(i,dict)for i in data): 
            raise ValueError("INVALID") 
        for i in range(len(data)):
            # print(data[i])
            commentData = data[i]
            comments.append(
                commentData['text']
            )
        # open('comments.json', 'w').write(json.dumps(data))
        return jsonify ({"success ": True, "data" : comments})
    except Exception as e:
        print(e)
        return jsonify({"success": False})


@app.route('/report', methods=['POST'])
def report():
    try:
        data = request.get_json()
        
        conn = sqlite3.connect('db/reports.db')
        cursor = conn.cursor()

        for commentData in data:
            cursor.execute('''
                        INSERT INTO reports (text, user, videoId ) 
                        VALUES (?, ?, ?)
                    ''', (commentData['text'], commentData['author'], commentData['videoId']))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Comments saved successfully."})
        

    except:
        pass

@app.route('/view_reports', methods=['GET'])
def view_reports():
    try:
        conn = sqlite3.connect('db/reports.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM reports")
        rows = cursor.fetchall()

        conn.close()

        report_list = []
        for row in rows:
            report_list.append({
                "id": row[0],
                "text": row[1],
                "user": row[2],
                "videoId": row[3]
            })

        return jsonify({"success": True, "data": report_list})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

    
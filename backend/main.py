from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import joblib

app=Flask(__name__)
CORS(app)

vectorizer = joblib.load('../ai-models/commentvectorizer.pkl')
model = joblib.load('../ai-models/model.pkl')


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
    try:
        data = request.get_json()
        open('comments.json', 'w').write(json.dumps(data))

        if not isinstance(data, list) or not all(isinstance(i, dict) for i in data): 
            raise ValueError("INVALID")

        for i in range(len(data)):
            commentData = data[i]
            comment_vec = vectorizer.transform([commentData['text']])
            check_comment = model.predict_proba(comment_vec)
            if check_comment[0][1] >= 0.75:
                # print("******", commentData['text'], "*******")
                data[i]['spam'] = True
            else:
                data[i]['spam'] = False
        
        print(jsonify({"success": True, "data": data}))
        return jsonify({"success": True, "data": data})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)})


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


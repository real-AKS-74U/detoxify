from flask import Flask, request, jsonify
import sqlite3 
app=Flask(__name__)

def init_db():
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute

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
        return jsonify ({"success ": True, "data" : comments})
    except Exception as e:
        print(e)
        return jsonify({"success": False})



if __name__ == '__main__':
    app.run(debug=True)


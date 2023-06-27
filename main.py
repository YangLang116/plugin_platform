from flask import Flask
from flask import request
import json
import sqlite3
import requests

DING_URL = 'https://oapi.dingtalk.com/robot/send?access_token=' \
           '77c63c50e879ba803480ae18bbc308dfa0ab948b68dffca474de4e44d3606fa1'

app = Flask(__name__)


@app.route('/api/advice', methods=['POST'])
def submit_advice():
    req = json.loads(request.data)
    app_key = req.get('app_key')
    title = req.get('title')
    content = req.get('content')
    # 钉钉提醒
    ding_data = {
        "msgtype": "text",
        "text": {
            "content": f"appKey:{app_key}\n title:{title}\n content:{content}"
        }
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(DING_URL, headers=headers, data=json.dumps(ding_data))
    # 保存数据到db
    connect = sqlite3.connect('./db/advice.db')
    try:
        # 创建表格
        connect.execute("CREATE TABLE IF NOT EXISTS Advice ("
                        "ID INTEGER AUTO_INCREMENT PRIMARY KEY,"
                        "APP_KEY VARCHAR(10) NOT NULL,"
                        "TITLE TEXT NOT NULL,"
                        "CONTENT TEXT NOT NULL);")
        # 更新数据
        connect.execute(f"INSERT INTO Advice (APP_KEY,TITLE,CONTENT) VALUES ('{app_key}','{title}','{content}');");
        # 保存数据
        connect.commit()
        return json.dumps({'code': 0, 'msg': 'ok'})
    except Exception as r:
        return json.dumps({'code': -1, 'msg': r})
    finally:
        connect.close()


if __name__ == '__main__':
    app.run()


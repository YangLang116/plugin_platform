import json
import sqlite3

import requests
from flask import Flask
from flask import request

DING_URL = 'https://oapi.dingtalk.com/robot/send?access_token=' \
           '77c63c50e879ba803480ae18bbc308dfa0ab948b68dffca474de4e44d3606fa1'

app = Flask(__name__)


@app.route('/api/advice', methods=['POST'])
def submit_advice():
    req = json.loads(request.data)
    os = req.get('os')
    title = req.get('title')
    content = req.get('content')
    version = req.get('version')
    app_key = req.get('app_key')

    # 钉钉提醒
    ding_data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "IDEA Plugin",
            "text": f"**APP_KEY**: {app_key}  \n  **OS**: {os}  \n  **VERSION**: {version}  \n  "
                    f"**TITLE**: {title}  \n  **CONTENT**: {content}  \n  "
                    "```java  \n  "
                    f"{content}  \n  "
                    "```"
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
                        "OS TEXT NOT NULL,"
                        "VERSION TEXT NOT NULL,"
                        "TITLE TEXT NOT NULL,"
                        "CONTENT TEXT NOT NULL);")
        # 更新数据
        connect.execute(
            f"INSERT INTO Advice (APP_KEY,OS,VERSION,TITLE,CONTENT) "
            f"VALUES ('{app_key}','{os}','{version}','{title}','{content}');"
        )
        # 保存数据
        connect.commit()
        return json.dumps({'code': 0, 'msg': 'ok'})
    except Exception as r:
        return json.dumps({'code': -1, 'msg': r})
    finally:
        connect.close()


if __name__ == '__main__':
    app.run()

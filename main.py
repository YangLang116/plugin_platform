import json

import requests
import sentry_sdk
from flask import Flask
from flask import request
from sentry_sdk import capture_message

from config import DING_URL, SENTRY_KEY

sentry_sdk.init(
    dsn=SENTRY_KEY,
    traces_sample_rate=1.0,
    profiles_sample_rate=0,
)

app = Flask(__name__)


@app.route('/api/advice', methods=['POST'])
def submit_advice():
    data = request.data.decode('utf-8')
    params = json.loads(data)
    # 钉钉提醒
    requests.post(DING_URL, headers={'Content-Type': 'application/json'}, data=json.dumps({
        "msgtype": "markdown",
        "markdown": {
            "title": "IDEA Plugin",
            "text": f"**APP_KEY**: {params.get('app_key')}  \n  "
                    f"**OS**: {params.get('os')}  \n  "
                    f"**IDE**: {params.get('ide')}  \n  "
                    f"**Build**: {params.get('build')}  \n  "
                    f"**VERSION**: {params.get('version')}  \n  "
                    f"**TITLE**: {params.get('title')}  \n  "
                    f"**CONTENT**:  \n  "
                    "```java  \n  "
                    f"{params.get('content')}  \n  "
                    "```"
        }
    }))
    # 保存数据到Sentry
    capture_message(params.get('content'),
                    user=params.get('app_key'),
                    level=params.get('title'),
                    tags={"os": params.get('os'),
                          "ide": params.get('ide'),
                          "build": params.get('build'),
                          "version": params.get('version')}
                    )
    return json.dumps({'code': 0, 'msg': 'ok'})


if __name__ == '__main__':
    app.run()

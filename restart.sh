netstat -tunpl | grep 5000 | awk '{print $7}' | cut -f 1 -d "/" | xargs -t kill -9
nohup python3 main.py

import os
from flask import Flask

app = Flask(__name__)

# Запускаем TensorBoard
os.system("tensorboard --logdir=tensorboard --host 0.0.0.0 --port 10000 &")

@app.route('/')
def home():
    return "TensorBoard работает! Перейдите по ссылке: <a href='/tensorboard'>TensorBoard</a>"

@app.route('/tensorboard')
def tensorboard():
    return "Перейдите по ссылке: <a href='http://YOUR_RENDER_URL:10000'>TensorBoard</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
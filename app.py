import os
import subprocess
from flask import Flask

app = Flask(__name__)

# Получаем порт из переменной окружения
PORT = int(os.getenv("PORT", 8080))

# Запускаем TensorBoard на порту 10000
subprocess.Popen(f"tensorboard --logdir=tensorboard --port=10000 --host=0.0.0.0", shell=True)

@app.route('/')
def index():
    return "Flask App is Running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)

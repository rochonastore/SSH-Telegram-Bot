from flask import Flask
from threading import Thread
import os
import traceback

app = Flask('YoYo')

os.system("tmate-2.4.0-static-linux-amd64/tmate -F > log.txt &")

@app.route('/')
def main():
    text = ""
    
    try:
        with open("log.txt", "r") as f:
            text = f.read()
    except:
        text = str(traceback.format_exc())
        pass
	
    return "<h1>Your Bot Is Alive!</h1><br/><br/>" + text

def run():
    try:
        app.run(host="0.0.0.0", port=int(os.environ['PORT']))
    except:
        app.run(host="0.0.0.0", port=int(8080))


def keep_alive():
    server = Thread(target=run)
    server.start()

# keep_alive()

from flask import Flask, render_template, send_from_directory, send_file, abort
from threading import Thread
import os
import traceback
from pathlib import Path
app = Flask('YoYo')


# @app.route('/')
# def main():
#     text = ""
    
#     try:
#         with open("log.txt", "r") as f:
#             text = f.read()
#     except:
#         text = str(traceback.format_exc())
#         pass
	
#     return "<h1>Your Bot Is Alive!</h1><br/><br/>" + text

# @app.route('/<path:filename>')
# def log(filename):
#     print("gg")
#     print(filename)
#     return send_from_directory(
#         os.path.abspath(''),
#         filename,
#         as_attachment=True
#     )

BASE_DIR = Path(__file__).resolve().parent

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def main(req_path):
   
    print(BASE_DIR)
    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        print(abs_path)
        try:
            return send_from_directory(
                abs_path,
                os.path.basename(abs_path),
                as_attachment=True
            )
        except:
            return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', files=files)

def run():
    try:
        app.run(host="0.0.0.0", port=int(os.environ['PORT']))
    except:
        app.run(host="0.0.0.0", port=int(8080))


def keep_alive():
    server = Thread(target=run)
    server.start()

# keep_alive()

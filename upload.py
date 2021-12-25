import telepot
from creds import botToken, my_chat_id
import sys
import os
import traceback
import ntpath


bot = telepot.Bot(botToken)
# cmd = " ".join(sys.argv).replace(os.path.basename(__file__), "").lstrip()

cmd = sys.argv

help_text = '''
Example: upload.py doc example.doc

Types: doc, video, audio, photo, transfer

`transfer` will transfer file to transfer.sh
'''

def runProcess(cmd):    
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while(True):
        # returns None while subprocess is running
        retcode = p.poll() 
        line = p.stdout.readline()
        yield line
        if retcode is not None:
            break

def transfer_cmd(file_path):
    file_abs_path = os.path.abspath(file_path)
    filename = ntpath.basename(file_abs_path)
    cmd = "curl --upload-file {} https://transfer.sh/{}".format(file_abs_path, filename)
    for line in runProcess(cmd.split()):
        print(line.decode('utf8'))

try:
    if 'doc' in cmd[1]:
        bot.sendDocument(my_chat_id, open(cmd[2], "rb"))
    elif 'video' in cmd[1]:
        bot.sendVideo(my_chat_id, open(cmd[2], "rb"))
    elif 'audio' in cmd[1]:
        bot.sendAudio(my_chat_id, open(cmd[2], "rb"))
    elif 'photo' in cmd[1]:
        bot.sendPhoto(my_chat_id, open(cmd[2], "rb"))
    elif 'transfer' in cmd[1]:
        transfer_cmd(cmd[2])
    else:
        bot.sendMessage(my_chat_id, help_text)
except:
    print(traceback.format_exc())




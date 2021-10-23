import subprocess
import sys, time, threading
import telepot
from telepot.loop import MessageLoop
from creds import botToken, my_chat_id
from pprint import pprint
import traceback
import os
import signal
import keep_alive
os.system("tmate-2.4.0-static-linux-amd64/tmate -F > log.txt &")
keep_alive.keep_alive()

bot = telepot.Bot(botToken)
bot.sendMessage(my_chat_id, "### I'm alive!!!")

s = ''
prev = '0'
prog_running = True
message_id = 0
process = ''
def print_thread():
    global prog_running, s, message_id, prev
    i = 0
    while prog_running:
        # print(s, flush=True)
        i += 1
        print(str(i) + "...program running...")
        if len(s) != 0:
            if prev != s:
                print("### tried sending message")
                editable_message = (my_chat_id, message_id)
                if len(s) < 3000:
                    try:
                        bot.editMessageText(msg_identifier=editable_message, text=s)
                    except:
                        print(str(traceback.format_exc()))
                else:
                    message_id = bot.sendMessage(my_chat_id, s)
                    message_id = message_id['message_id']
                prev = s
                # s = ''
        time.sleep(1)
    s = ''

def process_checker():
    global process, s, prog_running, prev
    while True:         
        realtime_output = process.stdout.readline()
        
        if realtime_output == '' and process.poll() is not None:
            time.sleep(1)
            prog_running = False
            break

        if realtime_output:
            # print(realtime_output.strip(), flush=True)
            s += realtime_output
            # time.sleep(2)

def on_chat_message(msg):
    global prog_running, s, message_id, process, prev
    # pprint(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)
    # print(content_type, chat_type, chat_id)
    if str(chat_id) == my_chat_id:
        if content_type == "text":
            if msg["text"] == "kill":
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            elif "/upload" in msg["text"]:
                try:
                    cmd = msg["text"].split(" ")
                    if cmd[1] == 'doc':
                        bot.sendDocument(my_chat_id, open(cmd[2], "rb"))
                    elif cmd[1] == 'video':
                        bot.sendVideo(my_chat_id, open(cmd[2], "rb"))
                    elif cmd[1] == 'audio':
                        bot.sendAudio(my_chat_id, open(cmd[2], "rb"))
                    elif cmd[1] == 'photo':
                        bot.sendPhoto(my_chat_id, open(cmd[2], "rb"))
                    else:
                        bot.sendMessage(my_chat_id, help_text)
                except:
                    reply = str(traceback.format_exc())
                    bot.sendMessage(my_chat_id, reply)
            # elif "/restart" in msg["text"]:
                # os.execv(sys.executable, ['python3'] + [sys.argv[0]])
            else:
                prog_running = True
                reply = "Got Command: " + str(msg["text"])
                message_id = bot.sendMessage(chat_id, reply)
                message_id = message_id['message_id']
                print(message_id)
                
                cmd = msg["text"]

                t = threading.Thread(target=print_thread)
                t.start()

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    encoding='utf-8',
                    errors='replace',
                    preexec_fn=os.setsid
                )
                
                t1 = threading.Thread(target=process_checker)
                t1.start()
            
        else:
            print("Downloading file...")
            try:
                file_id = msg[content_type]['file_id']
                file_name = msg[content_type]['file_name']
                bot.download_file(file_id, file_name)
            except Exception:
                reply = str(traceback.format_exc())
                bot.sendMessage(chat_id, reply)

# MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()
MessageLoop(bot, on_chat_message).run_as_thread()
while(1):
    time.sleep(10)

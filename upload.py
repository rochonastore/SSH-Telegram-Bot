import telepot
from creds import botToken, my_chat_id
import sys
import os
bot = telepot.Bot(botToken)
# cmd = " ".join(sys.argv).replace(os.path.basename(__file__), "").lstrip()

cmd = sys.argv

help_text = '''
Example: upload.py doc example.doc

Types: doc, video, audio, photo
'''

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




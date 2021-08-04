import telebot
import speech_recognition as sr
import subprocess
import speechEmotionRecognition as spr
import os 
from pydub import AudioSegment
import shutil

bot = telebot.TeleBot("1791987070:AAF6rlODgpy4u0AFrzPor40uBe0NESGq-e0")
r = sr.Recognizer();
# File location 
location_output = "./output"
location_input = "./input/Telegram"
file_name_wav = '/out.wav'
file_name_ogg = '/user_voice.ogg'
# Path 
path_ogg = os.path.join(location_input, 'user_voice.ogg') 
path_wav = os.path.join(location_input, 'out.wav') 
path_output = os.path.join(location_output) 

try:

  if os.path.exists(location_output):
    shutil.rmtree(location_output)

  @bot.message_handler(content_types=["voice","audio"])
  def get_audio_message(message):

    #eliminar el archivo si existe
    if os.path.exists(path_wav):
        os.remove(path_wav)

    r = sr.Recognizer();
    file_info = bot.get_file(message.voice.file_id)
    download_file = bot.download_file(file_info.file_path)
    with open(location_input+file_name_ogg,'wb') as new_file:
      new_file.write(download_file)
      dest_filename = location_input+file_name_wav
      process = subprocess.run(['ffmpeg','-i',location_input+file_name_ogg,dest_filename])
      file = sr.AudioFile(dest_filename)

      with file as source:
        audio = r.record(source)
        #text = r.recognize_google(audio, lenguaje ='es-ES')
        #eliminar el archivo el archivo ogg
        if os.path.exists(path_ogg):
            os.remove(path_ogg)
            bot.send_message(message.chat.id, 'holas, porcesando tu adio')
            result = spr.init_model()
            bot.send_message(message.chat.id, result[0])

  @bot.message_handler(commands=["helps"])
  def enviar(message):
      bot.reply_to(message, "Hola, Soy un bot de el grupo de procesos de soft.")

  @bot.message_handler(commands=["start"])
  def enviar(message):
      bot.reply_to(message, "Hola, bienvenido")
      
  @bot.message_handler(commands=["saludame"])
  def enviar(message):
      bot.reply_to(message, "Hola "+ message.from_user.first_name+", ¿como estas?" )
      print(message.from_user.first_name)

  # @bot.message_handler(commands=['foto'])
  # def send_photo(message):
  #     image = open("\tmp\bot.png", 'rb')
  #     bot.send_photo(message.chat.id,image )

  @bot.message_handler(func=lambda message: True)
  def echo_all(message):
    bot.reply_to(message, message.text)

  bot.polling()

except telebot.apihelper.ApiException as e:
  if e.result.status_code == 403 or e.result.status_code == 400:
    pass   
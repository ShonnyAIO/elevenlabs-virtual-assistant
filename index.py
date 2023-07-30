import telebot
from decouple import config

# CONVERT OGG TO WAV
from pydub import AudioSegment

# SPEECH RECOGNITION
import speech_recognition as sr
r = sr.Recognizer()

# ELEVENLABS SET API KEY 
from elevenlabs import set_api_key, generate, save
API_KEY = config("API_KEY")
set_api_key(API_KEY)

# huggingchat API - SET COOKIES
from hugchat import hugchat
chatbot = hugchat.ChatBot(cookie_path='cookies.json')

# API TELEGRAM
API_TELEGRAM = config("API_TELEGRAM")
bot = telebot.TeleBot(API_TELEGRAM)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Good Evening :D My friend {0}, I am HuggingChat, developed by @Jonathan_Torres96.".format(message.chat.username))

@bot.message_handler(content_types=['audio', 'voice'])
def handle_docs_audio(message):

    print('LOGS AUDIO:', message.chat.username)
    file_name = "request_" + str(message.chat.id) + ".ogg"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    ogg2wav(file_name)
    file_name_wav = file_name.replace('.ogg','.wav')

    # open the file
    with sr.AudioFile(file_name_wav) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        message.text = r.recognize_google(audio_data)
        bot.send_message(message.chat.id, "You said :" + message.text)
        print(message.text)

    callHungginFace(message)


@bot.message_handler(func=lambda msg: True)
def echo_all(message):

    print('LOGS:', message.chat.username, " : ", message.text)
    callHungginFace(message)


def ogg2wav(ofn):
    wfn = ofn.replace('.ogg','.wav')
    x = AudioSegment.from_file(ofn)
    x.export(wfn, format='wav')    # maybe use original resolution to make smaller

def callHungginFace(message):

    answer = chatbot.chat(str(message.text + "use at most 70 words"))

    fileAudio = "answers_" + str(message.chat.id) + ".ogg"

    bot.send_message(message.chat.id, 'Sending answers ...')
    audio = generate(
        text = str(answer),
        voice = "Wayne",
        model = "eleven_monolingual_v1"
    )
    save(audio, fileAudio)

    respuesta_audio = open(fileAudio, "rb")
    bot.send_message(message.chat.id, answer)
    bot.send_voice(message.chat.id, respuesta_audio)

    # Create a new conversation
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)

    # Get conversation list
    conversation_list = chatbot.get_conversation_list()


bot.infinity_polling(interval=0, timeout=60)
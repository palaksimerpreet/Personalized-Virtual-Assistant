notice = """
 Ida Virtual Assistant (BSL-1.0)
-----------------------
By Giga Blitz

Hi there. Ida is a digital assistant made by using python. She can read the news, the weather, open netflix, 
play music, and more.

Ida stands for:-
I - Intelligent
D - Data
A - Assistant

To install the modules, check the Modules_needed.txt file in the other stuff folder. 

Here's a playlist containing videos on how this works and other versions of this project.
Link = https://www.youtube.com/playlist?list=PL1RXSeeHn7FdCMy7ibMmS4zcSpzLPwpZ7

Check out my website!
Link = https://wp.me/PcdpL6-5

There will be future releases of this project so remember to check the playlist or subscribe to my channel!

If you have any ideas or code I could include in this project, contact me at gigablitzonline@gmail.com or 
comment in the comments section of my video or github.

If you want to publish this project, contact me at gigablitzonline@gmail.com.
"""

import time, os, webbrowser, random, requests, bs4, wikipediaapi, re, urllib, io, speech_recognition, pyaudio
from datetime import date
from gtts import gTTS
##from pyowm.owm import OWM
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from googletrans import Translator
from console.utils import wait_key
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

sr = speech_recognition
# My current version is 3.8.1

thepath = os.path.dirname(os.path.abspath(__file__))

def speak(mytext, audio_name, language = "en-uk"):
    thevoice = gTTS(text=mytext, lang=language, slow=False)
    thevoice.save(rf"{thepath}\audio\ " + audio_name + ".mp3")
    pygame.mixer.init()
    pygame.mixer.music.load(rf'{thepath}\audio\ ' + audio_name + '.mp3')
    pygame.mixer.music.play()

def recognize_speech_from_mic():
    global question, success

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    
    # when spacebar is clicked, it will start listening to your voice

    print ("     (Press Spacebar to speak)     ")
    
    wait_key(' ')

    # adjust the recognizer sensitivity to ambient/background noise and record audio
    # from the microphone

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print ("Listening...")
        audio = recognizer.listen(source)

    # set up the response variables
    success = True,
    error = None,
    question = None

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        question = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        success = False
        error = "The API is currently unavailable"
        speak (f"{error}. Please type it -> ")
        question = input (f"{error}. Please type it -> ")
    except sr.UnknownValueError:
        # speech was unintelligible
        error = "I am unable to recognize speech"
        speak (f"{error}. Please type it -> ")
        question = input (f"{error}. Please type it -> ")

translator = Translator()
LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',    
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'fil': 'filipino',
    'he': 'hebrew'
}
LANGCODES = dict(map(reversed, LANGUAGES.items()))


# Textual month, day, year and time
today = date.today()
date = today.strftime("%B %d, %Y")

t = time.localtime()
hour_now = time.strftime("%H", t)
current_time = time.strftime("%H:%M:%S", t)

account = open('account.txt', 'r')
details = account.readlines()
part1 = details[0].split(" - ")
name = part1[1]

if int(hour_now) >= 0 and int(hour_now) < 12:
    time_now = "Morning"
if int(hour_now) >= 12 and int(hour_now) < 17:
    time_now = "Afternoon"
if int(hour_now) >= 17 and int(hour_now) <= 23:
    time_now = "Evening"

message = [f"\n\nGood {time_now}, {name}. Ida here. What can I do for you?", f"\n\nHi {name}. Anything I can help you with?", f"\n\nHello {name}. Nice to see you!"]
welcome = random.choice(message)

speak (welcome, "welcome")
print (welcome)

song_source = [r"https://youtu.be/kNDkz-nThzc", r"https://youtu.be/YSF8MzeO5JE", r"https://youtu.be/gwMysFlo-08", r"https://youtu.be/Uo-GommYv7w", r"https://youtu.be/7S1Y2wcfSWM", r"https://www.youtube.com/watch?v=QHQWG_QOrMc"]
#6 songs

def asking_numbers():
    global num1, num2, num3, num4
    thecode = gTTS(text="Number 1?", lang="en", slow=False)
    thecode.save(rf"{thepath}\audio\num1.mp3")
    mixer.init()
    mixer.music.load(rf'{thepath}\audio\num1.mp3')
    mixer.music.play()
    num1 = input("Number 1 ->")

    thecode = gTTS(text="Number 2?", lang="en", slow=False)
    thecode.save(rf"{thepath}\audio\num2.mp3")
    mixer.init()
    mixer.music.load(rf'{thepath}\audio\num2.mp3')
    mixer.music.play()
    num2 = input("Number 2 ->")

    thecode = gTTS(text="Number 3?", lang="en", slow=False)
    thecode.save(rf"{thepath}\audio\num3.mp3")
    mixer.init()
    mixer.music.load(rf'{thepath}\audio\num3.mp3')
    mixer.music.play()
    num3 = input("Number 3 ->")

    thecode = gTTS(text="Number 4?", lang="en", slow=False)
    thecode.save(rf"{thepath}\audio\num4.mp3")
    mixer.init()
    mixer.music.load(rf'{thepath}\audio\num4.mp3')
    mixer.music.play()
    num4 = input("Number 4 ->")

##owm = OWM('Enter your API Key from the OpenWeatherMap')
##mgr = owm.weather_manager()
#observation = mgr.weather_at_place('London,UK')  # the observation object is a box containing a weather object
#weather = observation.weather
#weather.status           # short version of status (eg. 'Rain')
#weather.detailed_status  # detailed version of status (eg. 'light rain')

time.sleep(1)

stop = False

while stop == False:
    recognize_speech_from_mic()
    query = str(question)
    print(f"What I heard-> {question}")

    print ("\n")

    add_div = "O.K. In case you have less than four numbers, type in 0(Zero) in the blank spaces."
    sub_mul = "No problem. In case you have less than four numbers, type in 0(Zero) in the blank spaces."
    
    if query == "add some numbers":
        speak (add_div, "add")
        print (add_div)
        time.sleep(3)
        asking_numbers()
        sumis = int(num1) + int(num2) + int(num3) + int(num4)
        speak (f"The sum(answer) is {sumis}.", "answer")
        print (f"The sum(answer) is {sumis}.")
        time.sleep(5)
        
    elif query == "subtract some numbers":
        speak = (sub_mul, "subtract")
        print (sub_mul)
        time.sleep(3)
        asking_numbers()
        difference = int(num1) - int(num2) - int(num3) - int(num4)
        speak (f"The difference(answer) is {difference}.", "answer")
        print (f"The difference(answer) is {difference}.")
        time.sleep(5)
        
    elif query == "multiply some numbers":
        speak = (sub_mul, "multiply")
        print (sub_mul)
        time.sleep(3)
        asking_numbers()
        product = int(num1) * int(num2) * int(num3) * int(num4)
        speak (f"The product(answer) is {product}.", "answer")
        print (f"The product(answer) is {product}.")
        time.sleep(5)
        
    elif query == "divide some numbers":
        speak = (add_div, "divide")
        print (add_div)
        time.sleep(3)
        asking_numbers()
        quotient = int(num1) / int(num2) / int(num3) / int(num4)
        speak (f"The quotient(answer) is {quotient}.", "answer")
        print (f"The quotient(answer) is {quotient}.")
        time.sleep(5)
        
    elif query == "tell me the date":
        speak (f"Today's date is {date}.", "date")
        print (f"Today's date is {date}.")

    elif query == "tell me the time":
        speak (f"The time is {current_time}.", "time")
        print (f"The time is {current_time}.")

    elif query == "tell me the date and time" or query == "tell me the time and date":
        speak (f"Today's time and date are {current_time}, {date}.", "time_and_date") 
        print (f"Today's time and date are {current_time}, {date}.")

    elif query == "open audion lyrics" or query == "open audio lyrics":
        speak ("Alright, opening Audion Lyrics now", "open_audion")
        print ("Alright, opening Audion Lyrics now")
        webbrowser.open('https://studio.youtube.com/channel/UCJkg92B2ZcPlqMJkv-In_OA')

    elif "search in youtube " in query:
        splitvid_name = query.partition("youtube ")
        vid_name = str(splitvid_name[2])
        speak(f"Here are the results for {vid_name} in YouTube", "youtube_search")
        print (f"Here are the results for {vid_name} in YouTube")
        webbrowser.open(f'https://www.youtube.com/results?search_query={vid_name}')

    elif "search " in query:
        splitterm = query.partition("search ")
        term = str(splitterm[2])
        speak (f"Here are the results for {term} in Google.com", "google_search")
        print (f"Here are the results for {term} in Google.com")
        webbrowser.open("https://www.google.com/search?query="+term)

    elif "open website " in query:
        splitlink = query.partition("website ")
        link = str(splitlink[2])
        speak (f"Opening {link} now", "opening_link")
        print (f"Opening {link} now")
        webbrowser.open('www.' + link)

    elif "drop the needle" in query:
        song = random.choice(song_source)
        if song == song_source[0]:
            song_name = "Darkside by Alan Walker featuring Au\Ra and Tomine Harket"
        elif song == song_source[1]:
            song_name = "Faded by Alan Walker"
        elif song == song_source[2]:
            song_name = "Heading Home by Alan Walker & Ruben"
        elif song == song_source[3]:
            song_name = "Lifeline by Lvly (Myra Granberg) feat. Emmi"
        elif song == song_source[4]:
            song_name = "The Spectre by Alan Walker"
        elif song == song_source[5]:
            song_name = "Way Way Back by Lvly (Myra Granberg)"
        else:
            song_name = "a song"
        speak (f"Playing {song_name} now", "random_song")
        print (f"Playing {song_name} now")
        webbrowser.open(song)

    elif query == "play darkside":
        speak ("Playing Darkside by Alan Walker featuring Au\Ra and Tomine Harket now", "playing_darkside")
        print ("Playing Darkside by Alan Walker featuring Au\Ra and Tomine Harket now")
        webbrowser.open(song_source[0])

    elif query == "play faded":
        speak ("Playing Faded by Alan Walker now", "playing_faded")
        print ("Playing Faded by Alan Walker now")
        webbrowser.open(song_source[1])

    elif query == "play heading home":
        speak ("Playing Heading Home by Alan Walker & Ruben now", "playing_heading_home")
        print ("Playing Heading Home by Alan Walker & Ruben now")
        webbrowser.open(song_source[2])

    elif query == "play lifeline":
        speak ("Playing Lifeline by Lvly (Myra Granberg) feat. Emmi", "playing_lifeline")
        print ("Playing Lifeline by Lvly (Myra Granberg) feat. Emmi")
        webbrowser.open(song_source[3])

    elif query == "play spectre" or query == "play the spectre":
        speak ("Playing The Spectre by Alan Walker now", "playing_the_spectre")
        print ("Playing The Spectre by Alan Walker now")
        webbrowser.open(song_source[4])

    elif query == "play way way back":
        speak ("Playing Way Way Back by Lvly (Myra Granberg) now", "playing_way_way_back")
        print ("Playing Way Way Back by Lvly (Myra Granberg) now")
        webbrowser.open(song_source[5])

    elif query == "what is the weather today?" or query == "what is the weather today" or query == "what is the weather?" or query == "what is the weather":
        if weather.status == "rain" or weather.status == "snow":
            stats = f"Today, there is a chance for {weather.detailed_status}"
        elif weather.status == "clear sky":
            stats = f"Today, the weather seems to be a {weather.detailed_status}"
        else :
            stats = f"Today, the weather seems to be {weather.detailed_status}"
        speak (f"{stats} and the temperature is currently {weather.temperature('celsius')['temp']} degree celsius.", "weather")
        print (f"{stats} and the temperature is currently {weather.temperature('celsius')['temp']}°C.")
        time.sleep(2)
        
    elif query == "give me the weather report":
        if weather.status == "rain" or weather.status == "snow":
            stats = f"Today, there is a chance for {weather.detailed_status}."
        elif weather.status == "clear sky":
            stats = f"Today, the weather seems to be a {weather.detailed_status}."
        else :
            stats = f"Today, the weather seems to be {weather.detailed_status}."
        speak (f"{stats} The humidity level is {weather.humidity}. The temperature is {weather.temperature('celsius')['temp']}degree celsius and the levels will be as low as {weather.temperature('celsius')['temp_min']}degree celsius and as high as {weather.temperature('celsius')['temp_max']}degree celsius.", "weather_report")
        print (f"{stats}")
        print (f"The humidity level is {weather.humidity}.")
        print (f"The temperature is {weather.temperature('celsius')['temp']}°C")
        print (f"and the levels will be as low as {weather.temperature('celsius')['temp_min']}°C and as high as {weather.temperature('celsius')['temp_max']}°C.")
        time.sleep(13)

    elif query == "read usa news":
        news_url="https://news.google.com/rss/search?q=america"
        Client=urlopen(news_url)
        xml_page=Client.read()
        Client.close()

        soup_page=soup(xml_page,"xml")
        news_list=soup_page.findAll("item")
        # Print news title, url and publish date
        headline_num = 1
        for news in news_list:
                news_date = news.pubDate.text.split(" ")
                speak(news.title.text, f"headline{headline_num}")
                print(news.title.text)
                print(f"\nLink to article = {news.link.text}")
                print(f"\nPublished = {news.pubDate.text}")
                print("-"*60)
                print()        
                if headline_num == 10:
                    break
                headline_num = headline_num + 1
                theresult = len(re.findall(r'\w+', news.title.text))/2.17
                time.sleep(theresult)

    elif "read the news about " in query:
        splitnews = query.partition("about ")
        news_term = str(splitnews[2])
        news_url=f"https://news.google.com/rss/search?q={news_term}"
        Client=urlopen(news_url)
        xml_page=Client.read()
        Client.close()

        soup_page=soup(xml_page,"xml")
        news_list=soup_page.findAll("item")
        # Print news title, url and publish date
        headline_num = 1
        for news in news_list:
                news_date = news.pubDate.text.split(" ")
                speak(news.title.text, f"headline{headline_num}")
                print(news.title.text)
                print(f"\nLink to article = {news.link.text}")
                print(f"\nPublished = {news.pubDate.text}")
                print("-"*60)
                print()        
                if headline_num == 10:
                    break
                headline_num = headline_num + 1
                theresult = len(re.findall(r'\w+', news.title.text))/2.17
                time.sleep(theresult)


    elif query == "read the world news":
        news_url="https://news.google.com/news/rss/headlines/section/topic/WORLD"
        Client=urlopen(news_url)
        xml_page=Client.read()
        Client.close()

        soup_page=soup(xml_page,"xml")
        news_list=soup_page.findAll("item")
        # Print news title, url and publish date
        headline_num = 1
        for news in news_list:
                news_date = news.pubDate.text.split(" ")
                speak(news.title.text, f"headline{headline_num}")
                print(news.title.text)
                print(f"\nLink to article = {news.link.text}")
                print(f"\nPublished = {news.pubDate.text}")
                print("-"*60)
                print()        
                if headline_num == 10:
                    break
                headline_num = headline_num + 1
                theresult = len(re.findall(r'\w+', news.title.text))/2.17
                time.sleep(theresult)

    elif query == "read uk news":
        news_url="https://news.google.com/rss/search?q=uk"
        Client=urlopen(news_url)
        xml_page=Client.read()
        Client.close()

        soup_page=soup(xml_page,"xml")
        news_list=soup_page.findAll("item")
        # Print news title, url and publish date
        headline_num = 1
        for news in news_list:
                news_date = news.pubDate.text.split(" ")
                speak(news.title.text, f"headline{headline_num}")
                print(news.title.text)
                print(f"\nLink to article = {news.link.text}")
                print(f"\nPublished = {news.pubDate.text}")
                print("-"*60)
                print()        
                if headline_num == 10:
                    break
                headline_num = headline_num + 1
                theresult = len(re.findall(r'\w+', news.title.text))/2.17
                time.sleep(theresult)

    elif query == "read england news":
        news_url="https://news.google.com/rss/search?q=england"
        Client=urlopen(news_url)
        xml_page=Client.read()
        Client.close()

        soup_page=soup(xml_page,"xml")
        news_list=soup_page.findAll("item")
        # Print news title, url and publish date
        headline_num = 1
        for news in news_list:
                news_date = news.pubDate.text.split(" ")
                speak(news.title.text, f"headline{headline_num}")
                print(news.title.text)
                print(f"\nLink to article = {news.link.text}")
                print(f"\nPublished = {news.pubDate.text}")
                print("-"*60)
                print()        
                if headline_num == 10:
                    break
                headline_num = headline_num + 1
                theresult = len(re.findall(r'\w+', news.title.text))/2.17
                time.sleep(theresult)

    elif query == "play chess":
        speak ("Good Luck!", "chess")
        print ("Good Luck.")
        webbrowser.open('https://chess.mobialia.com/')

    elif query == "open netflix":
        speak ("Enjoy!", "netflix")
        print ("Enjoy!")
        try:
            os.startfile(r"C:\Users\HP\Desktop\Netflix.lnk")
        except:
            webbrowser.open('https://www.netflix.com/')

    elif "what is " in query:
        search_term = query.partition("is ")
        term = (str(search_term[2]))
        if "?" in query:
            termq = term.split("?")
            term = termq[0]
        if " a " in query:
            term2 = term.split('a ')
            terma = term2[1]
            term = terma
        if "an" in query:
            term2 = term.split('an ')
            terman = term2[1]
            term = terman
        if "the" in query:
            term2 = term.split('the ')
            termthe = term2[1]
            term = termthe
        speak (f"Here are the results for {term}", "results_term")
        print ("Here are the results")

        wiki_wiki = wikipediaapi.Wikipedia('en')
        page = wiki_wiki.page(term)
        print ("Page - Title: %s" % page.title)
        print ("Page - Summary: %s" % page.summary)
        speak ("Would you like me to read it?", "readornot")
        print ("\nWould you like me to read it? \n")
        recognize_speech_from_mic()
        yesorno = question
        if yesorno == "yes" or yesorno == "y":
            speak(f"Alright {page.summary}", "OK")
            print("Alright")
            theresult = len(re.findall(r'\w+', page.summary))/2.17
            time.sleep(theresult)
        else:
            speak("Alright", "Nope")
            print("Alright")

    elif "translate " in query:
        # e.g.translate english into french
        if " to " in query:
            split_statement = query.split(" to ")
        else:
            split_statement = query.split(" into ")
        trans_lang_split = split_statement[0].split("ranslate ")
        origin_lang = trans_lang_split[1]
        print (split_statement)
        req_lang = split_statement[1]
        trans_term = input ("What you want to translate ->")
        origin_lang_code = LANGCODES[origin_lang]
        lang_code = LANGCODES[req_lang]
        try:
            tr = translator.translate(trans_term, dest= lang_code, src= origin_lang_code)
            speak ("The translation is ", "saying")
            print ("The translation is ")
            speak (f".    {tr.text}.    ", "translation", lang_code)
            print (f"{tr.text}")
            speak (f"from {origin_lang} to {req_lang}.", "saying_continue")
            print (f"from {origin_lang} to {req_lang}.")
            speak ("Would you like me to save and open it in a text file?", "savefile")
            print ("Would you like me to save and open it in a text file?")
            recognize_speech_from_mic()
            saveornot = question.lower()
        except:
            speak ("I can't do it at the moment. Please ask me later.", "error")
            print ("I can't do it at the moment. Please ask me later.")
        if saveornot.lower() == "yes" or saveornot.lower() == "y":
                transl_file = io.open(rf"{thepath}\translation.txt","w+", encoding="utf-8")
                transl_file.write(f"Translation from {origin_lang} to {req_lang}\n")
                transl_file.write(f"\n\nOriginal :\n")
                transl_file.write(trans_term)
                transl_file.write(f"\n\nTranslation :\n")
                transl_file.write(str(tr.text))
                transl_file.close()
                speak ("File Saved!", "saved")
                print ("File Saved!")
                os.startfile(rf"{thepath}\translation.txt")

    elif query == "set an alarm":
        speak("When?")
        when = input("When?(minutes) -> ")
        alarm_time_file = open(rf'{thepath}\alarm\alarm_time.txt', 'w')
        alarm_time_file.write(when)
        alarm_time_file.close()
        os.startfile(r'.\alarm\Alarm.py')

    elif "set an alarm " in query:
        # set an alarm in 20 minutes
        split_sentence = query.split("in ")
        when = ["0", "1"]
        if "minutes" in query:
            when = split_sentence[1].split(" minutes")
        if "minute" in query:
            when = split_sentence[1].split(" minute")
        alarm_time_file = open(rf'{thepath}\alarm\alarm_time.txt', 'w')
        alarm_time_file.write(when[0])
        alarm_time_file.close()
        os.startfile(r'.\alarm\Alarm.py')

    elif query == "no" or query == "nothing bye ida" or query == "nothing by ida" or query == "nothing. bye ida" or query == "nothing.. by ida":
        speak (f"Bye {name}!","bye")
        print (f"Bye {name}")
        stop = True
        break

    elif query == "who created you" or query == "who is your creator":
        speak ("I was created by Giga Blitz. You can contact him at gigablitzonline@gmail.com", "creator")
        print ("I was created by Giga Blitz. You can contact him at gigablitzonline@gmail.com")
    
    else:
        speak ("Sorry. I don't know how to do that.", "not_a_clue")
        print ("Sorry. I don't know how to do that.")
    
    time.sleep(3)
    speak(f"Anything else I can help you with?", "anything")
    print(f"\n\nAnything else I can help you with?")
    time.sleep(1)

print ("CLOSING NOW")
time.sleep(3)
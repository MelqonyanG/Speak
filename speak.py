from gtts import gTTS
import os
import subprocess
import simpleaudio as sa
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import nltk
nltk.download('punkt')


def get_audio_size(video_path):
    cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(video_path)
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    return float(output)


def speak(mytext, language='en', name='temp'):
    if os.path.isfile(f'{name}.mp3'):
        os.remove(f'{name}.mp3')
    if os.path.isfile(f'{name}.wav'):
        os.remove(f'{name}.wav')

    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save(f"{name}.mp3")

    cmd = f'ffmpeg -i {name}.mp3 {name}.wav'
    subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

    # Playing the converted file
    wave_obj = sa.WaveObject.from_wave_file(f"{name}.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

    size = get_audio_size(f'{name}.wav')

    os.remove(f'{name}.mp3')
    os.remove(f'{name}.wav')
    return size

def get_sentences(filename):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    with open(filename) as f:
        data = f.read()
    sentences = tokenizer.tokenize(data)
    return sentences


def remove_punctuation(sentence):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    result = ' '.join(tokenizer.tokenize(sentence))
    return result


def speech_to_text(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
    return text


def record_response(wait=20, fs=44100):
    wait += 5
    name = 'output'
    if os.path.isfile(f'{name}.mp3'):
        os.remove(f'{name}.mp3')
    if os.path.isfile(f'{name}.wav'):
        os.remove(f'{name}.wav')

    myrecording = sd.rec(int(wait * fs), samplerate=fs, channels=2)
    sd.wait()
    write(f'{name}.mp3', fs, myrecording)

    cmd = f'ffmpeg -i {name}.mp3 {name}.wav'
    subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

    try:
        text = speech_to_text(f'{name}.wav')
    except:
        text = ''

    os.remove(f'{name}.mp3')
    os.remove(f'{name}.wav')
    return text


if __name__ == '__main__':
    text = input('input file path: ') or "texts/text1.txt"
    number = input('input start number: ')
    number = int(number) if number and number.isdigit() else 0
    sentences = get_sentences(text)
    for s in sentences[number:]:
        sentence = remove_punctuation(s)
        size = speak(s)
        quit = False
        while True:
            step = input('type: a - answer, r - repeat, s - show, o - omit, q - quit : ')
            if step not in ['a', 'r', 's', 'o', 'q']:
                break
            if step == 'a':
                print('Speak my dear ... You can ... ')
                response = record_response(wait=size)
                print(response)
                if response == sentence:
                    print('Correct')
                    break
                else:
                    print('Ooops, try again ...')
            elif step == 'r':
                speak(s)
            elif step == 'q':
                quit = True
                break
            elif step == 'o':
                break
            else:
                print(sentence)
        if quit:
            print('Bye ... ')
            break


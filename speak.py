from gtts import gTTS
import os
import subprocess
import simpleaudio as sa
import os
import nltk
nltk.download('punkt')


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

    os.remove(f'{name}.mp3')
    os.remove(f'{name}.wav')


def get_sentences(filename):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    with open(filename) as f:
        data = f.read()
    sentences = tokenizer.tokenize(data)
    return sentences


if __name__ == '__main__':
    text = "texts/text1.txt"
    sentences = get_sentences(text)
    for s in sentences:
        speak(s)



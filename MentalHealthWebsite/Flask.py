#some libraries we needed
from flask import Flask, render_template, request, jsonify
from datetime import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile
import pyaudio
import pickle
import sklearn

#loading the ML Model
filename = 'EmoDetectModel-2.sav'
ED_model = pickle.load(open(filename, 'rb'))

#creates an instance of the flask thingy, basically allows us to run the website
app = Flask(__name__)

#uses / to navigate the html file
@app.route('/')

#home page
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    my_recording = record()
    prediction = ED_model.predict(my_recording)
    output = prediction #what's the format of the prediction?  
    return render_template('index.html', prediction_text="Through Machine Learning, we've predicted that you're feeling:{}".format(output))

#tracks the user's day and plots it in relation to previous entries
def DayChart(User, day):
    User.GetDayRating(day)
    plt.plot(User.dayRating, range(len(User.dayRating)))
    return plt

#runs the website
if __name__ == '__main__':
    app.run()

#records audio... i think
def record(duration=3, fs=8000):
    nsamples = duration*fs
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True,
                    frames_per_buffer=nsamples)
    buffer = stream.read(nsamples)
    array = np.frombuffer(buffer, dtype='int16')
    stream.stop_stream()
    stream.close()
    p.terminate()
    return array

#records an audio journal entry
def JournalEntry(User):
    my_recording = record()
    User.journal.append(my_recording)
    return my_recording

#The html locatoin of where the audio will be inputed
@app.route('/join', methods=['GET','POST'])
def my_form_post():
    Username = request.form['text1']
    word = request.args.get('text1')
    combine = JournalEntry(Username)
    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

#A basic User Profile that tracks basic information
class Profile():
    def __init__(self, username):
        self.username = username
        self.audios = None
        self.journal = []
        self.dayRating = []

    def __str__(self):
        return f'{self.username}'

    def GetDayRating(self, day):
        self.dayRating.append(day)

        self.dayRating[self.dayRating.index(day)].append(datetime.today)

    


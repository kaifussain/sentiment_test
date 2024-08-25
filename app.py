from flask import Flask, render_template, request
app = Flask(__name__)

from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")
def giveSentiment(input,neutralLimit):
    result = sentiment_pipeline(input)
    score=result[0]['score']
    sentiment_real=result[0]['label']

    sentimentResult = ''

    if(score < neutralLimit):
        sentimentResult='*Neutral'
    else:
        sentimentResult=result[0]['label']
    return [sentimentResult,sentiment_real,score]


@app.route('/', methods=['GET', 'POST'])
def index():
    sentiment = ""
    neutralLimit = 0.97
    if request.method == 'POST':
        text = request.form['text']
        neutralLimit = float(request.form.get('neutralLimit', neutralLimit))
        [sentiment,sentiment_real,score]=giveSentiment(text,neutralLimit)
        return render_template('index.html', sentence=text,sentiment=sentiment,sentiment_real=sentiment_real,score=score,neutralLimit=neutralLimit)
    return render_template('index.html', sentiment="",neutralLimit=neutralLimit)

if __name__ == '__main__':
    app.run()
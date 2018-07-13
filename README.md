# flask-twitter-predictions
Flask app for running (age, gender and fake personality) predictions from Twitter data. 

This was built as an introduction to `Flask` and eventually Docker-izing `sklearn` inside a Flask API. 

**Disclaimer**: the personality predictions are not real. The model / data in the referenced paper is not actually used in this app. 


## Installation
First download from GitHub

```bash
$ git clone https://github.com/sjgiorgi/flask-twitter-predictions.git && cd flask-twitter-predictions
```

then open the `config.py` file and add your Twitter credentials:

```python
class TwitterConfig(object):
    CONSUMER_KEY = 'somekey'
    CONSUMER_SECRET = 'somesecret'
    ACCESS_TOKEN = 'sometoken'
    ACCESS_TOKEN_SECRET = 'sometokensecret'
```

Finally we run with Flask

```bash
$ export FLASK_APP=prediction.py
$ flask run
 * Serving Flask app "prediction"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [12/Jul/2018 20:46:17] "GET / HTTP/1.1" 200 -
...
```

## How It Works
Given a Twitter handle we download their latest 100 tweets, tokenize and produce age, gender and (fake) personality predictions. The age and gender predictions are derived from the paper [Developing age and gender predictive lexica over social media](http://wwbp.org/papers/emnlp2014_developingLexica.pdf).  

```
@inproceedings{developing2014emnlp, 
  author={Sap, Maarten and Park, Greg and Eichstaedt, Johannes C and Kern, Margaret L and Stillwell, David J and Kosinski, Michal and Ungar, Lyle H and Schwartz, H Andrew}, 
  title={{Developing age and gender predictive lexica over social media}}, 
  booktitle={Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing}, 
  series={EMNLP}, 
  year={2014},
}
```

## Demo
A live demo is running [here](http://sgiorgi.pythonanywhere.com).

## Dependencies

* Flask
* tweepy


## TODO
* dockerize
* Add real predictions from `sklearn`
* add API
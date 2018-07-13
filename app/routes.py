from flask import render_template, flash, redirect, request
from app import app
from app.forms import TwitterHandle
from utils.twitter_worker import TwitterWorker
from utils.feature_worker import FeatureWorker

from collections import Counter
import json
import os 

# ellen   0.299910635630314   -0.19268990620758   0.49188117600401    0.536104548407424   0.152613595051368
# jones   0.386598906161264   -0.816132951125842  -0.00630991760763223    -0.272916121169616  -0.297895801599225
# justin  -0.0863439936710128 -0.027274289981541  0.647498495470014   0.369953545082055   0.592560201180955
# kanye   -0.422376018977781  -0.70700766348138   -0.1814592617385    -0.545910848864254  -0.478598523290196
# obama   0.364144449474829   0.782577476333631   -0.629466673644038  0.303257228323024   0.720172564961502
# trump   0.101371095973346   0.677445134474663   -0.69110912913034   -0.224822424033124  0.200991891561543

DEFAULT_SAMPLES = {
    '25073877': {'name': 'Donald Trump', 'handle': 'realDonaldTrump', 'user_id': 25073877, 
        'default_image': 'img/samples/thumbnails/trump.jpg',
        'age': '', 'gender': '', 
        'personality': {'ope': 0.101371095973346, 'con': 0.677445134474663, 'ext': 0.69110912913034, 'agr': 0.224822424033124, 'neu': 0.200991891561543}},
    '813286': {'name': 'Barack Obama', 'handle': 'barackobama', 'user_id': 813286, 
        'default_image': 'img/samples/thumbnails/obama.jpg',
        'age': '', 'gender': '', 
        'personality': {'ope': 0.364144449474829, 'con': 0.782577476333631, 'ext': 0.629466673644038, 'agr': 0.303257228323024, 'neu': 0.720172564961502}},
    '47216804': {'name': 'Leslie Jones', 'handle': 'Lesdoggg', 'user_id': 47216804, 
        'default_image': 'img/samples/thumbnails/jones.jpg',
        'age': '', 'gender': '', 
        'personality': {'ope': 0.386598906161264, 'con': 0.816132951125842, 'ext': 0.00630991760763223, 'agr': 0.272916121169616, 'neu': 0.297895801599225}},
    '4913077814': {'name': 'Kayne West', 'handle': 'officiaikanye', 'user_id': 4913077814, 
        'default_image': 'img/samples/thumbnails/west.jpg',
        'age': '', 'gender': '', 
        'personality': {'ope': 0.422376018977781, 'con': 0.70700766348138, 'ext': 0.1814592617385, 'agr': 0.545910848864254, 'neu': 0.478598523290196}},
    '15846407': {'name': 'Ellen DeGeneres', 'handle': 'TheEllenShow', 'user_id': 15846407, 
        'default_image': 'img/samples/thumbnails/ellen.jpg',
        'age': '', 'gender': '', 
        'personality': {'ope': 0.299910635630314, 'con': 0.19268990620758, 'ext': 0.49188117600401, 'agr': 0.536104548407424, 'neu': 0.152613595051368}},
    '27260086': {'name': 'Justin Bieber', 'handle': 'justinbieber', 'user_id': 27260086, 
        'default_image': 'img/samples/thumbnails/bieber.jpg',
        'age': '', 'gender': '', 
        'personality': {'ope': 0.0863439936710128, 'con': 0.027274289981541, 'ext': 0.647498495470014, 'agr': 0.369953545082055, 'neu': 0.592560201180955}},
}

DEF_NUMBERED_SAMPLES = {
    'one': DEFAULT_SAMPLES['25073877'],
    'two': DEFAULT_SAMPLES['813286'],
    'three': DEFAULT_SAMPLES['47216804'],
    'four': DEFAULT_SAMPLES['4913077814'],
    'five': DEFAULT_SAMPLES['15846407'],
    'six': DEFAULT_SAMPLES['27260086'],
}

DEF_GENDER_MAPPING = {0: 'male', 1: 'female'}

DEF_N = 1

DEF_DATA_LOC = '/data/'
DEF_DATA_FILES = {
    'age_gender': {'lex': 'age_gender.json', 'intercepts': 'age_gender_intercepts.json'},
    'topics': {'lex': 'met_a30_2000_cp.json', 'intercepts': None},
}

def _load_data(data_file):
    if data_file:
        local = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + DEF_DATA_LOC
        with open(local + data_file) as json_file:  
            data = json.load(json_file)
        return data
    else:
        return None

def get_age_gender_preds(fw, data):
    ag_pred = fw.extractLexicon(data['ngrams'], 
        lex=_load_data(DEF_DATA_FILES['age_gender']['lex']), 
        intercepts=_load_data(DEF_DATA_FILES['age_gender']['intercepts']))
    data.update(ag_pred)
    
    data['age'] = int(data['age'])
    if data['age'] < 30:
        data['age_cat'] = 'young'
    elif data['age'] < 50:
        data['age_cat'] = 'middle'
    else:
        data['age_cat'] = 'old'
    
    if data['gender'] > 0:
        data['gender'] = 'female'
    else:
        data['gender'] = 'male'
    return data

def get_data_for_user(handle='', sample=False):
    data = {'name': '', 
        'handle': handle,
        'profile_image': '', 
        'prediction': True,
        'ngrams': dict(), 
        'age': None,
        'gender': None,
        'ope': 0.3, 'con': 0.3, 'ext': 0.3, 'agr': 0.3, 'neu': 0.3
        }

    tw = TwitterWorker()
    fw = FeatureWorker()
    if not handle: data['handle'] = tw.default_handle
    if sample: 
        data['handle'] = str(tw.getHandleFromUid(handle))
        data.update(DEFAULT_SAMPLES[handle]['personality'])

    #get profile info
    data.update(tw.get_profile(data['handle']))
    
    # extract ngrams
    posts = tw.get_tweets(data['handle'])
    data['ngrams'].update(fw.fullNGramExtract(posts, n=DEF_N))

    # extract topics
    topics = fw.extractLexicon(data['ngrams'], 
                    lex=_load_data(DEF_DATA_FILES['topics']['lex']), 
                    intercepts=_load_data(DEF_DATA_FILES['topics']['intercepts']))

    # get age and gender predictions
    data.update(get_age_gender_preds(fw, data))
    del data['ngrams']
    return data

@app.route('/', methods=["GET","POST"])
@app.route('/index', methods=["GET","POST"])
def index():
    form = TwitterHandle()
    if form.validate_on_submit():
            user_data = get_data_for_user(form.handle.data)
            return render_template('sample.html', form=form, sample_data=user_data, default_samples=DEF_NUMBERED_SAMPLES)
    return render_template('index.html', form=form, default_samples=DEF_NUMBERED_SAMPLES)

@app.route('/sample', methods=["GET","POST"])
def sample():
    form = TwitterHandle()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_data = get_data_for_user(form.handle.data)
            return render_template('sample.html', form=form, sample_data=user_data, default_samples=DEF_NUMBERED_SAMPLES)
        else:
            return render_template('index.html', form=form, default_samples=DEF_NUMBERED_SAMPLES)
    else:
        sample_handle = request.args.get('sample_handle')
        user_data = get_data_for_user(sample_handle, sample=True)
        return render_template('sample.html', form=form, sample_data=user_data, default_samples=DEF_NUMBERED_SAMPLES)
        
    




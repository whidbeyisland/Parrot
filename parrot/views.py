import base64
import io
import json
import os
import gdown
#import fastbook
#fastbook.setup_book()
import fastai
import pandas as pd
import requests
import torchtext
import nltk

from torchvision import models
from torchvision import transforms
from PIL import Image
from django.shortcuts import render
from django.conf import settings
#from fastbook import *
from torchtext.data import get_tokenizer
from fastai.text.all import *
#from pathlib import Path

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import wordnet
from nltk import FreqDist
from string import punctuation
import datetime

from .forms import TextEntryForm
from .download_pkls import *
from .work_with_models import *
from .tweet_manipulations import *
from .likes_replies_generator import LikesRepliesGenerator

def index(request):
    syn1 = wordnet.synsets('vaccine')
    syn2 = wordnet.synsets('illness')
    print(len(syn1))
    print(len(syn2))
    for i in range(0, len(syn1)):
        for j in range(0, len(syn2)):
            try:
                syn1_a = syn1[i]
                syn2_a = syn2[j]
                print(str(i) + "......" + str(j))
                print('wup: ' + str(syn1_a.wup_similarity(syn2_a)))
                print('path: ' + str(syn1_a.path_similarity(syn2_a)))
                print('lch: ' + str(syn1_a.lch_similarity(syn2_a)))
            except:
                pass



    
    # print(nltk.tag.pos_tag(['lgbtq']))
    # print(nltk.tag.pos_tag(['libdems']))
    # print(nltk.tag.pos_tag(['alamo']))
    # print(nltk.tag.pos_tag(['retweeted']))
    # print(nltk.tag.pos_tag(['misunderstood']))

    # t = TweetManipulations()
    # t.find_syns('irredeemable')
    # t.find_syns('hate')
    # t.find_syns('dude')
    # t.find_syns('kick')

    request_complete = False
    predicted_label = None
    today = datetime.now()
    todaydate = today.strftime("%I:%M %p · %B %d, %Y")
    user_alias = 'Username Alias'
    username = 'username'
    predicted_tweets = ['Tweet goes here', 'Tweet goes here']
    num_likes_replies = LikesRepliesGenerator().generate(2)
    num_likes_str_0, num_replies_str_0 = num_likes_replies[0][0], num_likes_replies[0][1]
    num_likes_str_1, num_replies_str_1 = num_likes_replies[1][0], num_likes_replies[1][1]

    if request.method == 'POST':
        form = TextEntryForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            prompt = form.cleaned_data['prompt']

            try:
                d = DownloadPkls()
                t = TweetManipulations()
                w = WorkWithModels(d, t)

                w.download_user_tweets(username)
                w.get_user_assets_ready(username)
                w.get_rare_words(username)
                w.get_syns_rare_words(username)
                # w.get_POS('retweeted', 'jimmy_wales')
                # w.get_POS('bitcoin', 'jimmy_wales')
                # w.get_POS('covid19', 'jimmy_wales')
                # w.get_POS('categories', 'jimmy_wales')
                # w.get_POS('ludicrous', 'jimmy_wales')
                w.get_generation_assets_ready()
                # vocab = w.get_vocab_of_learner(0)

                

                # w.get_categorization_assets_ready()
                # subs_to_generate = w.categorize_user(username)
                w.subs_eachuser[username] = [0, 1, 2]
                predicted_tweets = w.get_tweet_predictions(username, prompt)
                predicted_label = 'success!'
                user_alias = username # coati: retrieve person's alias
                request_complete = True

            except RuntimeError as re:
                predicted_label = re
                # predicted_label = "Prediction Error"

    else:
        form = TextEntryForm()

    context = {
        'form': form,
        'predicted_tweets': predicted_tweets,
        'predicted_label': predicted_label,
        'username': username,
        'user_alias': user_alias,
        'todaydate': todaydate,
        'num_likes_str_0': num_likes_str_0,
        'num_replies_str_0': num_replies_str_0,
        'num_likes_str_1': num_likes_str_1,
        'num_replies_str_1': num_replies_str_1,
        'request_complete': request_complete
    }
    return render(request, 'parrot/index.html', context)

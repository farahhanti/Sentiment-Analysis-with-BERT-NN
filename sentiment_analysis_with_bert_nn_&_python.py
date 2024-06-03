# -*- coding: utf-8 -*-
"""Sentiment Analysis with BERT NN & python.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12fem-TNsY7XCUZZMFjVP1K3WPsSlmINX

# ***1/ Install and import Dependencies***
"""

!pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

!pip install transformers requests beautifulsoup4 pandas numpy

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
from bs4 import BeautifulSoup
import re

"""# ***2/Instantiate Model***"""

tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

"""# ***3/ Encode and Calculate Sentiment***"""

tokens = tokenizer.encode('Don t like it anymore', return_tensors='pt')

result = model(tokens)

result.logits

int(torch.argmax(result.logits))+1

"""## ***4/ Collect Reviews***"""

r = requests.get('https://www.yelp.com/biz/social-brew-cafe-pyrmont')
soup = BeautifulSoup(r.text, 'html.parser')
regex = re.compile('.*comment.*')
results = soup.find_all('p', {'class': regex})
reviews = [result.text for result in results]

reviews

"""# ***5/ Load Reviews into DataFrame and Score***"""

import pandas as pd
import numpy as np

df = pd.DataFrame(np.array(reviews), columns=['review'])

df['review'].iloc[0]

def sentiment_score(review):
  tokens = tokenizer.encode('review', return_tensors='pt')
  result = model(tokens)
  return int(torch.argmax(result.logits))+1

sentiment_score(df['review'].iloc[1])

df['sentiment'] = df['review'].apply ( lambda x: sentiment_score(x[:512]))

df

df['review'].iloc[3]


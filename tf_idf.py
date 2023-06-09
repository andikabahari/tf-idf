# -*- coding: utf-8 -*-
"""tf_idf.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PsAQRFpO-5RV1F_jUTjnMIqnaY78S6KY

# Pembobotan menggunakan TF-IDF
"""

import nltk
from google.colab import drive
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import os
import math

nltk.download('stopwords')
nltk.download('wordnet')

# Commented out IPython magic to ensure Python compatibility.
drive.mount('/gdrive')
# %cd /gdrive

"""## Memuat dokumen

Setiap dokumen berasal dari file `.txt` yang berisi teks data berita dalam bahas Inggris. `docs` menampung semua dokumen yang telah dimuat.
"""

folder = '/gdrive/My Drive/Colab Notebooks/dataset/txt'
filenames = [
    'Ukraine ammunition depot reportedly hit in wave of Russian missile attacks.txt',
    'More than 20,000 Russian soldiers killed in five months in Ukraine, US says.txt',
    'Dutch police arrest fake ‘Boris Johnson’ for suspected drink-driving.txt'
]

docs = []
for name in filenames:
    src = os.path.join(folder, name)
    file = open(src, 'r')
    docs.append(file.read())
    file.close()

print('docs:')
for d in docs:
    print(repr(d))

"""## Mengubah teks menjadi token

Semua teks yang terkandung di dalam dokumen akan diubah menjadi token. Token diperoleh dari pemotongan teks berdasarkan karakter spasi, dengan demikian satu token mewakili satu kata di dalam teks. Adapun metode lemmatization yang diterapkan kepada token-token tersebut untuk mengubah bentuk kata ke kata dasar agar lebih relevan.
"""

lemmatizer = WordNetLemmatizer()

def tokenize(text):
    sentences = text.split('.')
    sentences = [re.sub(r"[^a-zA-Z ]", ' ', s) for s in sentences]
    tokens = [t for t in ' '.join(sentences).split(' ') if len(t) > 0]
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    tokens = [t.lower() for t in tokens]
    return tokens

def vocab_from_tokenized_docs(docs):
    vocab = []
    for d in docs:
        vocab.extend(d)
    return list(dict.fromkeys(vocab))

docs = [tokenize(d) for d in docs]

print('docs:')
for d in docs:
    print(d)

"""## Implementasi TF-IDF

Berikut ini implementasi TF-IDF untuk memberikan bobot terhadap token yang telah diperoleh.

### Term frequence

\begin{align}
    w_{t,d} = tf_{t,d}
\end{align}

Di mana $tf_{t,d} = $ jumlah kemunculan $t$ di dalam $d$.
"""

def term_freq(terms, docs):
    freq = {}
    for t in vocab_from_tokenized_docs(docs):
        freq[t] = 0
    for t in terms:
        freq[t] += 1
    return freq

w_td = [term_freq(d, docs) for d in docs]

print('w_td:')
for tf in w_td:
    print(tf)

"""### Log frequency

\begin{align}
w_{t,d} = \left\{
\begin{array}{cl}
1 + log(tf_{t,d}) & tf_{t,d} > 0 \\
0
\end{array}
\right.
\end{align}
"""

def log_freq(tf):
    freq = {}
    for t,f in tf.items():
        if f > 0:
            freq[t] = 1 + math.log(f, 10)
        else:
            freq[t] = 0
    return freq

w_td = [log_freq(tf) for tf in w_td]

print('w_td:')
for tf in w_td:
    print(tf)

"""### Document frequency"""

def doc_freq(w_td):
    freq = {}
    for t in w_td[0]:
        freq[t] = 0
    for tf in w_td:
        for t,f in tf.items():
            if f > 0:
                freq[t] += 1
    return freq

df = doc_freq(w_td)

print('df:', df)

"""### Inverse document frequency

\begin{align}
    idf = log\left(\frac{N}{df}\right)
\end{align}
"""

def inverse_doc_freq(df, N):
    freq = {}
    for t,f in df.items():
        freq[t] = math.log(N/f, 10)
    return freq

idf = inverse_doc_freq(df, len(docs))

print('idf:', idf)

"""### TF-IDF

\begin{align}
    w_{t,d} = tf \cdot idf
\end{align}
"""

def tf_idf(tf, idf):
    return {t: tf[t] * idf[t] for t in tf}

w_td = [tf_idf(tf, idf) for tf in w_td]

print('w_td:')
for tf in w_td:
    print(tf)

freq = {t: [] for t in w_td[0]}
for t in freq:
    for tf in w_td:
        freq[t].append(tf[t])
freq
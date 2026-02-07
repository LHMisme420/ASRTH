import joblib, sys, warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

m = joblib.load("fusionnet_nolf.pkl")
N = int(getattr(m, "n_features_in_", 0))

def feats(t):
    w=t.split()
    chars=len(t)
    words=len(w)
    uniq=len(set(w))/max(words,1)
    avg_word_len=(sum(len(x) for x in w)/max(words,1))
    punct=sum(1 for c in t if c in ".,;:!?\"'()-")
    digits=sum(c.isdigit() for c in t)
    upp=sum(c.isupper() for c in t)
    spaces=t.count(" ")
    bigrams=list(zip([x.lower() for x in w],[x.lower() for x in w[1:]]))
    uniqb=len(set(bigrams))/max(len(bigrams),1)
    base=[chars,words,uniq,avg_word_len,punct,digits,upp,spaces,uniqb]
    if N <= 0:
        return base
    if len(base) == N:
        return base
    if len(base) > N:
        return base[:N]
    return base + [0.0]*(N-len(base))

t = sys.stdin.read().strip()
x = feats(t)

cols = [f"f{i}" for i in range(len(x))]
X = pd.DataFrame([x], columns=cols)

p = float(m.predict_proba(X)[0][1])
print(p)

import json, os, sys
import numpy as np
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report
import joblib

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "datasets")
ART  = os.path.join(ROOT, "artifacts")
os.makedirs(ART, exist_ok=True)

MODEL_PATH = os.path.join(ROOT, "fusionnet_nolf.pkl")

def feats(t: str):
    w = t.split()
    chars = len(t)
    words = len(w)
    uniq = len(set(w)) / max(words, 1)
    avg_word_len = sum(len(x) for x in w) / max(words, 1)
    punct = sum(1 for c in t if c in ".,;:!?\"'()-")
    digits = sum(c.isdigit() for c in t)
    upp = sum(c.isupper() for c in t)
    spaces = t.count(" ")
    bigrams = list(zip([x.lower() for x in w], [x.lower() for x in w[1:]]))
    uniqb = len(set(bigrams)) / max(len(bigrams), 1)
    lines = t.count("\n")
    return [chars, words, uniq, avg_word_len, punct, digits, upp, spaces, uniqb, lines]

def load_lines(path: str):
    out = []
    with open(path, "r", encoding="utf8", errors="ignore") as f:
        for l in f:
            l = l.strip()
            if l:
                out.append(l)
    return out

def main():
    human_path = os.path.join(DATA, "human_small.txt")
    ai_path    = os.path.join(DATA, "ai_small.txt")

    if not os.path.exists(human_path) or not os.path.exists(ai_path):
        print("missing datasets/human_small.txt or datasets/ai_small.txt", file=sys.stderr)
        sys.exit(2)

    H = load_lines(human_path)
    A = load_lines(ai_path)

    X = np.array([feats(t) for t in (H + A)], dtype=np.float64)
    y = np.array([1]*len(H) + [0]*len(A), dtype=np.int64)

    m = joblib.load(MODEL_PATH)
    p = m.predict_proba(X)[:,1]

    auc = float(roc_auc_score(y, p)) if len(set(y)) == 2 else float("nan")

    thr = 0.55
    yhat = (p >= thr).astype(np.int64)

    cm = confusion_matrix(y, yhat, labels=[0,1]).tolist()
    rep = classification_report(y, yhat, labels=[0,1], target_names=["ai","human"], zero_division=0, output_dict=True)

    out = {
        "n_human": int(len(H)),
        "n_ai": int(len(A)),
        "auc": auc,
        "threshold": thr,
        "confusion_matrix_labels": ["ai(0)","human(1)"],
        "confusion_matrix": cm,
        "report": rep,
        "scores_summary": {
            "human_mean": float(np.mean(p[:len(H)])) if len(H) else None,
            "ai_mean": float(np.mean(p[len(H):])) if len(A) else None
        }
    }

    with open(os.path.join(ART, "eval.json"), "w", encoding="utf8") as f:
        json.dump(out, f, indent=2)

    print("AUC:", auc)
    print("WROTE artifacts/eval.json")

if __name__ == "__main__":
    main()

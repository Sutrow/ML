import copy
import random
from collections import defaultdict

text = ""
sign = [" ", "?", "!", ".", ";", "-"]
with open("train2.txt", "r", encoding="utf-8") as file:
    words = file.read().lower()
    for sym in words:
        text += sym if sym.isalpha() or sym in sign else ""

sentences = []
sentence = ""
for letter in text:
    if letter != "." and letter != "!" and letter != "?" and letter != ";":
        sentence += letter
    else:
        sentences.append(sentence.split())
        sentence = ""


model = defaultdict(lambda: [])

for sentence in sentences:
    for idx in range(0, len(sentence)):
        try:
            model[(sentence[idx])].append((sentence[idx + 1]))
            model[(sentence[idx], sentence[idx + 1])].append(sentence[idx + 2])
        except:
            pass


for (key, value) in model.items():
    words_with_weights = []
    uniq = set(value)
    for word in uniq:
        words_with_weights.append((word, value.count(word) / len(value)))
    model[key] = words_with_weights


def generate_sentence(prefix):
    start = copy.copy(prefix)
    text = [start[0], start[1]]
    for i in range(20):
        try:
            text.append(random.choices(model[start], weights=[x[1] for x in model[start]])[0][0])
        except:
            try:
                text.append(random.choices(model[start[-1]], weights=[x[1] for x in model[start[-1]]])[0][0])
            except:
                break
        start = (text[-2], text[-1])
    return " ".join(text)


def generate_text(count=20):
    res = []
    for i in range(count):
        res.append(generate_sentence(random.choice(list(model.keys()))))

    return res


print("\n".join(generate_text()))


import itertools
import random
import string

def generate_wordlist(first_names, last_names, specials, max_count=100):
    combos = set()
    for f in first_names:
        for l in last_names:
            combos.add(f + l)
            combos.add(f + l + "123")
            combos.add(f.capitalize() + l.capitalize())
            combos.add(f + "_" + l)
            combos.add(f + "123")
            combos.add(l + f)
            combos.add(f + random.choice(specials))
            combos.add(f + l + random.choice(specials))
    extra = [
        f + l + ''.join(random.choices(string.digits + ''.join(specials), k=2))
        for f, l in itertools.product(first_names, last_names)
    ]
    combos.update(extra)
    combo_list = list(combos)
    random.shuffle(combo_list)
    return combo_list[:max_count]

def save_wordlist(wordlist, filename="generated_wordlist.txt"):
    with open(filename, "w") as f:
        for word in wordlist:
            f.write(word + "\\n")

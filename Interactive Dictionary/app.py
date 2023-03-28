import json
from difflib import get_close_matches

data = json.load(open("data.json"))


def traslate(word):
    word = word.lower()
    if word in data:
        return data[word]
    elif word.title() in data:
        return data[word.title()]

    elif word.upper() in data:
        return data[word.upper()]

    elif len(get_close_matches(word, data.keys())) > 0:
        yn = input("Did you mean %s insteand? Enter Y if yes. Enter N if no.  " %
                   get_close_matches(word, data.keys())[0])
        yn = yn.upper()
        if yn == "Y":
            return data[get_close_matches(word, data.keys())[0]]
        elif yn == "N":
            return "the word does't exist. please doble check it"
        else:
            "we didn't undastand your word. "

    else:
        return "the word does't exist. please doble check it"


word_ = input("Enter a word: ")

output = traslate(word_)


if type(output) == list:
    for item in output:
        print(item)
else:
    print(output)

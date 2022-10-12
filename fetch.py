from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests
import json
import spacy
import lemminflect
from wiki import parse, get_meta_info, parsePos
import detectlanguage

detectlanguage.configuration.api_key = "80e5bcb4052ca36799eb1c4f8e5e305d"

nlp = spacy.load('en_core_web_lg')

app_id = "d2c3a956"
app_key = "d3aa6cf7a74f2c233c544cf0b600c8db"
language = "en-us"

app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = methods,
    allow_headers = headers    
)

@app.get("/")
def test():
    return {"message": "Hello"}

@app.get("/{word}")
def find_meaning(word):
    doc = nlp(word)
    print(doc[0].tag_)
    if (doc[0].pos_=="NOUN" and doc[0].tag_!='NNP'):
        word = doc[0]._.lemma()
    elif doc[0].tag_=='NNP':
        word = word.upper()
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word.lower()
    r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    json_text = json.loads(r.text)
    if ('results' in json_text):
        return json_text['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
    else:
        word = doc[0]._.lemma()
        url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word.lower()
        r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
        json_text = json.loads(r.text)
        if ('results' in json_text):
            return json_text['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
        else:
            return "Unable to find definition"

def find_pos(pos):
    if ('NN' == pos or 'NNS' == pos):
        return "Noun"
    elif 'NNP' == pos:
        return "Proper_noun"
    elif "VB" in pos or "MD" in pos:
        return "Verb"
    elif "JJ" in pos:
        return "Adjective"
    elif "UH" in pos:
        return "Interjection"
    elif "RB" in pos:
        return "Adverb"

def detect_lang(lang):
    langs = {'en': 'English', 'es': 'Spanish', 'ja': 'Japanese'}
    return langs[lang]

async def callUrl(word,pos):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"}
    url = f'https://en.wiktionary.org/w/index.php?title={word}&printable=yes'
    await res = requests.get(url, headers=headers)
    if (res.status_code==404):
        return None
    soup = BeautifulSoup(res.text, 'html.parser')
    jsonPos = get_meta_info(soup)
    json_res = parse(res, word, pos, jsonPos)
    return json_res

@app.get("/wiki/{word}")
def get_json(word, request: Request, other_lang=False):
    lang = "English"
    if other_lang:
        lang = detect_lang(detectlanguage.detect(word)[0]['language'])
    print(word)
    as_it_is = word
    word=word.lower()
    doc = nlp(word)
    pos = find_pos(doc[0].tag_)
    if (pos==None):
        pos = "Pronoun"
    print(pos)
    word = doc[0]._.lemma()
    res = None
    if (pos=="Noun"):
        word = doc[0]._.lemma()
        print(word)
        res = callUrl(word,pos)
        print(res)
        # Search as lower case if not found
        if (res==None):
            res = callUrl(word.title(),pos)
            if (res):
                return res
        else:
            return res
    elif pos=="Proper_noun":
        word = doc[0]._.lemma().title()
        res = callUrl(word,pos)
        # Search as lower case if not found
        if (res==None):
            res = callUrl(word.lower(),pos)
            if (res):
                return res
        else:
            return res
    else:
        print(f"Here {word}")
        res = callUrl(word,pos)
        # Search as capital
        if (res==None):
            res = callUrl(word.title(),pos)
            if (res):
                return res
        else:
            return res
    # If by now it hasn't returned, you must search as it is
    print(as_it_is)
    return callUrl(as_it_is, pos)

@app.get("/pos/{word}/{pos}/{syn}/{ant}/{rel}")
async def get_pos(word, pos, syn, ant, rel):
    url = f'https://en.wiktionary.org/w/index.php?title={word}&printable=yes'
    print(url)
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"}
    await res = requests.get(url, headers=headers)
    json_res = parsePos(res, word, pos, syn, ant, rel)
    return json_res

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    run(app, host="0.0.0.0", port=port)

import requests
from bs4 import BeautifulSoup
from nltk import sent_tokenize
import nltk
nltk.download('punkt')
import json
import re
import copy

scrape = re.compile(r"[a-zA-Z ]+")

# def extract_synonyms(en):
#   synonyms = en.findNext('span', {"id": "Synonyms"})
#   syns = []
#   if (synonyms):
#     synonyms = synonyms.parent.findNextSiblings('ul')
#     # print(synonyms)
#     synonyms = synonyms[0].find_all('li')
#     for synonym in synonyms:
#       syns.append(synonym.get_text())
#   return syns

# def extract_antonyms(en):
#   antonyms = en.findNext('span', {"id": "Antonyms"})
#   ants = []
#   if (antonyms):
#     antonyms = antonyms.parent.findNextSiblings('ul')
#     antonyms = antonyms[0].find_all('li')
#     for antonym in antonyms:
#       ants.append(antonym.get_text())
#   return ants

# def extract_terms(en):
#   rel = en.findNext("span", {"id": "Related_terms"})
#   terms = []
#   if (rel):
#     rel = rel.parent.findNextSiblings('ul')
#     rel = rel[0].find_all('li')
#     for term in rel:
#       terms.append(term.get_text())
#   return terms

# def extract_images(en):
#   images = en.find_all_next('img', {"class": "thumbimage"})
#   img_tags = []
#   for image in images:
#     img_tags.append("https://"+image['src'])
#   return img_tags

# def extract_meanings(en, res, pos):
#   lists = en.findNext('span', {"id": pos})
#   if (lists):
#     print(1)
#     lists = lists.parent.findNext('ol')
#   else:
#     print(2)
#     lists = en.findNext('span', {"id": "Noun"})
#     if (lists):
#       lists = lists.parent.findNext('ol')
#   cits = [x.extract() for x in lists.select('ul')]

#   li = lists.find_all('li')
#   i = 0

#   for l in li:
#     # Extract ib-content
#     ib_content = [x.extract() for x in l.select('span.ib-content')]
#     sentence = ""
#     if (ib_content!=[]):
#       ib_content = ib_content[0].get_text()
#       sentence=f"({ib_content}) "
#     ib_brac = [x.extract() for x in l.select('span.ib-brac')]
#     example = [y.get_text().strip() for y in [x.extract() for x in l.select('dd')]]
#     sentence += ' '.join(sent_tokenize(l.get_text().strip()))
#     sentence = sentence.strip()
#     res[i] = {}
#     res[i]['meaning'] = sentence
#     exs = []
#     for e in example:
#         exs.append(e)
#       # meanings[i]['example']
#     res[i]['examples'] = exs
#     i+=1
#     # li.find_all('dd')[1].get_text()

def get_meta_info(soup, res=None):
  if (not(res)):
    langs = []
    info = {" Synonyms": 0, " Antonyms": 0, " Related terms": 0}
    # pos = {' Noun': [False, {" Synonyms": False, " Antonyms": False, " Related terms": False}, 0], ' Verb': [False, {" Synonyms": False, " Antonyms": False, " Related terms": False}, 0], ' Adjective': [False, {" Synonyms": False, " Antonyms": False, " Related terms": False}, 0], ' Adverb': [False, {" Synonyms": False, " Antonyms": False, " Related terms": False}, 0], ' Interjection': [False, {" Synonyms": False, " Antonyms": False, " Related terms": False}, 0], ' Proper noun': [False, {" Synonyms": False, " Antonyms": False, " Related terms": False}, 0]}
    pos = {' Noun': [False, copy.deepcopy(info)], ' Verb': [False, copy.deepcopy(info)], ' Adjective': [False, copy.deepcopy(info)], ' Adverb': [False, copy.deepcopy(info)], ' Interjection': [False, copy.deepcopy(info)], ' Proper noun': [False, copy.deepcopy(info)], ' Pronoun': [False, copy.deepcopy(info)], ' Determiner': [False, copy.deepcopy(info)]}
    meta_info = {" Pronunciation": False}
    m_flag = 1
    for lang in soup.find_all('li', {"class": "toclevel-1"}):
      langs.append(lang.find('span', {"class": 'toctext'}).get_text())
    
    syns = 0
    ants = 0
    rels = 0

    try: 
      index = langs.index('English')
    except ValueError:
      try: 
        index = langs.index('Translingual')
      except ValueError:
        return None
      else:
        l = [x.get_text() for x in soup.find_all('span', {"class": "toctext"})[index].findNext('ul').find_all('li')]
        for text in l:
          search = re.findall(scrape, text)
          if (search[0].strip().lower()=='etymology'):
            continue
          # print(search)
          if (m_flag):
            for m in meta_info:
              if (m in search):
                m_flag = 0
                meta_info[m] = True

          for s in pos:
            if (not(pos[s][0])):
              if (s in search):
                pos[s][0] = True
                for i in pos[s][1]:
                  if (i in search):
                    if (i==' Synonyms'):
                      syns+=1
                      pos[s][1][i] = syns
                    if (i==' Antonyms'):
                      ants += 1
                      pos[s][1][i] = ants
                    if (i==' Related terms'):
                      rels += 1
                      pos[s][1][i] = rels
        pos['meta_info'] = meta_info
        return pos
    else:
        l = [x.get_text() for x in soup.find_all('span', {"class": "toctext"})[index].findNext('ul').find_all('li')]
        for text in l:
          search = re.findall(scrape, text)
          if (search[0].strip().lower()=='etymology'):
            continue
          # print(search)
          if (m_flag):
            for m in meta_info:
              if (m in search):
                m_flag = 0
                meta_info[m] = True

          for s in pos:
            if (not(pos[s][0])):
              if (s in search):
                pos[s][0] = True
                for i in pos[s][1]:
                  if (i in search):
                    print(s, i)
                    if (i==' Synonyms'):
                      syns+=1
                      pos[s][1][i] = syns
                    if (i==' Antonyms'):
                      ants += 1
                      pos[s][1][i] = ants
                    if (i==' Related terms'):
                      rels += 1
                      pos[s][1][i] = rels
        pos['meta_info'] = meta_info
        return pos
  else:
    print("Here")
    return res

# def parse(response, word, pos, lang="en"):
#   print(pos)
#   soup = BeautifulSoup(response.text, 'html.parser')
#   en = soup.find('span', {"id": lang.title()})
#   if (en):
#     en = en.parent
#   else:
#     en = soup.find('span', {"id": "Translingual"})
#     if (en==None):
#       return None
  
#   pronunciation = en.find_next('td', {'class': 'audiofile'})
#   if (pronunciation==None):
#     pronunciation = None
#   else:
#     pronunciation = pronunciation.find('source')['src']
#   res = {}
#   res['audio'] = pronunciation
#   res['word'] = word
#   res['pos'] = pos
#   extract_meanings(en, res, pos)
#   res['synonyms'] = extract_synonyms(en)
#   res['antonyms'] = extract_antonyms(en)
#   res['related_terms'] = extract_terms(en)
#   res['img_tags'] = extract_images(en)
#   # print(res)
#   print("Here")
#   f = open('temp.json', "w")
#   json.dump(res, f)
#   return res

def extract_synonyms(lists, pos_occ):
  if pos_occ!=1:
    synonyms = lists.findNext('span', {"id": f"Synonyms_{pos_occ}"})
  else:
    synonyms = lists.findNext('span', {"id": "Synonyms"})
  syns = []
  if (synonyms):
    synonyms = synonyms.parent.findNextSiblings('ul')
    synonyms = synonyms[0].find_all('li')
    for synonym in synonyms:
      syns.append(synonym.get_text())
  return syns

def extract_antonyms(lists, pos_occ):
  if pos_occ!=1:
    antonyms = lists.findNext('span', {"id": f"Antonyms_{pos_occ}"})
  else:
    antonyms = lists.findNext('span', {"id": "Antonyms"})
  ants = []
  if (antonyms):
    antonyms = antonyms.parent.findNextSiblings('ul')
    antonyms = antonyms[0].find_all('li')
    for antonym in antonyms:
      ants.append(antonym.get_text())
  return ants

def extract_terms(lists, pos_occ):
  if pos_occ!=1:
    rel = lists.findNext('span', {"id": f"Related_terms_{pos_occ}"})
  else:
    rel = lists.findNext('span', {"id": "Related_terms"})
  terms = []
  if (rel):
    rel = rel.parent.findNextSiblings('ul')
    if (not(rel)):
      return []
    rel = rel[0].find_all('li')
    for term in rel:
      terms.append(term.get_text())
  return terms

def extract_images(en):
  images = en.find_all_next('img', {"class": "thumbimage"})
  img_tags = []
  for image in images:
    img_tags.append(str(image))
  return img_tags

def extract_images(en):
  images = en.find_all_next('img', {"class": "thumbimage"})
  img_tags = []
  for image in images:
    img_tags.append('https://'+image['src'])
  return img_tags

def extract_meanings(lists, res):
  cits = [x.extract() for x in lists.select('ul')]

  li = lists.find_all('li')
  i = 0

  for l in li:
    # Extract ib-content
    ib_content = [x.extract() for x in l.select('span.ib-content')]
    sentence = ""
    if (ib_content!=[]):
      ib_content = ib_content[0].get_text()
      sentence=f"({ib_content}) "
    ib_brac = [x.extract() for x in l.select('span.ib-brac')]
    example = [y.get_text().strip() for y in [x.extract() for x in l.select('dd')]]
    sentence += ' '.join(sent_tokenize(l.get_text().strip()))
    sentence = sentence.strip()
    if sentence!='':
      res[i] = {}
      res[i]['meaning'] = sentence
      exs = []
      for e in example:
          exs.append(e)
        # meanings[i]['example']
      res[i]['examples'] = exs
      i+=1
    # li.find_all('dd')[1].get_text()

def get_audio(en):
  pronunciation = en.find_next('td', {'class': 'audiofile'})
  if (pronunciation==None):
    pronunciation = None
  else:
    pronunciation = pronunciation.find('source')['src']
  return pronunciation

def parse(response, word, pos, ps):
  if (ps==None):
    return None
  soup = BeautifulSoup(response.text, 'html.parser')
  en = soup.find('span', {"id": "English"})
  if (en):
    en = en.parent
  else:
    en = soup.find('span', {"id": "Translingual"})
    if (en==None):
      return None
  print(ps)
  res = {}
  if ps['meta_info'][' Pronunciation']:
    res['audio'] = get_audio(en)
  res['meta'] = ps
  res['word'] = word
  mod_pos = f' {pos}'
  if (pos=="Proper_noun"):
    mod_pos = f' Proper noun'
  res['pos'] = mod_pos.strip()
  if ps[mod_pos][0]:
    lists = en.findNext('span', {"id": f"{pos.strip()}"}).parent.findNext('ol')
    extract_meanings(lists, res)
    print(res)
    if ps[mod_pos][1][' Synonyms']:
      res['synonyms'] = extract_synonyms(lists, ps[mod_pos][1][' Synonyms'])
    if ps[mod_pos][1][' Antonyms']:
      res['antonyms'] = extract_antonyms(lists, ps[mod_pos][1][' Antonyms'])
    if ps[mod_pos][1][' Related terms']:
      res['related_terms'] = extract_terms(lists, ps[mod_pos][1][' Related terms'])
    res['img_tags'] = extract_images(en)
    # print(res)
  else:
    otherAva = None
    for key in ps:
      if (key=='meta_info'):
        continue
      if ps[key][0]==True:
        otherAva = key
        break
    if otherAva==None:
      return None
    print("otherAva:", otherAva)
    if otherAva!=None:
      res['pos'] = otherAva.strip()
      if (otherAva==" Proper noun"):
        otherAva = " Proper_noun"
      mod_pos = otherAva
      if (otherAva.strip()=="Proper_noun"):
        mod_pos = f' Proper noun'
      
      lists = en.findNext('span', {"id": f"{otherAva.strip()}"}).parent.findNext('ol')
      extract_meanings(lists, res)
      if ps[mod_pos][1][' Synonyms']:
        res['synonyms'] = extract_synonyms(lists, ps[mod_pos][1][' Synonyms'])
      if ps[mod_pos][1][' Antonyms']:
        res['antonyms'] = extract_antonyms(lists, ps[mod_pos][1][' Antonyms'])
      if ps[mod_pos][1][' Related terms']:
        res['related_terms'] = extract_terms(lists, ps[mod_pos][1][' Related terms'])
      res['img_tags'] = extract_images(en)
  # res = json.dumps(res, indent=4)
  print("I exist")
  return res

def parsePos(response, word, pos, syn, ant, rel):
  soup = BeautifulSoup(response.text, 'html.parser')
  en = soup.find('span', {"id": "English"})
  if (en):
    en = en.parent
  else:
    en = soup.find('span', {"id": "Translingual"})
    if (en==None):
      return None
  res = {}
  res['pos'] = pos.strip()
  if (pos=="Proper_noun"):
    res['pos'] = f'Proper noun'
  lists = en.findNext('span', {"id": f"{pos}"}).parent.findNext('ol')
  extract_meanings(lists, res)
  if syn!=0:
    res['synonyms'] = extract_synonyms(lists, syn)
  if ant!=0:
    res['antonyms'] = extract_antonyms(lists, ant)
  if rel!=0:
    res['related_terms'] = extract_terms(lists, rel)
    # print(res)
  # res = json.dumps(res, indent=4)
  return res

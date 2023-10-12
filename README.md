# TeenyTinyTitleTrove
# TinyTitleTrove

TinyTitleTrove is a name finder tool designed for assisting users in finding names that sound similar to character names from specific backgrounds. It uses takes in unlimited amount of books, scrap names using spacy NER in chunks, convert tit to audio using pyttsx3/gtts API, takes in a name and compare it with MFCC and sort the collected list of names in ascending order. The code can take in multiple names and sort the names on both individual similarity and average similarity. These are all saved in respective folders. Note that the output will be messy and can contain wrong data. made as part of an analysis project. It uses Euclidean distance for signal vectors.
## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [How to Use](#how-to-use)
- [Note](#Note)
- [sample output](#sample output)
- [License](#license)

## Introduction

TinyTitleTrove is a name finder tool created by a data analyst. Its primary purpose is to help users find names that pronounce similarly to character names from specific backgrounds, such as ideology, field, religion, century, fantasy, or country.

## Features

- Scrape names from a document and convert it to audio
- Sort the names wrt to the each given name. If multiple names are given, avg pronounciation of multiple names will be given as well.

## How to Use

To use TinyTitleTrove, follow these simple steps:

1. Provide a name (e.g., "Lenin") and specify the background ideology/field/religion/century/fantasy/country of the character.
2. Get the tool relevant names sources like books, newspapers, and documents to scraping the necessary data.
3. Receive a list of names that match the specified criteria.

## Note:
Not made for direct use. Output needs further processings.
default is low quality pyttsx3 engine(60% accuracy for non english words). recommended to use gtts api if can for best results.


## sample output
sample output(top few names) result for sandeep made in low quality pyttsx3:["santhi", "samvid", "santu", "sannati", "suddhi", "ciiti", "suffi", "saivya", "sundah", "suka", "sarpi", "sauti", "sanketa", "safi", "sande", "sandhi", "saddhya", "sayya", "sunder", "sanju", "sun  the", "suddhah", "saryu", "sivi", "sitaya", "saika", "saungi", "saadhvi", "sannivi", "supta", "saatvik", "satvik", "sapia", "syood", "sutji", "syiim", "syiin", "sakadh", "sunu", "sivya", "sasi", "sumna", "saikya", "sowkhya", "sanniv", "sutap", "samu", "santi", "sapya", "secti", "siaht", "sigheth", "sindhu", "sani", "sunda", "satya", "sonia", "saliga", "satyaki", "sipi", "syiid", "sindu", "sakyap", "sinec", "ciimia", "sadhu", "sarathi", "sibi", "samik", "tandi", "subhiin", "tiie", "simhaya", "sairya", "sandhya", "suhtra", "silaki", "sangat", "stutaya", "sudhama", "sanny", "syiit", "suni", "ciinya", "sonita", "syeni", "siong", "sito", "samiine", "samii", "satam", "xlii", "suddhena", "sudhana", "saktaya", "sanjayet", "sabdyate", "sunrta", "sthiini", "tunda", "kandi", "samiuddhi", "sanda", "satha", "saka", "sautabhi", "samiidhi", "sakti", "sudharma", "somay", "sarga", "summoneth", "samkha", "sakya", "syed", "saugandhi", "sadhri", "saiva", "certai", "navadeep", "sadhva", "sini", "santim", "thiki", "truwti", "shanthi", "soga", "ciinan", "samputa", "satyak", "sauchiti", "santih", "sunrita", "sundarim", "sudeshaya", "chindhi", "sree", "sri", "siuikhya", "samadhi", "saman", "cyam", "samedi", "suki", "suhma", "suta", "samprati", "sankhya", "sachi", "sthiti", "surya", "sambhuti", "diyate", "sankalp", "sruthi", "slee", "sushen", "kauneya", "stoka", "xion", "simhika", "suca", "sauryam", "shringi", "sanaat", "samika", "divy", "sambaya", "syiima", "sanskriti", "stallion", "sahadev", "sahdev", "sahgo", "sorria", "sarayti", "sata", "satah", "sarying", "sakheva", "sampat", "samhitam", "sevika", "santanu", "sarhhi", "sute", "chandi", "snia", "samata", "sammitah", "sanka", "sattvic", "satadri", "ciitur", "silina", "syena", "sankha", "saunka", "sanaka", "sambhu", "citya", "sitya", "synod", "santa", "santah", "sarnga", "srinoti", "ciii", "jaaya", "sandhaya", "senayor", "saroii", "sankhini", "suddham", "sankar", "saama", "sama", "subhima", "sarva", "dandi", "shaivya", "dufi", "sankata", "savdah", "subala", "sumad", "santan", "sivini", "sarvadi", "sathya", "sampaka", "sathvic", "subtil", "samudb", "tyat", "sakhin", "shaivite", "cintam", "sunita", "satta", "saba", "samhata", "cedi", "sola", "sayti", "samana", "salya", "gouni", "sanhita", "scion", 

## license:
GPL


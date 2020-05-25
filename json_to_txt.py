# json_to_txt.py 
# Reads news articles from a JSON file
# Splits the content into sentences
# Write each processed sentence into a text file

import json
import spacy
import re

# Loads the spaCy small English language model
nlp = spacy.load('en_core_web_sm')

def remove_special_chars(text):
	bad_chars = ["%", "#", '"', "*"] 
	for i in bad_chars: 
		text = text.replace(i, '')
	return text

def split_sentences(document):
	sentences = [sent.string.strip() for sent in document.sents]
	return sentences

def article_body_write(line):
	doc = nlp(line)
	sentences = split_sentences(doc)
	sentence_index = 0

	for sentence in sentences:
		sentence_index +=1
		print("Sentence #" + str(sentence_index) + "-" * 20)
		print(sentence)
		text_file.write(sentence + '\n')

def article_title_write(line):
	print("Title" + line[0])
	text_file.write(line[0] + '\n')

with open('/Users/erdemisbilen/Language/sports_article_body.json') as json_file:
	data = json.load(json_file)
	
	with open("sports_article_all.txt", "w") as text_file:
		for p in data:

			article_title = p['article_title']
			article_body = p['article_body']

			article_body = remove_special_chars(article_body)

			article_title_write(article_title)			
			article_body_write(article_body)

	text_file.close()
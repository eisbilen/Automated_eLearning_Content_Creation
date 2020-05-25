import json
import spacy
import textstat
import random

from spacy.tokenizer import Tokenizer
from spacy.lang.en import English # updated
from spacy.lang.en.stop_words import STOP_WORDS

from spacy.vectors import Vectors

from spacy.matcher import Matcher
from spacy.tokens import Span 

from collections import Counter
import re

PARENT_DIR = "/Users/erdemisbilen/Language/"
INPUT_FILE_NAME = "sports_article_all.txt"
OUTPUT_FILE_NAME = "sports_article_simple_test.txt"

EASY_MIN_SENTENCE_LENGTH = 4
EASY_MAX_SENTENCE_LENGTH = 9

MODARATE_MIN_SENTENCE_LENGTH = 10
MODARATE_MAX_SENTENCE_LENGTH = 16

DIFFICULT_MIN_SENTENCE_LENGTH = 17
DIFFICULT_MAX_SENTENCE_LENGTH = 22

RANDOM_LIST = [0,1]

LONG_WORDS_LIMIT = 5
POLYSYLLABIC_WORDS_LIMIT = 4

json_data = []
linguistic_features = []
named_entities = []

similar_words = []
missing_word = ""
option1 = ""
option2 = ""

def calculate_sentence_length(words):
  return (len(words))

def calculate_word_character_length_mavrg(words):
	total_char = 0
	for word in words:
		total_char += len(word)
	return (round(total_char/len(words),1))

def calculate_number_of_long_words (words):
  total_long_word = 0
  for word in words:
    if len(word) >  LONG_WORDS_LIMIT:
      total_long_word += 1
  return (total_long_word) 

def calculate_number_of_polysyllabic_words(words):
  total_polysyllabic_words = 0
  for word in words:
      if len(word) >  POLYSYLLABIC_WORDS_LIMIT:
        total_polysyllabic_words += 1
  return (total_polysyllabic_words)

def define_question_mark(words):
  question_mark = 0
  for word in words:
    if "?" in word:
      question_mark = 1
  return (question_mark) 

def simple_tokenization(line):
  sentence_length = 0
  linguistic_features = []
  tokenizer = Tokenizer(nlp.vocab)
  toks = tokenizer(line)

  for token in toks:
    print(token.text)

    if not "\n" in token.text:
      sentence_length += 1
      linguistic_features.append({'word': token.text})
  
  return(linguistic_features, sentence_length)

def define_missing_word(my_doc): 
  
  missing_word=""
  option1=""
  option2=""

  for token in my_doc:
    if token.is_punct != True and token.is_alpha == True :
      
      if (token.pos_ == "VERB" or token.pos_ == "ADJ" or token.pos_ == "ADV") and (random.choice(RANDOM_LIST)==1 or missing_word==""):
        w_id = nlp.vocab.strings[token.text]
        w_vector = nlp.vocab.vectors[w_id]
        most_similar = nlp.vocab.vectors.most_similar(w_vector.reshape(1,300), n=15)
        missing_word = token.text
        option1 = nlp.vocab.strings[most_similar[0][0][9]].lower()
        option2 = nlp.vocab.strings[most_similar[0][0][14]].lower()

  return(missing_word,option1,option2)

def define_named_entities(my_doc):
  named_entities = []
  for ent in my_doc.ents:
    named_entities.append({
      'entity': ent.text,
      'entity_label': ent.label_})
  return(named_entities)

def write_linguistic_features(matches_single):
  for match_id, start, end in matches_single:
    # Get the string representation 
    string_id = nlp.vocab.strings[match_id]  
    span = my_doc[start:end]  # The matched span
    print(match_id, string_id, start, end, span.text)  

# Loads the spaCy small English language model
nlp = spacy.load('en_core_web_md')

matcher_passive = Matcher(nlp.vocab)
matcher_conjuction = Matcher(nlp.vocab)
matcher_subject = Matcher(nlp.vocab)
matcher_object = Matcher(nlp.vocab)

matcher_future_tense = Matcher(nlp.vocab)

matcher_present_continuous_tense = Matcher(nlp.vocab)
matcher_present_perfect_tense = Matcher(nlp.vocab)
matcher_present_perfect_continuous_tense = Matcher(nlp.vocab)

matcher_simple_past_tense = Matcher(nlp.vocab)
matcher_simple_present_tense = Matcher(nlp.vocab)

matcher_possesive_ending = Matcher(nlp.vocab)
matcher_possesive_pronoun = Matcher(nlp.vocab)
matcher_prepositions_sub_conj = Matcher(nlp.vocab)

matcher_comparative_adjective = Matcher(nlp.vocab)
matcher_superlative_adjective = Matcher(nlp.vocab)

matcher_comparative_adverb = Matcher(nlp.vocab)
matcher_superlative_adverb = Matcher(nlp.vocab)

matcher_models = Matcher(nlp.vocab)
matcher_there_is_are = Matcher(nlp.vocab)
matcher_to_infinitive = Matcher(nlp.vocab)
matcher_gerunds = Matcher(nlp.vocab)

#Coordinating Conjunctions
#And, but, for, nor, or, so, and yet —these are the seven coordinating conjunctions. 

conjuction_rule_1 = [{'POS': 'CCONJ'}]
prepositions_sub_conj_rule_1 = [{'POS': 'ADP'}]

comparative_adjective_rule_1 = [{'TAG': 'JJR'}]
superlative_adjective_rule_1 = [{'TAG': 'JJS'}]

comparative_adverb_rule_1 = [{'TAG': 'RBR'}]
superlative_adverb_rule_1 = [{'TAG': 'RBS'}]

there_is_are_rule_1 = [{'TEXT': 'There', 'TEXT': 'there'},{'TEXT': 'is', 'TEXT': 'are'}]
models_rule_1 = [{'TAG': 'MD'},{'TAG': 'VB'} ]
to_infinitive_rule_1 = [{'TAG': 'TO'},{'TAG': 'VB'}]
gerunds_rule_1 = [{'TAG': 'VB'},{'TAG': 'VBG'}]

passive_rule_1 = [{'DEP': 'auxpass'}, {'TAG':'VBN'}]
subject_rule_1 = [{'DEP': 'csubj'}]
subject_rule_2 = [{'DEP': 'nsubj'}]
object_rule_1 = [{'DEP': 'dobj'}]

#Future Tenses With Auxiliaries
future_tense_rule_1 = [{'TEXT': 'will'}, {'TAG':'VB'}]
future_tense_rule_2 = [{'TEXT': 'shall'}, {'TAG':'VB'}]

#Morphological Present Tenses
simple_present_rule_1 = [{'POS': 'PRON'}, {'TAG': 'VBP','TAG': 'VBZ' }, {'TAG':'VB', 'TAG':'VBG', 'TAG':'VBN', 'OP': '!'}]
present_continuous_rule_1 = [{'TAG': 'VBZ', 'DEP': 'aux'}, {'TAG':'VBG', 'DEP': 'ROOT'}]
present_perfect_rule_1 = [{'TAG': 'VBZ', 'DEP': 'aux'}, {'TAG':'VBN', 'DEP': 'ROOT'}]
present_perfect_continuous_rule_1 = [{'TAG': 'VBZ', 'DEP': 'aux'}, {'TAG':'VBN'}, {'TAG':'VBN', 'DEP': 'ROOT'}]

#Morphological Past Tenses
simple_past_rule_1 = [{'POS': 'PRON'}, {'TAG': 'VBD'},{'TAG':'VB', 'TAG':'VBG', 'TAG':'VBN' , 'OP': '!'}]

#Possessive Endings the boy's ball
possesive_ending_rule_1 = [{'TAG':'POS'}]

#Possessive Pronoun
possesive_pronoun_rule_1 = [{'TAG':'PRP$'}]

matcher_passive.add('Passive', None, passive_rule_1)
matcher_subject.add('Subject', None, subject_rule_1)
matcher_subject.add('Subject', None, subject_rule_2)
matcher_object.add('Object', None, object_rule_1)
matcher_conjuction.add('Conjuction', None, conjuction_rule_1)

matcher_future_tense.add('Future Tense (will)', None, future_tense_rule_1)
matcher_future_tense.add('Future Tense (shall)', None, future_tense_rule_2)

matcher_present_continuous_tense.add('Present Continuous Tense', None, present_continuous_rule_1)
matcher_present_perfect_tense.add('Present Perfect Tense', None, present_perfect_rule_1)
matcher_present_perfect_continuous_tense.add('Present Perfect Continuous Tense', None, present_perfect_continuous_rule_1)

matcher_simple_past_tense.add('Simple Past Tense', None, simple_past_rule_1)

matcher_simple_present_tense.add('Simple Present Tense', None, simple_present_rule_1)
matcher_possesive_ending.add('Possesive Ending', None, possesive_ending_rule_1)
matcher_possesive_pronoun.add('Possesive Pronoun', None, possesive_pronoun_rule_1)

matcher_prepositions_sub_conj.add('Prepositions and Sub Conj', None, prepositions_sub_conj_rule_1)
matcher_comparative_adjective.add('Comparative Adjective', None, comparative_adjective_rule_1)
matcher_superlative_adjective.add('Superlative Adjective', None, superlative_adjective_rule_1)

matcher_comparative_adverb.add('Comparative Adverb', None, comparative_adverb_rule_1)
matcher_superlative_adverb.add('Superlative Adverb', None, superlative_adverb_rule_1)

matcher_models.add('Models', None, models_rule_1)
matcher_there_is_are.add('There is/are', None, there_is_are_rule_1)
matcher_to_infinitive.add('To+Infinitive', None, to_infinitive_rule_1)
matcher_gerunds.add('Gerunds', None, gerunds_rule_1)

# Using readlines() 
file = open(PARENT_DIR + INPUT_FILE_NAME, 'r') 
lines = file.readlines() 

with open(OUTPUT_FILE_NAME, "w") as text_file:
  # Strips the newline character 
  for line in lines:   
    linguistic_features = []
    named_entities = []
    my_doc = nlp(line)     

    words = [token.text for token in my_doc if token.is_punct != True and token.is_alpha == True]
    words_all = [token.text for token in my_doc]

    sentence_length = calculate_sentence_length(words)
    matches_subject = matcher_subject(my_doc)

    matches_comparative_adverb = matcher_comparative_adverb(my_doc)
    matches_there_is_are = matcher_there_is_are(my_doc)
    matches_to_infinitive = matcher_to_infinitive(my_doc)
    matches_gerunds = matcher_gerunds(my_doc)

    if sentence_length < EASY_MAX_SENTENCE_LENGTH and sentence_length > EASY_MIN_SENTENCE_LENGTH :
      word_character_length_mavrg = calculate_word_character_length_mavrg(words)
      number_of_long_words = calculate_number_of_long_words(words)
      linguistic_features, sentence_length = simple_tokenization(line)

      number_of_polysyllabic_words = calculate_number_of_polysyllabic_words(words)
      missing_word, option1, option2 = define_missing_word(my_doc)
      named_entities = define_named_entities(my_doc)
      question_mark = define_question_mark(words_all)

      matches_passive = matcher_passive(my_doc)      
      matches_conjuction = matcher_conjuction(my_doc)
      matches_subject = matcher_subject(my_doc)
      matches_object = matcher_object(my_doc)
      matches_simple_past_tense = matcher_simple_past_tense(my_doc)
      matches_future_tense = matcher_future_tense(my_doc)
      matches_present_continuous_tense = matcher_present_continuous_tense(my_doc)
      matches_present_perfect_tense = matcher_present_perfect_tense(my_doc)
      matches_present_perfect_continuous_tense = matcher_present_perfect_continuous_tense(my_doc)
      matches_simple_present_tense = matcher_simple_present_tense(my_doc)
      matches_possesive_ending = matcher_possesive_ending(my_doc)
      matches_possesive_pronoun = matcher_possesive_pronoun(my_doc)
      matches_prepositions_sub_conj = matcher_prepositions_sub_conj(my_doc)
 
      matches_comparative_adjective = matcher_comparative_adjective(my_doc)
      matches_superlative_adjective = matcher_superlative_adjective(my_doc)

      matches_comparative_adverb = matcher_comparative_adverb(my_doc)
      matches_superlative_adverb = matcher_superlative_adverb(my_doc)

      matches_models = matcher_models(my_doc)
      matches_there_is_are = matcher_there_is_are(my_doc)
      matches_to_infinitive = matcher_to_infinitive(my_doc)
      matches_gerunds = matcher_gerunds(my_doc)

      write_linguistic_features(matches_passive)
      write_linguistic_features(matches_conjuction)
      write_linguistic_features(matches_subject)
      write_linguistic_features(matches_object)
      write_linguistic_features(matches_simple_past_tense)
      write_linguistic_features(matches_future_tense)
      write_linguistic_features(matches_present_continuous_tense)
      write_linguistic_features(matches_present_perfect_tense)
      write_linguistic_features(matches_present_perfect_continuous_tense)
      write_linguistic_features(matches_simple_present_tense)
      write_linguistic_features(matches_possesive_ending)
      write_linguistic_features(matches_possesive_pronoun)
      write_linguistic_features(matches_prepositions_sub_conj)

      write_linguistic_features(matches_comparative_adjective)
      write_linguistic_features(matches_superlative_adjective)
      write_linguistic_features(matches_comparative_adverb)
      write_linguistic_features(matches_superlative_adverb)

      write_linguistic_features(matches_models)
      write_linguistic_features(matches_there_is_are)
      write_linguistic_features(matches_to_infinitive)
      write_linguistic_features(matches_gerunds)

      
      difficulty_score = (sentence_length + word_character_length_mavrg)

      print("-----------------------------------------------------------------------")
      print(words)
      print(f"Sentece Length: {sentence_length}")
      print(f"Mean Average Word Length: {word_character_length_mavrg}")
      print(f"Number of Long Words: {number_of_long_words}")
      print(f"Number of Polysyllabic Words: {number_of_polysyllabic_words}")

      print(f"Question Sentence: {question_mark}")

      print("-----------------------------------------------------------------------")
      
      json_data.append({
        'sentence': line,
        'sentence_length': sentence_length,
        'difficulty_score': difficulty_score,
        'missing_word': missing_word,
        'option1': option1,
        'option2': option2,
        'word_character_length_mavrg': word_character_length_mavrg,
        'number_of_long_words': number_of_long_words,
        'named_entities': named_entities,
        'linguistic_features': linguistic_features},
        )
  
      with open('simple_sentences.json', 'w') as outfile:
        json.dump(json_data, outfile)

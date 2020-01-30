# -*- coding: utf-8 -*-

import re
import json
import requests
import spacy
import pandas as pd
from nltk.corpus import stopwords
from flashtext import KeywordProcessor
from flask import Flask, request
import labelconfig
from textblob import TextBlob

from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from spacy.util import compile_prefix_regex, compile_infix_regex, compile_suffix_regex

# load spaCy model
global nlp
nlp = spacy.load('en_core_web_sm')
prefix_re = compile_prefix_regex(nlp.Defaults.prefixes)
suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)
infix_re = compile_infix_regex(nlp.Defaults.infixes)
simple_url_re = re.compile(r'''[a-zA-Z0-9]+(?:[-](?![-])[a-zA-Z0-9]+)+''') #regex to keep words having intra-word-dash as single token

def custom_tokenizer(nlp):
    return Tokenizer(nlp.vocab, English.Defaults.tokenizer_exceptions, 
                                prefix_search=prefix_re.search,
                                suffix_search=suffix_re.search,
                                infix_finditer=infix_re.finditer,
                                token_match=simple_url_re.match)


# set max_Ngrams length
n = 3
# set regex to remove punctuation except intra-word-dash(es) and abbreviations like "U.K.", "U.S.A" etc.
# p = re.compile(r"(\b[-']\b)|[\W_]")
p = re.compile(r"(\b[-']\b|\b[.])|[\W_]")


# stanford api
url = 'http://0.0.0.0:9000/?properties=%7B%22annotators%22%3A%22tokenize%2Cssplit%2Cpos%2Cner%22%2C%22outputFormat%22%3A%22json%22%7D'
headers = {"Content-Type": "application/json"}
LABELS = labelconfig.label_config["LABELS"]


# generate POS tags and entities using spaCy
def spacy_pos_tags(val):
    global ner_texts
    global ner_labels
    global modifiers
    ner_labels = []
    ner_texts = []
    temp_data = []
    modifiers = []
    nlp.tokenizer = custom_tokenizer(nlp)
    doc = nlp(val)
    for sent in doc.sents:
        tokens, tags = [], []
        for token in sent:
            tokens.append(token.text)
            tags.append(token.tag_)
        temp_data.append([' '.join(tokens), ' '.join(tags)])
    for token in doc:
        if token.dep_ in ['amod', 'nmod', 'compound']:
            modifiers.append(token.text)
    for ent in doc.ents:
        if ent.label_ in ['FAC', 'ORG', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'PERCENT', 'NORP']:
            if ent.text not in modifiers:
                ner_texts.append(ent.text)
                ner_labels.append((ent.text, ent.label_))
    #print(ner_texts)
    return(pd.DataFrame(temp_data, columns=['Sentence', 'Tags']))


# generate POS tags and entities using stanford corenlp
def stanford_pos_tags(val):
    val = val.encode("utf-8").decode("ascii", "ignore")
    tokens = requests.post(url = url, headers = headers, data = val).content
    tokens = tokens.decode('utf8')
    tokens = json.loads(tokens)
    #print(tokens)
    temp_data = []

    for index in tokens['sentences']:
        tokens, tags = [], []
        for token in index['tokens']:
            tokens.append(token['originalText'])
            tags.append(token['pos'])
        temp_data.append([' '.join(tokens), ' '.join(tags)])
        for token in index['entitymentions']:
            #print(token['text'], token['ner'])
            if token['ner'] in ['PERSON', 'MONEY', 'DATE', 'TIME', 'LOCATION', 'ORGANIZATION', 'EMAIL', 'URL', 'CITY', 'STATE_OR_PROVINCE', 'COUNTRY', 'NATIONALITY', 'RELIGION', 'CAUSE_OF_DEATH', 'PERCENT', 'TITLE', 'CRIMINAL_CHARGE', 'IDEOLOGY', 'DURATION']:
                if token['text'].lower() not in stopwords.words('english') and token['text'] not in modifiers:
                    ner_texts.append(token['text'])
                    ner_labels.append((token['text'], token['ner']))
    #print(ner_texts)
    return(pd.DataFrame(temp_data, columns=['Sentence', 'Tags']))


# combine both POS tags dataframes into a single dataframe
def spacy_stanford_pos_tags(val):
    return(pd.concat([spacy_pos_tags(val), stanford_pos_tags(val)], ignore_index=True))


# find Ngrams of a sentence
def find_ngrams(val):
    input_list = val.split()
    n_grams = []
    for j in range(n):
        lst = zip(*[input_list[i:] for i in range(j+1)])
        for item in lst:
            n_gram = ' '.join(item)
            n_grams.append(n_gram)
    return n_grams 


# generate dataframe of Ngrams and their respective POS tags
def create_ngrams_df(val):
    ngrams = []
    for row in spacy_stanford_pos_tags(val).applymap(find_ngrams).iterrows():
        ngrams.extend(list(zip(row[1]["Sentence"], row[1]["Tags"])))
    return(pd.DataFrame(ngrams, columns=['Ngrams', 'Tags']))


# filter Ngrams having only noun and adjective POS tags
def filter_noun_adj(val):
    valid_pos_list = ['NNP', 'NN', 'NNS', 'NNPS', 'JJ', 'JJR', 'JJS']
    return val.split()[-1][0] == 'N' and (set(val.split()).issubset(valid_pos_list))


# filter Ngrams again based on punctuations(preserve Ngrams having intra-word-dash(es)) and stopwords
def remove_punct(sentence):
    result = p.sub(lambda m: (m.group(1) if m.group(1) else " "), sentence)
    result = re.sub(" +", " ",result)
    return(sentence == result and not (set(sentence.split()).issubset(stopwords.words('english'))))


# filter Ngrams using ner_texts list
def remove_Ngrams_ner_texts(val):
    return not any(item in val for item in list(set(ner_texts))) # removes keywords like 'email id abc@xyz.com' if 'abc@xyz.com' is present in ner_texts


# create merged dataframe to input in flashtext's KeywordProcessor
def generate_merged_df(val, ner_texts, data):
    datas = pd.DataFrame(val, columns=['Keywords', 'Labels'])
    count_df = data
    #count_df = count_df.groupby('Ngrams', as_index=False).max()
    count_df = count_df.sort_values('count', ascending=False).drop_duplicates('Ngrams').sort_index().reset_index(drop=True)
    count_df.columns = ['Keywords', 'Tags', 'ngram_count', 'Noun_Count']
    
    grouped = count_df.groupby(['ngram_count'], as_index=False)
    uni_df = pd.DataFrame(columns = ['Keywords', 'Tags', 'ngram_count', 'Noun_Count'])
    bi_df = pd.DataFrame(columns = ['Keywords', 'Tags', 'ngram_count', 'Noun_Count'])
    tri_df = pd.DataFrame(columns = ['Keywords', 'Tags', 'ngram_count', 'Noun_Count'])
    for name,group in grouped:
        if name==1:
            uni_df = group.reset_index(drop=True)
            uni_df = uni_df.sort_values('Noun_Count', ascending=False, kind='heapsort').reset_index(drop=True)
        elif name==2:
            bi_df = group.reset_index(drop=True)
            bi_df = bi_df.sort_values('Noun_Count', ascending=False, kind='heapsort').reset_index(drop=True)
        else:
            tri_df = group.reset_index(drop=True)
            tri_df = tri_df.sort_values('Noun_Count', ascending=False, kind='heapsort').reset_index(drop=True)
#     print(uni_df)
#     print(bi_df)
#     print(tri_df)
    frames = [tri_df, bi_df, uni_df]
    ngram_df = pd.concat(frames, ignore_index=True)
    
    for i,item in enumerate(datas.Labels.tolist()):
        for label in LABELS:
            if item in label['name']:
                datas.Labels[i] = label['key']
    
    keywords_list = list(set(ner_texts)) + ngram_df['Keywords'].drop_duplicates().tolist()
    keywords_df = pd.DataFrame(keywords_list, columns = ['Keywords'])
    
    merged = pd.merge(keywords_df, datas, on='Keywords', how='left')
    merged = merged.drop_duplicates()
    merged = merged.fillna('OTHER')
    merged['Labels_Keywords_combine'] = list(zip(merged.Keywords.tolist(), merged.Labels.tolist()))
    
    merged = pd.merge(merged, count_df, on='Keywords', how='left')
    merged = merged.fillna(4, downcast='infer')
    merged.drop('Tags', axis=1, inplace = True)
    #merged = merged.sort_values('Noun_Count', ascending=False).reset_index(drop=True)
    return merged
            

# generate keywords using flashtext
def add_ngrams(val):
    global kp
    # flashtext processor
    kp = KeywordProcessor()

    for row in val.iterrows():
        kp.add_keyword(row[1][0], row[1][1])
    return


def get_keyword(corpus):
    return(kp.extract_keywords(corpus, span_info=True))

app = Flask(__name__)

def get_sentiment(sentence):
    sentiment = []
    doc = nlp(sentence)
    blob = TextBlob(sentence)
    if blob.sentiment.polarity < 0:
    	status = "NEGATIVE"
    elif blob.sentiment.polarity == 0:
    	status = "NEUTRAL"
    else:
    	status = "POSITIVE"
    sentiment.append(("Entire Document", status))
    for sent in doc.sents:
        blob = TextBlob(sent.text)
        if blob.sentiment.polarity < 0:
            status = "NEGATIVE"
        elif blob.sentiment.polarity == 0:
            status = "NEUTRAL"
        else:
            status = "POSITIVE"
        sentiment.append((sent.text, status))
    return(sentiment)


# function to calculate ngram_count
def count(val):
    return len(val.split())


def noun_count(val):
    count = 0
    for item in val.split():
        if item[0] == 'N':
            count += 1
    return count


def create_corpus(val):
    global sentence
    global corpus
    if val[0] in sentence:
        corpus = corpus.append({'keyword': val[0], 'label_keyword_combine': val}, ignore_index=True)
        sentence = sentence.replace(val[0], "*")


@app.route('/keywords' , methods = ['POST'])
def api_call():
    try:
        val = re.sub(" +", " ", request.json['text']).strip()
        val = " ".join(val.split('\r\n'))
        print(val)
        nlp.tokenizer = custom_tokenizer(nlp)
        doc = nlp(val)
        global corpus
        corpus = pd.DataFrame(columns=['keyword', 'label_keyword_combine'])
        global sentence
        corpus_ = []
        sent_list_length = len(list(doc.sents))
        for index, sent in enumerate(list(doc.sents)):
            data = create_ngrams_df(str(sent))
            data = data[data.Tags.apply(filter_noun_adj)]
            if data.empty == True:
                corpus_.append(pd.DataFrame(columns=['keyword', 'label_keyword_combine']))
#                 print(pd.concat(corpus_, ignore_index=True))
                if corpus.empty == True and index == sent_list_length-1:
                    return json.dumps({'keywords' : []})
                continue
            #print(data) 
            data = data[data.Ngrams.apply(remove_punct)]
            #print(data)
            if len(ner_texts) != 0:
                data = data[data.Ngrams.apply(remove_Ngrams_ner_texts)]
            data['ngram_count'] = data['Tags'].apply(count)
            data['count'] = data['Tags'].apply(noun_count)
            #print(data)
            #print(ner_texts)
            print(ner_labels)
            #keywords_list = data.Ngrams.drop_duplicates().tolist() + list(set(ner_texts))
            log_df = generate_merged_df(ner_labels, ner_texts, data)
            sentence = str(sent)
            log_df.Labels_Keywords_combine.apply(create_corpus) #this line just provides us with the corpus df to input in keyword processor
            corpus_.append(corpus)
#         print(pd.concat(corpus_, ignore_index=True))
        add_ngrams(pd.concat(corpus_, ignore_index=True))
#         add_ngrams(corpus)
        keywords = []
        output  = []
        keywords = get_keyword(val)
        for keyword in keywords:
            body_structure = {
                    "name" : keyword[0][0],
                    "category" : keyword[0][1],
                    "start" : keyword[1],
                    "end" : keyword[2]
                }
            output.append(body_structure)
        log_structure = {
                "sentence" : val,
                "dataframe" : log_df['Labels_Keywords_combine'].tolist(),
                "response" : output
                }
        logFile = open("log.json", "a")
        print(json.dumps(log_structure), file=logFile)
        logFile.close()
        sentiment = []
        sentiments = get_sentiment(val)
        for item in sentiments:
            if item[0] != "Entire Document":
                body_structure = {
                        "sentence" : item[0],
                        "sentiment" : item[1]
                    }
                sentiment.append(body_structure)
            else:
                doc_sentiment = item[1]
                
        return json.dumps({'text' : val, 'keywords' : output, 'sentiment' : sentiment, 'doc_sentiment' : doc_sentiment})
    except Exception as e:
        return json.dumps({'error' : str(e)})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

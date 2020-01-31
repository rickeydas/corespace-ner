![CoreSpace NER](https://raw.githubusercontent.com/rickeydas/corespace-ner/master/assets/logo.jpg)


# CoreSpace NER

> Named Entity Recognition for NLP.

> Extracts 24 standard named entities.

> Noun chunk extraction. (Tagged as : OTHER)

> Sentiment Analysis.

> REST API port **5002**.

> Built on top of TextBlob, CoreNLP & Spacy.

---

## Standard Entities

1. ORGANIZATION
2. PERSON
3. LOCATION
4. DATE
5. TIME
6. MONEY
7. CITY
8. STATE
9. COUNTRY
10. NATIONALITY
11. RELIGION
12. EVENT
13. EMAIL
14. URL
15. PRODUCT
16. WORK OF ART
17. LAW
18. LANGUAGE
19. ARCHITECTURE
20. PERCENT
21. TITLE
22. CRIMINAL CHARGE
23. IDEOLOGY
24. DURATION
25. OTHER


---

## Example

```
=== INPUT ===
{"text":"Ramesh Jha, born in a Indian middle class family on 12-06-1991 (Monday), has finally got his scholarship of $10000 from London School of Economics. He is going to reach London after 1 month. In future, he wants to be a CEO of his own venture. You can reach him at rameshjha@lse.edu or rameshjha.com."}


=== OUTPUT ===
{
  "text": "Ramesh Jha, born in a Indian middle class family on 12-06-1991 (Monday), has finally got his scholarship of $10000 from London School of Economics. He is going to reach London after 1 month. In future, he wants to be a CEO of his own venture. You can reach him at rameshjha@lse.edu or rameshjha.com.",
  "keywords": [
    {
      "name": "Ramesh Jha",
      "category": "PERSON",
      "start": 0,
      "end": 10
    },
    {
      "name": "middle class",
      "category": "IDEOLOGY",
      "start": 29,
      "end": 41
    },
    {
      "name": "family",
      "category": "OTHER",
      "start": 42,
      "end": 48
    },
    {
      "name": "12-06-1991",
      "category": "DATE",
      "start": 52,
      "end": 62
    },
    {
      "name": "Monday",
      "category": "DATE",
      "start": 64,
      "end": 70
    },
    {
      "name": "scholarship",
      "category": "OTHER",
      "start": 93,
      "end": 104
    },
    {
      "name": "$10000",
      "category": "MONEY",
      "start": 108,
      "end": 114
    },
    {
      "name": "London School of Economics",
      "category": "ORGANIZATION",
      "start": 120,
      "end": 146
    },
    {
      "name": "London",
      "category": "CITY",
      "start": 169,
      "end": 175
    },
    {
      "name": "1 month",
      "category": "DURATION",
      "start": 182,
      "end": 189
    },
    {
      "name": "future",
      "category": "DATE",
      "start": 194,
      "end": 200
    },
    {
      "name": "CEO",
      "category": "TITLE",
      "start": 219,
      "end": 222
    },
    {
      "name": "own venture",
      "category": "OTHER",
      "start": 230,
      "end": 241
    },
    {
      "name": "rameshjha@lse.edu",
      "category": "EMAIL",
      "start": 264,
      "end": 281
    },
    {
      "name": "rameshjha.com",
      "category": "URL",
      "start": 285,
      "end": 298
    }
  ],
  "sentiment": [
    {
      "sentence": "Ramesh Jha, born in a Indian middle class family on 12-06-1991 (Monday), has finally got his scholarship of $10000 from London School of Economics.",
      "sentiment": "NEUTRAL"
    },
    {
      "sentence": "He is going to reach London after 1 month.",
      "sentiment": "NEUTRAL"
    },
    {
      "sentence": "In future, he wants to be a CEO of his own venture.",
      "sentiment": "POSITIVE"
    },
    {
      "sentence": "You can reach him at rameshjha@lse.edu or rameshjha.com.",
      "sentiment": "NEUTRAL"
    }
  ],
  "doc_sentiment": "POSITIVE"
}
```

---

## Docker

- Coming soon.

---

## Installation


### Requirements

- Java 8 or greater.
- Python 3.6 or greater.

### Setup

> Fire up a Terminal :

```shell
# Install Spacy and EN model.
$ sudo pip3 install -U spacy
$ sudo python3 -m spacy download en_core_web_sm

# Clone the repo.
$ git clone https://github.com/rickeydas/corespace-ner.git
$ cd corespace-ner

# Download CoreNLP.
$ wget "http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip"
$ unzip stanford-corenlp-full-2018-10-05.zip && mv stanford-corenlp-full-2018-10-05 stanford_corenlp

# Run CoreNLP server.
$ cd stanford_corenlp
$ nohup java -cp "*" -mx4g edu.stanford.nlp.pipeline.StanfordCoreNLPServer &

# Run corespace_ner api.
$ cd ..
$ nohup python3 corespace_ner.py &
```
---

## Rest API parse text.

```
http://<ip_address>:5002/keywords
Method : POST
Accept / Content_type : application/json
Data : {"text": "<your_text>"}
```
---

## Support

Reach out to me at one of the following places!

- <a href="https://www.linkedin.com/in/rickeydas/" target="_blank">`LinkedIn`</a>
- <a href="karam.shine@gmail.com" target="_blank">`Email`</a>
- <a href="http://www.github.com/rickeydas" target="_blank">`Github`</a>

---

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


- **[GNU General Public License](https://opensource.org/licenses/GPL-3.0)**

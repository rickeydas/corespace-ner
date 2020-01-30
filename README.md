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
{"text":"LetsEndorse is a social enterprise/digital collaborative ecosystem/NGO network headquartered in Bengaluru, India, which is in a mission to radicate the social issues like polio vactionation, healthcare, malnutrition, clean energy. Letsendorse was founded in 2014. Varun Kashyap is the Co-Founder of Letsendorse and the organisation has an estimated annual revenue of $7.9M."}


=== OUTPUT ===
{
  "text": "LetsEndorse is a social enterprise/digital collaborative ecosystem/NGO network headquartered in Bengaluru, India, which is in a mission to radicate the social issues like polio vactionation, healthcare, malnutrition, clean energy. Letsendorse was founded in 2014. Varun Kashyap is the Co-Founder of Letsendorse and the organisation has an estimated annual revenue of $7.9M.",
  "keywords": [
    {
      "name": "Letsendorse",
      "category": "PERSON",
      "start": 0,
      "end": 11
    },
    {
      "name": "social enterprise",
      "category": "OTHER",
      "start": 17,
      "end": 34
    },
    {
      "name": "digital collaborative ecosystem",
      "category": "OTHER",
      "start": 35,
      "end": 66
    },
    {
      "name": "NGO network",
      "category": "OTHER",
      "start": 67,
      "end": 78
    },
    {
      "name": "Bengaluru",
      "category": "LOCATION",
      "start": 96,
      "end": 105
    },
    {
      "name": "India",
      "category": "COUNTRY",
      "start": 107,
      "end": 112
    },
    {
      "name": "mission",
      "category": "OTHER",
      "start": 128,
      "end": 135
    },
    {
      "name": "social issues",
      "category": "OTHER",
      "start": 152,
      "end": 165
    },
    {
      "name": "polio vactionation",
      "category": "OTHER",
      "start": 171,
      "end": 189
    },
    {
      "name": "healthcare",
      "category": "OTHER",
      "start": 191,
      "end": 201
    },
    {
      "name": "malnutrition",
      "category": "EVENT",
      "start": 203,
      "end": 215
    },
    {
      "name": "clean energy",
      "category": "OTHER",
      "start": 217,
      "end": 229
    },
    {
      "name": "Letsendorse",
      "category": "PERSON",
      "start": 231,
      "end": 242
    },
    {
      "name": "2014",
      "category": "DATE",
      "start": 258,
      "end": 262
    },
    {
      "name": "Varun Kashyap",
      "category": "PERSON",
      "start": 264,
      "end": 277
    },
    {
      "name": "the Co-Founder of Letsendorse",
      "category": "PRODUCT",
      "start": 281,
      "end": 310
    },
    {
      "name": "organisation",
      "category": "OTHER",
      "start": 319,
      "end": 331
    },
    {
      "name": "estimated annual revenue",
      "category": "OTHER",
      "start": 339,
      "end": 363
    },
    {
      "name": "$7.9M.",
      "category": "MONEY",
      "start": 367,
      "end": 373
    }
  ],
  "sentiment": [
    {
      "sentence": "LetsEndorse is a social enterprise/digital collaborative ecosystem/NGO network headquartered in Bengaluru, India, which is in a mission to radicate the social issues like polio vactionation, healthcare, malnutrition, clean energy.",
      "sentiment": "POSITIVE"
    },
    {
      "sentence": "Letsendorse was founded in 2014.",
      "sentiment": "NEUTRAL"
    },
    {
      "sentence": "Varun Kashyap is the Co-Founder of Letsendorse and the organisation has an estimated annual revenue of $7.9M.",
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

- Linkedin at <a href="http://www.linkedin.com/rickeydas" target="_blank">`rickeydas`</a>
- Email at <a href="karam.shine@gmail.com" target="_blank">`Karamjit Das`</a>
- Github at <a href="http://www.github.com/rickeydas" target="_blank">`Karamjit Das`</a>

---

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


- **[GNU General Public License](https://opensource.org/licenses/GPL-3.0)**

# Telegram Media Monitoring & Source Tracing System

A system for monitoring Telegram news channels, automatically collecting posts into a MySQL database, and identifying the original source of news using NLP (TF-IDF and cosine similarity).

The service must identify identical, similar, and paraphrased posts, illustrating how a specific topic, quote, or key narrative spreads across different sources.

Users should be able to input a phrase or quote.

Once submitted, the system must:

* find related publications;
* identify the earliest recorded mention;
* build a timeline of its spread;
* measure and display text similarity levels;

The main goal of the project is to provide straightforward answers to the following questions:

* "Where did this first appear?"
* "Who shared/amplified it afterward?"
* "How similar are the publications?"
* "When did the main wave start?"
* "Has this information surfaced before?"
* "Which sources were involved in the spread?"

---

## 📌 Key Features

* **Automatic Ingestion:** Monitoring and parsing posts from a specified list of Telegram channels via the Telethon API.
* **Natural Language Processing (NLP):** Cleaning text of links and special characters, and filtering out Ukrainian stop words.
* **Source Identification:** Analyzing the similarity of news posts using `TfidfVectorizer` and `cosine_similarity`.
* **Dissemination Analysis:** Tracking the chronology of news reposts and calculating the time lag between publications.
* **Data Storage:** Storing channels, posts, search queries, and matches in MySQL.

---

## 🛠️ Technology Stack

* **Programming language:** Python 3.10+
* **Database:** MySQL
* **Main libraries:**
  * `telethon` — works with the Telegram API
  * `scikit-learn` — TF-IDF vectorization and cosine similarity
  * `mysql-connector-python` — interacts with the MySQL database
  * `python-dotenv` — manages environment variables

---

## 📁 Project structure

```
.
├── main.py              # CLI interface for searching for news and identifying the original source
├── main_ingest.py       # Script for parsing posts from Telegram channels
├── db.py                # MySQL connection and SQL queries
├── text_matcher.py      # Logic for calculating text similarity (TF-IDF + Cosine Similarity)
├── nlp_utils.py         # Text preprocessing and stopword list
├── schema.sql           # MySQL database schema dump
├── requirements.txt     # Project dependencies
├── .env.example         # Environment variable template
└── README.md            # Project documentation
```


## 🚀 Installation and Setup
* 1. Cloning the repository

    git clone [https://github.com/your_nickname/repository_name.git](https://github.com/your_nickname/repository_name.git)
    cd repository_name

* 2. Setting up a virtual environment

    * Creating a virtual environment

    python -m venv venv

    * Activating the environment:
        * For Windows:
            venv\Scripts\activate
        * For macOS/Linux:
            source venv/bin/activate

    * Installing dependencies
    pip install -r requirements.txt

* 3. Deploying the Database
    Create a database in MySQL and import the schema from the schema.sql file:

    mysql -u root -p < schema.sql

* 4. Configuring Environment Variables
    Create a .env file based on the .env.example template:

    cp .env.example .env

    Fill in the .env file with your data:

    TG_API_ID=your_telegram_api_id
    TG_API_HASH=your_telegram_api_hash
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=your_mysql_password
    DB_NAME=media_monitorings

    Note: You can obtain the TG_API_ID and TG_API_HASH values from the official portal at my.telegram.org.

## 💻 Usage

* 1. Collecting Data from Telegram
    To parse the latest messages from the channels you’re tracking, run:

    python main_ingest.py

    The first time you run it, Telethon will ask you to enter your phone number and the verification code from Telegram for authorization.

* 2. Searching for the Original Source of a News Story
    To verify a news story and find the channel that first published it, run:

    python main.py

    Enter the text of the news story or a quote into the command line. The program will display:

    The original source found (channel, publication time in UTC, percentage match).

    A timeline of dissemination (who reposted the news and how many minutes/hours later).
# Seraphina (Chatbot with Contextual Memory and Entity-Based Response Generation)
Seraphina project is part of a training course for intermediate level developers and also aimed at those who want to gain practical experience . 
Seraphina is an intelligent chatbot designed to create seamless, human-like conversations through the power of Artificial Intelligence (AI) and Natural Language Processing (NLP). Built to deliver insightful and contextually aware responses, Seraphina leverages MySQL for maintaining contextual memory, allowing it to save, recall, and respond accurately based on conversational history. This feature ensures continuity, relevance, and a personalized interaction experience, ideal for applications like customer service, telecom information assistance, and FAQ support
# Features
Contextual Memory: Stores and recalls user intents and entities for contextually appropriate responses .
Entity & Intent Detection: Detects and processes user input entities (e.g., "price," "CEO") and intents (e.g., "ask price," "inquire CEO") .
Spelling Correction: Enhances understanding through automatic spelling corrections and entity normalization .
Dynamic Response Generation: Provides dynamic responses based on detected entities and conversational history .
Comparison and Retrieval Functions: Retrieves specific information such as comparing plans or checking entity details (e.g., service offers) .

# Skills Used
Python Programming: Core language for development and logic.
Database Management: MySQL setup and SQL for contextual storage and retrieval.
NLP: Processing user input, entity normalization, and similarity matching.
Data Handling: String processing, tokenization, and data cleansing.
Error Handling: Implemented robust error handling for reliable user experience.

# Feature Implementation Breakdown
Database Connectivity: Establishes and maintains a connection to a MySQL database for storing and retrieving intents and entities, using mysql.connector.
Entity Normalization: Standardizes user input to match a predefined list of entities, utilizing fuzzywuzzy for similarity checks and unidecode for character standardization.
**Contextual Memory:**
Save Intent and Entities: Functions to save the user’s intent and entities from each interaction.
Retrieve Context: Enables the chatbot to recall the previous conversation’s context if missing in the current query.
Response Generation:
Comparison-Based Responses: Generates comparative messages based on detected entities.
General Message Generation: Forms responses using available information, contextual data, and predefined templates.
Error Handling and Logging: Error checks in database operations and interactions to ensure stability and track issues.

# Project Structure
.
├── data/
│   └── corr.txt                  # Spelling correction dictionary .
├── main.py                        # Main file with chatbot logic and database connection .
├── imports.py                     # Import configurations . 
├── models_config.py               # Configuration for models . 
├── db_config.py                   # MySQL database configurations . 
└── README.md                      # Project README file . 

main.py: Core of the chatbot logic, handling entity processing, context saving, and response generation.
imports.py: Manages necessary imports for the project.
models_config.py: Configurations related to model or intent classification settings.
db_config.py: Contains the configuration settings for connecting to the MySQL database.
data/corr.txt: A text file with common misspellings and their corrections, used to improve entity recognition.

# Technologies
Programming Language: `Python`
Database: `MySQL`
Natural Language Processing: `fuzzywuzzy` for entity matching, `unidecode` for text standardization.
Database Connector: `mysql.connector` for Python-MySQL connection.

# Installation and Setup
1- **Clone the Repository:**
`git clone https://github.com/mohamedelghazali/chatbot-contextual-memory.git`
`cd chatbot-contextual-memory` 
2- **Set up the MySQL Database:**
Create a MySQL database for storing intents and entities.
Update `db_config.py` with your MySQL connection details:

`db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'database': 'your_database'
}
`
3- **Install Required Python Packages:**
pip install -r requirements.txt
`pip install -r requirements.txt`
4- **Prepare Spelling Correction File:**
Edit `data/corr.txt` to include commonly misspelled words for your use case.
5- **Run the Chatbot:**
`python main.py`

The bot will connect to your MySQL database and be ready to process user input with contextual memory!





from imports import *
from models_config import *
from db_config import *
import mysql.connector
import ast
import re
from fuzzywuzzy import fuzz, process
from unidecode import unidecode

# Database connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
print("Connected to the MySQL database!")

# ----------- Helper functions for processing entities and intents -----------

def convert(entities):
    """Converts entities using predefined conversion constants."""
    new_entities = []
    for ent in entities:
        new_entities.append(constants.CONVERSIONS.get(ent.lower(), ent.lower()))
    return new_entities

def insert_query_gen(attributes):
    """Generates an SQL insert query with the provided attributes."""
    query = "INSERT INTO conversations (" + ", ".join(attributes) + ") VALUES (" + ", ".join(["%s"] * len(attributes)) + ")"
    return query

def save_message(attributes, values, cursor):
    """Saves a message in the database."""
    query = insert_query_gen(attributes)
    cursor.execute(query, values)

def correct_spelling(entities_single_words, user_text, spacy_nlp):
    """Corrects spelling in user text based on an NLP model and similarity threshold."""
    doc = spacy_nlp(user_text)
    filtered_tokens = [
        token.text for token in doc
        if not (token.is_stop or token.like_num or token.is_digit or token.pos_ == "VERB")
    ]
    text = user_text
    for word in filtered_tokens:
        if utils.full_process(word):
            token, score = process.extract(word, entities_single_words)[0]
            if score >= 70:
                text = text.replace(word, token)
    confidence = fuzz.token_set_ratio(text, user_text)
    return text, confidence

def correct_entities(user_text, entities):
    """Corrects entities in the user text based on identified entities."""
    entity_values = convert(entities)
    for i, ent in enumerate(entities):
        user_text = user_text.replace(ent, entity_values[i])
    return user_text

def spelling_correction(user_input):
    """Corrects spelling based on replacements defined in the file."""
    for original_word_pattern, corrected_word in replacements.items():
        user_input = re.sub(original_word_pattern, corrected_word, user_input)
    return user_input

def read_file(file_name):
    """Reads and parses a spelling correction file."""
    with open(file_name, "r", encoding="utf-8") as file:
        return ast.literal_eval(file.read())

# Load spelling corrections
replacements = read_file("./data/corr.txt")

def text_clean(text):
    """Cleans and standardizes text."""
    text = unidecode(str(text).lower())
    return re.sub(r"[^A-Za-z0-9\s\']", " ", text)

# ----------- Functions to save and retrieve conversation context -----------

def save_intent(intent, cursor, conn):
    """Saves the intent in the database."""
    intent = intent[0] if isinstance(intent, list) and intent else intent
    cursor.execute("DELETE FROM intents")  # Clear previous intents
    cursor.execute("INSERT INTO intents (intent) VALUES (%s)", (intent,))
    conn.commit()
    print(f"Saved intent: {intent}")

def save_entities(entities, cursor, conn):
    """Saves entities in the database and displays saved entities."""
    cursor.execute("DELETE FROM entities")  # Clear previous entities
    for entity in entities:
        cursor.execute("INSERT INTO entities (entity) VALUES (%s)", (entity,))
    conn.commit()
    print(f"Saved entities: {entities}")

def get_last_intent(cursor):
    """Retrieves the last saved intent from the database."""
    cursor.execute("SELECT intent FROM intents ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    return result[0] if result else None

def get_last_entities(cursor):
    """Retrieves the last saved entities from the database."""
    cursor.execute("SELECT entity FROM entities")
    return [row[0] for row in cursor.fetchall()]

def save_context(pred_class, entities, cursor, conn):
    """Saves intent and entities in the database."""
    if pred_class:
        save_intent(pred_class, cursor, conn)
    if entities:
        save_entities(entities, cursor, conn)
    print(f"Context saved: Intent = {pred_class}, Entities = {entities}")

def retrieve_context_if_missing(pred_class, entities, cursor):
    """Retrieves missing context from a previous question if the current context is incomplete."""
    return (get_last_entities(cursor) if not entities else entities, get_last_intent(cursor) if not pred_class else pred_class)

# ----------- Example of Closing the Connection -----------

def close_connection():
    """Closes the database connection and cursor."""
    cursor.close()
    conn.close()

# ----------- Example Functions for Generating Responses -----------

def generate_general_message(entities):
    """Generates a general message based on entities."""
    return ''.join(constants.GENERAL_ANSWERS_DICT.get(ent, '') for ent in entities)

def generate_comparison_message(entities, labels):
    """Generates a comparison message based on entities."""
    msg = ""
    for ent in entities:
        if ent in constants.PRICES:
            offer = constants.PRICES[ent][-1 if "COMPARE_PLUS" in labels else 0]
            msg += f"<p> - The {'highest' if 'COMPARE_PLUS' in labels else 'lowest'} offer for {ent} is {offer['name']} at {offer['price']} DA.</p>\n"
    return msg

def detect_ceo_intent(entities, labels):
    """Checks if the question implies a CEO-related entity or intent."""
    ceo_entities = {"ceo", "president", "director"}
    return any(ent.lower() in ceo_entities for ent in entities) or "ceo_query" in labels

def handle_ceo_response():
    """Generates a standard response for CEO-related questions."""
    CEO_NAME = "Adel Bentoumi"
    return f"The current CEO of Algeria Telecom is {CEO_NAME}, known for his efforts to modernize the company."

# ----------- Example of Context and Response Testing -----------

# Test saving and retrieving context
save_context("offer", ["internet", "adsl"], cursor, conn)
entities, pred_class = retrieve_context_if_missing(None, [], cursor)
print(f"Retrieved context: Intent = {pred_class}, Entities = {entities}")

# Test CEO response
response = handle_ceo_response()
print("CEO response:", response)

# Close connection after operations
close_connection()

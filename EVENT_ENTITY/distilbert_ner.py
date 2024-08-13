import nltk
import pandas as pd
from transformers import pipeline

# Download necessary NLTK data
nltk.download('punkt')

# Load and tokenize the content
with open("../Content.txt", "r") as file:
    content = file.read()

sentences = nltk.sent_tokenize(content)

# Load a pre-trained model for Named Entity Recognition (NER)
nlp = pipeline("ner", model="dslim/bert-base-NER")

# Extract events from the text
events_dict = {}
for sentence in sentences:
    entities = nlp(sentence)
    event = ""
    events = []
    for entity in entities:
        if entity['entity'].startswith("B-") or entity['entity'].startswith("I-"):
            if entity['word'].startswith("##"):
                event += entity['word'][2:]  # Remove the '##' prefix and continue the word
            else:
                if event:
                    events.append(event)
                event = entity['word']  # Start a new event word
    if event:  # Catch any remaining event word
        events.append(event)

    # Combine events and save in a dictionary
    if sentence in events_dict:
        events_dict[sentence].extend(events)
    else:
        events_dict[sentence] = events

# Convert the dictionary to a DataFrame
df = pd.DataFrame([
    {"Sentence": sentence, "Event": ", ".join(set(events))} 
    for sentence, events in events_dict.items()
])

# Save the DataFrame to an Excel file
df.to_excel("extracted_events.xlsx", index=False)

print("Events extracted and saved to extracted_events_grouped.xlsx")

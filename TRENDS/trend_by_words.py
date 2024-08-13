import os
import spacy
import pandas as pd

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

# Path to the Trends.txt file
file_name = 'Trend.txt'

# Directory containing the text file (current working directory)
directory = os.getcwd()

# Keywords related to trends
trend_keywords = [
    'trend', 'increase', 'decrease', 'growth', 'decline',
    'upward', 'downward', 'fall', 'rise', 'surge', 'drop',
    'escalation', 'reduction', 'spike', 'plunge', 'gain',
    'loss', 'progress', 'regression', 'expansion', 'contraction',
    'improvement', 'deterioration', 'advance', 'retreat',
    'upturn', 'downturn', 'boost', 'slump', 'peak', 'trough'
]

# Function to analyze trends based on keywords using spaCy
def analyze_trends(text):
    found_keywords = {}
    doc = nlp(text)
    for keyword in trend_keywords:
        matches = []
        for sent in doc.sents:
            if keyword in sent.text.lower():
                matches.append(sent.text)
        if matches:
            found_keywords[keyword] = matches
    return found_keywords

# Process the file to analyze trends
trends_data = []
file_path = os.path.join(directory, file_name)
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    trends = analyze_trends(text)
    if trends:
        for keyword, contexts in trends.items():
            for context in contexts:
                trends_data.append({'File': file_name, 'Keyword': keyword, 'Context': context})
    else:
        trends_data.append({'File': file_name, 'Keyword': 'None', 'Context': 'No trend-related keywords found'})
else:
    print(f"File not found: {file_path}")

# Convert the results to a DataFrame
df_trends = pd.DataFrame(trends_data)

# Save results to Excel
df_trends.to_excel('trend_analysis.xlsx', index=False)

# Print a summary of trends
print(df_trends)

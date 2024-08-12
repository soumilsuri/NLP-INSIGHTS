import os
import pandas as pd
from keybert import KeyBERT

# Initialize KeyBERT model
kw_model = KeyBERT()

# List of text files to process
file_names = [
    'Content1.txt',
    'Content2.txt',
    'Content3.txt',
    'Content4.txt',
    'Content5.txt',
    # 'Content6.txt',
    # 'Content7.txt',
    # 'Content8.txt',
    # 'Content9.txt',
    # 'Content10.txt'
]

# Directory containing text files (current working directory)
directory = os.getcwd()

# Function to extract key phrases from a text file
def extract_key_phrases(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')
    return keywords

# Process specified text files and collect key phrases
all_keywords = {}
for file_name in file_names:
    file_path = os.path.join(directory, file_name)
    if os.path.exists(file_path):
        keywords = extract_key_phrases(file_path)
        all_keywords[file_name] = keywords
    else:
        print(f"File not found: {file_path}")

# Convert key phrases to DataFrame
keyword_data = []
for file_name, keywords in all_keywords.items():
    for keyword, score in keywords:
        keyword_data.append({'File': file_name, 'Keyword': keyword, 'Score': score})

df_keywords = pd.DataFrame(keyword_data)

# Pivot table to get scores of each keyword across files
pivot_df = df_keywords.pivot_table(index='Keyword', columns='File', values='Score', fill_value=0)

# Calculate score change and trends
pivot_df['Score_Change'] = pivot_df.filter(like='.txt').diff(axis=1).sum(axis=1)
pivot_df['Trend'] = pivot_df['Score_Change'].apply(lambda x: 'Up' if x > 0 else ('Down' if x < 0 else 'Stable'))

# Save results to Excel
pivot_df.to_excel('keyword_trends.xlsx')

# Print trends
print(pivot_df[['Score_Change', 'Trend']])

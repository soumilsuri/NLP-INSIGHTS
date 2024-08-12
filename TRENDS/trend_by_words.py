import os
import re
import pandas as pd

# List of text files to process
file_names = [
    'Content1.txt',
    'Content2.txt',
    'Content3.txt',
    'Content4.txt',
    'Content5.txt',
]

# Directory containing text files (current working directory)
directory = os.getcwd()

# Keywords related to trends
trend_keywords = ['trend', 'increase', 'decrease', 'growth', 'decline', 'upward', 'downward', 'fall', 'rise']

# Function to analyze trends based on keywords
def analyze_trends(text):
    found_keywords = {}
    for keyword in trend_keywords:
        # Search for keyword and context (a few words before and after)
        pattern = rf'\b(?:\w+\W+){0,3}{keyword}(?:\W+\w+){0,3}\b'
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found_keywords[keyword] = matches
    return found_keywords

# Process each file to analyze trends
trends_data = []
for file_name in file_names:
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

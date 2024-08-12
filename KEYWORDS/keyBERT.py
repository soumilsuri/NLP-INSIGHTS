from keybert import KeyBERT
import pandas as pd

# Initialize KeyBERT model
keybert_model = KeyBERT('sentence-transformers/all-MiniLM-L6-v2')

# Read the content from the text file
with open('../Content.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Extract keywords
keywords_with_scores = keybert_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=20)

# Create a dictionary to keep track of the highest score for each unique keyword/phrase
unique_keywords_dict = {}
for score, keyword in keywords_with_scores:
    if keyword not in unique_keywords_dict or score > unique_keywords_dict[keyword]:
        unique_keywords_dict[keyword] = score

# Convert dictionary to a list of tuples (score, keyword)
unique_keywords_with_scores = [(score, keyword) for keyword, score in unique_keywords_dict.items()]

# Sort by score in descending order (optional)
unique_keywords_with_scores.sort(reverse=True, key=lambda x: x[0])

# Print extracted keywords in terminal
print("Unique keywords extracted using KeyBERT:")
for score, keyword in unique_keywords_with_scores:
    print(f"{keyword}: {score}")

# Save keywords to Excel file
df = pd.DataFrame(unique_keywords_with_scores, columns=['Score', 'Keyword'])
df.to_excel('keywords_keybert_unique.xlsx', index=False)

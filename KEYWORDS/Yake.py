import yake
import pandas as pd

# Initialize YAKE extractor
yake_extractor = yake.KeywordExtractor()

# Read the content from the text file
with open('../Content.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Extract keywords
keywords_with_scores = yake_extractor.extract_keywords(text)

# Ensure unique keywords (YAKE should already provide unique keywords, but let's ensure this)
unique_keywords_dict = {}
for keyword, score in keywords_with_scores:
    if keyword not in unique_keywords_dict or score > unique_keywords_dict[keyword]:
        unique_keywords_dict[keyword] = score

# Convert dictionary to a list of tuples (score, keyword)
unique_keywords_with_scores = [(score, keyword) for keyword, score in unique_keywords_dict.items()]

# Sort by score in descending order (optional)
unique_keywords_with_scores.sort(reverse=True, key=lambda x: x[0])

# Print extracted keywords in terminal
print("Unique keywords extracted using YAKE:")
for score, keyword in unique_keywords_with_scores:
    print(f"{keyword}: {score}")

# Save keywords to Excel file
df = pd.DataFrame(unique_keywords_with_scores, columns=['Score', 'Keyword'])
df.to_excel('keywords_yake_unique.xlsx', index=False)

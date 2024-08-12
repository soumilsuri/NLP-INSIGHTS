from rake_nltk import Rake
import pandas as pd

# Initialize RAKE
rake = Rake()

# Read the content from the text file
with open('../Content.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Extract keywords
rake.extract_keywords_from_text(text)
keywords_with_scores = rake.get_ranked_phrases_with_scores()

# Create a dictionary to keep track of the highest score for each unique phrase
unique_keywords_dict = {}
for score, keyword in keywords_with_scores:
    if keyword not in unique_keywords_dict or score > unique_keywords_dict[keyword]:
        unique_keywords_dict[keyword] = score

# Convert dictionary to a list of tuples (score, keyword)
unique_keywords_with_scores = [(score, keyword) for keyword, score in unique_keywords_dict.items()]

# Sort by score in descending order (optional)
unique_keywords_with_scores.sort(reverse=True, key=lambda x: x[0])

# Print extracted keywords in terminal
print("Unique keywords extracted using RAKE:")
for score, keyword in unique_keywords_with_scores:
    print(f"{keyword}: {score}")

# Save keywords to Excel file
df = pd.DataFrame(unique_keywords_with_scores, columns=['Score', 'Keyword'])
df.to_excel('keywords_rake_unique.xlsx', index=False)

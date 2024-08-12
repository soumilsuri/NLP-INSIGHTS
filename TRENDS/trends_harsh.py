import pandas as pd
from rake_nltk import Rake
import nltk

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Initialize RAKE
rake = Rake()

# Define trend categories and associated keywords
trend_categories = {
    "up": ["growth", "increase", "expansion", "demand", "profit", "revenue"],
    "down": ["decline", "decrease", "drop", "loss", "cut", "reduction"],
    "stable": ["steady", "constant", "unchanged", "stable", "consistent"]
}

# Define a function to determine trend based on keywords
def determine_trend(keyword):
    keyword_lower = keyword.lower()
    for trend, keywords in trend_categories.items():
        if any(trend_keyword in keyword_lower for trend_keyword in keywords):
            return trend
    return "stable"  # Default to stable if no match

# Read the content from the text file
with open('../Content.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Extract keywords using RAKE
rake.extract_keywords_from_text(text)
keywords_with_scores = rake.get_ranked_phrases_with_scores()

# Create a dictionary to keep track of the highest score for each unique phrase
unique_keywords_dict = {}
for score, keyword in keywords_with_scores:
    if keyword not in unique_keywords_dict or score > unique_keywords_dict[keyword]:
        unique_keywords_dict[keyword] = score

# Convert dictionary to a list of tuples (score, keyword)
unique_keywords_with_scores = [(score, keyword) for keyword, score in unique_keywords_dict.items()]

# Sort by score in descending order
unique_keywords_with_scores.sort(reverse=True, key=lambda x: x[0])

# Print extracted keywords
print("Top 10 keywords extracted using RAKE:")
for score, keyword in unique_keywords_with_scores[:10]:
    print(f"{keyword}: {score}")

def generate_trend_insights(keywords):
    trends = []
    for keyword in keywords:
        trend = determine_trend(keyword)
        trends.append((keyword, trend))
    return trends

# Generate trend insights
top_keywords = [keyword for _, keyword in unique_keywords_with_scores[:10]]  # Top 10 keywords
trends = generate_trend_insights(top_keywords)

# Print the trend insights
print("\nTrend Insights:")
for keyword, trend in trends:
    print(f"{keyword}: Trend is {trend}")

# Save trend insights to a text file
with open('trend_insights.txt', 'w') as f:
    for keyword, trend in trends:
        f.write(f"{keyword}: Trend is {trend}\n")
print("\nTrend insights saved to 'trend_insights.txt'.")

# Save insights to Excel file
trends_df = pd.DataFrame(trends, columns=['Keyword', 'Trend'])
trends_df.to_excel('trend_insights.xlsx', index=False)
print("Trend insights also saved to 'trend_insights.xlsx'.")

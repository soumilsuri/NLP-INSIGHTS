import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import pandas as pd

# Load pre-trained model and tokenizer
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForSequenceClassification.from_pretrained(model_name)

# Read the content from the text file
with open('../Content.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Define maximum sequence length for the model
max_length = tokenizer.model_max_length

# Tokenize text and split into chunks if necessary
def analyze_sentiment(text, model, tokenizer, max_length):
    sentiments = []
    chunk_info = []
    stride = max_length // 2
    
    for start in range(0, len(text), stride):
        end = start + max_length
        chunk = text[start:end]
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=max_length, padding='max_length')
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sentiment_scores = predictions.numpy().flatten()
        sentiment_avg = sentiment_scores.mean()
        
        chunk_info.append({
            'Chunk Start': start,
            'Chunk End': end,
            'Chunk Text': chunk,  # Add text of the chunk
            'Positive Score': sentiment_scores[1],
            'Negative Score': sentiment_scores[0],
            'Average Sentiment': sentiment_avg
        })
        
        sentiments.append(sentiment_scores)

    # Calculate average sentiment score for each class and overall average
    positive_scores = [score[1] for score in sentiments]
    negative_scores = [score[0] for score in sentiments]
    
    avg_positive_score = sum(positive_scores) / len(positive_scores)
    avg_negative_score = sum(negative_scores) / len(negative_scores)
    
    # Determine overall average sentiment
    avg_scores = {
        'Positive': avg_positive_score,
        'Negative': avg_negative_score
    }
    overall_sentiment = max(avg_scores, key=avg_scores.get)

    return avg_scores, overall_sentiment

# Analyze sentiment
average_scores, overall_sentiment = analyze_sentiment(text, model, tokenizer, max_length)

# Convert results to DataFrame and save to Excel
df = pd.DataFrame([{
    'Average Positive Score': average_scores['Positive'],
    'Average Negative Score': average_scores['Negative'],
    'Overall Sentiment': overall_sentiment
}])

df.to_excel('average_sentiment_analysis_distilbert.xlsx', index=False)

print("Average Sentiment Analysis Results saved to 'average_sentiment_analysis_distilbert.xlsx'.")

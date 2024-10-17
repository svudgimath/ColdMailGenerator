from textblob import TextBlob

def analyze_sentiment(email_text):
    """
    Analyze the sentiment and tone of the generated email.
    Returns the polarity and subjectivity of the email.
    Polarity ranges from [-1, 1], where -1 is negative and 1 is positive.
    Subjectivity ranges from [0, 1], where 0 is objective and 1 is subjective.
    """
    blob = TextBlob(email_text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Determine tone based on polarity
    if polarity > 0:
        tone = "positive"
    elif polarity < 0:
        tone = "negative"
    else:
        tone = "neutral"
    
    return polarity, subjectivity, tone
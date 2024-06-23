from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

def sentiment_analyzer():
    df = pd.read_csv(r'C:\\Users\\bonag\\Desktop\\pdata.csv')
    stop_words = set(stopwords.words('english'))
    df['review'] = df['review'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

    sia = SentimentIntensityAnalyzer()
    df['polarity'] = df['review'].apply(lambda x: sia.polarity_scores(x)['compound'])

    df['label'] = df['polarity'].apply(lambda x: 'positive' if x >= 0 else 'negative')

    X_train, X_test, y_train, y_test = train_test_split(df['review'], df['label'], test_size=0.2, random_state=42)

    vectorizer = TfidfVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    rf_classifier = RandomForestClassifier()
    rf_classifier.fit(X_train_vectorized, y_train)

    y_pred = rf_classifier.predict(X_test_vectorized)

    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    df['prediction'] = rf_classifier.predict(vectorizer.transform(df['review']))
    df_sorted = df.sort_values(by='polarity', ascending=False)

    top_reviews = df_sorted.head(3)['review'].tolist()

    return top_reviews, accuracy, cm

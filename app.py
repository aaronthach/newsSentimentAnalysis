# api key: eefd40be6df94883b5b53e4233e406dc

# import re
# import requests
# import streamlit as st
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import nltk
#
# # Download the VADER lexicon (if you haven't already)
# nltk.download('vader_lexicon')
#
# # Initialize the VADER SentimentIntensityAnalyzer
# vader_analyzer = SentimentIntensityAnalyzer()
#
#
# class NewsClient:
#     '''
#     Generic News Class for sentiment analysis using VADER.
#     '''
#
#     def __init__(self, api_key):
#         '''
#         Class constructor or initialization method.
#         '''
#         self.api_key = api_key
#         self.base_url = "https://newsapi.org/v2/everything"
#
#     def clean_text(self, text):
#         '''
#         Utility function to clean text by removing links, special characters using simple regex statements.
#         '''
#         return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
#
#     def get_text_sentiment_vader(self, text):
#         '''
#         Use VADER for sentiment analysis. Returns positive, negative, or neutral sentiment based on compound score.
#         '''
#         sentiment_score = vader_analyzer.polarity_scores(self.clean_text(text))['compound']
#         if sentiment_score >= 0.05:
#             return 'positive'
#         elif sentiment_score <= -0.05:
#             return 'negative'
#         else:
#             return 'neutral'
#
#     def get_news(self, query, count=10):
#         '''
#         Main function to fetch news articles and parse them.
#         '''
#         articles = []
#         try:
#             # Fetch news articles
#             params = {
#                 'q': query,
#                 'apiKey': self.api_key,
#                 'pageSize': count
#             }
#             response = requests.get(self.base_url, params=params)
#             if response.status_code == 200:
#                 news_data = response.json()
#                 for article in news_data.get('articles', []):
#                     # Extract title and description
#                     title = article.get('title', '')
#                     description = article.get('description', '')
#                     content = title + " " + description
#                     url = article.get('url', '')
#
#                     # Debug: Check if the article has content
#                     if not content.strip() or (article.get('title') == '[Removed]'):
#                         continue
#
#                     # Analyze sentiment using VADER
#                     sentiment_vader = self.get_text_sentiment_vader(content)
#                     articles.append({
#                         'title': title,
#                         'description': description,
#                         'sentiment_vader': sentiment_vader,
#                         'url': url
#                     })
#             else:
#                 print(f"Error: {response.status_code}")
#             return articles
#         except Exception as e:
#             print(f"Error occurred: {e}")
#             return None
#
#
# def main():
#     # Replace with your News API key
#     API_KEY = "eefd40be6df94883b5b53e4233e406dc"
#
#     # Set up the Streamlit interface
#     st.title("News Sentiment Analysis Dashboard")
#     query = st.text_input("Enter search query", "Technology")
#     count = st.slider("Number of articles to analyze", min_value=5, max_value=20, value=10, step=1)
#
#     if st.button('Fetch and Analyze News'):
#         # Create NewsClient object
#         news_client = NewsClient(api_key=API_KEY)
#
#         # Fetch and analyze news
#         articles = news_client.get_news(query=query, count=count)
#
#         if articles is None or len(articles) == 0:
#             st.error("No articles found or an error occurred.")
#             return
#
#         # Categorize articles by sentiment (only VADER)
#         positive_articles_vader = [article for article in articles if article['sentiment_vader'] == 'positive']
#         negative_articles_vader = [article for article in articles if article['sentiment_vader'] == 'negative']
#         neutral_articles_vader = [article for article in articles if article['sentiment_vader'] == 'neutral']
#
#         total_articles = len(articles)
#
#         # Display sentiment analysis results for VADER
#         st.subheader("VADER Sentiment Analysis Results:")
#         st.write(f"Positive articles: {100 * len(positive_articles_vader) / total_articles:.2f}%")
#         st.write(f"Negative articles: {100 * len(negative_articles_vader) / total_articles:.2f}%")
#         st.write(f"Neutral articles: {100 * len(neutral_articles_vader) / total_articles:.2f}%")
#
#         # Display articles based on sentiment (for VADER)
#         if len(positive_articles_vader) > 0:
#             st.subheader("Articles with Positive Sentiment:")
#             for article in positive_articles_vader[:5]:
#                 st.markdown(f"[{article['title']}]({article['url']})")
#                 st.write(f"- {article['description'] or 'No description available.'}")
#
#         if len(negative_articles_vader) > 0:
#             st.subheader("Articles with Negative Sentiment:")
#             for article in negative_articles_vader[:5]:
#                 st.markdown(f"[{article['title']}]({article['url']})")
#                 st.write(f"- {article['description'] or 'No description available.'}")
#
#         if len(neutral_articles_vader) > 0:
#             st.subheader("Articles with Neutral Sentiment:")
#             for article in neutral_articles_vader[:5]:
#                 st.markdown(f"[{article['title']}]({article['url']})")
#                 st.write(f"- {article['description'] or 'No description available.'}")
#
#
# if __name__ == "__main__":
#     main()

import re
import requests
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from datetime import datetime, timedelta

# Download the VADER lexicon (if you haven't already)
nltk.download('vader_lexicon')

# Initialize the VADER SentimentIntensityAnalyzer
vader_analyzer = SentimentIntensityAnalyzer()


class NewsClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"

    def clean_text(self, text):
        return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

    def get_text_sentiment_vader(self, text):
        sentiment_score = vader_analyzer.polarity_scores(self.clean_text(text))['compound']
        if sentiment_score >= 0.05:
            return 'positive'
        elif sentiment_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'

    def get_news(self, query, count=10, from_date=None, to_date=None):
        articles = []
        try:
            params = {
                'q': query,
                'apiKey': self.api_key,
                'pageSize': count,
                'from': from_date,  # Optional: Date filter (from_date)
                'to': to_date  # Optional: Date filter (to_date)
            }
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                news_data = response.json()
                for article in news_data.get('articles', []):
                    title = article.get('title', '')
                    description = article.get('description', '')
                    content = title + " " + description
                    url = article.get('url', '')
                    if not content.strip() or (article.get('title') == '[Removed]'):
                        continue
                    sentiment_vader = self.get_text_sentiment_vader(content)
                    articles.append({
                        'title': title,
                        'description': description,
                        'sentiment_vader': sentiment_vader,
                        'url': url
                    })
            else:
                print(f"Error: {response.status_code}")
            return articles
        except Exception as e:
            print(f"Error occurred: {e}")
            return None


# Custom CSS for aesthetics
def set_custom_css():
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(to bottom, #f5f7fa, #c3cfe2);
            font-family: Arial, sans-serif;
        }
        .stButton>button {
            color: #4CAF50;
            border-radius: 8px;
        }
        .stButton>button:hover {
            color: white;
        }
        .sentiment-header {
            font-size: 24px;
            color: #333333;
        }
        .article {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
            background-color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .expander {
            font-size: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def add_vertical_space(space=1):
    """Adds vertical space in the Streamlit app."""
    for _ in range(space):
        st.markdown("<br>", unsafe_allow_html=True)


def main():
    API_KEY = "eefd40be6df94883b5b53e4233e406dc"

    set_custom_css()
    st.title("📊 News Sentiment Analysis Dashboard using VADER")
    st.write("This interactive dashboard allows users to fetch and analyze up to 20 of the most relevant news articles in the specified date range based on a custom search query. By leveraging VADER (Valence Aware Dictionary for sEntiment Reasoning), it classifies articles as positive, negative, or neutral based on their content. Users can specify the number of articles to display and the sentiment categories are visually presented with percentages. Articles are displayed with their titles and descriptions, and users can click to read the full article.")

    add_vertical_space(2)

    # Search query and number of articles
    query = st.text_input("Enter search query", "Technology")

    # Date range input (default: last 7 days)
    today = datetime.today()
    one_month_ago = today - timedelta(days=30)
    from_date = st.date_input("From date", one_month_ago)
    to_date = st.date_input("To date", today)

    if st.button('Fetch and Analyze News'):
        news_client = NewsClient(api_key=API_KEY)
        articles = news_client.get_news(query=query, count=20, from_date=from_date, to_date=to_date)

        if articles is None or len(articles) == 0:
            st.error("No articles found or an error occurred.")
            return

        positive_articles = [a for a in articles if a['sentiment_vader'] == 'positive']
        negative_articles = [a for a in articles if a['sentiment_vader'] == 'negative']
        neutral_articles = [a for a in articles if a['sentiment_vader'] == 'neutral']
        total_articles = len(articles)

        add_vertical_space(2)

        st.markdown("### Sentiment Analysis Results")
        st.write(f"**Positive articles:** {100 * len(positive_articles) / total_articles:.2f}% ✅")
        st.write(f"**Negative articles:** {100 * len(negative_articles) / total_articles:.2f}% ❌")
        st.write(f"**Neutral articles:** {100 * len(neutral_articles) / total_articles:.2f}% ⚠️")

        add_vertical_space(2)  # Add space before displaying articles

        def display_articles(articles, sentiment_label):
            st.markdown(f"### {sentiment_label} Articles")
            add_vertical_space(1)  # Add space before each category
            for article in articles:
                with st.expander(article['title']):
                    st.markdown(f"[Read full article here]({article['url']})")
                    st.write(article['description'] or "No description available.")
            add_vertical_space(2)  # Add space after each category

        if positive_articles:
            display_articles(positive_articles, "Positive")
        if negative_articles:
            display_articles(negative_articles, "Negative")
        if neutral_articles:
            display_articles(neutral_articles, "Neutral")


if __name__ == "__main__":
    main()
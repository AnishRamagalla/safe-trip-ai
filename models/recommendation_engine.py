from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_safe_countries(user_input, df):
    tfidf = TfidfVectorizer()
    descriptions = df["country"].tolist()
    tfidf_matrix = tfidf.fit_transform(descriptions+[user_input])
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    top_indices = similarity_scores[0].argsort()[-5:][::-1]
    return df.iloc[top_indices]
    
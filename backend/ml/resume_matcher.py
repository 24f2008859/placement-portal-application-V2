from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_match_score(student_text, job_text):
    documents = [student_text, job_text]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    score = similarity[0][0]
    percentage = round(score * 100, 2)

    return percentage 

if __name__ == '__main__':
    score = compute_match_score("Python Flask SQL", "Python Django SQL")
    print(f"Match score: {score}%")
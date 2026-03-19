from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class PropertyRecommender:
    def __init__(self):
        self.tfidf = TfidfVectorizer(stop_words='english')

    def recommend(self, current_property_id, properties_data):
        """
        properties_data: List of dicts [{'property_id': 1, 'description': '...', 'location': '...'}, ...]
        """
        if not properties_data:
            return []

        # Combine features for similarity
        # We use description and location
        data_text = [f"{p['location']} {p['property_type']} {p.get('description', '')}" for p in properties_data]
        
        tfidf_matrix = self.tfidf.fit_transform(data_text)
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        
        # Find index of current property
        idx = -1
        for i, p in enumerate(properties_data):
            if p['property_id'] == current_property_id:
                idx = i
                break
        
        if idx == -1:
            return []

        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6] # Top 5 similar, skip self (index 0)
        
        property_indices = [i[0] for i in sim_scores]
        return [properties_data[i] for i in property_indices]

recommender = PropertyRecommender()

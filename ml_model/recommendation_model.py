import math
from collections import Counter

class PropertyRecommender:
    def __init__(self):
        pass

    def _get_tokens(self, text):
        return set(text.lower().split())

    def _cosine_similarity(self, text1, text2):
        # A simple keyword-based cosine similarity instead of full Tfidf
        vec1 = Counter(self._get_tokens(text1))
        vec2 = Counter(self._get_tokens(text2))
        
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        return float(numerator) / denominator

    def recommend(self, current_property_id, properties_data):
        if not properties_data:
            return []

        # Find current property details
        current_prop = next((p for p in properties_data if p['property_id'] == current_property_id), None)
        if not current_prop:
            return []

        current_text = f"{current_prop['location']} {current_prop['property_type']} {current_prop.get('description', '')}"
        
        scores = []
        for p in properties_data:
            if p['property_id'] == current_property_id:
                continue
            
            p_text = f"{p['location']} {p['property_type']} {p.get('description', '')}"
            score = self._cosine_similarity(current_text, p_text)
            scores.append((p, score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return [p[0] for p in scores[:5]]

recommender = PropertyRecommender()

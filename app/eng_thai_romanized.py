from pythainlp.transliterate import romanize
from lingua import Language, LanguageDetectorBuilder

class NameMatcher:
    def __init__(self, confidence=50):
        self.confidence = confidence
        self.detector = LanguageDetectorBuilder.from_languages(Language.THAI, Language.ENGLISH).build()

    def detect_language(self, text):
        return self.detector.detect_language_of(text)
    
    def romanize_thai(self, thai_text):
        return romanize(thai_text, "thai2rom")

    def compute_matching_score(self, to_check_name, true_name):
        match_count = 0
        true_name_list = list(true_name.lower())
        print(true_name_list)
        for char in to_check_name.lower():
            if char in true_name_list:
                match_count += 1
                true_name_list.remove(char)
        return (match_count/len(true_name)) *100

    def compare_names(self, to_check_name, true_name):
        lang_to_check = self.detect_language(to_check_name)
        lang_true_name = self.detect_language(true_name)

        # If `to_check_name` is thai it need to romanized and check with `true_name` which is in English
        if lang_to_check == Language.THAI and lang_true_name == Language.ENGLISH:
            romanized_to_check = self.romanize_thai(to_check_name)
            match_score = self.compute_matching_score(romanized_to_check, true_name)
        # If `to_check_name` if it's both Thai just compare
        elif lang_to_check == Language.THAI and lang_true_name == Language.THAI:
            match_score = self.compute_matching_score(to_check_name, true_name)
        # If both is in English, jsut compare
        elif lang_to_check == Language.ENGLISH and lang_true_name == Language.ENGLISH:
            match_score = self.compute_matching_score(to_check_name, true_name)
        else:
            return {"error": "Uneexpected language combination"}
        
        # Check that it's more than confidence
        is_match = match_score >= self.confidence
        if lang_to_check == Language.THAI:
            return {
                "to_check_th_romanized": romanized_to_check,
                "is_match": is_match,
                "match_score": match_score
            }
        else:
            return {
                "is_match": is_match,
                "match_score": match_score
            }

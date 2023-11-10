from enum import Enum, auto

class MatchingMode(Enum):
    NORMAL = auto()
    LEVENSHTEIN = auto()

import re
from pythainlp.transliterate import romanize
from typing import Optional
from lingua import Language, LanguageDetectorBuilder
from Levenshtein import distance as levenshtein_distance


class NameMatcher:
    def __init__(self, confidence: int=50, mode=MatchingMode.NORMAL):
        self.confidence = confidence
        self.mode = mode
        self.detector = LanguageDetectorBuilder.from_languages(Language.THAI, Language.ENGLISH).build()

    def detect_language(self, text: str) -> Optional[Language]:
        return self.detector.detect_language_of(text)
    
    def romanize_thai(self, thai_text: str):
        return romanize(thai_text, "thai2rom")

    @property
    def matching_mode(self):
        return self.mode
    
    @matching_mode.setter
    def matching_mode(self, mode):
        if not isinstance(mode, MatchingMode):
            raise ValueError("Invalid mode. Must be an instance of MatchingMode")
        self.mode = mode

    def text_normalizer(self, text: str):
        text = text.lower()
        text = re.sub(r'\W+', '', text)
        return text
    
    def compute_matching_score(self, name1, name2):
        if self.mode == MatchingMode.NORMAL:
            return self._normal_matching_score(name1,name2)
        elif self.mode == MatchingMode.LEVENSHTEIN:
            return self._levenshtein_matching_score(name1, name2)
        
    def _normal_matching_score(self, name1, name2):
        match_count = 0
        name2_list = list(name2)
        for char in name1:
            if char in name2_list:
                match_count += 1
                name2_list.remove(char)
        return (match_count/len(name2)) *100

    def _levenshtein_matching_score(self, name1, name2):
        lev_distance = levenshtein_distance(name1, name2)
        longest_word_length = max(len(name1), len(name2))
        return (1-lev_distance/ longest_word_length) * 100

    def compare_names(self, name1, name2):
        lang_name1 = self.detect_language(name1)
        lang_name2 = self.detect_language(name2)

        if lang_name1 == lang_name2:
            match_score = self.compute_matching_score(name1, name2)
        else:
            if lang_name1 == Language.THAI:
                romanized_name1 = self.text_normalizer(self.romanize_thai(name1))
                normalized_name2 = self.text_normalizer(name2)
                print(romanized_name1)
                match_score = self.compute_matching_score(romanized_name1, normalized_name2)
            elif lang_name2 == Language.THAI:
                romanized_name2 = self.text_normalizer(self.romanize_thai(name2))
                normalized_name1 =  self.text_normalizer(name1)
                print(romanized_name2)
                match_score = self.compute_matching_score(romanized_name2, normalized_name1)

        is_match = match_score >= self.confidence
        return {
            "name1_romanized" : name1 if lang_name1 == Language.THAI else None,
            "name2_romanized" : name2 if lang_name2 == Language.THAI else None,
            "is_match": is_match,
            "match_score": match_score
        }
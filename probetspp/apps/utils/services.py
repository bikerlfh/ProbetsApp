import re
import math
from collections import Counter


def get_similarity_text(
    first_text: str,
    second_text: str
) -> float:
    """
    compare the similarity between two texts
    https://stackoverflow.com/questions/38365389/
    compare-similarity-between-names
    """
    word_ = re.compile(r'\w+')
    first_text = first_text.strip().lower()
    second_text = second_text.strip().lower()
    vec1 = Counter(word_.findall(first_text))
    vec2 = Counter(word_.findall(second_text))

    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    return float(numerator) / denominator

import re
import numpy as np

def structural_features(text_series):
    features = []

    for text in text_series:
        text = str(text).lower()

        has_link = int(bool(re.search(r'http[s]?://', text)))
        has_google_form = int("forms.gle" in text)
        urgency_words = len(re.findall(r'urgent|immediate|final|act now|limited|deadline|expire|last chance|registration link|apply now', text))
        money_words = len(re.findall(r'cash|profit|earn|loan|refund|prize|bonus|investment|payment|stipend|scholarship|referral|fee|training fee|stipend-based', text))
        authority_words = len(re.findall(r'government|bank|rbi|aicte|court|income tax|ministry|nasscom|official|admin|capgemini|inspire leap|hr|hiring|aenexz|vel tech|ibm|microsoft|wipro|mnc', text))
        exclamation_count = text.count("!")

        features.append([
            has_link,
            has_google_form,
            urgency_words,
            money_words,
            authority_words,
            exclamation_count
        ])

    return np.array(features)

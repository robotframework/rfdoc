def get_keyword_names(keywords):
    return keywords[1:-1].replace(' and ', ', ').split('", "')
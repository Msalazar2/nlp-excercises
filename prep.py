def basic_clean(text):
    
    text = text.lower()
    
    text = unicodedata.normalize('NFKD', text)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    
    text = re.sub(r"[^a-z0-9'\s]", '', text)
    
    return text


def tokenize(text):
    
    tokenizer = nltk.tokenize.ToktokTokenizer()

    text = tokenizer.tokenize(text, return_str=True)
    
    return text


def stem(text):
    
    ps = nltk.porter.PorterStemmer()
    
    stems = [ps.stem(word) for word in text.split()]
    
    text_stemmed = ' '.join(stems)
    
    return text_stemmed


def lemmatize(text):
    
    wnl = nltk.stem.WordNetLemmatizer()
    
    lemmas = [wnl.lemmatize(word) for word in text.split()]
    
    text_lemmatized = ' '.join(lemmas)

    return text_lemmatized


def remove_stopwords(text, extra_words = None, exclude_words = None):
    
    stopword_list = stopwords.words('english')
    
    if exclude_words is not None:
        
        for w in exclude_words:
        
            stopword_list.remove(w)
    
    if extra_words is not None:
        
        for w in extra_words:
        
            stopword_list.append(w)
    
    words = text.split()
    
    filtered_words = [w for w in words if w not in stopword_list]

    print('Removed {} stopwords'.format(len(words) - len(filtered_words)))
    print('---')

    text_without_stopwords = ' '.join(filtered_words)

    return text_without_stopwords
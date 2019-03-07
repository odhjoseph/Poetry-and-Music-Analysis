


def get_lda_from_lists_of_words(lists_of_words, **kwargs):
    from gensim import corpora, models
    import pandas as pd
    dictionary = corpora.Dictionary(lists_of_words) # this dictionary maps terms to integers
    dictionary.filter_extremes(no_below=10, no_above=0.2)
    corpus = [dictionary.doc2bow(text) for text in lists_of_words] # create a bag of words from each document
    tfidf = models.TfidfModel(corpus) # this models the significance of words by document
    corpus_tfidf = tfidf[corpus]
    kwargs["id2word"] = dictionary # set the dictionary
    lda_model = models.LdaModel(corpus_tfidf, **kwargs)
    def get_topics(words): 
        return dict(lda_model[dictionary.doc2bow(words)])
    topics_df = pd.DataFrame(get_topics(text) for text in lists_of_words).fillna(0.001)
    topics_df.columns = [str(cn) for cn in topics_df.columns]
    return lda_model, topics_df, dictionary, corpus

def format_topics_sentences(ldamodel, corpus, texts):
    # Init output
    import pandas as pd
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return sent_topics_df

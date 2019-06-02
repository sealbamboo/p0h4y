# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Show top n keywords for each topic
def show_topics(vectorizer=None, lda_model=None, n_words=20):
    keywords = np.array(vectorizer.get_feature_names())
    topic_keywords = []
    for topic_weights in lda_model.components_:
        top_keyword_locs = (-topic_weights).argsort()[:n_words]
        topic_keywords.append(keywords.take(top_keyword_locs))
    return topic_keywords


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Define function to predict topic for a given text document.
def predict_topic(text, nlp=None):
    global sent_to_words
    global lemmatization

    # Step 1: Clean with simple_preprocess
    mytext_2 = list(sent_to_words_by_single(text))
    #print(mytext_2)

    # Step 2: Lemmatize
    mytext_3 = lemmatization_by_single(mytext_2, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    #print(mytext_3)

    # Step 3: Vectorize transform
    mytext_4 = vectorizer.transform(mytext_3)
    #print(type(mytext_4))

    # Step 4: LDA Transform
    topic_probability_scores = best_lda_model.transform(mytext_4)
    print(topic_probability_scores, np.argmax(topic_probability_scores))
    
    # Get dominant topic for each document
    dominant_topic = np.argmax(df_document_topic.values, axis=1)
    
    topic = df_topic_keywords.iloc[np.argmax(topic_probability_scores), :].values.tolist()
    return topic, topic_probability_scores


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
def similar_documents(text, doc_topic_probs, documents = None, nlp=None, top_n=5, verbose=False):
    topic, x  = predict_topic(text)
    dists = euclidean_distances(x.reshape(1, -1), doc_topic_probs)[0]
    doc_ids = np.argsort(dists)[:top_n]
    if verbose:        
        print("Topic KeyWords: ", topic)
        print("Topic Prob Scores of text: ", np.round(x, 1))
        print("Most Similar Doc's Probs:  ", np.round(doc_topic_probs[doc_ids], 1))
    return doc_ids, np.take(documents, doc_ids)


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Plot
def plotting_clusters(x, y, clusters):
    plt.figure(figsize=(12, 12))
    plt.scatter(x, y, c=clusters)
    plt.xlabel('Component 2')
    plt.xlabel('Component 1')
    plt.title("Segregation of Topic Clusters", )
    

def test():
    doc_lens = [len(d) for d in frame['list_text'].values]

    # Plot
    plt.figure(figsize=(16,7), dpi=80)
    plt.hist(doc_lens, bins = 10000, color='navy')
    plt.text(880, 80, "Mean   : " + str(round(np.mean(doc_lens))))
    plt.text(880, 76, "Median : " + str(round(np.median(doc_lens))))
    plt.text(880, 72, "Stdev   : " + str(round(np.std(doc_lens))))
    plt.text(880, 68, "1%ile    : " + str(round(np.quantile(doc_lens, q=0.01))))
    plt.text(880, 64, "99%ile  : " + str(round(np.quantile(doc_lens, q=0.99))))

    plt.gca().set(xlim=(0, 1000), ylabel='Number of Documents', xlabel='Document Word Count')
    plt.tick_params(size=16)
    plt.xticks(np.linspace(0,1000,9))
    plt.title('Distribution of Document Word Counts', fontdict=dict(size=22))
    plt.show()
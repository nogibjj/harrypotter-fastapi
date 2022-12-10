import numpy as np
from random import choices
from collections import Counter


def generate_corpus(book_num):
    """
    This is to generate the corpus using Harry Potter Books Corpora

    Parameters:
        book_num(int) - Book Number, from 1-7

    Returns:
        A list with words in the selected book
    """
    filepath = "./Data/Book" + str(book_num) + ".txt"
    file1 = open(filepath, "r", encoding="utf-8")
    Lines = file1.readlines()

    word_list = []
    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        if len(line.strip()) < 2:
            continue
        if line.startswith("Page"):
            continue
        word_list.append(line.strip().split(" "))

    word_list = [w.lower() for words in word_list for w in words]
    return word_list


def generate_prob_matrix(n, corpus):
    """
    This is to generate the probability matrix of Hidden Markov Model

    Parameters:
        n(int) - n-gram
        corpus(list) - The corpus on which the generated text is based

    Returns:
        ngram_idx: index dictionary of ngrams
        word_idx: index dictionary of words
        p_matrix: probability matrix of the words of the n-grams
    """
    word_idx = {}
    w_idx = 0
    ngram_li = []
    ngram_idx = {}
    g_idx = 0

    # iterate each word in corpus
    for i in range(len(corpus)):

        # generate word index dictionary
        if corpus[i] not in word_idx:
            word_idx[corpus[i]] = w_idx
            w_idx += 1

        # generate ngrams and their index dictionary
        if i >= n - 1:
            gram = tuple(corpus[i + 1 - n : i + 1])
            ngram_li.append(gram)
            if gram[:-1] not in ngram_idx:
                ngram_idx[gram[:-1]] = g_idx
                g_idx += 1

    # calculate the probability matrix
    p_matrix = np.zeros((len(word_idx), len(ngram_idx)))

    for ngram in ngram_li:
        prefix = ngram[:-1]
        p_matrix[word_idx[ngram[-1]]][ngram_idx[prefix]] += 1

    p_matrix = p_matrix / np.sum(p_matrix, axis=0, keepdims=True)

    return ngram_idx, word_idx, p_matrix


def ngram_data(n, corpus):
    """
    Use stupid backoff, store from ngram to bigram

    Parameters:
        n(int) - n-gram
        corpus(list) - The corpus on which the generated text is based

    Returns:
        word_idx: index dictionary of words
        n_li: list of ngram number
        ngram_dict_li: list of the ngrams
        p_matrix_li: list of probability matrix
    """
    ngram_dict_li = []
    p_matrix_li = []
    n_li = []
    for j in range(n, 1, -1):
        n_li.append(j)
        ngram_idx, word_idx, p_matrix = generate_prob_matrix(j, corpus)
        ngram_dict_li.append(ngram_idx)
        p_matrix_li.append(p_matrix)
    return word_idx, n_li, ngram_dict_li, p_matrix_li


def unigram(corpus, deterministic=False):
    """
    Generate word with unigram mode.

    Parameters:
        corpus(list) - The corpus on which the generated text is based
        deterministic(bool) - If true, choose at each step the single most probable next token. Otherwise, generate randomly

    Returns:
        pred_word(string) - A predicted word
    """
    if deterministic:
        pred_word = Counter(corpus).most_common(1)[0][0]
    else:
        pred_word = choices(corpus)[0]
    return pred_word


def finish_sentence(sentence, n, corpus, text_length, deterministic=False):
    """
    Text generator

    Parameters:
        sentence(string) - Starting text to be generated
        n(int) - n-grams
        corpus(list) - The corpus on which the generated text is based
        text_length(int) - Length of text to be generated
    Returns:
        sentence

    """

    sentence = sentence.strip().split(" ")
    # if unigram
    if n == 1:
        while len(sentence) < text_length:
            pred_word = unigram(corpus, deterministic)
            sentence.append(pred_word)

    # not unigram
    else:
        word_idx, n_li, ngram_dict_li, p_matrix_li = ngram_data(n, corpus)

        # Begin text generation
        while len(sentence) < text_length:
            for k in range(len(n_li)):
                prefix = tuple(sentence[-n_li[k] + 1 :])
                gram_idx = ngram_dict_li[k].get(prefix)
                if gram_idx is not None:
                    break

            # Still no data for bigram: unigram
            if gram_idx is None:
                pred_word = unigram(corpus, deterministic)
            else:
                if deterministic:
                    pred_idx = np.argmax(p_matrix_li[k][:, gram_idx])
                else:
                    pred_idx = choices(
                        np.arange(len(word_idx)), p_matrix_li[k][:, gram_idx]
                    )[0]

                pred_word = [i for i in word_idx if word_idx[i] == pred_idx][0]

            sentence.append(pred_word)
    return " ".join(sentence)

"""
# Test text generator
if __name__ == "__main__":
    # This is a sample of using the text generator
    Sentence = "It is made of"  # sentence to start with
    N = 3  # ngram, number of words before to be considered. Better with 2-4
    Book_num = 1  # 1-7, but better with 1-3 because the book files were small
    Text_length = 100  # length of text to generate

    Corpus = generate_corpus(Book_num)
    ans = finish_sentence(Sentence, N, Corpus, Text_length)
    print(ans)
"""
import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    corpus = {}
    for f in os.scandir(directory):
        if f.is_file():
            corpus[f.name] = open(f.path, 'r', encoding="utf-8").read()
    return corpus


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.tokenize.word_tokenize(document.lower())
    i = 0
    while i < len(words):
        word = words[i]
        if word in nltk.corpus.stopwords.words("english"):
            words.remove(word)
            i -= 1
        else:
            j = 0
            while j < len(word):
                if word[j] in string.punctuation:
                    word = word[:j] + word[j+1:]
                    j -= 1
                j += 1
            if word == "":
                words.remove(words[i])
                i -= 1
            else:
                words[i] = word
        i += 1
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = {}
    # frequency
    for document in documents:
        for word in list(set(documents[document])):
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
    # idf
    for word in words:
        words[word] = math.log(len(documents) / words[word])
    return words


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidf = {}
    for file in files:
        tfidf[file] = 0
        for word in query:
            if word in files[file]:
                tfidf[file] += files[file].count(word) * idfs[word]
    return sorted(tfidf, key=tfidf.get, reverse=True)[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    mwm = {}
    qtd = {}
    for sentence in sentences:
        mwm[sentence] = 0
        qtd[sentence] = 0
        for word in query:
            if word in sentences[sentence]:
                mwm[sentence] += idfs[word]
                qtd[sentence] += 1
        qtd[sentence] /= len(sentence)
    return sorted(sorted(qtd, key=qtd.get, reverse=True), key=mwm.get, reverse=True)[:n]


if __name__ == "__main__":
    main()

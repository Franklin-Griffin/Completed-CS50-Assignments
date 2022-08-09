import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):

    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    mod = {}
    # outgoing links
    sites = corpus[page]
    # initial val
    damped = (1 - damping_factor) / len(corpus) if len(sites) != 0 else 1 / len(corpus)

    for i in corpus:
        mod[i] = damped

    if len(sites) != 0:
        for i in sites:
            mod[i] += damping_factor / len(sites)

    return mod
    

def sample_pagerank(corpus, damping_factor, n):

    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    ranks = {}
    trans = {}
    last = None

    for i in corpus:
        ranks[i] = 0
        trans[i] = transition_model(corpus, i, damping_factor)

    for s in range(n):
        rand = random.random()
        if last == None:
            # random
            for i in corpus:
                rand -= 1 / len(corpus)
                if rand <= 0:
                    last = i
                    ranks[i] += 1 / n
                    break

        else:
            # trans model
            for i in trans[last]:
                if i in trans[last]:
                    rand -= trans[last][i]
                    if rand <= 0:
                        last = i
                        ranks[i] += 1 / n
                        break
    
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {}
    # avoid changing ranks during calculation
    oldranks = {}
    change = True

    for i in corpus:
        ranks[i] = 1 / len(corpus)

    while change == True:
        change = False
        oldranks = ranks.copy()
        # change each page
        for page in corpus:
            summation = 0
            for link in corpus:
                if page in corpus[link]:
                    summation += oldranks[link] / len(corpus[link])
                elif len(corpus[link]) == 0:
                    summation += oldranks[link] / len(corpus)
            ranks[page] = ((1 - damping_factor) / len(corpus)) + summation * damping_factor
            if abs(ranks[page] - oldranks[page]) >= 0.001:
                change = True

    return oldranks


if __name__ == "__main__":
    main()

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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # number of pages present in the corpus
    num_of_pages = len(corpus)

    # number of out links for page
    num_of_links = len(corpus[page])

    # empty dic for the output distribution
    probability_distribution = {}

    # if the current page has no links, return random probability among all pages
    if not corpus[page]:
        return {p: 1 / num_of_pages for p in corpus}

    random_page_prob = (1 - damping_factor) / num_of_pages

    for page_read in corpus:
        probability = damping_factor * (1 / num_of_links)
        # we want to exclude the current page from the corpus
        if page_read not in corpus[page]:
            probability = 0
        # adding prob for choosing any page at random
        probability += random_page_prob
        probability_distribution[page_read] = probability

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize a dictionary to store the count of samples for each page
    page_count = {page: 0 for page in corpus}

    # Initial sample: choose a page at random
    current_sample = random.choice(list(corpus.keys()))

    # Generate n-1 additional samples
    for _ in range(n - 1):
        # Get the transition model for the current sample
        transition_probabilities = transition_model(
            corpus, current_sample, damping_factor
        )

        # Choose the next sample based on the transition model
        next_sample = random.choices(
            list(transition_probabilities.keys()),
            weights=list(transition_probabilities.values()),
        )[0]

        # Update the count for the current sample
        page_count[current_sample] += 1

        # Update the current sample for the next iteration
        current_sample = next_sample

    # Count the last sample
    page_count[current_sample] += 1

    # Normalize the counts to get PageRank estimates (proportions)
    pagerank_estimates = {page: count / n for page, count in page_count.items()}

    return pagerank_estimates


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize dictionaries to store old and new rank values
    previous_pagerank = {}
    current_pagerank = {}

    # Assigning each page a rank of 1/n, where n is the total number of pages in the corpus
    total_pages = len(corpus)
    for page in corpus:
        previous_pagerank[page] = 1 / total_pages

    # Repeatedly calculating new rank values based on all of the current rank values
    while True:
        for page in corpus:
            new_rank = 0

            # Iterate over all pages in the corpus
            for linking_page in corpus:
                # Check if the linking_page has a link to our page
                if page in corpus[linking_page]:
                    new_rank += previous_pagerank[linking_page] / len(
                        corpus[linking_page]
                    )

                # If linking_page has no links, interpret it as having one link for every other page
                if len(corpus[linking_page]) == 0:
                    new_rank += (previous_pagerank[linking_page]) / len(corpus)

            # Apply the PageRank formula
            new_rank *= damping_factor
            new_rank += (1 - damping_factor) / total_pages

            # Update the new rank value for the current page
            current_pagerank[page] = new_rank

        # Calculate the maximum difference between old and new rank values
        max_difference = max(
            [abs(current_pagerank[x] - previous_pagerank[x]) for x in previous_pagerank]
        )

        # Check for convergence
        if max_difference < 0.001:
            break
        else:
            # Update previous_pagerank with the new rank values
            previous_pagerank = current_pagerank.copy()

    return previous_pagerank


if __name__ == "__main__":
    main()

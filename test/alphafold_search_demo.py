import requests
import json


def search_alphafold_db(keywords, max_results=10):
    """
    Search AlphaFold Database using keywords

    Parameters:
    keywords (str): Search terms to query the database
    max_results (int): Maximum number of results to return (default: 10)

    Returns:
    dict: Search results in JSON format
    """
    # AlphaFold DB API endpoint
    # base_url = "https://www.ebi.ac.uk/proteins/api/proteins/search"
    base_url = f"https://www.ebi.ac.uk/proteins/api/proteins?keywords={keywords}"

    try:
        # Send GET request to AlphaFold DB API
        response = requests.get(base_url)

        # Parse JSON response
        results = response.content

        return results

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while searching AlphaFold DB: {e}")
        return None


def display_results(results):
    """
    Display search results in a formatted way
    """
    if not results or 'hits' not in results:
        print("No results found or invalid response")
        return

    print(f"\nFound {results['hits']['total']['value']} total matches")
    print(f"Showing top {len(results['hits']['hits'])} results:\n")

    for hit in results['hits']['hits']:
        entry = hit['_source']
        print(f"Entry ID: {entry.get('entry_id', 'N/A')}")
        print(f"UniProt ID: {entry.get('uniprot_accession', 'N/A')}")
        print(f"Description: {entry.get('uniprot_description', 'N/A')}")
        print(f"Organism: {entry.get('organism_scientific_name', 'N/A')}")
        print(f"Model URL: {entry.get('latest_model_url', 'N/A')}")
        print("-" * 50)


def main():
    # Get search keywords from user
    keywords = input("Enter search keywords: ")

    # Perform search
    results = search_alphafold_db(keywords)

    # Display results
    if results:
        display_results(results)
    else:
        print("Search failed. Please try again.")


if __name__ == "__main__":
    main()
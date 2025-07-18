import requests
from urllib.parse import urlparse, urlunparse
from concurrent.futures import ThreadPoolExecutor
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def format_url_enhanced(url: str) -> str:
    """Formats a URL to ensure it has a scheme (https) and a netloc (www. if not present).

    :param url: The input URL string.
    :returns: The formatted URL string.
    """
    parsed_url = urlparse(url)

    scheme = parsed_url.scheme if parsed_url.scheme else 'https'
    netloc = parsed_url.netloc
    path = parsed_url.path

    # No netloc found by urlparse, often means the whole string is the domain
    if not netloc:
        netloc = url # Treat the entire input URL as the netloc
        path = '' # clear the path
    else:
        # If netloc was found, but the path might still contain the netloc itself
        if path == netloc or path == '/' + netloc:
             path = '' # Clear path if it's redundant

    if not netloc.startswith('www.') and '.' in netloc:
        netloc = 'www.' + netloc

    # Reconstruct the URL
    formatted_url = urlunparse((scheme, netloc, path,
                                parsed_url.params, parsed_url.query,
                                parsed_url.fragment))
    return formatted_url

def check_connectivity(url: str, timeout: int = 5, retries: int = 2) -> dict:
    """Checks the connectivity of a given URL with retries.

    :param url: The URL to check.
    :param timeout: The maximum time to wait for a response in seconds.
    :param retries: The number of times to retry the request if it fails.
    :returns: A dictionary containing the URL, status, and an optional error message/status code.
    """
    original_url = url
    url = format_url_enhanced(url)

    for attempt in range(retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                logging.info(f"{url} is up. Status: {response.status_code}")
                return {"url": original_url, "status": "up", "status_code": response.status_code}
            else:
                logging.warning(f"{url} is down or not reachable. Status code: {response.status_code}")
                return {"url": original_url, "status": "down", "status_code": response.status_code}
        except requests.exceptions.Timeout:
            if attempt < retries:
                logging.warning(f"Timeout reaching {url}. Retrying ({attempt + 1}/{retries})...")
                time.sleep(1) # Small delay before retrying
            else:
                logging.error(f"Failed to reach {url} after {retries} retries: Timeout.")
                return {"url": original_url, "status": "down", "error": "Timeout"}
        except requests.exceptions.ConnectionError as e:
            if attempt < retries:
                logging.warning(f"Connection error for {url}. Retrying ({attempt + 1}/{retries})...")
                time.sleep(1)
            else:
                logging.error(f"Failed to reach {url} after {retries} retries: Connection Error - {e}")
                return {"url": original_url, "status": "down", "error": f"Connection Error: {e}"}
        except requests.exceptions.RequestException as e:
            if attempt < retries:
                logging.warning(f"An unexpected request error occurred for {url}. Retrying ({attempt + 1}/{retries})...")
                time.sleep(1)
            else:
                logging.error(f"Failed to reach {url} after {retries} retries: Unexpected Error - {e}")
                return {"url": original_url, "status": "down", "error": f"Unexpected Error: {e}"}
    return {"url": original_url, "status": "unknown", "error": "Reached end of retry loop without definite status."}


def check_websites_concurrently(urls: list[str]) -> list[dict]:
    """Checks a list of websites concurrently using a ThreadPoolExecutor.

    :param urls: A list of URL strings to check.
    :returns: A list of dictionaries, each representing the check result for a URL.
    """
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(check_connectivity, url): url for url in urls}

        for future in future_to_url:
            result = future.result() # block until the result is available
            results.append(result)
    return results

if __name__ == '__main__':
    websites_to_check = [
        "https://www.google.com",
        "github.com",
        "http://stackoverflow.com",
        "www.python.org",
        "nonexistentwebsite.example",
        "http://httpbin.org/status/500",
        "http://httpbin.org/delay/6"
    ]
    logging.info("Starting website connectivity checks...")
    check_results = check_websites_concurrently(websites_to_check)

    print("\n--- Connectivity Report ---")
    for result in check_results:
        if result["status"] == "up":
            print(f"✅ {result['url']} is UP (Status: {result.get('status_code', 'N/A')})")
        else:
            print(f"❌ {result['url']} is DOWN (Error: {result.get('error', 'N/A')}, Status: {result.get('status_code', 'N/A')})")
    logging.info("Finished website connectivity checks.")


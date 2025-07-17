import requests
import threading

def connectivity_checker(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"{url} is up.")
        else:
            print(f"{url} is down or not reachable. Status code is {response.status_code}.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to reach {url}. {e}")


def threading_url_checker(*args):
    threads = []

    for url in args:
        thread = threading.Thread(target=connectivity_checker, args=(url, ))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    websites_to_check = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.python.org",
    "https://nonexistentwebsite.example"
    ]
    threading_url_checker(*websites_to_check)

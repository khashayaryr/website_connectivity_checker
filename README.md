# 🌐 Website Availability Checker

A powerful and user-friendly web application built with Streamlit and Python for checking the real-time availability of multiple websites concurrently.

## ✨ Features

* **Concurrent Checks**: Leverages `ThreadPoolExecutor` for efficient, parallel checking of multiple website URLs.
* **Smart URL Formatting**: Automatically formats input URLs to ensure consistency (e.g., adds `https://` and `www.`).
* **Robust Error Handling**: Distinguishes between various network issues (timeouts, connection errors, HTTP status codes) and provides detailed feedback.
* **Interactive UI**:
    * Add and remove URLs dynamically.
    * Clear all URLs from the list.
    * One-click "Check All" functionality with a loading indicator.
    * Clear input field for ease of use.
    * Displays clear "Up" (✅) or "Down" (❌) status.
    * Provides detailed error messages and HTTP status codes for unavailable websites.
    * Persists URL list and check results using Streamlit's session state.
    * Shows the timestamp of the last check.


## 🚀 Installation

Make sure you have Python 3.8+ installed.   
Follow these steps to get the Website Availability Checker up and running on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/khashayaryr/website_connectivity_checker.git
    ```

2.  **Navigate to the project's root directory in your terminal:**
    ```bash
    cd website_connectivity_checker
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃 How to Run

To run the Streamlit application:

1.  **Add the current directory to your `PYTHONPATH` to ensure Python can find the `src` module:**
    ```bash
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    ```

2.  **Run the Streamlit application::**
    ```bash
    streamlit run src/app.py
    ```

## 📁 Project Structure
```
.
├── .gitignore                      # Specifies intentionally untracked files to ignore
├── LICENSE                         # MIT License
├── README.md                       # This file
├── requirements.txt                # Project dependencies
└── src/
    ├── app.py                      # Main Streamlit UI application
    └── connectivity_checker.py     # Contains core logic for URL formatting and connectivity checks
```

## 🛠️ Built With

* [Python](https://www.python.org/) - The programming language
* [Streamlit](https://streamlit.io/) - The web application framework
* [Requests](https://requests.readthedocs.io/) - HTTP library for Python
* [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) - For high-level interfaces for asynchronously executing callables

## 🤝 Contributing

Feel free to fork this repository and contribute! If you have suggestions for improvements or find any issues, please open an issue or submit a pull request.

## 📄 License

This project is open source and available under the [MIT License](https://github.com/khashayaryr/website_connectivity_checker/blob/main/LICENSE).

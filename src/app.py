import streamlit as st
import requests
from connectivity_checker import format_url_enhanced, check_websites_concurrently
import time

# Configuration
st.set_page_config(page_title="Website Availability Checker")

# Streamlit UI
def main():
    st.title("🌐 Website Availability Checker")
    st.markdown("Check the status of your favorite websites concurrently.")

    # Session State Initialization
    if 'urls' not in st.session_state:
        st.session_state.urls = []
    if 'check_results' not in st.session_state:
        st.session_state.check_results = {} # Store results as a dict: {formatted_url: result_dict}
    if 'last_checked_timestamp' not in st.session_state:
        st.session_state.last_checked_timestamp = None

    # Add URL Section
    st.header("Add a Website URL")
    new_url_input = st.text_input("Enter URL (e.g., google.com, https://www.github.com)",
                                  key="new_url_input",
                                  placeholder="https://example.com")

    col_add, col_clear_input = st.columns([1, 1])
    with col_add:
        if st.button("➕ Add URL", use_container_width=True):
            if new_url_input:
                formatted_url = format_url_enhanced(new_url_input)
                if formatted_url not in st.session_state.urls:
                    st.session_state.urls.append(formatted_url)
                    st.success(f"Added: `{formatted_url}`")
                    st.session_state.check_results = {} # Clear results when list changes
                    st.session_state.last_checked_timestamp = None
                else:
                    st.warning(f"URL `{formatted_url}` is already in the list.")
            else:
                st.warning("Please enter a URL to add.")
    with col_clear_input:
        # Clear the text input box after adding/error
        if st.button("Clear Input", use_container_width=True):
            st.session_state.new_url_input = "" # This clears the text_input widget
            st.experimental_rerun() # Rerun to reflect cleared input

    st.markdown("---")

    # List & Check Section
    st.header("Websites to Check")
    if not st.session_state.urls:
        st.info("No websites added yet. Use the input field above to add some.")
    else:
        # Display the list of URLs with remove buttons
        st.subheader("Current List:")
        cols_list_header = st.columns([0.8, 0.2])
        cols_list_header[0].markdown("**URL**")
        cols_list_header[1].markdown("**Action**",)

        for i, url in enumerate(st.session_state.urls):
            cols_list = st.columns([0.8, 0.2])
            with cols_list[0]:
                st.text(url)
            with cols_list[1]:
                if st.button("Remove", key=f"remove_{i}", use_container_width=True):
                    st.session_state.urls.pop(i)
                    st.session_state.check_results = {} # Clear results when list changes
                    st.session_state.last_checked_timestamp = None
                    st.experimental_rerun() # Rerun to update the list immediately

        st.markdown("---")

        col_check, col_clear_all = st.columns(2)
        with col_check:
            if st.button("🚀 Check All Websites", use_container_width=True):
                if st.session_state.urls:
                    with st.spinner("Checking websites... This may take a moment."):
                        # Call the backend function
                        raw_results = check_websites_concurrently(st.session_state.urls)

                        # Store results in a dictionary for easy lookup by URL
                        st.session_state.check_results = {r['url']: r for r in raw_results}
                        st.session_state.last_checked_timestamp = time.time()
                    st.success("Check complete!")
                else:
                    st.warning("No URLs in the list to check. Please add some first.")

        with col_clear_all:
            if st.button("🗑️ Clear All Websites", use_container_width=True):
                st.session_state.urls.clear()
                st.session_state.check_results = {} # Clear results when list changes
                st.session_state.last_checked_timestamp = None
                st.success("All URLs cleared from the list.")
                st.experimental_rerun() # Rerun to update UI immediately

        # Display Results
        if st.session_state.check_results:
            st.header("Connectivity Report")
            if st.session_state.last_checked_timestamp:
                st.info(f"Last checked: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.session_state.last_checked_timestamp))}")

            # Create a header row for results
            cols_results_header = st.columns([0.3, 0.2, 0.5]) # URL | Status | Details
            cols_results_header[0].markdown("**URL**")
            cols_results_header[1].markdown("**Status**")
            cols_results_header[2].markdown("**Details**")
            st.markdown("---") # Visual separator for headers

            for url_in_list in st.session_state.urls:
                result = st.session_state.check_results.get(url_in_list)
                if result:
                    cols_results = st.columns([0.4, 0.1, 0.5])
                    with cols_results[0]:
                        st.text(url_in_list)
                    with cols_results[1]:
                        if result["status"] == "up":
                            st.markdown("✅ Up")
                        else:
                            st.markdown("❌ Down")
                    with cols_results[2]:
                        if result["status"] == "up":
                            st.write(f"Status: {result.get('status_code', 'N/A')}")
                        else:
                            error_msg = result.get('error', 'Unknown error')
                            status_code = result.get('status_code', 'N/A')
                            st.write(f"Status: {status_code}, Error: {error_msg}")
                else:
                    # This case should ideally not happen if logic is tight, but good for robustness
                    st.text(f"{url_in_list} (Not yet checked or result missing)")

if __name__ == "__main__":
    main()
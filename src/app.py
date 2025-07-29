import streamlit as st
import requests
from connectivity_checker import format_url_enhanced, check_websites_concurrently



# Streamlit UI
def main():
    st.title("Website Availability Checker")

    # Session state to store the list of URLs
    if 'urls' not in st.session_state:
        st.session_state.urls = []

    st.markdown("Enter a URL to add to the list:")
    col1, col2 = st.columns(2)
    with col1:
        new_url = st.text_input("URL", label_visibility="collapsed")

    with col2:
        # Button to add the URL with formatted URL
        if st.button("Add URL"):
            formatted_url = format_url_enhanced(new_url)
            if formatted_url not in st.session_state.urls and new_url != "":
                st.session_state.urls.append(formatted_url)


    col1, col2 = st.columns(2)
    with col1:
        results = []
        if st.button("Check All"):
            results = check_websites_concurrently(st.session_state.urls)

    with col2:
        if st.button("Clear List"):
            st.session_state.urls.clear()


    st.markdown("## Websites to be checked:")
    col1, col2 = st.columns([4,1])
    with col1:
        st.markdown("### URL")
        for url in st.session_state.urls:
            st.write(url)
    with col2:
        st.markdown("### Status")
        for result in results:
            if result["status"] == "up":
                st.write(f"✅")
            else:
                st.write(f"❌")

if __name__ == "__main__":
    main()
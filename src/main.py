from config.settings import APP_TITLE

import streamlit as st


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="🍽️", layout="wide")
    st.title(APP_TITLE)
    st.write("A preference-driven restaurant recommender powered by structured data and LLM reasoning.")

    st.info("Phase 0 scaffold is ready. The recommendation pipeline will be implemented in later phases.")


if __name__ == "__main__":
    main()

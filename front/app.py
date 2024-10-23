import streamlit as st
from client.client import SQLAgentClient


APP_TITLE = "SQL Agent"
APP_ICON = "🔍"


def main():
    client = SQLAgentClient()
    st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON)
    st.title(APP_TITLE)
    
    question = st.text_input("**Question:**")

    if st.button("Submit"):
        if question:
            response = client.query(question)
            if answer := response.get("answer"):
                st.success(f"{answer}")
            elif error_message := response.get("error_message"):
                st.error(f"{error_message}")
        else:
            st.warning("Please enter a question.")


if __name__ == "__main__":
    main()

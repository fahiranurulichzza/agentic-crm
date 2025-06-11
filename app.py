try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except (ImportError, KeyError):
    pass

import streamlit as st
from crewai import Agent, Task, Crew, Process
from modules.agent import SalesAnalystAgent
from modules.output_handler import capture_output
import os
import re

OUTPUT_PATH = "output/"


def main():
    st.title("AI Sales Analysis Assistant")
    st.write("Ask questions about sales analysis, CRM, and business insights")

    # Initialize the SalesAnalystAgent
    analyst = SalesAnalystAgent()
    crew = analyst.create_crew()

    # Create a text input for user questions
    user_question = st.text_input("Enter your question:")

    start_research = st.button(
        "🚀 Start Research", use_container_width=False, type="primary")

    if start_research:
        with st.status("🤖 Researching...", expanded=True) as status:
            process_container = st.container(border=True)
            output_container = process_container.container()

            with capture_output(output_container):
                result = crew.kickoff(inputs={'question': user_question})

                status.update(label="✅ Research completed!",
                              state="complete", expanded=False)

    markdown_files = [f for f in os.listdir(
        OUTPUT_PATH) if f.endswith(('.md', '.markdown'))]

    if not markdown_files:
        st.warning("No Markdown files found in the specified folder.")
    else:
        # Create a dropdown to select a Markdown file
        selected_file = st.selectbox(
            "Choose a Markdown file", markdown_files)

    markdown_files = [f for f in os.listdir(
        OUTPUT_PATH) if f.endswith(('.md', '.markdown'))]

    # Read and display the selected file
    file_path = os.path.join(OUTPUT_PATH, selected_file)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
            markdown_content = re.sub(
                r'^```markdown\n|\n```$', '', markdown_content, flags=re.MULTILINE)

        st.markdown(markdown_content, unsafe_allow_html=False)
    except Exception as e:
        st.error(f"Error reading {selected_file}: {str(e)}")


if __name__ == "__main__":
    main()

import streamlit as st

from ingestion import extract_pages
from search import answer_question
from chunker import create_chunks
from embedding import embed
from similarity_finder import find_similar_chunks

# -----------------------------
# Page title
# -----------------------------

st.title("Document RAG Assistant")


# -----------------------------
# PDF upload
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)


# -----------------------------
# Only show question section
# after PDF is uploaded
# -----------------------------

if uploaded_file:

    # PDF filename
    pdf_title = uploaded_file.name

    st.subheader("Document")

    st.write(pdf_title)

    # Read uploaded PDF
    pdf_file = uploaded_file.getvalue()

    # Extract pages
    pages = extract_pages(pdf_file)

    # Display page count
    st.write("Pages extracted:", len(pages))


    # -----------------------------
    # Question section
    # -----------------------------

    st.subheader("Ask a Question")

    question = st.text_input(
        "Enter your question:"
    )


    # -----------------------------
    # Ask button
    # -----------------------------

    if st.button("Ask"):

        if not question.strip():

            st.error("Please enter a question.")

        else:

            with st.spinner(
                "Searching document and generating answer..."
            ):

                c1 = create_chunks(pages)
                e1 = embed(c1)
                s_c = find_similar_chunks(question, c1, e1)
                
                result = answer_question(question, s_c)


            # -----------------------------
            # Answer
            # -----------------------------

            st.subheader("Answer")

            st.write(result["answer"])


            # -----------------------------
            # Token usage
            # -----------------------------

            st.subheader("Token Usage")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Input Tokens",
                    result["input_tokens"]
                )

            with col2:

                st.metric(
                    "Output Tokens",
                    result["output_tokens"]
                )

            with col3:

                st.metric(
                    "Total Tokens",
                    result["total_tokens"]
                )
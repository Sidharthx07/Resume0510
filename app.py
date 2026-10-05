import streamlit as st
from markitdown import MarkItDown
import tempfile
import os
import io
import zipfile

# ---------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------

st.set_page_config(
    page_title="File to Markdown Converter",
    page_icon="📄",
    layout="centered"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📄 File to Markdown Converter")

st.write(
    "Convert PDF, Word, PowerPoint and Excel files "
    "into clean Markdown format for easier AI processing."
)

st.caption(
    "Built with Python, Streamlit and Microsoft MarkItDown"
)

# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload your files",
    type=["pdf", "docx", "pptx", "xlsx"],
    accept_multiple_files=True
)

# ---------------------------------------------------
# CONVERSION
# ---------------------------------------------------

if uploaded_files:

    if st.button("🚀 Convert to Markdown", use_container_width=True):

        converter = MarkItDown()

        converted_files = []
        failed_files = []

        progress_bar = st.progress(0)

        for index, uploaded_file in enumerate(uploaded_files):

            filename = uploaded_file.name

            try:

                # Create a temporary file
                file_extension = os.path.splitext(filename)[1]

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=file_extension
                ) as temp_file:

                    temp_file.write(uploaded_file.getbuffer())
                    temp_path = temp_file.name

                # Convert using Microsoft MarkItDown
                result = converter.convert(temp_path)

                # Get Markdown text
                markdown_text = result.text_content

                # Create Markdown filename
                base_name = os.path.splitext(filename)[0]
                markdown_filename = base_name + ".md"

                converted_files.append(
                    (markdown_filename, markdown_text)
                )

                # Delete temporary file
                os.remove(temp_path)

            except Exception as error:

                # Store failed files
                failed_files.append(
                    (filename, str(error))
                )

                # Remove temporary file if it exists
                try:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                except:
                    pass

            # Update progress
            progress_bar.progress(
                (index + 1) / len(uploaded_files)
            )

        # ---------------------------------------------------
        # RESULTS
        # ---------------------------------------------------

        st.divider()

        if converted_files:

            st.success(
                f"✅ {len(converted_files)} file(s) converted successfully!"
            )

            st.subheader("Converted Files")

            # Individual downloads
            for markdown_filename, markdown_text in converted_files:

                st.download_button(
                    label=f"⬇️ Download {markdown_filename}",
                    data=markdown_text,
                    file_name=markdown_filename,
                    mime="text/markdown"
                )

            # ---------------------------------------------------
            # CREATE ZIP
            # ---------------------------------------------------

            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(
                zip_buffer,
                "w",
                zipfile.ZIP_DEFLATED
            ) as zip_file:

                for markdown_filename, markdown_text in converted_files:

                    zip_file.writestr(
                        markdown_filename,
                        markdown_text
                    )

            zip_buffer.seek(0)

            st.download_button(
                label="📦 Download All as ZIP",
                data=zip_buffer,
                file_name="markdown_files.zip",
                mime="application/zip",
                use_container_width=True
            )

        # ---------------------------------------------------
        # FAILED FILES
        # ---------------------------------------------------

        if failed_files:

            st.warning(
                f"⚠️ {len(failed_files)} file(s) could not be converted."
            )

            for filename, error in failed_files:

                st.write(f"❌ {filename}")

        elif converted_files:

            st.info("🎉 All uploaded files were converted successfully!")

else:

    st.info(
        "Upload one or more PDF, Word, PowerPoint or Excel files to begin."
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "Student project | Python + Streamlit + Microsoft MarkItDown"
)
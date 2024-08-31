import streamlit as st
import os
from dotenv import load_dotenv
import base64
import pymongo

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")  # Make sure you have this in your .env file

# MongoDB setup
client = pymongo.MongoClient(MONGO_URI)
db = client["Contact_Form"]  # Replace with your actual database name
collection = db["contact_form_responses"]  # Replace with your desired collection name


def thank_you():
    """Displays the thank you page with the Calendly link."""
    st.title("Thank You!")
    st.write(
        "Thanks for reaching out! You can schedule a time to chat using the link below:"
    )
    st.markdown(
        "[Schedule a meeting with me on Calendly](https://calendly.com/harineepurush)"
    )


def main():
    st.title("Contact Me")
    st.write("Please fill out the form below to get in touch with me.")

    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email", help="Required")
        contact_no = st.text_input("Contact Number (Optional)")
        message = st.text_area("Message", help="Required")
        file = st.file_uploader(
            "Optional Document/File Upload", type=["pdf", "docx", "txt"]
        )
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if not email or not message:
                st.error("Please fill out the required fields.")
            else:
                try:
                    # Handle file upload
                    if file is not None:
                        file_name = file.name
                        file_contents = base64.b64encode(file.getvalue()).decode(
                            "utf-8"
                        )
                    else:
                        file_name = None
                        file_contents = None

                    # Store data in MongoDB
                    collection.insert_one(
                        {
                            "name": name,
                            "email": email,
                            "contact_no": contact_no,
                            "message": message,
                            "file_name": file_name,
                            "file_contents": file_contents,
                        }
                    )

                    st.success("Form submitted successfully!")

                    # Redirect to thank you page
                    st.session_state.thank_you_page = True
                    st.experimental_rerun()

                except Exception as e:
                    st.error(f"An error occurred while submitting the form: {e}")

    # Thank you page
    if st.session_state.get("thank_you_page"):
        thank_you()


if __name__ == "__main__":
    main()

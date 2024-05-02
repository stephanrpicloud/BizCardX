from streamlit_option_menu import option_menu
from io import BytesIO
from PIL import Image
import pandas as pd
import numpy as np
import streamlit as st
import easyocr
import base64
import cv2
import sqlite3
import re

st.set_page_config(page_title = "BizCardX",
                   page_icon = 'card_file_box',
                    layout= "wide" )

st.markdown(
    "<h1 style='text-align: center; color: white; '> Extract Business Card Data</h1>",
    unsafe_allow_html=True
    )

with st.container():
    selected = option_menu(
        menu_title= None,
        options = ["Home", "Extract Data", "Edit Extracted Data","Export Data as CSV"],
        icons = ['house-fill','blockquote-left','pencil-square','filetype-csv'],
        menu_icon = None,
        default_index=0,
        orientation="horizontal"
        )

if selected == "Home":
    def main():
        # About project
        st.markdown(
            "<h3 style='text-align: center; color: white; '> This interactive App empowers you to Extract data from Business cards effortlessly.</h3>",
            unsafe_allow_html=True
            )
        
        st.write("**Introduction:**")
        st.write("The Business Card Data Management System is a web application designed to extract, edit, and export data from business cards. It provides an intuitive interface for users to upload images of business cards, extract text information, edit the extracted data, and export it as a CSV file. The system utilizes Streamlit for building the user interface and SQLite for database management.")

        st.write("**Features:**")
        st.write("1. **Data Extraction Page:**")
        st.write("   - **Functionality:** This feature allows users to upload images of business cards, extract text information from them, categorize the extracted data into fields such as name, email, phone, etc., and save the data into a SQLite database.")
        st.write("   - **Key Components:**")
        st.write("     - Image Upload: Users can upload business card images in PNG, JPG, or JPEG format.")
        st.write("     - Text Extraction: The system uses EasyOCR to extract text from uploaded images.")
        st.write("     - Data Categorization: Extracted text is categorized into fields like name, email, phone, etc.")
        st.write("     - Data Display and Editing: Extracted data is displayed for editing, allowing users to modify and confirm the information.")
        st.write("     - Database Interaction: Extracted and edited data is stored in a SQLite database for future reference.")

        st.write("2. **Edit Extracted Data:**")
        st.write("   - **Functionality:** This feature enables users to edit and manage the extracted data stored in the SQLite database.")
        st.write("   - **Key Components:**")
        st.write("     - Data Retrieval: Users can fetch existing data from the database for editing.")
        st.write("     - Data Update: Users can modify specific records in the database, including fields like name, email, phone, etc.")
        st.write("     - Data Deletion: Users have the option to delete specific records from the database.")

        st.write("3. **Export Data as CSV:**")
        st.write("   - **Functionality:** This feature allows users to export data from the SQLite database as a CSV file for external use.")
        st.write("   - **Key Components:**")
        st.write("     - Data Retrieval: Users can select specific records or export all data from the database.")
        st.write("     - CSV Generation: The system converts the selected data into CSV format.")
        st.write("     - Download Link: Users are provided with a download link to retrieve the generated CSV file.")

        st.write("**Usage:**")
        st.write("To use the Business Card Data Management System, follow these steps:")
        st.write("1. Navigate to the web application URL.")
        st.write("2. Choose the desired action from the available options: 'Extract Data', 'Edit Extracted Data', or 'Export Data as CSV'.")
        st.write("3. Follow the instructions provided on each page to upload images, edit data, or export data as needed.")

        # About the Project Section
        st.header("About the Project:")
        st.markdown("""
        The Business Card Data Management System provides a convenient solution for extracting, editing, and exporting data from business cards. Its user-friendly interface and robust functionality make it suitable for various business and organizational needs related to data management.
        """)
        st.markdown("[Project Documentation](https://drive.google.com/file/d/1Svz1KBeOtSs6UVLAQnX69ga9qBxD9GW3/view?pli=1)")
        st.markdown("[Easy OCR](https://www.jaided.ai/easyocr/tutorial/)")
        st.markdown("[SQL lite 3](https://docs.python.org/3/library/sqlite3.html)")
        st.markdown("[Streamlit Documentation](https://docs.streamlit.io/library/api-reference)")
        st.markdown("[Pillow Documentation](https://pillow.readthedocs.io/en/stable/)")
        st.markdown("[Linkedin](https://www.linkedin.com/in/stephan-raj-aa0993211/)")

    if __name__ == "__main__":
        main()

if selected == "Extract Data":
    def app():

        # widget to upload image
        uploaded_file = st.file_uploader("Upload a Business Card", type=["png", "jpg", "jpeg"])
        col1, col2 = st.columns(2)

        with col1:
            # Function to read text from image using easyocr
            def extract_text_from_image(image):
                reader = easyocr.Reader(['en'])
                # Convert to grayscale
                gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
                # Apply Gaussian blur
                blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
                results = reader.readtext(blurred_image)
                return results


            def create_database():
                conn = sqlite3.connect('bizcardx.db')
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS cards
                    (id INTEGER PRIMARY KEY,
                    name TEXT,
                    designation TEXT,
                    company TEXT,
                    phone TEXT,
                    email TEXT,
                    website TEXT,
                    address TEXT,
                    UNIQUE(name, email, phone))''')  # Ensure uniqueness)''')
                conn.commit()
                conn.close()


            create_database()

            # Function to calculate the size of the text in the image based on its bounding box
            def get_text_size(bounding_box):
                top_left, top_right, bottom_right, bottom_left = bounding_box
                width = top_right[0] - top_left[0]
                height = bottom_right[1] - top_right[1]
                return width * height

            # Function to find the largest text in the OCR results, used for extracting company name
            def find_largest_text(ocr_results):
                large_text_fraction = 0.53  # threshold to consider the text as large ( used to find company name)

                # Find the largest text size
                max_size = max(get_text_size(result[0]) for result in ocr_results)

                # List to hold large texts in their original order
                large_texts_in_order = []

                for result in ocr_results:
                    text = result[1]
                    text_size = get_text_size(result[0])

                    # Check if the text size is larger than the fraction of the largest text
                    if text_size >= max_size * large_text_fraction:
                        large_texts_in_order.append(text)

                # Join them to form the company name, preserving the original order
                company_name = ' '.join(large_texts_in_order)
                return company_name

            # Function to categorize extracted text into different fields like company, email, etc.
            def categorize_text(ocr_results):
                data = {
                    "company_name": find_largest_text(ocr_results),
                    "card_holder": "",
                    "designation": "",
                    "email": "",
                    "phone": [],  # Initialize as an empty list
                    "website": "",
                    "address": ""
                }
                # Regular expression pattern to identify phone numbers
                phone_pattern = re.compile(r"(\+\d{3}-\d{3}-\d{4}|\d{3}-\d{3}-\d{4})")
                address_lines = []

                for i, result in enumerate(ocr_results):
                    text = result[1]
                    text_lower = text.lower()

                    if phone_pattern.match(text):
                        data["phone"].append(text)
                    elif "@" in text_lower and not data["email"]:
                        data["email"] = text
                    elif "www" in text_lower or "http" in text_lower and not data["website"]:
                        data["website"] = text_lower
                    elif i == 0:
                        data["card_holder"] = text
                        continue  # Skip adding card holder to the address
                    elif i == 1:
                        data["designation"] = text
                        continue  # Skip adding designation to the address
                    elif text in data["company_name"]:
                        continue  # Skip adding company name to the address
                    else:
                        address_lines.append(text)

                # Convert the list of phone numbers to a string AFTER deduplication
                data["phone"] = ', '.join(set(data["phone"]))
                # Join address lines to form a single address string
                data["address"] = ' '.join(address_lines)
                return data

            # Function to insert extracted and categorized data into the database
            def insert_data(name, designation, company, phone, email, website, address):
                try:
                    conn = sqlite3.connect('bizcardx.db')
                    c = conn.cursor()
                    # The SQL query for inserting data
                    query = '''INSERT INTO cards (name, designation, company, phone, email, website, address) VALUES (?, ?, ?, ?, ?, ?, ?)'''
                    # Executing the query with the data
                    c.execute(query, (name, designation, company, phone, email, website, address))
                    conn.commit()
                    message = "Data saved successfully!"
                except sqlite3.IntegrityError:
                    message = "Data already exists."
                finally:
                    conn.close()
                return message

            create_database()


            # Extract and display the text
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption='Uploaded Business Card.', width=600)
                ocr_results = extract_text_from_image(image)

                categorized_data = categorize_text(ocr_results)

                # Extract and display the data in an editable format
                card_holder = categorized_data["card_holder"]
                designation = categorized_data["designation"]
                company_name = categorized_data["company_name"]
                email = categorized_data["email"]
                phone = (categorized_data["phone"])
                website = categorized_data["website"]
                address = categorized_data["address"]
            
            # Create an expandable section to display extracted information
            with col2:
                if uploaded_file is not None:  
                    with st.expander("Extracted Information", expanded=True):
                        # Create a two-column layout
                        col1, col2 = st.columns(2)

                        # In the left column, display fields for name, designation, and company
                        with col1:
                            card_holder = st.text_input("Card Holder", card_holder)
                            designation = st.text_input("Designation", designation)
                            company_name = st.text_input("Company Name", company_name)

                        # In the right column, display fields for email, phone, and website
                        with col2:
                            email = st.text_input("Email", email)
                            phone = st.text_input("Phone", phone)
                            website = st.text_input("Website", website)
                        # Display a text area for the address in bottom center
                        address = st.text_area("Address", address, height=100)

                    # Optionally, add a button to confirm the edits
                    if st.button('Confirm Edits'):
                        result_message = insert_data(card_holder, designation, company_name, phone, email, website, address)
                        if "successfully" in result_message:
                            st.success(result_message)
                        else:
                            st.error(result_message)

    if __name__ == "__main__":
        app()

if selected == "Edit Extracted Data":
    # Function to fetch data from the database
    def fetch_data():
        conn = sqlite3.connect('bizcardx.db')  # Connect to SQLite DB file
        c = conn.cursor()
        c.execute("SELECT * FROM cards")  # Fetch all fields
        data = c.fetchall()
        conn.close()
        return data

    # Function to update a specific record in the database
    def update_data(record_id, name, designation, company, phone, email, website, address):
        conn = sqlite3.connect('bizcardx.db')
        c = conn.cursor()
        query = '''UPDATE cards
                SET name = ?, designation = ?, company = ?, phone = ?, email = ?, website = ?, address = ?
                WHERE id = ?'''
        c.execute(query, (name, designation, company, phone, email, website, address, record_id))
        conn.commit()
        conn.close()

    # Function to delete a specific record from the database
    def delete_data(record_id):
        conn = sqlite3.connect('bizcardx.db')
        c = conn.cursor()
        query = "DELETE FROM cards WHERE id = ?"
        c.execute(query, (record_id,))
        conn.commit()
        conn.close()
        st.experimental_rerun()

    def app():
        data = fetch_data()
        if not data:
            st.warning("No data found")
            return

        company_mapping = {row[0]: row[3] for row in data}
        col1 , col2 , col3 = st.columns([1,2,1])
        with col2:
            selected_id = st.selectbox("Select a company to edit", list(company_mapping.keys()), format_func=lambda x: company_mapping[x])

        selected_record = next((row for row in data if row[0] == selected_id), None)
        if selected_record:
            new_name = st.text_input("Name", selected_record[1])
            new_designation = st.text_input("Designation", selected_record[2])
            new_company = st.text_input("Company", selected_record[3])
            new_phone = st.text_input("Phone", selected_record[4])
            new_email = st.text_input("Email", selected_record[5])
            new_website = st.text_input("Website", selected_record[6])
            new_address = st.text_input("Address", selected_record[7])

            confirm_delete = st.checkbox("Confirm deletion")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update Record"):
                    update_data(selected_id, new_name, new_designation, new_company, new_phone, new_email, new_website, new_address)
                    st.success("Record updated successfully!")

            with col2:
                if st.button("Delete Record", disabled=not confirm_delete):
                    delete_data(selected_id)
                    st.success("Record deleted successfully!")

    if __name__ == "__main__":
        app()

if selected == "Export Data as CSV":
    # Function to fetch all data from the SQLite database
    def fetch_all_data():
        conn = sqlite3.connect('bizcardx.db')  # SQLite database file
        c = conn.cursor()
        c.execute("SELECT * FROM cards")
        data = c.fetchall()
        conn.close()
        return data

    # Function to convert data to CSV format and encode it for download
    def to_csv(data):
        output = BytesIO()  # Create a BytesIO object to hold the CSV data
        # Convert data to DataFrame then to CSV
        pd.DataFrame(data, columns=['ID', 'Name', 'Designation', 'Company', 'Phone', 'Email', 'Website', 'Address']).to_csv(output, index=False, encoding='utf-8')
        encoded = base64.b64encode(output.getvalue()).decode()  # Encode CSV data for download
        return f"data:text/csv;base64,{encoded}"
    
    # Function to process data for download and create a download link
    def process_and_download(data):
        if data:
            csv = to_csv(data)  # Convert DataFrame to CSV
            # Create a download link for the CSV file
            st.markdown(f'<a href="{csv}" download="exported_data.csv">Download CSV File</a>', unsafe_allow_html=True)
        else:
            st.write("No records selected or available")

    def app():
        col1 , col2 , col3 = st.columns([1,2,1])
        with col2:
            all_data = fetch_all_data()
            if not all_data:
                st.write("No data available to export")
                return

            # Allow user to select records to export
            options = {f"{row[0]}: {row[3]}" for row in all_data}
            selected = st.multiselect('Select records to export', options)
            col1 , col2 = st.columns(2)
            with col1:
                if st.button('Export Selected'):
                    selected_ids = [int(s.split(":")[0]) for s in selected]
                    selected_data = [row for row in all_data if row[0] in selected_ids]
                    process_and_download(selected_data)
            with col2:
                if st.button('Export All Data'):
                    process_and_download(all_data)  # Process and download all data

    if __name__ == "__main__":
        app()
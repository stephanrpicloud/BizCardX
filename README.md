# Business Card Data Management System

## Introduction

The Business Card Data Management System is a web application designed to extract, edit, and export data from business cards. It provides an intuitive interface for users to upload images of business cards, extract text information, edit the extracted data, and export it as a CSV file. The system utilizes Streamlit for building the user interface and SQLite for database management.

## Features

1. **Data Extraction Page:**
   - **Functionality:** Allows users to upload images of business cards, extract text information from them, categorize the extracted data into fields such as name, email, phone, etc., and save the data into a SQLite database.
   - **Key Components:**
     - Image Upload: Users can upload business card images in PNG, JPG, or JPEG format.
     - Text Extraction: The system uses EasyOCR to extract text from uploaded images.
     - Data Categorization: Extracted text is categorized into fields like name, email, phone, etc.
     - Data Display and Editing: Extracted data is displayed for editing, allowing users to modify and confirm the information.
     - Database Interaction: Extracted and edited data is stored in a SQLite database for future reference.

2. **Edit Extracted Data:**
   - **Functionality:** Enables users to edit and manage the extracted data stored in the SQLite database.
   - **Key Components:**
     - Data Retrieval: Users can fetch existing data from the database for editing.
     - Data Update: Users can modify specific records in the database, including fields like name, email, phone, etc.
     - Data Deletion: Users have the option to delete specific records from the database.

3. **Export Data as CSV:**
   - **Functionality:** Allows users to export data from the SQLite database as a CSV file for external use.
   - **Key Components:**
     - Data Retrieval: Users can select specific records or export all data from the database.
     - CSV Generation: The system converts the selected data into CSV format.
     - Download Link: Users are provided with a download link to retrieve the generated CSV file.

## Usage

To use the Business Card Data Management System, follow these steps:
1. Navigate to the web application URL.
2. Choose the desired action from the available options: 'Extract Data', 'Edit Extracted Data', or 'Export Data as CSV'.
3. Follow the instructions provided on each page to upload images, edit data, or export data as needed.

## Requirements

- Python 3.x
- Streamlit
- SQLite
- EasyOCR
- OpenCV
- Pandas
- NumPy
- Base64

1. Clone the repository:

   ```bash
   https://github.com/stephanrpicloud/BizCardX.git   
   ```

2. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

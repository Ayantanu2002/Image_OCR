# OCR Text Extraction with Byaldi and Qwen2-VL

This project implements Optical Character Recognition (OCR) using the **ColPali implementation of the Byaldi library** and **Hugging Face's Qwen2-VL model**. The extracted text from images (containing Hindi and English) is displayed through a simple web application built using **Streamlit**. Users can search for specific keywords within the extracted text.

## Project Overview

The project involves:

- **OCR Implementation**: Using ColPali's Byaldi library and Hugging Face transformers (Qwen2-VL model) to extract text from images.
- **Web Application**: A Streamlit web interface that allows users to upload images, view extracted text, and search within the text.
- **Deployment**: The web application is deployed on platforms like **Streamlit Sharing** or **Hugging Face Spaces**, making it accessible via a public URL.

## Features

- **OCR Extraction**: Extract text from images in Hindi and English using the Byaldi + Qwen2-VL model.
- **Keyword Search**: Search within the extracted text for specific keywords, with matching results highlighted.
- **User-Friendly Interface**: Upload and process images via a simple and intuitive Streamlit web interface.

## Requirements

- Python 3.8 or higher
- Install dependencies using the provided `requirements.txt`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Ayantanu2002/Image_OCR.git
    cd Image_OCR
    ```

2. Set up the virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use .venv\Scripts\activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Once the installation is complete, you can start the Streamlit app:

```bash
streamlit run app.py

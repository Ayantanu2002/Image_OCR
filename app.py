
import streamlit as st
from PIL import Image
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
import torch
from qwen_vl_utils import process_vision_info

# Load the model and processor
@st.cache_resource  # Cache the model loading for performance
def load_model():
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        "Qwen/Qwen2-VL-2B-Instruct",
        trust_remote_code=True,
        torch_dtype=torch.bfloat16
    ).cpu().eval()
    processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-2B-Instruct")
    return model, processor

# Preprocess the image
def preprocess_image(image):
    image = image.convert("RGB")
    return image

# Extract text from the image using the model
def extract_text_from_image(image, model, processor):
    messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": image},  # Replace 'image' with your actual image data
            {"type": "text", "text": "Extract all text from this image, including both Hindi and English."}
        ]
    }
    ]


    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)

    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt"
    ).to("cpu")

    generated_ids = model.generate(**inputs, max_new_tokens=128)
    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]

    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )

    return output_text

# Highlight search term in text
def highlight_text(text, search_term):
    highlighted_text = text.replace(search_term, f"<mark>{search_term}</mark>")
    return highlighted_text

# Streamlit App
st.title("OCR Web Application")

# Upload the image file
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption="Uploaded Image.", use_column_width=True)

    # Load the OCR model and processor
    model, processor = load_model()

    # Preprocess and run OCR
    processed_image = preprocess_image(input_image)
    extracted_text = extract_text_from_image(processed_image, model, processor)

    # extracted_text is a list, so join it into a single string
    extracted_text_str = " ".join(extracted_text)  # Convert list to a single string
    extracted_text_str = " ".join(extracted_text_str.split())  # Clean up spaces

# Now you can safely use extracted_text_str as a normal string

    print("Extracted text:", extracted_text_str)
    # Display extracted text
    st.subheader("Extracted Text:")
    st.write(extracted_text_str)

    # Search functionality
    search_query = st.text_input("Search for keywords in extracted text")
    if search_query:
        if search_query.lower() in extracted_text_str.lower():
            highlighted_result = highlight_text(extracted_text_str, search_query)
            st.subheader("Search Results:")
            st.markdown(f"<p>{highlighted_result}</p>", unsafe_allow_html=True)
        else:
            st.subheader("Search Results:")
            st.write("No matches found.")
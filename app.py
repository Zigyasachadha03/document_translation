from flask import Flask, render_template, request, redirect
from PIL import Image
import pytesseract
import os
from transformers import MarianTokenizer, MarianMTModel
import math
from tempfile import NamedTemporaryFile
from pdf2image import convert_from_path

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "temp"

translation_model_directory = "C:\\Users\\zigya\\OneDrive\\Desktop\\Project\\Document_Translation\\saved_model"
translation_tokenizer = MarianTokenizer.from_pretrained(translation_model_directory)
translation_model = MarianMTModel.from_pretrained(translation_model_directory)

def translate_document(input_document):
    try:
        input_ids = translation_tokenizer.encode(input_document, return_tensors="pt", truncation=True)
        translated_ids = translation_model.generate(input_ids.to(translation_model.device), max_length=512)
        translated_text = translation_tokenizer.decode(translated_ids[0], skip_special_tokens=True)
        return translated_text
    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")

def translate_document_pdf(input_document, max_length=512):
    input_ids = translation_tokenizer.encode(input_document, return_tensors="pt")
    num_chunks = math.ceil(input_ids.size(1) / max_length)
    translated_text = ""
    
    for i in range(num_chunks):
        start_idx = i * max_length
        end_idx = start_idx + max_length
        input_chunk = input_ids[:, start_idx:end_idx]
        
        translated_ids = translation_model.generate(input_chunk)
        translated_text += translation_tokenizer.decode(translated_ids[0], skip_special_tokens=True)
    
    return translated_text

def extract_text_from_pdf(pdf_file):
    images = convert_from_path(pdf_file)

    extracted_text = ""
    for image in images:
        text = pytesseract.image_to_string(image, lang='spa')
        extracted_text += text

    return extracted_text

@app.route('/')
def home():
    return render_template('index.html')

# Translation route
@app.route('/translate', methods=['POST'])
def translate():    
    print("translate() function is called") 
    doc_type = request.form.get('doc-type')
    if doc_type == "text":
        text = request.form.get("text")
        translated_text = translate_document(text)
        return render_template("view_text.html", translated_text=translated_text)
    elif doc_type == "pdf":
        pdf_file = request.files["pdf"]
        filename = pdf_file.filename
        
        # Save the uploaded file to a temporary location
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            pdf_file.save(temp_path)
        
        if filename.endswith(".pdf"): 
            extracted_text = extract_text_from_pdf(temp_path)
            translated_text = translate_document_pdf(extracted_text)
            
            os.remove(temp_path)
            return render_template("view_text.html", translated_text=translated_text)
    return redirect('/')


@app.route('/goback')
def go_back():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

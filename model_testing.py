from transformers import MarianMTModel, MarianTokenizer
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
from tempfile import NamedTemporaryFile
import math

# Translate a Spanish document to English
# def translate_document(input_document):
#     # Tokenize the input document
#     input_ids = tokenizer.encode(input_document, return_tensors="pt")

#     # Generate the translation
#     translated_ids = model.generate(input_ids)

#     # Decode the translated output
#     translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)

#     return translated_text

input_document = '''
El 17 de septiembre de 1954 se celebra en Ronda la primera corrida goyesca con motivo del segundo centenario del nacimiento del torero Pedro Romero, al estilo de la celebrada en la plaza de toros de Zaragoza en 1927. El cartel taurino inaugural se compuso por Antonio Bienvenida, César Girón y Cayetano Ordóñez que para la ocasión se vistieron al estilo del siglo xviii en honor al torero rondeño
'''
input_pdf = "Document_Translation\\spanish-doc.pdf"

translation_model_directory = "C:\\Users\\zigya\\OneDrive\\Desktop\\Project\\Document_Translation\\saved_model"
translation_tokenizer = MarianTokenizer.from_pretrained(translation_model_directory)
translation_model = MarianMTModel.from_pretrained(translation_model_directory)


def extract_text_from_pdf(pdf_file):
    images = convert_from_path(pdf_file)

    extracted_text = ""
    for image in images:
        text = pytesseract.image_to_string(image, lang='spa')
        extracted_text += text

    return extracted_text

def translate_document():
    input_ids = translation_tokenizer.encode(input_document, return_tensors="pt", truncation=True)
    translated_ids = translation_model.generate(input_ids.to(translation_model.device), max_length=512)
    translated_text = translation_tokenizer.decode(translated_ids[0], skip_special_tokens=True)
    return translated_text

# Translate a document from Spanish to English
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

# pdf_path = save_pdf(input_pdf)
extracted_text = extract_text_from_pdf(input_pdf)
print("Spanish Text: \n")
print(extracted_text)
translated_text = translate_document_pdf(extracted_text)
print("English Text: \n")
print(translated_text)
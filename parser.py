import docx2txt
import nltk
import re
import subprocess  # noqa: S404
 
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
 
def extract_text_from_docx(docx_path):
    txt = docx2txt.process(docx_path)
    if txt:
        return txt.replace('\t', ' ')
    return None
 
 
def extract_names(txt):
    person_names = []
 
    for sent in nltk.sent_tokenize(txt):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(
                    ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves())
                )
 
    return person_names
 
def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)
    #number = ''.join(phone[0])
    #return number
    return phone
 
if __name__ == '__main__':
    text = extract_text_from_docx('demo.docx')
    names = extract_names(text)
    phone_number = extract_phone_number(text)
    
    if names:
        print(names[0])  # noqa: T001           # Name is extracted here

    if phone_number :
        print(phone_number[0])                  # Phone number is extracted here
    
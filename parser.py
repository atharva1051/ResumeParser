import docx2txt
import nltk
import re
import subprocess  # noqa: S404
 
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')

SKILLS_DB = [
    'machine learning',
    'data science',
    'python',
    'word',
    'excel',
    'English',
    'nlp',
    'html',
    'css',
    'java',
    'c++',
    'git',
    'software engineering'
]

PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
GPA_REG = re.compile(r'^[0-9]*[.,]{0,1}[0-9]*$')
 
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

def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)

def extract_skills(input_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)
 
    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]
 
    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]
 
    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
 
    # we create a set to keep the results in.
    found_skills = set()
 
    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower() in SKILLS_DB:
            found_skills.add(token)
 
    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.lower() in SKILLS_DB:
            found_skills.add(ngram)
 
    return found_skills

def extract_gpa(resume_text):
    return re.findall(GPA_REG,resume_text)  ## ERROR IN THIS LINE
 
if __name__ == '__main__':
    text = extract_text_from_docx('demo.docx')
    names = extract_names(text)
    phone_number = extract_phone_number(text)
    email = extract_emails(text)
    skills = extract_skills(text)
    gpa = extract_gpa(text)

    if names:
        print(names[0])  # noqa: T001           # Name is extracted here // add to dictionary later

    if phone_number :
        print(phone_number[0])                  # Phone number is extracted here    // add to dictionary later
    
    if email :
        print(email)

    if skills :
        print(skills)

    if gpa :
        print(gpa)
import docx

def extract_text(filepath):
    doc = docx.Document(filepath)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

if __name__ == "__main__":
    text = extract_text(r"c:\Users\LOKOUN Kris\Desktop\projects\Prtfolio STREAMLIT\projet_final\RAPPORT_FINAL_EXPERT_LOKOUN_THYS.docx")
    with open("extracted_report.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Done")

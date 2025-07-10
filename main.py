from src.medex.term_ex import MedicalTermsExtraction
from src.medex.file_converter import texter
import os 


def main():
    path =r"C:\Users\admin dell\Desktop\RAG series\Naive RAG\src\resources\record2.txt"
    api_key = os.getenv('GeminiApiKey')
    model = "gemini-2.5-flash"
    text = texter(path)
    mte = MedicalTermsExtraction(api_key, model, text)
    print("===== Diagnosis terms ==========")
    mte.dextraction()
    print("\n===== Procedural terms ==========")
    mte.pextraction()
    print("\n===== Modifier terms ==========")
    mte.mextraction()


if __name__ == "__main__":
    main()
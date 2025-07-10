def texter(path):
    with open(path, 'r', encoding= 'utf-8') as f: 
        text = f.read()
        return text

if __name__ == "__main__":
    path = r'C:\Users\admin dell\Desktop\RAG series\Naive RAG\src\resources\record.txt'
    text = texter(path)
    print(text)
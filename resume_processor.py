import json
from resume_parser import ResumeParser
from document_parser import DocumentParser
from file_downloader import FileDownloader

class ResumeProcessor:
  def __init__(self, OPENAI_API_KEY):
    self.parser = ResumeParser(OPENAI_API_KEY)
    self.file_downloader = FileDownloader()
    self.document_parser = DocumentParser()

  def process_resume(self, url):
    file_path, file_type = self.file_downloader.download_file(url)

    document_text = None
    if file_type == 'pdf':
        document_text = self.document_parser.pdf2string(file_path)
    elif file_type == 'doc':
        document_text = self.document_parser.doc2string(file_path)

    if document_text:
        prompt = self.parser.prompt_questions + "\n" + document_text
        engine = "text-davinci-002"
        max_tokens = 4097

        response = self.parser.query_completion(prompt, engine=engine, max_tokens=max_tokens)
        response_text = response["choices"][0]["text"].strip()
        resume = json.loads(response_text)
        return resume

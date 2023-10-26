import pdftotext
import requests
import openai
import re
import json
import subprocess
import tempfile
from tokenizer import num_tokens_from_string

class ResumeParser:
  def __init__(self, OPENAI_API_KEY):
    openai.api_key = OPENAI_API_KEY
    self.prompt_questions = """Summarize the text below into a JSON with exactly the following structure 
    { full_name, email, location, years_of_experience, main_profession, 
    external_urls_hash: {github_url, linkedin_url, portfolio_url},
    candidate_experiences: [{title, description, region_name, company_name, experience_type, effective_date_range}],
    candidate_educations: [{level, major_name, degree_name, grade_value, grade_metric, education_name, effective_date_range}],
    candidate_skills: [{emsi_id, skill_name, skill_type}], birthdate: ,
    languages: [], phone_number: null, publications: [], referees: [],
    resume_url, sections: [{body, header, page_index, section_type }] }
    """

  def pdf2string(self, pdf_file):
    try:
        with open(pdf_file, "rb") as f:
            pdf = pdftotext.PDF(f)
        pdf_str = "\n\n".join(pdf)
        pdf_str = re.sub("\s[,.]", ",", pdf_str)
        pdf_str = re.sub("[\n]+", "\n", pdf_str)
        pdf_str = re.sub("[\s]+", " ", pdf_str)
        pdf_str = re.sub("http[s]?(://)?", "", pdf_str)

        return pdf_str
    except Exception as e:
        print(f"Error: {e}")
        return None

  def doc2string(self, doc_file):
    try:
        text = subprocess.check_output(["antiword", doc_file])
        text = text.decode('utf-8')
        text = text.replace("\n", " ")
        text = " ".join(text.split())
        text = re.sub(r"\s[,.]", ",", text)

        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

  def query_completion(self, prompt: str, engine: str = "text-curie-001",
                       temperature: float = 0.0, max_tokens: int = 100,
                       top_p: int = 1, frequency_penalty: int = 0,
                       presence_penalty: int = 0) -> object:

    estimated_prompt_tokens = num_tokens_from_string(prompt, engine)
    estimated_answer_tokens = max_tokens - estimated_prompt_tokens

    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=estimated_answer_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    return response

  def download_pdf(self):
    response = requests.get('https://weguide-medical-dev.s3.ap-southeast-2.amazonaws.com/dummy-resume.pdf?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEoaCmFwLXNvdXRoLTEiRzBFAiAz3T2gsA8mRBxCJ93Q3nCIVgRggDv%2F5He%2FcHErE7CaWAIhALRPRMAb3bbol5UUGgClR1Aqa7S3V81%2BHdbEIbCwB11MKv0CCHMQAhoMNjkwNjU3NzY4MzQ4IgyaCZTaSgWcftlr1Msq2gLa4GG09w4tg7ojBm6J8fxO0KVImOpIP8vJsCqTSmifAn%2FUyYk1e8Cnn8jQ0tZdAM4Fh%2BXaM4AkWF6g2ab4zKVXRXZsJpzOa26XgX0SdXlCaYV%2FmojPQGa1kXyi%2B3VlIybKw8BLdZjNhNbqdnQqTFb413OzV%2BXGAnsXuwBk1jJex8r9VbHG4t%2FrfonzzeNigo7Wlm8kK7F78CjbklCNO2QfPJZtyexNCzvJnvi0F0nhCWXpQdkmBiPCbzPUvq2DL5gUpTY314N1WuZx4aLyqQBpdM115S5IR%2FcF8fP82u%2FVt5cky8MkmDDRIXUK1v5701Wyt7rA4vDFIuV2OyMFmKUdHwkujRx7O0uYcVqbLPaAoTPLSP220Rz8RfcpRCzPsi%2Bx7hpUM8J%2B5%2FnhgBk3JoqOSmi4cq3aL0QzgWs5qa74Cap9tSFzR44qCMxRJKw02XhevOVSYttQHjSvMOT66KkGOrMCxTlICU%2FcGcieckLeZVLIbGplqBfzb3cj1QmjYkjfehAj1X5UERr9shRnvSX14vFvmTLPgMZx%2BP5AfU6Zqvy65kf7PTI5JogBYCDhymZ14fTJi7EtypSyXFBfUNL1PNfOjrecUD235F8d1Jd%2FEfDgr7WGDirSty7ukwGD2BktdUTlWFf3xAX8cdBULBH9z4ccnjEo5rlC2oea%2F9Xy2N7W3PApU5bHhlNqNBgZijggo%2FVc%2Bo149orOB8JX9REb%2FTUmheoYhrl2qoFjj8%2FfgPTejzFrKki8zpu6xWu1ewtRxy6b4P9WTK%2FcYI8WS12R80DTihSS9KEXMc0o9sWpot0rQq1JS3rZ5hCkDnf2feeDDvwVtciJeNxfnlyOaAHWNPV24bHv2V3UyRp7n68GBZHoTJVaMw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231026T102120Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA2BTTJGOOMDMW7WU5%2F20231026%2Fap-southeast-2%2Fs3%2Faws4_request&X-Amz-Signature=892e15e39870db32fc6fff3cc196d71f8cf2e7ca60fe517aab82e2e768ff90fb')

    content_type = response.headers.get('Content-Type', '').lower()

    if 'pdf' in content_type:
        file_type = 'pdf'
    elif 'msword' in content_type:
        file_type = 'doc'
    else:
        raise ValueError("Unsupported file type. Expected PDF or DOC.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_type}') as temp_file:
        temp_file.write(response.content)

    return temp_file.name, file_type

  def query_resume(self) -> dict:
    file_path, file_type = self.download_pdf()
    if file_type == 'pdf':
        pdf_str = self.pdf2string(file_path)
    elif file_type == 'doc':
        pdf_str = self.doc2string(file_path)

    prompt = self.prompt_questions + "\n" + pdf_str

    engine = "text-davinci-002"
    max_tokens = 4097

    response = self.query_completion(prompt, engine=engine, max_tokens=max_tokens)
    response_text = response["choices"][0]["text"].strip()
    resume = json.loads(response_text)

    return resume
    

def main():
  OPENAI_API_KEY = "place_open_ai_key_here"
  parser = ResumeParser(OPENAI_API_KEY)
  pdf_text = parser.query_resume()
  print(pdf_text)

if __name__ == "__main__":
    main()

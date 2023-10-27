from resume_processor import ResumeProcessor

def main():
  OPENAI_API_KEY = "open_api_key"
  url = 's3_file_url'
  processor = ResumeProcessor(OPENAI_API_KEY)
  json_text = processor.process_resume(url)

  print(json_text)

if __name__ == "__main__":
  main()

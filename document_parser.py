import pdftotext
import re
import subprocess

class DocumentParser:
  @staticmethod
  def pdf2string(pdf_file):
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

  @staticmethod
  def doc2string(doc_file):
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
      

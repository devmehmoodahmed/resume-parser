import requests
import tempfile

class FileDownloader:
  @staticmethod
  def download_file(url):
    response = requests.get(url)
    content_type = response.headers.get('Content-Type', '').lower()

    if 'pdf' in content_type:
      file_type = 'pdf'
    elif 'doc' in content_type:
      file_type = 'doc'
    else:
      raise ValueError("Unsupported file type. Expected PDF or DOC.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_type}') as temp_file:
      temp_file.write(response.content)

    return temp_file.name, file_type

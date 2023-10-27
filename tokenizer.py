import tiktoken

def num_tokens_from_string(string: str, model: str) -> int:
  encoding = tiktoken.encoding_for_model(model)
  num_tokens = len(encoding.encode(string))
  return num_tokens


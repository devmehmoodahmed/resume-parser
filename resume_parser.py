import openai
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

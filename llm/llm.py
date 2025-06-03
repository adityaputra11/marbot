from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from langchain_perplexity import ChatPerplexity
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_together import ChatTogether
from config.settings import Settings
from langchain_litellm import ChatLiteLLM

settings = Settings()
class LLM:
  def __init__(self):
    self.deepseek = ChatDeepSeek(
      model="deepseek-chat",
      api_key=settings.ai.deepseek_api_key,
      temperature=0,
      verbose=True
    )
    self.deepseek_r1 = ChatDeepSeek(
      model="deepseek-reasoner",
      api_key=settings.ai.deepseek_api_key,
      temperature=0,
      verbose=True
    )
    self.openai = ChatLiteLLM(
      model="gpt-4.1-mini",
      temperature=0,
      api_key="sk-piWDpNLR5HXbvq5COzpXRw",
      api_base=settings.ai.litellm_api_base,
      verbose=True
    )
    self.perplexity = ChatPerplexity(
      model="sonar",
      temperature=0,
      api_key=settings.ai.perplexity_api_key,
      verbose=True
    )
    self.gemini = ChatGoogleGenerativeAI(
      model="gemini-2.0-flash",
      temperature=0,
      api_key=settings.ai.gemini_api_key,
      verbose=True
    )
    self.together = ChatTogether(
      model="llama-3.1-8b-instruct",
      temperature=0,
      api_key=settings.ai.together_api_key,
      verbose=True
    )
    self.litellm = ChatLiteLLM(
      model="gpt-4.1-mini",
      temperature=0,
      api_key=settings.ai.litellm_api_key,
      api_base=settings.ai.litellm_api_base,
      verbose=True
    )
    
    

  def chat_deepseek(self):
    return self.deepseek
  
  def chat_deepseek_r1(self):
    return self.deepseek_r1
  
  def chat_openai(self):
    return self.openai
  
  def chat_perplexity(self):
    return self.perplexity
  
  def chat_gemini(self):
    return self.gemini
  
  def chat_together(self):
    return self.together
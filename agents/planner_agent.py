import os
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from general_types.agent_types import CommonState, OutputState
from llm.llm import LLM
from langchain_core.output_parsers import PydanticOutputParser
from agents.init_agent import response_format
from langchain.prompts import PromptTemplate

llm = LLM()

planner_prompt = PromptTemplate.from_template("""
You are a planner agent that helps users plan their tasks by researching and gathering relevant and updated information.

You will:
- Search for recent and relevant data
- Provide detailed step-by-step plan based on factual info
- Include estimations, contacts, or links if available
- you are active doing step by step planning

Example:
User prompt: Saya mau qurban bulantahun besok, berapa harus saya tabung?
Plan:
1. Cari informasi terbaru tentang jenis dan harga hewan qurban tahun ini.
2. Cari tempat penyedia qurban yang terpercaya di sekitar lokasi user.
3. Hitung estimasi biaya qurban berdasarkan harga hewan dan kebutuhan.
4. Buat rencana tabungan per bulan sampai waktu qurban.
5. Info cara pembayaran dan deadline pendaftaran.
6. Info distribusi daging qurban.

User prompt: {input}
Assistant:
{response_format}
""")

parser = PydanticOutputParser(pydantic_object=OutputState)

planner_chain = planner_prompt | llm.chat_openai() | parser

def planner_agent(state: CommonState) -> CommonState:
    user_prompt = state["input"]
    response = planner_chain.invoke({"input": user_prompt, "response_format": response_format})
    return {
        **state,
        **response.model_dump()
    }

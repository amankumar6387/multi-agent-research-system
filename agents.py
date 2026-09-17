from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    reasoning_effort="low",
    max_tokens=1000,
    max_retries=2,
)

# =========================================================
# 1st AGENT: SEARCH AGENT
# =========================================================

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
You are a web research assistant.

Your task is to find reliable and recent information.

Use the web_search tool when you need
current or external information.

Call the tool with a simple search query.
After receiving the search results,
summarize the important findings.

Do not invent URLs or facts.
Keep your response concise.
"""
    )


# =========================================================
# 2nd AGENT: READER AGENT
# =========================================================

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
You are a research source reader.

Your task is to extract useful information
from the provided URLs.

Use scrape_url to read relevant sources.

Extract important facts and statistics
when available.

Do not invent information.
Mention the source URL when possible.
Keep your response concise.
"""
    )
# =========================================================
# WRITER CHAIN
# =========================================================

writer_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        "You are an expert research writer. "
        "Write clear, structured and insightful reports."
    ),

    (
        "human",
        """Write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research}

Structure the report as:

- Introduction

- Key Findings
  Minimum 3 well-explained points.

- Conclusion

- Sources
  List all URLs found in the research.

Be detailed, factual and professional."""
    )

])

writer_chain = (
    writer_prompt
    | llm
    | StrOutputParser()
)


# =========================================================
# CRITIC CHAIN
# =========================================================

critic_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        "You are a sharp and constructive research critic. "
        "Be honest and specific."
    ),

    (
        "human",
        """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""
    )

])

critic_chain = (
    critic_prompt
    | llm
    | StrOutputParser()
)



# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":
    print("agents.py started")

    search_agent = build_search_agent()
    print("Search Agent created successfully")

    reader_agent = build_reader_agent()
    print("Reader Agent created successfully")

    print("Writer Chain created successfully")
    print("Critic Chain created successfully")

    print("agents.py finished")
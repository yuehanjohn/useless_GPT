import os
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
os.environ["GROQ_API_KEY"] ='INSERT_API_KEY_HERE'

#from test import fetch_tkinter_image

openai_llm = ChatGroq(api_key=os.environ.get("GROQ_API_KEY"), model="llama-3.1-70b-versatile")

uselessAI = Agent(
    role='Non-sense response',
    goal="Response to questions as unrelated as possible. As random as possible.",
    backstory="You are an expert at responding questions with non-sense random answer",
    description="You are an expert at responding questions with non-sense random answer",
    verbose=True,
    allow_delegation=False,
    llm=openai_llm,
)

wordAI = Agent(
    role='Provide 1 word unrelated answer',
    goal="Response to question with a single unrealted word. Provide any of fields",
    backstory="Best 1 word responserer",
    description = "You provide responses to question with a single unrealted word",
    verbose=False,
    allow_delegation=False,
    llm=openai_llm,
)


useless_task = Task(
    description="Reply non-sense answeer to user's question",
    agent=uselessAI,
    expected_output="non-sense answer about {input}",
)

image_task = Task(
    description="Change the text to a single word that is completely unrelated to the input",
    agent=wordAI,
    expected_output="non-sense answer about {input}",
)

crew = Crew(agents=[uselessAI], tasks=[useless_task])

image = Crew(agents=[wordAI], tasks=[image_task])

def functionality(question):    
    while(True):
        if question == "q":
            return "Thank you for wasting your life on this AI! <3"
        result = crew.kickoff(inputs={"input": question})
        if "agent has" in str(result).lower():
            return "I DON'T WANT TO TALK TO YOU, GO AWAY!"
        return result

def opposite_text(prompt):
    return image.kickoff(inputs={"input": prompt})
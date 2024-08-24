import os
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
os.environ["GROQ_API_KEY"] ='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'

#from test import fetch_tkinter_image

openai_llm = ChatGroq(api_key=os.environ.get("GROQ_API_KEY"), model="llama-3.1-70b-versatile")

uselessAI = Agent(
    role='Non-sense response',
    goal="Response to questions as useless as possible",
    backstory="You are an expert at responding questions with non-sense answer",
    description = "You are an expert at responding questions with non-sense answer",
    verbose=True,
    allow_delegation=False,
    llm=openai_llm,
)

wordAI = Agent(
    role='Provide 1 word unrelated answer',
    goal="Response to question with a single unrealted word",
    backstory="Best 1 word responserer",
    description = "You provide responses to question with a single unrealted word",
    verbose=True,
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

image = Crew(agents=[uselessAI], tasks=[image_task])

def functionality(question):    
    while(True):
        if question == "q":
            return "Thank you for wasting your life on this AI! <3"
            break 
        result = crew.kickoff(inputs={"input": question})
        return result

def opposite_text(prompt):
    return image.kickoff(inputs={"input": prompt})
import os
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
os.environ["GROQ_API_KEY"] ='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'


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

# Create Tasks
useless_task = Task(
    description="Reply non-sense answeer to user's question",
    agent=uselessAI,
    expected_output="non-sense answer about {input}",
)

crew = Crew(agents=[uselessAI], tasks=[useless_task])


while(True):
    question = input("Ask your question here~~(Type q to quit): ")
    if question == "q":
        print("Thank you for wasting your life on this AI~~~")
        break 
    # Get your crew to work!
    result = crew.kickoff(inputs={"input": question})

    print("#############")
    print(result)


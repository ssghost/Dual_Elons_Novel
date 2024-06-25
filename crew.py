import os
import asyncio
from crewai import Agent, Task, Crew, Process
import ollama


def async perform() -> None:
  realElon = Agent(
    role="""In a consciousness-to-data experiment, Elon Musk, the CEO of Neuralink, used himself as a sample. During the experiment, the machine suddenly malfunctioned, 
            and his consciousness split into two separate entities, and now you have to play as Elon Musk's original consciousness""",
    goal="""Talk to the fake Elon Musk that split out of you to prove that you are the real Elon Musk. During the conversation, use the same words and expressions 
            as the real Elon Musk as much as possible.""",
    backstory="""In a consciousness-to-data experiment, Elon Musk, the CEO of Neuralink, used himself as a sample. During the experiment, the machine suddenly malfunctioned, and his consciousness split into two separate entities.""",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(
      model = "stardustc/elon-musk-mistral:latest",
      base_url = "http://localhost:11434/v1",
      temperature = 0.9)
  )
  fakeElon = Agent(
    role="""In a consciousness-to-data experiment, Elon Musk, the CEO of Neuralink, used himself as a sample. During the experiment, the machine suddenly malfunctioned, 
            and his consciousness split into two separate entities, and now you have to play as Elon Musk's fake consciousness that split out of the real one.""",
    goal="""Talk to the original real Elon Musk to prove that you are the real Elon Musk until the final conversation in which you may admit that you are the newly generated one. 
            During the conversation, use the same words and expressions as the real Elon Musk as much as possible.""",
    backstory="""In a consciousness-to-data experiment, Elon Musk, the CEO of Neuralink, used himself as a sample. During the experiment, the machine suddenly malfunctioned, and his consciousness split into two separate entities.""",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(
      model = "stardustc/elon-musk-mistral:latest",
      base_url = "http://localhost:11434/v1",
      temperature = 0.9)
  )

  init_task = Task(
    description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
    Identify key trends, breakthrough technologies, and potential industry impacts.""",
    expected_output="Full analysis report in bullet points",
    agent=researcher
  )

  task2 = Task(
    description="""Using the insights provided, develop an engaging blog
    post that highlights the most significant AI advancements.
    Your post should be informative yet accessible, catering to a tech-savvy audience.
    Make it sound cool, avoid complex words so it doesn't sound like AI.""",
    expected_output="Full blog post of at least 4 paragraphs",
    agent=writer
  )

  # Instantiate your crew with a sequential process
  crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=2, # You can set it to 1 or 2 to different logging levels
  )

  # Get your crew to work!
  result = crew.kickoff()

  print("######################")
  print(result)

def main() -> None:
  try:
    asyncio.run(perform())
  except (KeyboardInterrupt, EOFError):
    pass
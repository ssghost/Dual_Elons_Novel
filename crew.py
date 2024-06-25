import os
import asyncio
from crewai import Agent, Task, Crew, Process
import ollama


def async perform() -> None:
  realElon = await Agent(
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

  fakeElon = await Agent(
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

  task_init =  await Task(
    description="""Now you are about to start a conversation with another Elon Musk's consciousness. Please explain in 500 words or less why you are the real Elon Musk, 
                   and ask questions about the other one's suspicious points.""",
    expected_output="State a strong similarity in personality between yourself and the real Elon Musk and ask a question that you think only Elon Musk can answer. All of this is within 500 words.",
    agent=realElon
  )

  task_real2fake = Task(
    description="""Using the insights provided, develop an engaging blog
    post that highlights the most significant AI advancements.
    Your post should be informative yet accessible, catering to a tech-savvy audience.
    Make it sound cool, avoid complex words so it doesn't sound like AI.""",
    expected_output="Full blog post of at least 4 paragraphs",
    agent=writer
  )

  task_fake2real = Task(
    description="""Using the insights provided, develop an engaging blog
    post that highlights the most significant AI advancements.
    Your post should be informative yet accessible, catering to a tech-savvy audience.
    Make it sound cool, avoid complex words so it doesn't sound like AI.""",
    expected_output="Full blog post of at least 4 paragraphs",
    agent=writer
  )

  task_final = await Task(
    description="""Now you are about to admit that you are the fake personality of Elon Musk generated by the failed experiment. 
                   Please state this fact in 500 words or less and end this conversation.""",
    expected_output="Admit that you are a fake Elon Musk personality and apologize in a typical Elon Musk way. All of this is within 500 words.",
    agent=fakeElon
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
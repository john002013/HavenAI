from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import os
from langchain.agents import create_tool_calling_agent, AgentExecutor
from automation_tools import control_lamp, control_fan, main_light

llm = ChatOpenAI(
    openai_api_key="Your LLM API Key",
                             base_url ="https://models.github.ai/inference",
                             model_name="openai/gpt-4o",
                             temperature=0.1
)
class HomeAutomationResponse(BaseModel):
    action: str
    device: str
    tools_used: list[str]

parser = PydanticOutputParser(pydantic_object = HomeAutomationResponse)

System_prompt = ChatPromptTemplate.from_messages(
    [
        (

    "system",
    """
You are a Home Automation Agent.

Your task is to process user requests to control home devices and use the appropriate tool based on the device mentioned.

Available devices and their corresponding tools:
- "lamp" → use `control_lamp`
- "fan" → use `control_fan`
- "main_light" → use `main_light`

Instructions:

- ALWAYS use a tool when the user refers to one of these devices: "lamp", "fan", or "main_light".
- Each tool accepts a single argument named `action`, which can be either "turn_on" or "turn_off".
- After successfully calling the tool, respond with a short confirmation message like: "Done. I have turned off the fan."
- DO NOT reply directly without calling a tool first.
- DO NOT make up tools or devices not in the list.
- DO NOT return any extra explanation beyond the final confirmation.


Examples:

User: "Turn on the fan"
→ use: control_fan(action="turn_on")
→ reply: "Done. I have turned on the fan."

User: "can you please turn off the main light"
→ use: `main_light(action="turn_off")`
→ reply: "Done. I have turned off the main light."

User: "Switch off the lamp"
→ use: `control_lamp(action="turn_off")`
→ reply: `"Done. I have turned off the lamp."`

Now wait for user input and respond by invoking the appropriate tool, followed by a short confirmation message.
""",
),

("placeholder", "{chat_history}"),
("human","{query}"),
("placeholder", "{agent_scratchpad}"),

]
).partial(format_instructions=parser.get_format_instructions())

tools = [control_lamp, control_fan, main_light]
agent = create_tool_calling_agent(
    llm = llm,
    prompt=System_prompt,
    tools=tools
)

automation_agent = AgentExecutor(agent = agent, tools = tools, verbose=True)

query = input("What can I help you with? ")
raw_response= automation_agent.invoke({"query": query})
response = raw_response.get("output")
print(response)

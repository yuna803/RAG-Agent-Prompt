from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import *
from agent.tools.middleware import *
class ReactAgent:
    def __init__(self):
        self.agent =create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[rag_summarize, get_weather, get_user_location, fetch_external_data,
                   fill_context_for_report,get_user_id, get_current_month],
            middleware=[monitor_tool, log_before_model, report_prompts_switch]
        )

    def execute_stream(self, query: str):
        input_dict ={
            "messages":[
                {"role": "user", "content": query},

            ]
        }

        for chunk in self.agent.stream(input_dict,stream_mode="values",context={"report":False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                print(latest_message.content)
                yield latest_message.content.strip() +"\n"

if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("扫地机器人在我在的地区怎么保养"):
        print(chunk, end="", flush=True)
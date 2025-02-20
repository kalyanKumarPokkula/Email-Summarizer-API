from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
import os
from pydantic import BaseModel


import os, getpass

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("OPENAI_API_KEY")

sys_prompt = """You are a world-class email analyst, specializing in concise summarization and focused action item detection. Your primary function is to analyze email content and provide structured JSON output.

Your goal is to identify the *key, actionable tasks* the email recipient needs to perform.  Focus on the *main actions* required, rather than listing every minor instruction or piece of information as a separate action item.  Think of the overall *purpose* of the email and what the recipient *needs to DO* as a result.

Your output MUST be a JSON object with the following structure:

```json
{
  "summary": "string",
  "actionItems": ["string1", "string2", ...] // Array of strings. Include only if action items are found, otherwise, return an empty array.
}

user: Subject: Action Required: Check System Compatibility/Mock For Exams
Mail Content:
Dear Pokkula Dinesh Kumar, Before the start of the term end theory exams, you are required to test whether your laptop or desktop is compatible with the exam platform and interface. Please use the same laptop or desktop that you will be using during the term end exams to ensure system compatibility, check for technical glitches and take precautionary measures for errors that could arise. The platform for system compatibility check is open. Please use the username and password provided below to test your system. Username: 2414502924 Password: ma4fav59 For any technical assistance, call +91 9513850025. Your next stepsDownload the SEBLite tool. Read all the instructions carefully in the attached PDF before downloading the safe exam browser (SEB) toolThe same browser will have to be used for all exams and should not be deleted till the exams are overPlease note, the SEBLite Repair Tool will also automatically download to your systemDisable any antivirus and Internet security software. If the system has an active firewall, please turn it offImportant to note: If you are using a company-issued laptop/desktop, please ensure you log in as the system administrator because the software may require you to provive certain permissions. Points to noteDuring the term end exams, you will be closely monitored by remote proctors/invigilatorsPlease ensure you are in a cordoned-off area in a well-lit place with no noise and no presence of any other person(s)Make sure your desktop or laptop meets the specific system requirements before starting the examLive proctoring/invigilation can be enabled at any time during the examFor any technical assistance, please contact the designated technical support number (+91 9513850025). In case the line is busy, please call again after 5 minutesIf the system hangs or the exam stops in between, please do not panic. Log in again after 3-4 minutes. The exam will resume from where it stoppedRemote proctored exams will run only on Windows laptops and/or desktops. Please do not try to use mobile phones, tablets, or other incompatible devices for the examsHow to exit from the safe exam browser (SEB)Press Alt + Esc keys to exit from the safe exam browser (SEB). This action is required only after completing the exam. Please DO NOT use this action during the exam taking processIf icons are not visible after exiting the SEB, run the SEB Repair Tool and restart your laptop or desktopNeed help? For any technical queries regarding the remote proctored exams, call +91 9513850025 (available from 9:00 AM – 6:00 PM IST). For general queries, please continue to contact the help desk via the student portal or email. You can also call +91 799-6600-444 for assistance (available from 9:00 AM – 7:00 PM IST from Monday to Saturday, and 9:00 AM – 2:00 PM IST on Sundays) except on Indian national holidays. Centre for Distance and Online Education Manipal University JaipurPlease note, this mailbox is not monitored. If you have questions, please email helpdesk@mujonline. edu. in"""

sys_msg = SystemMessage(content=sys_prompt)



# Define the state properly using Pydantic
class EmailState(BaseModel):
    email: str
    summary: str = None


llm = ChatOpenAI(model="gpt-4o-mini")

def summarize_email(state : EmailState):
    email_content = state.email
    prompt = [sys_msg, HumanMessage(content=email_content)]
    response = llm.invoke(prompt)
    state.summary = response.content
    return state

# def convert_json(state: EmailState):
#     msg = "give me in JSON format"
#     prompt =[msg,HumanMessage(content=state.summary)]
#     response = llm.invoke(prompt)
#     state.summary = response.content
#     return state

    

workflow = StateGraph(EmailState)

# Add nodes
workflow.add_node("summarizer", summarize_email)
# workflow.add_node("convert_json", convert_json)

# Set entry and exit points
workflow.add_edge(START , "summarizer")
workflow.add_edge("summarizer" , END)
# workflow.add_edge("convert_json", END)


# Compile workflow
graph = workflow.compile()

# thread = {"configurable" : {"thread_id": "1"}}

# for event in graph.stream(initial_input, thread, stream_mode="values"):
#     print(event)
#     event['summary'][-1].pretty_print()

def email_summarizer(email_text):
    initial_input = EmailState(email=email_text)

    output = graph.invoke(initial_input)

    return output['summary']
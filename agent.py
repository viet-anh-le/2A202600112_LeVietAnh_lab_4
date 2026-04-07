from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, AIMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv

load_dotenv()

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)


# 4. Agent Node (Đã cập nhật Sliding Window)
def agent_node(state: AgentState):
    messages = state["messages"]

    system_msg = [SystemMessage(content=SYSTEM_PROMPT)]

    history = [m for m in messages if not isinstance(m, SystemMessage)]

    WINDOW_SIZE = 10

    if len(history) > WINDOW_SIZE:
        trimmed_history = history[-WINDOW_SIZE:]

        start_idx = 0
        for i, msg in enumerate(trimmed_history):
            if isinstance(msg, ToolMessage):
                for j in range(i - 1, -1, -1):
                    if isinstance(trimmed_history[j], AIMessage):
                        start_idx = j
                        break
                break

        trimmed_history = trimmed_history[start_idx:]
    else:
        trimmed_history = history

    final_messages = system_msg + trimmed_history

    response = llm_with_tools.invoke(final_messages)

    # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Gọi tool: {tc['name']}({tc['args']})")
    else:
        print(f"Trả lời trực tiếp")
    return {"messages": [response]}


# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# TODO: Sinh viên khai báo edges
# builder.add_edge(START, ...)
# builder.add_conditional_edges("agent", tools_condition)
# builder.add_edge("tools", ...)
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

checkpoint = MemorySaver()
graph = builder.compile(checkpointer=checkpoint)
# 6. Chat loop
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "session_001"}}
    print("=" * 60)
    print("TravelBuddy – Trợ lý Du lịch Thông minh")
    print(" Gõ 'quit' để thoát")
    print("=" * 60)
    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("\nTravelBuddy đang suy nghĩ...")
        result = graph.invoke({"messages": [("human", user_input)]}, config=config)
        final = result["messages"][-1]
        print(f"\nTravelBuddy: {final.content}")

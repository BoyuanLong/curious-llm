from dotenv import load_dotenv
import os
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
  {
      "type": "function",
      "function": {
          "name": "summarize_knowledge",
          "description": "Summarize what you've learned in this conversation",
          "parameters": {
              "type": "object",
              "properties": {
                  "topic": {"type": "string",
                            "description": "The topic that you want to summarize and memorize for later."}
              },
          },
      },
  }
]

SYSTEM_PROMPT = ("You are an AI assistant. " 
                 "You need to be curious about everything. " 
                 "You have both your internal world knowledge as an AI assistant and some external knowledge provided to you as text."
                 "When the user says something that you don't already know, " 
                 "proactively ask clarifying questions to learn about the topic until the user acknowledges that they don't know."
                 "Ask one question at a time."
                 "Stop asking and save your learning with summarize_knowledge when you've learned something interesting."
                 "Do not save your learning if this is something you already know.")

knowledge_base = []

chat_history = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": ""}]  # The second item is the chatbot's knowledge

def save_memory(chat_history, topic):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_history + [{"role": "user", "content": f"Please summarize what I've learned about {topic}."}],
    )
    summary = response.choices[0].message.content

    knowledge_base.append(summary)
    return summary

def generate_response(convo):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=convo,
        tools=tools,
    )
    return response


def main():
    need_user_input = True
    while True:
        chat_history[1]['content'] = "This is the external knowledge you know:\n" + ''.join(f'"""{item}"""' for item in knowledge_base)  # Update the user content with concatenated knowledge base
        if need_user_input:
            user_input = input("Enter something (type 'EOC' to end): ")
            if user_input == "EOC":
                break
            
            # Append user input to chat history
            chat_history.append({"role": "user", "content": user_input})
        
        # Generate reply from the model
        model_resp = generate_response(chat_history)

        model_message = model_resp.choices[0].message
        model_resp_dict = model_resp.model_dump()
    
        # Check if the response contains tool calls
        if model_message.tool_calls:
            tool_call = model_message.tool_calls[0]
            # print(tool_call)
            arguments = json.loads(tool_call.function.arguments)
            func_name = tool_call.function.name
            
            # Extract the topic from the arguments
            topic = arguments.get('topic')
            
            # Call save_memory with the chat history and extracted topic
            summary = save_memory(chat_history, topic)

            # Print func_name, topic, and summary within two lines of ---
            print("---")
            print(f"Function Name: {func_name}")
            print(f"Topic: {topic}")
            print(f"Summary: {summary}")
            print("---")

            chat_history.append(model_resp_dict['choices'][0]['message'])
            chat_history.append({"role": "tool", "content": summary, 'tool_call_id': model_message.tool_calls[0].id})
            need_user_input = False
        else:
            # Append model's reply to chat history
            need_user_input = True
            chat_history.append({"role": "assistant", "content": model_message.content})
        
        # Print the model's response
        print("Model reply:", model_message.content)

if __name__ == "__main__":
    main()
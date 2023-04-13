import streamlit as st
import json
import httpx
import pandas as pd
import pydeck as pdk

st.title("ChatGPT Streamlit App")

url = "http://127.0.0.1:8000/chat"

default_messages = [
  {
    "role": "system",
    "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English."
  },
  {
    "role": "user",
    "content": "Return a nice looking report for me in markdown titled 55 words from 5!  It should have the first 55 words from each of 5 famous speeches.  For each speech include information about the speech and time period.  What were the conditions like?  Why was the speech made?  Include where, when, why, and who.  Then include a summary of whether or not it was impactful and why.  Make it presentation ready."
  }
]
messages_str = st.text_area("Edit Messages", json.dumps(default_messages, indent=2))

if st.button("Submit"):
    messages = json.loads(messages_str)

    payload = {
        "model": "gpt-35-turbo",
        "messages": messages,
        "stream": True
    }


    st.markdown("----")
    response_box = st.empty()

    # Set the read timeout to 10 seconds
    timeout = (2, 30)

    headers = {"Content-Type": "application/json"}

    with httpx.stream('POST', url, json=payload, timeout=timeout ) as r:
        response=""
        for chunk in r.iter_raw():  

            print(chunk)

            response += chunk.decode("utf-8")
            response_box.markdown(response, unsafe_allow_html=True)
                        # try:
            #     # Decode the byte stream and parse the JSON data
            #     chunk_data = json.loads(chunk.decode("utf-8"))

            #     response = []

            #     # Access the 'choices' attribute from the parsed JSON data
            #     response.append(chunk_data['choices'][0]['text'])
            #     result = "".join(response).strip()
            #     result = result.replace("\n", "")        
            #     response_box.markdown(f'*{result}*') 

            # except json.JSONDecodeError:
            #     # Ignore the invalid JSON data
            #     pass            # Decode the byte stream and parse the JSON data
            # chunk_data = json.loads(chunk.decode("utf-8"))

    st.markdown("----")


    # with httpx.stream('POST', url, json=payload) as r:
    #     st.write("Streaming response:")
    #     output_area = st.empty()

    #     for chunk in r.iter_raw():
    #         output_area.text(chunk.decode("utf-8"))
    #         print(chunk)

# from utils import config_azure_openai

# openai = config_azure_openai()

# response = openai.ChatCompletion.create(
#     engine="gpt-4-32k", # engine = "deployment_name".
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
#         {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
#         {"role": "user", "content": "Do other Azure Cognitive Services support this too?"}
#     ]
# )

# print(response)
# st.write(response['choices'][0]['message']['content'])

# https://towardsdatascience.com/build-your-own-chatgpt-like-app-with-streamlit-20d940417389
# https://github.com/AI-Yash/st-chat
# https://www.youtube.com/watch?v=W7kDwsWFjvE
# https://blog.futuresmart.ai/building-a-gpt-4-chatbot-using-chatgpt-api-and-streamlit-chat
# https://medium.com/@avra42/how-to-stream-output-in-chatgpt-style-while-using-openai-completion-method-b90331c15e85
# https://www.youtube.com/watch?v=cHjlperESbg&list=PLqQrRCH56DH8JSoGC3hsciV-dQhgFGS1K&index=1
# https://www.youtube.com/watch?v=CqqELxWGUy8&list=PLqQrRCH56DH8JSoGC3hsciV-dQhgFGS1K&index=4
# https://www.pinecone.io/learn/langchain-intro/
# https://medium.com/@kamaljp/meet-langchains-cutting-edge-agents-4-revolutionary-ai-llm-powered-decision-makers-8677045e8a69
# https://github.com/avrabyt


# SEE THIS
# https://platform.openai.com/docs/guides/chat
# https://platform.openai.com/docs/guides/chat/introduction
# https://platform.openai.com/docs/guides/chat/instructing-chat-models
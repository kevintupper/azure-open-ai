from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel as PydanticBaseModel
from typing import List, Any, Optional, Union, Dict
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff
from utils import config_azure_openai

import json
import time

#======================================================================================================================
# Great documentation on this technique: 
#======================================================================================================================
#  https://tmmtt.medium.com/how-to-stream-chatgpt-api-responses-b783f1e5f13d
#  https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb
#  https://stackoverflow.com/questions/75740652/fastapi-streamingresponse-not-streaming-with-generator-function
# https://github.com/openai/openai-cookbook/blob/main/examples/How_to_handle_rate_limits.ipynb
#======================================================================================================================

# Get the OpenAI API object
openai = config_azure_openai()

app = FastAPI()


class BaseModel(PydanticBaseModel):
    def dict(self, **kwargs) -> Dict[str, Any]:
        return super().dict(exclude_none=True, **kwargs)

class Message(BaseModel):
    role: str
    content: str
    name: Optional[str] = None


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 1
    top_p: Optional[float] = 1
    n: Optional[int] = 1
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = 0
    frequency_penalty: Optional[float] = 0
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

def get_streaming_response(request: ChatRequest):

    try:

        response = completion_with_backoff(
            # CHATPG GPT API REQQUEST
            engine=request.model,
            messages=[message.dict() for message in request.messages],
            temperature=request.temperature,
            top_p=request.top_p,
            n=request.n,
            stream=True,
            stop=request.stop,
            max_tokens=request.max_tokens,
            presence_penalty=request.presence_penalty,
            frequency_penalty=request.frequency_penalty,
            logit_bias=request.logit_bias or {},
            user=request.user or ""
        )

        for chunk in response: 
            chunk_text = chunk['choices'][0]['delta'] 
            answer = chunk_text.get('content', '')
            yield answer.encode('utf-8')

    except openai.error.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")

    except openai.error.AuthenticationError as e:
        # Handle Authentication error here, e.g. invalid API key
        print(f"OpenAI API returned an Authentication Error: {e}")

    except openai.error.APIConnectionError as e:
        # Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")

    except openai.error.InvalidRequestError as e:
        # Handle connection error here
        print(f"Invalid Request Error: {e}")

    except openai.error.RateLimitError as e:
        # Handle rate limit error
        print(f"OpenAI API request exceeded rate limit: {e}")

    except openai.error.ServiceUnavailableError as e:
        # Handle Service Unavailable error
        print(f"Service Unavailable: {e}")

    except openai.error.Timeout as e:
        # Handle request timeout
        print(f"Request timed out: {e}")
        
    except:
        # Handles all other exceptions
        print("An exception has occured.")

@app.post("/chat")
def process_chat_request(request: ChatRequest):
    return StreamingResponse(get_streaming_response(request), media_type='text/event-stream')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)
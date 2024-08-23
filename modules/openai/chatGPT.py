from modules.openai.openai_client import get_openai_api_client
from utils.constants import SYSTEM_ROLE


class chatGPT():
    def __init__(self) -> None:
        self.client = get_openai_api_client()

    def make_request(self, input_text:str, current_code:str) -> str:
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": SYSTEM_ROLE
                },
                {
                    "role": "user", 
                    "content": f"I need you to make the specified changes:{input_text}\nApply this on the current code{current_code}"
                }
            ]
        )
        return completion.choices[0].message.content

    def stream_response(self, input_text):
        stream = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": SYSTEM_ROLE
                },
                {
                    "role": "user", 
                    "content": f"{input_text}"
                }
            ],
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")

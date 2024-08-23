import os

from openai import OpenAI


def get_openai_api_client():
	client = OpenAI(
		api_key=os.environ.get("OPENAI_API_KEY"),
	)
	return client


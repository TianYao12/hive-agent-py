import os
import logging

from dotenv import load_dotenv

load_dotenv()

if "LANGTRACE_API_KEY" in os.environ:
    from langtrace_python_sdk import langtrace

    langtrace.init(api_key=os.getenv("LANGTRACE_API_KEY"))

from llama_index.llms.openai import OpenAI
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.ollama import Ollama
from llama_index.llms.mistralai import MistralAI
from llama_index.core.settings import Settings
from hive_agent.config import Config


def init_llm_settings(config):
    model = config.get("model", "model", "gpt-3.5-turbo")
    if "gpt" in model:
        Settings.llm = OpenAI(
            model=model, request_timeout=config.get("timeout", "llm", 30)
        )
        logging.info(f"OpenAI model selected")
    elif "claude" in model:
        Settings.llm = Anthropic(model=model, api_key=os.getenv("ANTHROPIC_API_KEY"))
        logging.info(f"Claude model selected")
    elif "llama" in model:
        Settings.llm = Ollama(
            model="llama3", request_timeout=config.get("timeout", "llm", 30)
        )
        logging.info(f"Ollama model selected")
    elif "mixtral" or "mistral" in model:
        Settings.llm = MistralAI(model=model, api_key=os.getenv("MISTRAL_API_KEY"))
        logging.info(f"Mistral model selected")
    else:
        Settings.llm = OpenAI(
            model=model, request_timeout=config.get("timeout", "llm", 30)
        )
        logging.info(f"Default OpenAI model selected")

    Settings.chunk_size = 1024
    Settings.chunk_overlap = 20

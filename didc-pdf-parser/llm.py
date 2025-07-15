
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings


from models import SimpleReport, ExplicitIKCReport, ExplicitAKHReport
from typing import Optional
import os

system_prompt = """
You are a medical report parser. Your task is to extract structured data from medical reports written in Markdown format.

Please follow these instructions:
1. Parse the Markdown document and extract all relevant information into the schema defined.
2. Ensure all fields are extracted, including patient ID, project, sections, and their data.
3. Pay attention to special characters like asterisks (*) which indicate out-of-range values.
4. Handle comments that may follow blood values, ensuring they are not confused with references. Do not mismatch this with the reference which usually looks like "202.3 - 416.5 or < 0.5. 
5. Extract the birth year and the genden. Those are usually just after the patient ID. The gender is (M) or (W).

Add all the test available.
"""


def extract_structured(
    text: str, 
    model_name: str, 
    base_url: str, 
    schema: str = "IKC",
    api_key: Optional[str] = None,
    temperature: float = 0.1,
    top_p: float = 1.0,
    top_k: int = 0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    repetition_penalty: float = 1.1,
    min_p: float = 0.0,
    top_a: float = 0.0,
    max_tokens: int = 32000
):

    model = OpenAIModel(
        model_name=model_name,
        provider=OpenAIProvider(base_url=base_url, api_key=api_key),
    )

    model_settings = ModelSettings(
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        repetition_penalty=repetition_penalty,
        min_p=min_p,
        top_a=top_a,
        max_tokens=max_tokens
    )

    schemas = {
        "IKC": ExplicitIKCReport,
        "AKH": ExplicitAKHReport
    }

    agent = Agent(model, output_type=schemas[schema], model_settings=model_settings, system_prompt=system_prompt, retries=3)

    result = agent.run_sync(text)

    print(result.usage())
    return result.output
from pathlib import Path
from docling.document_converter import DocumentConverter   # swap for olmocr if preferred
from pydantic_ai import Agent
#from llama_cpp import Llama
from jambo.schema_converter import SchemaConverter
import json
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from pydantic import BaseModel
from typing import List

import os

class Sample(BaseModel):
    sample_id: str
    date: str  # Expected format: dd.mm.yy
    time: str  # Expected format: hh:mm

class SectionData(BaseModel):
    substance: str
    result: str
    unit: str
    reference: str

class Section(BaseModel):
    section_name: str
    data: List[SectionData]

class ReportSchema(BaseModel):
    title: str
    report: str
    project: str
    patient_id: str
    samples: Sample
    sections: List[Section]

# # Load the JSON schema
# with open('/app/schemas/schema.json', 'r') as schema_file:
#     schema = json.load(schema_file)

# BloodSample = SchemaConverter.build(schema)

def parse_document(path: Path) -> str:
    doc = DocumentConverter().convert(path)
    # choose level of granularity: whole document, specific pages, etc.
    return doc.document.export_to_markdown()            # plain text is fine for LLM

# def extract_structured(text: str) -> BloodSample:
#     agent = Agent(
#         Llama("mistral-7b-instruct.gguf"),               # local weights
#         system_prompt="You are a careful data extractor…",
#         output_type=BloodSample,
#     )
#     return agent.run_sync(text)



system_prompt = """
Please parse the the following HTML document and extract the relevant information into the schema defined.
"""

def extract_structured(text: str) -> ReportSchema:
    # ollama_model = OpenAIModel(
    #     model_name='phi4', provider=OpenAIProvider(base_url='http://localhost:11434/v1')
    # )
    model = OpenAIModel(
        model_name='anthropic/claude-3.5-sonnet',
        provider=OpenAIProvider(base_url='https://openrouter.ai/api/v1',
                                api_key=os.getenv("OPENROUTER_API_KEY"))
    )

    agent = Agent(model, output_type=ReportSchema,  system_prompt=system_prompt)

    result = agent.run_sync(text, system_prompt=system_prompt)


    print(result.usage())
    return result.output

if __name__ == "__main__":
    raw_text = parse_document("/app/data/AKH_3666766.pdf")
    print(raw_text)
    structured = extract_structured(raw_text)
    Path("output.json").write_text(structured.model_dump_json())

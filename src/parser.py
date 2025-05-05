# import transformers

# pipeline = transformers.pipeline(
#     "text-generation",
#     model="microsoft/phi-4",
#     model_kwargs={"torch_dtype": "auto"},
#     device_map="auto",
# )

# messages = [
#     {"role": "system", "content": "You are a medieval knight and must provide explanations to modern people."},
#     {"role": "user", "content": "How should I explain the Internet?"},
# ]

# outputs = pipeline(messages, max_new_tokens=128)
# print(outputs[0]["generated_text"][-1])

from pydantic import BaseModel
from pydantic_ai import Agent
import json
from jambo.schema_converter import SchemaConverter

# Load the JSON schema
with open('schema.json', 'r') as schema_file:
    schema = json.load(schema_file)

BloodSample = SchemaConverter.build(schema)

system_prompt = """
Please parse the the following HTML document and extract the relevant information into the schema defined.
"""

with open('data.html', 'r') as file:
    data = file.read()


from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

ollama_model = OpenAIModel(
    model_name='phi4', provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)

agent = Agent(ollama_model, output_type=BloodSample,  system_prompt=system_prompt)

result = agent.run_sync(data, system_prompt=system_prompt)

print(result.output)
print(result.usage())
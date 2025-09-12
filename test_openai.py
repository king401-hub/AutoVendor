from openai import OpenAI

client = OpenAI(
  api_key="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"
)

response = client.responses.create(
  model="gpt-4o-mini",
  input="write a haiku about ai",
  store=True,
)

print(response.output_text);

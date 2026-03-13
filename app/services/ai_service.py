import re
import json

import os
from openai import OpenAI
from dotenv import load_dotenv

import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_llm_output(raw_output: str) -> str:
    # Remove markdown fences like ```json ```
    cleaned = re.sub(r"```json|```", "", raw_output)

    # Extract first JSON object
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        return match.group(0).strip()

    return cleaned.strip()

def extract_invoice_data(text: str) -> str:

    prompt = f"""
You are an AI invoice extraction system.

Extract invoice information from the text below.

Rules:
- Map variations like 'Invoice No', 'Invoice #', 'Inv ID' to invoice_number.
- Do not guess missing values.
- If field not found, return null.
- Return ONLY valid JSON.
- Do not add explanations.
- If value is missing, return null.
- Do not invent data.
- Return STRICT JSON.
- Do not wrap in markdown.
- Do not add commentary.
- If unsure, return null.
- Return STRICTLY valid JSON.
- Do NOT include markdown.
- Do NOT include explanations.
- Do NOT rename keys.
- If a field value is missing, return null.
- Confidence must be between 0 and 1.
- If no line items are found, return an empty list [] for "line_items".

Return in this exact schema:

{{
  "invoice_number": {{ "value": "", "confidence": 0.0 }},
  "invoice_date": {{ "value": "", "confidence": 0.0 }},
  "vendor_name": {{ "value": "", "confidence": 0.0 }},
  "buyer_name": {{ "value": "", "confidence": 0.0 }},
  "total_amount": {{ "value": "", "confidence": 0.0 }},
  "vat_amount": {{ "value": "", "confidence": 0.0 }},
  "currency": {{ "value": "", "confidence": 0.0 }},
  "line_items": [
    {{
      "description": "",
      "quantity": "",
      "unit_price": "",
      "total": ""
    }}
  ]
}}

Invoice text:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a strict JSON extraction engine. Return ONLY valid JSON. No explanations. No markdown. No extra text."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],        
        temperature=0
    )

    raw_output = response.choices[0].message.content
    cleaned_output = clean_llm_output(raw_output)

    try:
        parsed = json.loads(cleaned_output)
    except Exception:
        return {"error": "Invalid JSON returned from AI", "raw_output": raw_output}

    return parsed
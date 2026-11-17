from httpx import AsyncClient
from dotenv import load_dotenv
import os
from fastapi import HTTPException
import logging
from pydantic import ValidationError

from models.schemas import AIOutput
import httpx
from json import JSONDecodeError


logger = logging.getLogger(__name__)
load_dotenv()

ai_api_key = os.getenv("AI_API_KEY")
if not ai_api_key:
    raise ValueError('AI API key is missing')
url = os.getenv("AI_URL")
if not url:
    raise ValueError('AI URL is missing')



async def get_ai_output(text: str):
    async with AsyncClient(timeout=60) as client:
        payload = {
            "model": "nvidia/nemotron-3.5-bolt-e4b",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a text analysis assistant. "
                        "Summarize the user's text in one short sentence. "
                        "Classify its sentiment as positive, negative, or neutral. "
                        "Return ONLY a valid JSON object with exactly two fields: "
                        "summary and sentiment. "
                        "Do not include markdown or explanations."
                    )
                },
                {"role": "user", "content": text}
            ],
            "temperature": 1,
            "top_p": 0.95,
            "max_tokens": 512,
            "stream": False,
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        }

        try:
            response = await client.post(url,headers={
                "Authorization": f"Bearer {ai_api_key}",
                "Content-Type": "application/json"
            } , json=payload)

            response.raise_for_status()

        except httpx.HTTPStatusError as e:

            logger.error("NVIDIA API returned HTTP %s",
                         e.response.status_code)
            raise HTTPException(
                status_code=502,
                detail="AI server error"
            )


        except httpx.TimeoutException:
            logger.error("Nvidia API timed out")

            raise HTTPException(
                status_code=504,
                detail="Timeout error. Please try again."
            )

        except httpx.RequestError:
            logger.error("NVIDIA API connection error")

            raise HTTPException(
                status_code=502,
                detail="Internal server error. Please try again."
            )
        try:
            content = response.json()["choices"][0]["message"]["content"]
            if not isinstance(content, str) or len(content.strip()) == 0:
                logger.error("NVIDIA API response is empty or incorrect format")
                raise HTTPException(
                    status_code=502,
                    detail="Internal server error. Please try again."
                )
        except  (IndexError, JSONDecodeError, KeyError, TypeError) as e:
            logger.error("Invalid NVIDIA API response structure")
            raise HTTPException(
                status_code=502,
                detail="Internal server error. Please try again."
            )



        try:
            result = AIOutput.model_validate_json(content)
        except ValidationError:

            logger.exception("Validation error")
            raise HTTPException(
                status_code=502,
                detail="Internal server error. Please try again."
            )


        return result



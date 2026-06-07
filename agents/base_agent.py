import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from openai import OpenAI, AsyncOpenAI
from anthropic import Anthropic
from loguru import logger
from config.settings import settings


class MemoryBuffer(list):
    """List wrapper that keeps memory size bounded."""

    def __init__(self, max_items: int, *args):
        super().__init__(*args)
        self.max_items = max_items

    def _trim(self):
        if len(self) > self.max_items:
            del self[: -self.max_items]

    def append(self, item):
        super().append(item)
        self._trim()

    def extend(self, iterable):
        super().extend(iterable)
        self._trim()

    def insert(self, index, item):
        super().insert(index, item)
        self._trim()

    def __iadd__(self, iterable):
        result = super().__iadd__(iterable)
        self._trim()
        return result


class BaseAgent:
    """Base class for all AI agents"""

    def __init__(self, agent_name: str, model: Optional[str] = None):
        self.agent_name = agent_name
        # Prefer explicit model, then settings, then safe default
        self.model = model or getattr(settings, "OPENAI_MODEL", "gpt-3.5-turbo")
        if model is None and self.model != "gpt-3.5-turbo":
            logger.info(f"Using configured OPENAI_MODEL: {self.model}")
        if self.model == "gpt-4-turbo-preview":
            logger.warning(
                "Model gpt-4-turbo-preview is deprecated or unavailable."
                " Set OPENAI_MODEL env var to a supported model."
            )

        # Initialize clients
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.async_openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        else:
            self.anthropic_client = None

        self.max_memory = 10
        self.memory = MemoryBuffer(
            self.max_memory * 2
        )  # Conversation memory bounded by message count

    async def think(self, prompt: str, system_prompt: str = None) -> str:
        """Core reasoning capability using OpenAI"""

        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Add recent conversation history
        recent_memory = self.memory[-self.max_memory :]
        messages.extend(recent_memory)

        # Add current prompt
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self.async_openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
            )

            result = response.choices[0].message.content

            # Store in memory
            self.memory.append({"role": "user", "content": prompt})
            self.memory.append({"role": "assistant", "content": result})

            return result

        except Exception as e:
            logger.error(f"Agent {self.agent_name} error: {e}")
            return None

    async def analyze_with_structure(self, prompt: str, output_schema: Dict) -> Dict:
        """Get structured JSON output from LLM"""

        system_prompt = f"""You are {self.agent_name}, an expert AI agent.
        Always respond in valid JSON format matching this exact schema:
        {json.dumps(output_schema, indent=2)}
        
        Rules:
        1. Return ONLY the JSON object, no other text
        2. Use double quotes for all strings
        3. Ensure all required fields are present
        4. Use null for unknown values, not "N/A" """

        for attempt in range(3):  # Retry up to 3 times
            try:
                response = await self.think(prompt, system_prompt)

                # Clean response
                response = response.strip()
                if response.startswith("```json"):
                    response = response[7:]
                if response.startswith("```"):
                    response = response[3:]
                if response.endswith("```"):
                    response = response[:-3]

                return json.loads(response)

            except json.JSONDecodeError as e:
                logger.warning(f"JSON parse attempt {attempt + 1} failed: {e}")
                if attempt == 2:
                    logger.error("Failed to get valid JSON after 3 attempts")
                    return {"error": "Failed to parse response", "raw": response}

        return {}

    def clear_memory(self):
        """Clear conversation memory"""
        self.memory = MemoryBuffer(self.max_memory * 2)
        logger.info(f"Memory cleared for {self.agent_name}")

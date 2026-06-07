import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from openai import OpenAI, AsyncOpenAI
from anthropic import Anthropic
import google.generativeai as genai
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
        self.model = model or getattr(settings, "OPENAI_MODEL", "gpt-3.5-turbo")
        self.provider = settings.LLM_PROVIDER.lower()
        
        if model is None and self.model != "gpt-3.5-turbo":
            logger.info(f"Using configured OPENAI_MODEL: {self.model}")
        if self.model == "gpt-4-turbo-preview":
            logger.warning(
                "Model gpt-4-turbo-preview is deprecated or unavailable."
                " Set OPENAI_MODEL env var to a supported model."
            )

        # Initialize clients based on provider
        if self.provider == "openai":
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.async_openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.anthropic_client = None
            logger.info(f"{self.agent_name} using OpenAI provider")
        elif self.provider == "gemini":
            genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel(settings.GEMINI_MODEL)
            self.openai_client = None
            self.async_openai = None
            self.anthropic_client = None
            logger.info(f"{self.agent_name} using Gemini provider")
        elif self.provider == "anthropic":
            self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            self.openai_client = None
            self.async_openai = None
            logger.info(f"{self.agent_name} using Anthropic provider")
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")

        self.max_memory = 10
        self.memory = MemoryBuffer(
            self.max_memory * 2
        )  # Conversation memory bounded by message count

    async def think(self, prompt: str, system_prompt: str = None) -> str:
        """Core reasoning capability using selected LLM provider"""

        try:
            if self.provider == "gemini":
                return await self._think_gemini(prompt, system_prompt)
            elif self.provider == "anthropic":
                return await self._think_anthropic(prompt, system_prompt)
            else:  # openai
                return await self._think_openai(prompt, system_prompt)
        except Exception as e:
            logger.error(f"Agent {self.agent_name} error: {e}")
            return None

    async def _think_openai(self, prompt: str, system_prompt: str = None) -> str:
        """OpenAI implementation"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Add recent conversation history
        recent_memory = self.memory[-self.max_memory :]
        messages.extend(recent_memory)

        # Add current prompt
        messages.append({"role": "user", "content": prompt})

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

    async def _think_gemini(self, prompt: str, system_prompt: str = None) -> str:
        """Gemini implementation (async wrapper around sync API)"""
        # Gemini API is synchronous, so we run it in a thread
        loop = asyncio.get_event_loop()
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        result = await loop.run_in_executor(
            None, self._gemini_call, full_prompt
        )

        # Store in memory
        self.memory.append({"role": "user", "content": prompt})
        self.memory.append({"role": "assistant", "content": result})

        return result

    def _gemini_call(self, prompt: str) -> str:
        """Synchronous Gemini call"""
        response = self.gemini_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=2000,
            ),
        )
        return response.text

    async def _think_anthropic(self, prompt: str, system_prompt: str = None) -> str:
        """Anthropic implementation"""
        messages = []

        # Add recent conversation history
        recent_memory = self.memory[-self.max_memory :]
        messages.extend(recent_memory)

        # Add current prompt
        messages.append({"role": "user", "content": prompt})

        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            system=system_prompt or "",
            messages=messages,
        )

        result = response.content[0].text

        # Store in memory
        self.memory.append({"role": "user", "content": prompt})
        self.memory.append({"role": "assistant", "content": result})

        return result

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


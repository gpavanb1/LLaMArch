from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from agent_base import GenerativeAIAgent, AgentResponse
import openai
from typing import Dict, Any


class GPTAgent(GenerativeAIAgent):
    def __init__(self, agent_id: str, model_name: str, api_key: str):
        super().__init__(agent_id, model_name)
        openai.api_key = api_key

    async def generate_response(self, query: str) -> AgentResponse:
        """Generate response using OpenAI's GPT model"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model_name,
                messages=[{"role": "user", "content": query}],
                temperature=0.7
            )

            return AgentResponse(
                agent_id=self.agent_id,
                response=response.choices[0].message.content,
                confidence=float(response.choices[0].finish_reason == "stop"),
                metadata={"model": self.model_name}
            )
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            raise


class HuggingFaceAgent(GenerativeAIAgent):
    def __init__(self, agent_id: str, model_name: str):
        super().__init__(agent_id, model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    async def generate_response(self, query: str) -> AgentResponse:
        """Generate response using HuggingFace model"""
        try:
            inputs = self.tokenizer(query, return_tensors="pt")
            outputs = self.model.generate(
                **inputs,
                max_length=100,
                num_return_sequences=1,
                temperature=0.7
            )

            response_text = self.tokenizer.decode(
                outputs[0], skip_special_tokens=True)

            return AgentResponse(
                agent_id=self.agent_id,
                response=response_text,
                confidence=0.8,  # Simplified confidence score
                metadata={"model": self.model_name}
            )
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            raise

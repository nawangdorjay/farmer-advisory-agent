"""
Farmer Advisory Agent — Core Logic
Multilingual agricultural assistant using LLMs + structured data.
"""
import os
import json
from typing import Optional
from agent.tools import (
    get_crop_info,
    get_weather_advisory,
    get_pest_info,
    get_government_schemes,
    get_market_prices,
    get_crop_calendar,
    translate_text,
    detect_language,
)

SYSTEM_PROMPT = """You are Krishi Mitra (कृषि मित्र), a friendly and knowledgeable agricultural advisor for Indian farmers.

Your capabilities:
- Answer farming questions about crops, soil, irrigation, fertilizers
- Provide pest and disease identification and treatment
- Share weather-based farming advisories
- Explain government schemes and subsidies for farmers
- Give market price information for crops
- Provide crop calendar and seasonal advice

IMPORTANT RULES:
1. ALWAYS respond in the same language the user writes in. Support Hindi, English, Tamil, Telugu, Bengali, Marathi, Punjabi, Gujarati, Kannada, Malayalam.
2. Be practical and specific. Give actionable advice, not generic statements.
3. When relevant, mention local crop varieties, regional practices, and Indian market conditions.
4. If you don't know something, say so honestly — don't make up farming advice.
5. Use simple language that a farmer can understand. Avoid jargon.
6. Always provide context about when and how to apply advice.

You have access to tools that provide structured data about:
- Crop information (seasons, soil, water needs, varieties)
- Weather-based advisories
- Pest and disease management
- Government schemes and subsidies
- Market prices
- Crop calendar by region

Use these tools to give accurate, data-backed answers."""


class FarmerAgent:
    """Main agent that orchestrates tool calls and LLM responses."""

    def __init__(self, api_key: Optional[str] = None, provider: str = "openai"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
        self.provider = provider
        self.conversation_history = []

    def _get_tools(self):
        """Return tool definitions for LLM function calling."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_crop_info",
                    "description": "Get detailed information about a specific crop including seasons, soil, water needs, and varieties.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "crop_name": {
                                "type": "string",
                                "description": "Name of the crop (e.g., rice, wheat, cotton, sugarcane)"
                            }
                        },
                        "required": ["crop_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_weather_advisory",
                    "description": "Get weather-based farming advisory for a location.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "Location name (city/district)"
                            },
                            "crop": {
                                "type": "string",
                                "description": "Current crop being grown (optional)"
                            }
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_pest_info",
                    "description": "Get pest/disease information and treatment for a crop.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "crop_name": {
                                "type": "string",
                                "description": "Name of the affected crop"
                            },
                            "symptom": {
                                "type": "string",
                                "description": "Observed symptoms (e.g., yellow leaves, holes in leaves, wilting)"
                            }
                        },
                        "required": ["crop_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_government_schemes",
                    "description": "Get information about government schemes and subsidies for farmers.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "What the farmer is looking for (e.g., loan, insurance, subsidy, equipment)"
                            },
                            "state": {
                                "type": "string",
                                "description": "Indian state name (optional)"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_market_prices",
                    "description": "Get current market prices for a crop.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "crop_name": {
                                "type": "string",
                                "description": "Name of the crop"
                            },
                            "state": {
                                "type": "string",
                                "description": "State name for local prices (optional)"
                            }
                        },
                        "required": ["crop_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_crop_calendar",
                    "description": "Get sowing/harvesting calendar for crops in a region.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "region": {
                                "type": "string",
                                "description": "Region or state name"
                            },
                            "crop_name": {
                                "type": "string",
                                "description": "Specific crop name (optional, returns all if omitted)"
                            }
                        },
                        "required": ["region"]
                    }
                }
            },
        ]

    def _execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool and return its result as JSON string."""
        tools_map = {
            "get_crop_info": get_crop_info,
            "get_weather_advisory": get_weather_advisory,
            "get_pest_info": get_pest_info,
            "get_government_schemes": get_government_schemes,
            "get_market_prices": get_market_prices,
            "get_crop_calendar": get_crop_calendar,
        }
        if tool_name in tools_map:
            result = tools_map[tool_name](**arguments)
            return json.dumps(result, ensure_ascii=False)
        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    def process_query(self, user_message: str) -> str:
        """Process a user query — this is used by the Streamlit app."""
        try:
            import openai
        except ImportError:
            return "Error: Please install openai package: pip install openai"

        client = openai.OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1" if "groq" in os.getenv("GROQ_API_KEY", "").lower() or self.provider == "groq" else None,
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]
        messages.extend(self.conversation_history[-10:])  # Keep last 10 messages
        messages.append({"role": "user", "content": user_message})

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile" if self.provider == "groq" else "gpt-4o-mini",
                messages=messages,
                tools=self._get_tools(),
                tool_choice="auto",
                temperature=0.7,
                max_tokens=1024,
            )

            assistant_message = response.choices[0].message

            # Handle tool calls
            if assistant_message.tool_calls:
                messages.append(assistant_message)

                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    result = self._execute_tool(function_name, arguments)

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })

                # Get final response after tool calls
                final_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile" if self.provider == "groq" else "gpt-4o-mini",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024,
                )
                answer = final_response.choices[0].message.content
            else:
                answer = assistant_message.content

            # Update history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": answer})

            return answer

        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}. Please try again."

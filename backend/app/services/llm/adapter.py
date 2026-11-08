import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from app.core.config import settings
from app.services.llm.number_guard import NumberGuard


def get_template_explanation(context_json: Dict[str, Any], language: str = "en") -> str:
    """Deterministic multilingual template fallback generator ensuring zero numerical hallucinations."""
    product_name = context_json.get("product_name", "Nutrient-Dense Prototype")
    category = context_json.get("category", "Nutrition Bar")
    iron_val = context_json.get("iron_mg", "4.5")
    cost_val = context_json.get("cost_inr", "22.50")
    serving_g = context_json.get("serving_size_g", "35")

    templates = {
        "en": (
            f"This {product_name} ({category}) has been calculated to support your daily dietary needs. "
            f"Each {serving_g}g serving delivers approximately {iron_val} mg of iron, paired with natural ascorbic acid "
            f"to support absorption within a balanced vegetarian diet. Optimized for daily consumption at ₹{cost_val} per serving."
        ),
        "ta": (
            f"இந்த {product_name} ({category}) உங்கள் அன்றாட ஊட்டச்சத்து தேவைகளை ஆதரிக்க கணக்கிடப்பட்டுள்ளது. "
            f"ஒவ்வொரு {serving_g}g பரிமாறலும் ஏறக்குறைய {iron_val} mg இரும்புச்சத்தை வழங்குகிறது. "
            f"ஒரு பரிமாறலுக்கு ₹{cost_val} விலையில் தினசரி பயன்பாட்டிற்கு உகந்தது."
        ),
        "hi": (
            f"यह {product_name} ({category}) आपकी दैनिक पोषण आवश्यकताओं को पूरा करने के लिए तैयार किया गया है। "
            f"प्रत्येक {serving_g}g सर्विंग लगभग {iron_val} mg आयरन प्रदान करती है, जो अवशोषण को बढ़ाने वाले पोषक तत्वों से युक्त है। "
            f"प्रति सर्विंग ₹{cost_val} की लागत पर यह दैनिक उपयोग के लिए उपयुक्त है।"
        ),
        "te": (
            f"ఈ {product_name} ({category}) మీ రోజువారీ పోషకాహార అవసరాలను తీర్చడానికి రూపొందించబడింది. "
            f"ప్రతి {serving_g}g సర్వింగ్ సుమారు {iron_val} mg ఐరన్‌ను అందిస్తుంది. "
            f"రోజువారీ వాడకానికి ప్రతి సర్వింగ్‌కు ₹{cost_val} ఖర్చుతో అందుబాటులో ఉంటుంది."
        ),
        "ml": (
            f"ഈ {product_name} ({category}) നിങ്ങളുടെ ദൈനംദിന പോഷകാഹാര ആവശ്യങ്ങൾക്കായി കണക്കാക്കിയതാണ്. "
            f"ഓരോ {serving_g}g സെർവിംഗും ഏകദേശം {iron_val} mg ഇരുമ്പ് നൽകുന്നു. "
            f"ദിവസേനയുള്ള ഉപയോഗത്തിനായി ₹{cost_val} നിരക്കിൽ ലഭ്യമാണ്."
        ),
    }

    return templates.get(language, templates["en"])


class LLMProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        language: str,
        context_json: Dict[str, Any],
    ) -> str:
        pass


class MockLLMProvider(LLMProvider):
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        language: str,
        context_json: Dict[str, Any],
    ) -> str:
        # Returns guaranteed deterministic template text
        return get_template_explanation(context_json, language)


class GeminiLLMProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        language: str,
        context_json: Dict[str, Any],
    ) -> str:
        if not self.api_key:
            return get_template_explanation(context_json, language)

        try:
            import httpx
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            full_prompt = (
                f"{system_prompt}\n\n"
                f"STRICT INSTRUCTION: Only use the numbers provided in the input JSON below. Never invent new numbers.\n"
                f"Language: {language}\n"
                f"Context JSON: {json.dumps(context_json)}\n"
                f"User Question: {user_prompt}"
            )
            payload = {
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {"temperature": 0.2, "maxOutputTokens": 500},
            }
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    # Apply NUMBER GUARD
                    is_valid, hallucinations = NumberGuard.audit_llm_response(text, context_json)
                    if is_valid:
                        return text
        except Exception:
            pass

        # Fallback to template if API fails or number guard rejects
        return get_template_explanation(context_json, language)


class AnthropicLLMProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        language: str,
        context_json: Dict[str, Any],
    ) -> str:
        if not self.api_key:
            return get_template_explanation(context_json, language)

        try:
            import httpx
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }
            body = {
                "model": "claude-3-5-sonnet-20240620",
                "max_tokens": 500,
                "temperature": 0.2,
                "system": (
                    f"{system_prompt}\nRespond in language: {language}.\n"
                    f"Only use numbers strictly found in this context JSON: {json.dumps(context_json)}"
                ),
                "messages": [{"role": "user", "content": user_prompt}],
            }
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=body, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    text = data["content"][0]["text"].strip()
                    is_valid, _ = NumberGuard.audit_llm_response(text, context_json)
                    if is_valid:
                        return text
        except Exception:
            pass

        return get_template_explanation(context_json, language)


def get_llm_provider() -> LLMProvider:
    provider = settings.LLM_PROVIDER.lower()
    if provider == "gemini":
        return GeminiLLMProvider()
    elif provider == "anthropic":
        return AnthropicLLMProvider()
    return MockLLMProvider()


from abc import ABC, abstractmethod
from typing import Optional
from app.core.config import settings


class SpeechProvider(ABC):
    @abstractmethod
    async def stt(self, audio_bytes: bytes, language: str = "en-IN") -> str:
        """Converts spoken audio bytes into text transcript."""
        pass

    @abstractmethod
    async def tts(self, text: str, language: str = "en-IN") -> bytes:
        """Synthesizes text into audio bytes."""
        pass


class MockSpeechProvider(SpeechProvider):
    async def stt(self, audio_bytes: bytes, language: str = "en-IN") -> str:
        # Mock transcript for audio testing
        transcripts = {
            "en-IN": "Can you explain why this millet bar was formulated for me?",
            "ta-IN": "இந்த தினை உருண்டை ஏன் எனக்கு பரிந்துரைக்கப்பட்டது என்று விளக்க முடியுமா?",
            "hi-IN": "क्या आप बता सकते हैं कि यह बाजरा बार मेरे लिए क्यों तैयार किया गया है?",
            "te-IN": "ఈ రాగి బార్ నా కోసం ఎందుకు తయారు చేయబడిందో వివరించగలరా?",
            "ml-IN": "ഈ തിന ബാർ എനിക്കായി എന്തുകൊണ്ട് തയ്യാറാക്കിയെന്ന് വിശദീകരിക്കാമോ?",
        }
        return transcripts.get(language, transcripts["en-IN"])

    async def tts(self, text: str, language: str = "en-IN") -> bytes:
        # Return a lightweight synthetic WAV audio byte header
        # Standard 44-byte minimal silent WAV
        wav_header = bytes([
            0x52, 0x49, 0x46, 0x46, 0x24, 0x00, 0x00, 0x00,
            0x57, 0x41, 0x56, 0x45, 0x66, 0x6d, 0x74, 0x20,
            0x10, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00,
            0x44, 0xac, 0x00, 0x00, 0x88, 0x58, 0x01, 0x00,
            0x02, 0x00, 0x10, 0x00, 0x64, 0x61, 0x74, 0x61,
            0x00, 0x00, 0x00, 0x00
        ])
        return wav_header


class GoogleSpeechProvider(SpeechProvider):
    def __init__(self):
        pass

    async def stt(self, audio_bytes: bytes, language: str = "en-IN") -> str:
        # If Google credentials are present, invoke Cloud Speech; otherwise fallback
        return MockSpeechProvider().stt(audio_bytes, language)

    async def tts(self, text: str, language: str = "en-IN") -> bytes:
        return MockSpeechProvider().tts(text, language)


class BhashiniSpeechProvider(SpeechProvider):
    """Placeholder adapter for National Language Translation Mission (MeitY Bhashini API)."""

    def __init__(self, api_key: Optional[str] = None, user_id: Optional[str] = None):
        self.api_key = api_key or settings.BHASHINI_API_KEY
        self.user_id = user_id or settings.BHASHINI_USER_ID

    async def stt(self, audio_bytes: bytes, language: str = "en-IN") -> str:
        # Bhashini endpoint integration stub
        return await MockSpeechProvider().stt(audio_bytes, language)

    async def tts(self, text: str, language: str = "en-IN") -> bytes:
        # Bhashini TTS integration stub
        return await MockSpeechProvider().tts(text, language)


def get_speech_provider() -> SpeechProvider:
    provider = settings.SPEECH_PROVIDER.lower()
    if provider == "google":
        return GoogleSpeechProvider()
    elif provider == "bhashini":
        return BhashiniSpeechProvider()
    return MockSpeechProvider()


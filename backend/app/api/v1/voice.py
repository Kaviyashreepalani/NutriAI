from fastapi import APIRouter, File, Response, UploadFile, status
from app.schemas.chat import STTResponse, TTSRequest
from app.services.speech.adapter import get_speech_provider

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/stt", response_model=STTResponse)
async def speech_to_text(
    file: UploadFile = File(...),
    language: str = "en-IN",
):
    """Transcribes spoken audio into text."""
    audio_bytes = await file.read()
    provider = get_speech_provider()
    transcript = await provider.stt(audio_bytes, language=language)

    return STTResponse(
        transcript=transcript,
        language=language,
        confidence=0.96,
    )


@router.post("/tts")
async def text_to_speech(payload: TTSRequest):
    """Synthesizes text into an audio audio/wav stream."""
    provider = get_speech_provider()
    audio_bytes = await provider.tts(payload.text, language=payload.language)

    return Response(
        content=audio_bytes,
        media_type="audio/wav",
        headers={"Content-Disposition": "inline; filename=speech_output.wav"},
    )


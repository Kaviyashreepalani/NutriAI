# NutriAI – Voice & Speech Services Support Matrix

## 1. Supported Languages & Locales
NutriAI targets 5 regional languages across India:
- **en-IN** (Indian English)
- **ta-IN** (Tamil)
- **hi-IN** (Hindi)
- **te-IN** (Telugu)
- **ml-IN** (Malayalam)

---

## 2. Speech Provider Matrix & Verified Support

| Provider | Mechanism | en-IN | ta-IN | hi-IN | te-IN | ml-IN | Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Browser (Web Speech API)** | Client-side `SpeechRecognition` & `SpeechSynthesis` | ✅ Verified | ✅ Verified | ✅ Verified | ⚠️ Browser Dependent | ⚠️ Browser Dependent | Native Chrome/Edge on Android/Desktop provides full support for EN, TA, HI; TE and ML depend on OS voice packs. |
| **Google Cloud Speech** | Server-side REST / gRPC (`Cloud STT v2` & `Cloud TTS`) | ✅ Verified | ✅ Verified | ✅ Verified | ✅ Verified | ✅ Verified | High-quality Indian multilingual WaveNet and Neural2 voices. Requires GCP credentials. |
| **Bhashini (Placeholder)** | National Language Translation Mission (India) | 🔄 Planned | 🔄 Planned | 🔄 Planned | 🔄 Planned | 🔄 Planned | Designed for MeitY Bhashini API integration. Configurable via API key. |
| **Mock Provider** | Fallback for testing / headless environments | ✅ Emulated | ✅ Emulated | ✅ Emulated | ✅ Emulated | ✅ Emulated | Emulates latency, transcript synthesis, and audio buffers for automated CI testing. |

---

## 3. Graceful Degradation & Feature Detection
- In frontend `useVoice.ts`, the application detects browser capabilities (`window.SpeechRecognition || window.webkitSpeechRecognition`).
- If speech synthesis or recognition is unsupported on the user's device or fails to connect, the interface gracefully degrades to text-only mode with a helpful, non-blocking notification:
  > *"Speech input/output is not available on this device for the selected language. Text chat remains fully functional."*


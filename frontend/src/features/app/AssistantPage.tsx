import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { api } from '../../lib/api';
import { useVoice } from '../../hooks/useVoice';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { MedicalDisclaimer } from '../../components/safety/MedicalDisclaimer';
import { PrototypeBadge } from '../../components/safety/PrototypeBadge';
import {
  Bot,
  User,
  Send,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  RefreshCw,
  AlertCircle,
  Info,
  Sparkles,
} from 'lucide-react';

interface Message {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
  language?: string;
}

const QUICK_CHIPS = [
  'Why was this food product recommended for me?',
  'How much iron is in my formulation per serving?',
  'Why do I need vitamin C with iron?',
  'Is this product a medicine or treatment?',
  'What is haemoglobin and why does it matter?',
  'Can I eat this if I have thalassaemia trait?',
];

export const AssistantPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      sender: 'assistant',
      text: 'Hello! I am the NutriAI assistant. I can explain your formulation results, nutrition science, and ICMR guidelines — in 5 languages. I never invent numbers; all values I mention come from your verified formulation data. How can I help you today?',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [ttsEnabled, setTtsEnabled] = useState(true);
  const [speakingId, setSpeakingId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { isListening, startListening, stopListening, isSupported, speak, stop: stopSpeaking } = useVoice({
    language: i18n.language,
    onResult: (text) => setInput((prev) => prev + text),
  });

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (text?: string) => {
    const query = (text || input).trim();
    if (!query || loading) return;

    const userMsg: Message = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      language: i18n.language,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await api.post('/chat/message', {
        message: query,
        language: i18n.language,
      });

      const assistantMsg: Message = {
        id: `assistant-${Date.now()}`,
        sender: 'assistant',
        text: res.data.reply,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        language: i18n.language,
      };

      setMessages((prev) => [...prev, assistantMsg]);

      // Auto-speak if TTS enabled
      if (ttsEnabled && res.data.reply) {
        setSpeakingId(assistantMsg.id);
        speak(res.data.reply);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: `error-${Date.now()}`,
          sender: 'assistant',
          text: 'I could not process your query at this moment. The number guard is active — only verified formulation data is shared. Please try again.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSpeak = (msg: Message) => {
    if (speakingId === msg.id) {
      stopSpeaking();
      setSpeakingId(null);
    } else {
      setSpeakingId(msg.id);
      speak(msg.text);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-4">
      <MedicalDisclaimer />

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-bold text-gray-900">Voice & Text Assistant</h1>
          <p className="text-sm text-gray-600 mt-0.5">ICMR-grounded explanations in 5 Indian languages.</p>
        </div>
        <div className="flex items-center gap-2">
          <PrototypeBadge />
          <button
            onClick={() => setTtsEnabled(!ttsEnabled)}
            className={`flex items-center gap-1.5 text-xs font-medium px-2.5 py-1.5 rounded-lg border transition ${ttsEnabled ? 'bg-primary-50 border-primary-300 text-primary-700' : 'bg-gray-100 border-gray-200 text-gray-500'}`}
          >
            {ttsEnabled ? <Volume2 className="w-3.5 h-3.5" /> : <VolumeX className="w-3.5 h-3.5" />}
            Auto-read {ttsEnabled ? 'On' : 'Off'}
          </button>
        </div>
      </div>

      {/* Number Guard Notice */}
      <div className="p-3 rounded-xl bg-primary-50 border border-primary-200 flex gap-2 text-xs text-primary-800">
        <Sparkles className="w-4 h-4 text-primary-600 shrink-0 mt-0.5" />
        <span>
          <strong>Number Guard Active:</strong> This assistant only references numbers from your verified formulation data. Any AI-generated response containing unverified numbers is automatically rejected and replaced with a template-based explanation.
        </span>
      </div>

      {/* Quick Chips */}
      <div className="flex flex-wrap gap-2">
        {QUICK_CHIPS.map((chip, i) => (
          <button
            key={i}
            onClick={() => handleSend(chip)}
            className="text-xs px-3 py-1.5 rounded-full bg-white border border-gray-200 text-gray-700 hover:bg-primary-50 hover:border-primary-300 hover:text-primary-700 transition"
          >
            {chip}
          </button>
        ))}
      </div>

      {/* Chat Window */}
      <Card className="flex flex-col h-[480px] overflow-hidden p-0">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-[#F7F9F8]">
          {messages.map((msg) => (
            <div key={msg.id} className={`flex gap-2.5 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              {msg.sender === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-primary-100 border border-primary-200 flex items-center justify-center text-primary-700 shrink-0 mt-0.5">
                  <Bot className="w-4 h-4" />
                </div>
              )}
              <div className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed shadow-sm ${
                msg.sender === 'user'
                  ? 'bg-primary-600 text-white rounded-br-none'
                  : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none'
              }`}>
                <p>{msg.text}</p>
                <div className="flex items-center justify-between mt-1.5 gap-2">
                  <span className="text-[10px] opacity-60">{msg.timestamp}</span>
                  {msg.sender === 'assistant' && isSupported && (
                    <button
                      onClick={() => handleSpeak(msg)}
                      className="text-[11px] flex items-center gap-0.5 text-primary-600 hover:underline"
                    >
                      {speakingId === msg.id ? <VolumeX className="w-3 h-3" /> : <Volume2 className="w-3 h-3" />}
                      {speakingId === msg.id ? 'Stop' : 'Listen'}
                    </button>
                  )}
                </div>
              </div>
              {msg.sender === 'user' && (
                <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 shrink-0 mt-0.5">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div className="flex gap-2 items-center text-xs text-gray-500">
              <RefreshCw className="w-4 h-4 text-primary-500 animate-spin" />
              <span>Verifying numbers and generating response…</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Disclaimer bar */}
        <div className="px-4 py-1.5 bg-amber-50 border-t border-amber-100 flex items-center gap-2 text-[11px] text-amber-800">
          <AlertCircle className="w-3.5 h-3.5 text-amber-600 shrink-0" />
          Nutrition support only. Never replaces medical advice. All numbers from verified data.
        </div>

        {/* Input bar */}
        <form
          onSubmit={(e) => { e.preventDefault(); handleSend(); }}
          className="px-4 py-3 bg-white border-t border-gray-200 flex items-center gap-2"
        >
          {isSupported && (
            <button
              type="button"
              onClick={isListening ? stopListening : startListening}
              className={`p-2 rounded-xl transition ${isListening ? 'bg-red-500 text-white animate-pulse' : 'text-gray-500 hover:bg-gray-100'}`}
              title={isListening ? 'Stop recording' : 'Start voice input'}
            >
              {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
            </button>
          )}
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t('chat.input_placeholder', 'Ask about your formulation, iron, or bioavailability…')}
            className="flex-1 text-sm px-3 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="p-2 bg-primary-600 hover:bg-primary-700 disabled:opacity-50 text-white rounded-xl transition"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </Card>

      <MedicalDisclaimer />
    </div>
  );
};


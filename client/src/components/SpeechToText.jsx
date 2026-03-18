import React, { useEffect, useState, useRef } from 'react';

const VOICE_OPTIONS = [
  { value: 'male',   label: '♂ Male (American)'  },
  { value: 'female', label: '♀ Female (American)' },
  { value: 'indian', label: '♀ Indian Accent'     },
];

const SpeechToText = ({ onResult, selectedVoice, onVoiceChange }) => {
  const [isRecognizing, setIsRecognizing] = useState(false);
  const recognitionRef = useRef(null);

  // Initialise speech recognition once
  useEffect(() => {
    if (!('SpeechRecognition' in window) && !('webkitSpeechRecognition' in window)) {
      console.warn('Speech recognition not supported in this browser.');
      return;
    }
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recog = new SR();
    recog.continuous     = false;
    recog.interimResults = false;
    recog.lang           = 'en-IN';

    recog.onresult = (event) => {
      const speechTranscript = event.results[0][0].transcript;
      console.log('Transcript:', speechTranscript);
      if (onResult) onResult(speechTranscript);
    };

    recog.onend = () => {
      console.log('Speech recognition stopped');
      setIsRecognizing(false);
    };

    recog.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsRecognizing(false);
    };

    recognitionRef.current = recog;
  }, []);

  // ── START / STOP helpers ──────────────────────────────────
  const startRecognition = () => {
    if (!recognitionRef.current || isRecognizing) return;
    recognitionRef.current.start();
    setIsRecognizing(true);
    console.log('Speech recognition started');
  };

  const stopRecognition = () => {
    if (!recognitionRef.current || !isRecognizing) return;
    recognitionRef.current.stop();
    setIsRecognizing(false);
    console.log('Speech recognition stopped');
  };

  // ── Hold-T keyboard shortcut ──────────────────────────────
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.key === 'T' || e.key === 't') && !isRecognizing) startRecognition();
    };
    const handleKeyUp = (e) => {
      if ((e.key === 'T' || e.key === 't') && isRecognizing) stopRecognition();
    };
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup',   handleKeyUp);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup',   handleKeyUp);
    };
  }, [isRecognizing]);

  // ── UI ────────────────────────────────────────────────────
  return (
    <div className="speech-controls">

      {/* Voice selector dropdown */}
      <div className="voice-selector">
        <label htmlFor="voiceSelect">Voice</label>
        <select
          id="voiceSelect"
          value={selectedVoice}
          onChange={(e) => onVoiceChange(e.target.value)}
        >
          {VOICE_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      {/* Mic button — hold to talk */}
      <button
        className={`mic-btn ${isRecognizing ? 'mic-btn--active' : ''}`}
        onMouseDown={startRecognition}
        onMouseUp={stopRecognition}
        onTouchStart={(e) => { e.preventDefault(); startRecognition(); }}
        onTouchEnd={(e)   => { e.preventDefault(); stopRecognition();  }}
        title="Hold to speak (or hold T)"
      >
        {isRecognizing ? (
          <>
            <span className="mic-icon">🔴</span>
            <span>Listening…</span>
          </>
        ) : (
          <>
            <span className="mic-icon">🎙️</span>
            <span>Hold to Talk</span>
          </>
        )}
      </button>

      <p className="mic-hint">or hold <kbd>T</kbd></p>
    </div>
  );
};

export default SpeechToText;
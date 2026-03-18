import React, { useState, useEffect, useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { Environment } from '@react-three/drei';
import './app.css';
import SpeechToText from './components/SpeechToText.jsx';
import Exp from './components/Exp.jsx';

function App() {
  const [transcript, setTranscript]       = useState('');
  const [isSpeaking, setIsSpeaking]       = useState(false);
  const [isIdle, setIsIdle]               = useState(true);
  const [lipsyncData, setLipsyncData]     = useState(null);
  const [audioProgress, setAudioProgress] = useState(0);
  const [selectedVoice, setSelectedVoice] = useState('male'); // default voice
  const audioRef = useRef(null);

  const handleSpeechResult = async (speechTranscript) => {
    setTranscript(speechTranscript);
    console.log('Recognized text:', speechTranscript);

    try {
      const response = await fetch('http://localhost:8000/voice-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: speechTranscript,
          voice: selectedVoice,       // ← send selected voice to backend
        }),
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const { audio_url, mouthCues } = await response.json();

      // Stop and reset previous audio
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
        audioRef.current = null;
      }

      if (!audio_url) {
        console.warn('No audio URL returned');
        return;
      }

      // Create new audio instance
      const audio = new Audio(audio_url);
      audioRef.current = audio;

      // Pass real mouthCues from backend to avatar
      setLipsyncData(mouthCues);

      setIsSpeaking(true);
      setIsIdle(false);
      audio.play();

      audio.ontimeupdate = () => setAudioProgress(audio.currentTime);

      audio.onended = () => {
        setIsSpeaking(false);
        setIsIdle(true);
        setAudioProgress(0);
        setLipsyncData(null);
      };

    } catch (error) {
      console.error('Error fetching audio or lipsync data:', error);
    }
  };

  const stopSpeaking = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setIsSpeaking(false);
      setIsIdle(true);
      setAudioProgress(0);
      setLipsyncData(null);
    }
  };

  // Space bar stops speaking
  useEffect(() => {
    const handleKeyPress = (event) => {
      if (event.code === 'Space') stopSpeaking();
    };
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, []);

  return (
    <div className="container">
      <Canvas className="canvas">
        <ambientLight intensity={0.5} />
        <Environment preset="sunset" />
        <Exp
          isSpeaking={isSpeaking}
          isIdle={isIdle}
          lipsyncData={lipsyncData}
          audioProgress={audioProgress}
        />
      </Canvas>

      {/* Voice selector + speech input */}
      <SpeechToText
        onResult={handleSpeechResult}
        selectedVoice={selectedVoice}
        onVoiceChange={setSelectedVoice}
      />
    </div>
  );
}

export default App;
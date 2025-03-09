import React, { useState, useEffect, useRef } from 'react';
import { Canvas, useThree } from '@react-three/fiber';
import { Center, Environment, OrbitControls } from '@react-three/drei';
import './app.css';
import SpeechToText from './components/SpeechToText.jsx';
import Exp from './components/Exp.jsx';
import * as THREE from 'three';

function App() {
  const [transcript, setTranscript] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isIdle, setIsIdle] = useState(true);
  const [lipsyncData, setLipsyncData] = useState(null);
  const [audioProgress, setAudioProgress] = useState(0);
  const audioRef = useRef(null);

  const handleSpeechResult = async (speechTranscript) => {
    setTranscript(speechTranscript);
    console.log('Recognized text:', speechTranscript);

    try {
      const response = await fetch('http://localhost:8000/voice-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: speechTranscript }),
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const { audio_url, mouthCues } = await response.json();

      const audio = new Audio(audio_url);
      audioRef.current = audio;
      setLipsyncData(mouthCues);

      setIsSpeaking(true);
      setIsIdle(false);
      audio.play();

      audio.ontimeupdate = () => setAudioProgress(audio.currentTime);

      audio.onended = () => {
        setIsSpeaking(false);
        setIsIdle(true);
        setAudioProgress(0);
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
    }
  };

  useEffect(() => {
    const handleKeyPress = (event) => {
      if (event.code === 'Space') stopSpeaking();
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, []);

  return (
    
      <div className="container">
        {/* Floating div to see placement */}
   
        <Canvas className="canvas">
          <ambientLight intensity={0.5} />
          <Environment preset="sunset" />
    
          {/* Place the avatar slightly right using position */}
          <Exp
            isSpeaking={isSpeaking}
            isIdle={isIdle}
            lipsyncData={lipsyncData}
            audioProgress={audioProgress}
          />
        </Canvas>
        
        <SpeechToText onResult={handleSpeechResult} />
      </div>
    
    
  );
}

export default App;

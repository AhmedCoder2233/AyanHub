import { useEffect, useRef, useState } from 'react'
import './App.css'

function App() {
  const [listening, setListening] = useState(false)
  const [transcript, setTranscript] = useState()
  const [botmsg, setBotMsg] = useState()
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [address, setAddress] = useState("")
  const [accountnumber, setAccountNumber] = useState("")
  const [userInfoSent, setUserInfoSent] = useState(false)
  const [shouldConnect, setShouldConnect] = useState(false)

  const ws = useRef(null)
  const recognitionRef = useRef(null)
  const isConnected = useRef(false)
  const manualClose = useRef(false)

  useEffect(() => {
    if (!shouldConnect) return

    const connectionWS = new WebSocket("ws://127.0.0.1:8080/ws")
    connectionWS.onopen = () => {
      console.log("WebSocket Connected")
      isConnected.current = true

      if (!userInfoSent && email && phone && address && accountnumber) {
        const userPayload = {
          type: "init",
          email,
          phone,
          address,
          accountnumber
        }
        connectionWS.send(JSON.stringify(userPayload))
        setUserInfoSent(true)
      }
    }

    connectionWS.onmessage = (event) => {
      if (typeof event.data === "string") {
        setBotMsg(event.data)
      } else if (event.data instanceof Blob) {
        const audioBlob = new Blob([event.data])
        const audioUrl = URL.createObjectURL(audioBlob)
        const audio = new Audio(audioUrl)

    audio.onended = () => {
      console.log("Audio ended, restarting mic...");
  if (listening) {
    setTimeout(() => startListening(), 500)  
  }
}

        audio.play()
      }
    }

    connectionWS.onerror = (event) => {
      console.log(`WebSocket Error: ${event}`)
    }

    connectionWS.onclose = () => {
      isConnected.current = false
      if (!manualClose.current) {
        console.warn("WebSocket closed. Reconnecting...")
        setTimeout(() => setShouldConnect(true), 2000)
      }
    }

    ws.current = connectionWS
  }, [shouldConnect]) 

const isRecognizing = useRef(false); 

const startListening = () => {
  if (!isConnected.current || !listening || isRecognizing.current) return;

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  recognition.lang = "en";
  recognition.interimResults = false;
  recognition.continuous = false;

  recognition.onstart = () => {
    console.log("🎤 Mic started");
    isRecognizing.current = true;
  };

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    setTranscript(text);

    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      if (text.trim() !== "") {
        ws.current.send(JSON.stringify({ type: "message", text }));
        console.log("📤 Sending to backend");
      } else {
        console.log("🗣️ Empty speech");
      }
    } else {
      console.warn("WebSocket not open.");
    }
  };

  recognition.onend = () => {
    console.log("🛑 Mic ended");
    isRecognizing.current = false;

    if (listening) {
      setTimeout(() => startListening(), 1000); 
    }
  };

  recognition.onerror = (err) => {
    console.error("❌ Mic Error:", err.error);
    isRecognizing.current = false;

    if (listening && err.error !== "aborted") {
      setTimeout(() => startListening(), 1000);
    }
  };

  recognitionRef.current = recognition;
  try {
    recognition.start();
  } catch (e) {
    console.warn("⚠️ Could not start mic:", e.message);
  }
};



  const handleStart = () => {
    if (!email || !phone || !address) {
      alert("Please enter email, phone, and address first.")
      return
    }

    setListening(true)
    setShouldConnect(true)
    startListening()
  }

  const handleStop = () => {
    manualClose.current = true
    setListening(false)
    recognitionRef.current?.stop()
    ws.current?.close()
  }

  return (
    <div className="app-container">
      <div className="voice-agent-box">
        {listening && <div className="listening-indicator"></div>}
        <h1>🤖 AI Voice Agent</h1>
        <p className="subtitle">Talk to your smart e-commerce assistant</p>

        <div className="section">
          <label>You said:</label>
          <div className="message user-msg">{transcript || "Waiting for your voice..."}</div>
        </div>

        <div className="section">
          <label>Agent said:</label>
          <div className="message agent-msg">{botmsg || "Agent response will appear here."}</div>
        </div>

        <div className="input-group">
          <input className='innerinput' type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <input className='innerinput' type="text" placeholder="Phone" value={phone} onChange={(e) => setPhone(e.target.value)} />
          <input className='innerinput' type="text" placeholder="Address" value={address} onChange={(e) => setAddress(e.target.value)} />
          <input className='innerinput' type="text" placeholder="AccountNumber" value={accountnumber} onChange={(e) => setAccountNumber(e.target.value)} />
        </div>

        <div className="button-group">
          <button className="btn start" onClick={handleStart}>▶️ Start</button>
          <button className="btn stop" onClick={handleStop}>🛑 Stop</button>
        </div>
      </div>
    </div>
  )
}

export default App

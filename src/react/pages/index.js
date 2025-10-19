import { useState, useEffect } from 'react';

const API_URL = 'https://ec9e34c28fee.ngrok-free.app';

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await fetch(`${API_URL}/api/health`);
        setIsConnected(response.ok);
      } catch {
        setIsConnected(false);
      }
    };
    
    checkConnection();
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading || !isConnected) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: input, 
          format: 'standard',
          session_id: 'web-session' 
        })
      });

      if (response.ok) {
        const data = await response.json();
        const aiMessage = {
          id: data.id,
          type: 'ai',
          content: data.response,
          timestamp: new Date(data.timestamp),
          metadata: {
            confidence: data.confidence,
            sources: data.sources,
            sourceDetails: data.source_details,
            safetyNote: data.safety_note
          }
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error('Failed to send message');
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now(),
        type: 'system',
        content: `Error: ${error.message}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setIsLoading(false);
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)', padding: '2rem' }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '3rem', fontWeight: 'bold', background: 'linear-gradient(45deg, #667eea 0%, #764ba2 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', marginBottom: '1rem' }}>
            Radeon AI Knowledge Base
          </h1>
          <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '0.5rem' }}>
            566 Articles • 2.25M Words • Enhanced AI Responses
          </p>
          <p style={{ fontSize: '1rem', color: '#888' }}>
            Ask questions about robotics, AI, automation, and technology
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
          <div style={{ background: 'white', padding: '1rem', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', borderLeft: '4px solid #3b82f6' }}>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <div style={{ width: '12px', height: '12px', borderRadius: '50%', marginRight: '12px', background: isConnected ? '#10b981' : '#ef4444', animation: isConnected ? 'pulse 2s infinite' : 'none' }}></div>
              <div>
                <p style={{ fontSize: '0.875rem', color: '#666', margin: 0 }}>Backend Status</p>
                <p style={{ fontWeight: '600', color: '#111', margin: 0 }}>{isConnected ? 'Connected' : 'Disconnected'}</p>
              </div>
            </div>
          </div>
          <div style={{ background: 'white', padding: '1rem', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', borderLeft: '4px solid #10b981' }}>
            <p style={{ fontSize: '0.875rem', color: '#666', margin: 0 }}>Knowledge Articles</p>
            <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#111', margin: 0 }}>566</p>
          </div>
          <div style={{ background: 'white', padding: '1rem', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', borderLeft: '4px solid #8b5cf6' }}>
            <p style={{ fontSize: '0.875rem', color: '#666', margin: 0 }}>Total Words</p>
            <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#111', margin: 0 }}>2.25M</p>
          </div>
          <div style={{ background: 'white', padding: '1rem', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', borderLeft: '4px solid #f59e0b' }}>
            <p style={{ fontSize: '0.875rem', color: '#666', margin: 0 }}>Domains Covered</p>
            <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#111', margin: 0 }}>16</p>
          </div>
        </div>

        <div style={{ background: 'white', borderRadius: '16px', boxShadow: '0 10px 25px rgba(0,0,0,0.1)', overflow: 'hidden' }}>
          <div style={{ padding: '1rem', background: isConnected ? '#ecfdf5' : '#fef2f2', borderBottom: '1px solid #e5e7eb', color: isConnected ? '#065f46' : '#991b1b', fontSize: '0.875rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: isConnected ? '#10b981' : '#ef4444', animation: isConnected ? 'pulse 2s infinite' : 'none' }}></div>
              {isConnected ? 'Connected to Radeon AI Backend' : 'Disconnected - Check backend server'}
            </div>
          </div>

          <div style={{ height: '400px', overflowY: 'auto', padding: '1rem' }}>
            {messages.map((message) => (
              <div key={message.id} style={{ display: 'flex', gap: '12px', marginBottom: '1rem', flexDirection: message.type === 'user' ? 'row-reverse' : 'row' }}>
                <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: '#e5e7eb', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.125rem', flexShrink: 0 }}>
                  {message.type === 'user' ? '👤' : message.type === 'ai' ? '🤖' : '⚠️'}
                </div>
                <div style={{ flex: 1, textAlign: message.type === 'user' ? 'right' : 'left' }}>
                  <div style={{ 
                    display: 'inline-block', 
                    padding: '12px 16px', 
                    borderRadius: '12px', 
                    maxWidth: '100%',
                    background: message.type === 'user' ? '#3b82f6' : message.type === 'system' ? '#fef3c7' : 'white',
                    color: message.type === 'user' ? 'white' : message.type === 'system' ? '#92400e' : '#111',
                    border: message.type === 'ai' ? '1px solid #e5e7eb' : 'none'
                  }}>
                    <div style={{ whiteSpace: 'pre-wrap' }}>{message.content}</div>
                    {message.metadata?.sources && (
                      <div style={{ marginTop: '12px', paddingTop: '12px', borderTop: '1px solid #e5e7eb', fontSize: '0.875rem', color: '#3b82f6' }}>
                        📚 {message.metadata.sources} Sources
                        {message.metadata.safetyNote && (
                          <div style={{ marginTop: '8px', color: '#f59e0b' }}>
                            🛡️ {message.metadata.safetyNote}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '4px' }}>
                    🕒 {message.timestamp.toLocaleTimeString()}
                    {message.metadata?.confidence && ` • ⚡ ${(message.metadata.confidence * 100).toFixed(0)}%`}
                  </div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div style={{ display: 'flex', gap: '12px', marginBottom: '1rem' }}>
                <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: '#e5e7eb', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.125rem' }}>🤖</div>
                <div style={{ background: 'white', border: '1px solid #e5e7eb', borderRadius: '12px', padding: '12px 16px' }}>
                  <div style={{ display: 'flex', gap: '4px' }}>
                    <div style={{ width: '8px', height: '8px', background: '#9ca3af', borderRadius: '50%', animation: 'bounce 1.4s infinite ease-in-out' }}></div>
                    <div style={{ width: '8px', height: '8px', background: '#9ca3af', borderRadius: '50%', animation: 'bounce 1.4s infinite ease-in-out 0.16s' }}></div>
                    <div style={{ width: '8px', height: '8px', background: '#9ca3af', borderRadius: '50%', animation: 'bounce 1.4s infinite ease-in-out 0.32s' }}></div>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div style={{ padding: '1rem', borderTop: '1px solid #e5e7eb', background: 'white' }}>
            <form onSubmit={sendMessage} style={{ display: 'flex', gap: '8px' }}>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={isConnected ? "Ask about robotics, AI, or automation..." : "Connect to backend first..."}
                disabled={!isConnected || isLoading}
                style={{
                  flex: 1,
                  padding: '12px 16px',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '1rem',
                  outline: 'none',
                  opacity: (!isConnected || isLoading) ? 0.5 : 1,
                  cursor: (!isConnected || isLoading) ? 'not-allowed' : 'text'
                }}
              />
              <button
                type="submit"
                disabled={!input.trim() || !isConnected || isLoading}
                style={{
                  padding: '12px 16px',
                  background: '#3b82f6',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  fontSize: '1rem',
                  cursor: 'pointer',
                  opacity: (!input.trim() || !isConnected || isLoading) ? 0.5 : 1,
                  pointerEvents: (!input.trim() || !isConnected || isLoading) ? 'none' : 'auto'
                }}
              >
                📤 Send
              </button>
            </form>
          </div>
        </div>

        <div style={{ textAlign: 'center', marginTop: '2rem', fontSize: '0.875rem', color: '#6b7280' }}>
          <p>Always follow proper safety protocols when working with robotics systems.</p>
        </div>
      </div>

      <style jsx>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }
      `}</style>
    </div>
  );
}
import React, { useState, useRef, useEffect } from 'react';
import './ChatWidget.css';

interface Message {
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function ChatWidget() {
  const [messages, setMessages] = useState<Message[]>([
    {
      content: "Hi! I'm the AI assistant for Mountain Coaching. How can I help you today? 😊",
      role: 'assistant',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      content: input,
      role: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          session_id: sessionId,
          conversation_history: messages.map(m => ({
            content: m.content,
            role: m.role
          }))
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      setSessionId(data.session_id);

      const assistantMessage: Message = {
        content: data.response,
        role: 'assistant',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        content: "Sorry, I'm having trouble connecting. Please try again or email coach@mountaincoaching.com",
        role: 'assistant',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!isOpen) {
    return (
      <button 
        className="chat-bubble"
        onClick={() => setIsOpen(true)}
        aria-label="Open chat"
      >
        💬
      </button>
    );
  }

  return (
    <div className="chat-widget">
      <div className="chat-header">
        <div className="chat-header-content">
          <div className="chat-avatar">🎯</div>
          <div className="chat-header-text">
            <h3>Mountain Coaching</h3>
            <p className="online-status">
              <span className="status-dot"></span>
              Online now
            </p>
          </div>
        </div>
        <button 
          className="close-button"
          onClick={() => setIsOpen(false)}
          aria-label="Close chat"
        >
          ✕
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((message, index) => (
          <div 
            key={index}
            className={`message ${message.role}`}
          >
            {message.role === 'assistant' && (
              <div className="message-avatar">🎯</div>
            )}
            <div className="message-content">
              <p>{message.content}</p>
              <span className="message-time">
                {message.timestamp.toLocaleTimeString('en-US', { 
                  hour: 'numeric', 
                  minute: '2-digit' 
                })}
              </span>
            </div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="message-avatar">🎯</div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <input
          type="text"
          className="chat-input"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
        />
        <button 
          className="send-button"
          onClick={sendMessage}
          disabled={loading || !input.trim()}
          aria-label="Send message"
        >
          {loading ? '⏳' : '➤'}
        </button>
      </div>

      <div className="chat-footer">
        <span>Powered by AI • </span>
        <a href="mailto:coach@mountaincoaching.com">Need help?</a>
      </div>
    </div>
  );
}

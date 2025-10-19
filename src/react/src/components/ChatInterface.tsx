'use client';

import { useState } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: number;
  hasMore?: boolean;
  fullContent?: string;
}

export default function ChatInterface() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [responseFormat, setResponseFormat] = useState('standard');
  const [expandedMessages, setExpandedMessages] = useState<Set<string>>(new Set());

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    const messageId = Date.now().toString();
    setInput('');
    setMessages(prev => [...prev, { id: messageId, role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: userMessage,
          format: responseFormat,
          session_id: 'web-session'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const assistantMessage: Message = {
          id: data.id || Date.now().toString(),
          role: 'assistant',
          content: data.response,
          sources: data.sources,
          hasMore: data.has_more,
          fullContent: data.full_content
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        setMessages(prev => [...prev, { 
          id: Date.now().toString(),
          role: 'assistant', 
          content: 'Sorry, I encountered an error connecting to the knowledge base.' 
        }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, { 
        id: Date.now().toString(),
        role: 'assistant', 
        content: 'Connection error. Make sure the backend server is running.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExpandMessage = (messageId: string) => {
    const newExpanded = new Set(expandedMessages);
    if (newExpanded.has(messageId)) {
      newExpanded.delete(messageId);
    } else {
      newExpanded.add(messageId);
    }
    setExpandedMessages(newExpanded);
  };

  const handleFormatRequest = async (format: string, originalContent: string) => {
    const formatPrompts = {
      essay: `Please provide an essay-style response about: ${originalContent.substring(0, 100)}...`,
      detailed: `Please provide a detailed explanation about: ${originalContent.substring(0, 100)}...`,
      summary: `Please provide a concise summary of: ${originalContent.substring(0, 100)}...`,
    };
    
    const prompt = formatPrompts[format as keyof typeof formatPrompts] || originalContent;
    
    const messageId = Date.now().toString();
    setMessages(prev => [...prev, { id: messageId, role: 'user', content: `[${format.toUpperCase()} FORMAT] ${prompt}` }]);
    setIsLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: prompt,
          format: format,
          session_id: 'web-session'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const assistantMessage: Message = {
          id: data.id || Date.now().toString(),
          role: 'assistant',
          content: data.response,
          sources: data.sources,
          hasMore: data.has_more,
          fullContent: data.full_content
        };
        setMessages(prev => [...prev, assistantMessage]);
      }
    } catch (error) {
      console.error('Format request error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg">
      <div className="h-96 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
              message.role === 'user' 
                ? 'bg-blue-500 text-white' 
                : 'bg-gray-200 text-gray-800'
            }`}>
              <div className="whitespace-pre-wrap">
                {expandedMessages.has(message.id) && message.fullContent 
                  ? message.fullContent 
                  : message.content
                }
                {(message.content.endsWith('...') || message.hasMore) && (
                  <button
                    onClick={() => handleExpandMessage(message.id)}
                    className="ml-2 text-blue-600 hover:underline text-sm"
                  >
                    {expandedMessages.has(message.id) ? 'Show Less' : 'Read More'}
                  </button>
                )}
              </div>
              
              {message.role === 'assistant' && (
                <div className="mt-3 flex flex-wrap gap-2">
                  <button
                    onClick={() => handleFormatRequest('essay', message.content)}
                    className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs hover:bg-blue-200"
                  >
                    Essay Format
                  </button>
                  <button
                    onClick={() => handleFormatRequest('detailed', message.content)}
                    className="px-2 py-1 bg-green-100 text-green-700 rounded text-xs hover:bg-green-200"
                  >
                    More Details
                  </button>
                  <button
                    onClick={() => handleFormatRequest('summary', message.content)}
                    className="px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs hover:bg-purple-200"
                  >
                    Quick Summary
                  </button>
                </div>
              )}
              
              {message.sources && (
                <div className="mt-2 text-xs text-gray-600">
                  {message.sources} sources • Always follow proper safety protocols
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg">
              Thinking...
            </div>
          </div>
        )}
      </div>
      
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="space-y-2">
          <div className="flex gap-2">
            <select
              value={responseFormat}
              onChange={(e) => setResponseFormat(e.target.value)}
              className="px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            >
              <option value="standard">Standard</option>
              <option value="detailed">Detailed</option>
              <option value="summary">Summary</option>
              <option value="essay">Essay</option>
            </select>
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about robotics, AI, or technology..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              Send
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
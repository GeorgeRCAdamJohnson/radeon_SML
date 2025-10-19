'use client';

import ChatInterface from '@/components/ChatInterface';
import { AIProvider } from '@/contexts/AIContext';

export default function Home() {
  return (
    <AIProvider>
      <main className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                Radeon AI Knowledge Base
              </h1>
              <p className="text-lg text-gray-600 dark:text-gray-300">
                Ask questions about robotics, AI, and technology
              </p>
            </div>
            <ChatInterface />
          </div>
        </div>
      </main>
    </AIProvider>
  );
}
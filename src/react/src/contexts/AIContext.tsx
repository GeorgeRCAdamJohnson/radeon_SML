'use client';

import { createContext, useContext, ReactNode } from 'react';

const AIContext = createContext({});

export const useAI = () => useContext(AIContext);

export function AIProvider({ children }: { children: ReactNode }) {
  return (
    <AIContext.Provider value={{}}>
      {children}
    </AIContext.Provider>
  );
}
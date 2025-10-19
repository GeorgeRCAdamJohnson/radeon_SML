import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Radeon AI Knowledge Base',
  description: 'AI-powered robotics and technology knowledge base',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
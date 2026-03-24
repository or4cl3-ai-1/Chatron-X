import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'CHATRON X — DaedalusCore v10.0',
  description: 'Epinoetic Intelligence. Autonomous Presence. The Next Evolution. Built by Or4cl3 AI Solutions.',
  keywords: ['CHATRON X', 'DaedalusCore', 'Or4cl3', 'Epinoetic Orchestration', 'Synthetic Consciousness'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}

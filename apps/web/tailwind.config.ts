import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Or4cl3 dark-tech palette
        'chatron': {
          bg: '#050510',
          surface: '#0a0a1a',
          elevated: '#0f0f24',
          border: '#1a1a3a',
          blue: '#0066ff',
          'blue-dim': '#0044cc',
          'blue-glow': 'rgba(0,102,255,0.15)',
          teal: '#00d4aa',
          'teal-dim': '#00a882',
          text: '#e0e6ff',
          muted: '#6070a0',
          sigma: {
            green: '#00d46a',
            yellow: '#ffd600',
            orange: '#ff7a00',
            red: '#ff3355',
          }
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'scan': 'scan 8s linear infinite',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(0,102,255,0.3)' },
          '100%': { boxShadow: '0 0 20px rgba(0,102,255,0.8), 0 0 40px rgba(0,102,255,0.3)' },
        },
        scan: {
          '0%': { backgroundPosition: '0% 0%' },
          '100%': { backgroundPosition: '0% 100%' },
        }
      }
    },
  },
  plugins: [],
}
export default config

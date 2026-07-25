/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        "american-oak": ["AmericanOak-Script", "cursive"],
        "american-oak-serif": ["AmericanOak-Serif", "serif"],
        "instrument-serif": ["Instrument Serif", "serif"],
      },
      colors: {
        primary: "#494fdf",
        "primary-bright": "#4f55f1",
        "primary-deep": "#3a40c4",
        "on-primary": "#ffffff",
        "canvas-light": "#ffffff",
        "canvas-dark": "#000000",
        "surface-soft": "#f4f4f4",
        "surface-card": "#ffffff",
        "surface-deep": "#0a0a0a",
        "surface-elevated": "#16181a",
        "hairline-light": "#e2e2e7",
        "hairline-dark": "rgba(255, 255, 255, 0.12)",
        "hairline-strong": "#191c1f",
        ink: "#191c1f",
        body: "#1f2226",
        charcoal: "#3a3d40",
        mute: "#505a63",
        ash: "#5c5e60",
        stone: "#8d969e",
        faint: "#c9c9cd",
        "on-dark": "#ffffff",
        "on-dark-mute": "rgba(255, 255, 255, 0.72)",
        "accent-teal": "#00a87e",
        "accent-danger": "#e23b4a",
      },
      spacing: {
        xxs: "4px",
        xs: "6px",
        sm: "8px",
        md: "14px",
        lg: "16px",
        xl: "24px",
        xxl: "32px",
        xxxl: "48px",
        block: "80px",
        section: "88px",
        band: "120px",
      },
      borderRadius: {
        none: "0px",
        sm: "8px",
        md: "12px",
        lg: "20px",
        xl: "28px",
        full: "9999px",
      },
      animation: {
        'loading-skeleton': 'loading-skeleton 2s infinite',
        'pulse-opacity': 'pulse-opacity 1s infinite',
        'spin': 'spin 1s linear infinite',
        'dash': 'dash 1.5s ease-in-out infinite',
      },
      keyframes: {
        'loading-skeleton': {
          '0%': { backgroundPosition: '200% 0' },
          '100%': { backgroundPosition: '-200% 0' },
        },
        'pulse-opacity': {
          '0%, 100%': { opacity: '0.4' },
          '50%': { opacity: '1' },
        },
        'dash': {
          '0%': { strokeDasharray: '1, 200', strokeDashoffset: '0' },
          '50%': { strokeDasharray: '40, 200', strokeDashoffset: '-20px' },
          '100%': { strokeDasharray: '40, 200', strokeDashoffset: '-60px' },
        }
      }
    },
  },
  plugins: [],
}

import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#16a765",
        primaryLight: "#e6f4ea",
        primaryDark: "#0d7a3e",
        accent: "#22c55e",
        white: "#ffffff",
        graySoft: "#f3f4f6",
        grayDark: "#111827",
        dark: "#111827",
      },
      boxShadow: {
        soft: "0 2px 10px rgba(0,0,0,0.06)",
        glow: "0 0 0 3px rgba(22,167,101,0.25)",
      },
      keyframes: {
        fadeIn: { "0%": { opacity: "0" }, "100%": { opacity: "1" } },
        slideUp: { "0%": { opacity: "0", transform: "translateY(20px)" }, "100%": { opacity: "1", transform: "translateY(0)" } },
        slideRight: { "0%": { opacity: "0", transform: "translateX(-20px)" }, "100%": { opacity: "1", transform: "translateX(0)" } },
        pulseSoft: { "0%,100%": { opacity: "1" }, "50%": { opacity: "0.8" } },
        shake: { "0%,100%": { transform: "translateX(0)" }, "20%": { transform: "translateX(-6px)" }, "40%": { transform: "translateX(6px)" }, "60%": { transform: "translateX(-4px)" }, "80%": { transform: "translateX(4px)" } },
      },
      animation: {
        fadeIn: "fadeIn 0.35s ease-out",
        slideUp: "slideUp 0.45s ease-out",
        slideRight: "slideRight 0.35s ease-out",
        pulseSoft: "pulseSoft 2s ease-in-out infinite",
        shake: "shake 0.45s ease-in-out",
      },
    },
  },
  plugins: [],
} satisfies Config;
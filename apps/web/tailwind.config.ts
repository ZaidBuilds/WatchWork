import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        cream: "#FAF7F2",
        copper: "#C68B59",
        espresso: "#2C1810",
        coral: "#E8825A",
        ink: "#211915",
        line: "#E8DED3"
      },
      boxShadow: {
        soft: "0 16px 40px rgba(44, 24, 16, 0.08)"
      }
    }
  },
  plugins: []
};

export default config;

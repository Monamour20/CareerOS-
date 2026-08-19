import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        linen: "#f8f4ee",
        oyster: "#e7ded4",
        rose: "#c47a85",
        clay: "#a66d69",
        ink: "#242222",
        graphite: "#383231"
      },
      boxShadow: {
        glass: "0 24px 60px rgba(36, 34, 34, 0.12)"
      }
    }
  },
  plugins: []
};

export default config;

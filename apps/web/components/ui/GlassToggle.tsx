"use client";

import { motion } from "motion/react";

interface GlassToggleProps {
  value: boolean;
  onChange: (value: boolean) => void;
  labels?: [string, string];
}

export default function GlassToggle({ value, onChange, labels = ["Overview", "Details"] }: GlassToggleProps) {
  return (
    <motion.button
      type="button"
      onClick={() => onChange(!value)}
      aria-pressed={value}
      whileTap={{ scale: 0.985 }}
      className="glass-toggle relative flex h-[54px] w-[220px] items-center rounded-full border border-white/85 bg-white/[0.22] p-1.5 text-[#514744] shadow-[0_20px_46px_rgba(55,40,35,.14),inset_0_1px_0_rgba(255,255,255,.98),inset_0_-1px_0_rgba(255,255,255,.16)] backdrop-blur-2xl"
    >
      <motion.span
        aria-hidden="true"
        className="absolute left-1.5 top-1.5 bottom-1.5 w-[calc(50%-6px)] overflow-hidden rounded-full border border-white bg-white/[0.72] shadow-[0_9px_28px_rgba(55,40,35,.16),inset_0_1px_0_rgba(255,255,255,1)] backdrop-blur-xl"
        animate={{ x: value ? "100%" : "0%" }}
        transition={{ type: "spring", stiffness: 520, damping: 30, mass: 0.62 }}
      >
        <span className="absolute inset-x-5 top-1 h-px bg-white" />
        <span className="absolute -inset-4 rounded-full bg-[radial-gradient(circle_at_30%_15%,rgba(255,255,255,.86),transparent_46%)]" />
      </motion.span>
      <span className={`relative z-10 flex h-full w-1/2 items-center justify-center text-sm transition-colors duration-200 ${!value ? "font-semibold text-[#302a28]" : "text-[#81736f]"}`}>{labels[0]}</span>
      <span className={`relative z-10 flex h-full w-1/2 items-center justify-center text-sm transition-colors duration-200 ${value ? "font-semibold text-[#302a28]" : "text-[#81736f]"}`}>{labels[1]}</span>
    </motion.button>
  );
}

"use client";

import { motion } from "motion/react";
import type { ReactNode } from "react";

interface GlassGlowProps {
  children: ReactNode;
  className?: string;
  intensity?: "soft" | "medium" | "strong";
}

const values = {
  soft: { opacity: 0.14, scale: 1.035 },
  medium: { opacity: 0.21, scale: 1.055 },
  strong: { opacity: 0.29, scale: 1.08 },
};

export default function GlassGlow({ children, className = "", intensity = "medium" }: GlassGlowProps) {
  const value = values[intensity];
  return (
    <div className={`relative ${className}`}>
      <motion.div
        aria-hidden="true"
        className="pointer-events-none absolute -inset-16 rounded-[52px] blur-3xl"
        style={{ background: "radial-gradient(circle, rgba(235,157,140,.86) 0%, rgba(235,157,140,.28) 34%, rgba(255,240,235,.10) 50%, transparent 72%)" }}
        animate={{ scale: [0.94, value.scale, 0.94], opacity: [value.opacity * .58, value.opacity, value.opacity * .58] }}
        transition={{ duration: 5.5, repeat: Infinity, ease: "easeInOut" }}
      />
      <div className="relative z-10">{children}</div>
    </div>
  );
}

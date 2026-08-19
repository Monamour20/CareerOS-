"use client";

import { motion } from "motion/react";
import type { CSSProperties, PointerEvent, ReactNode } from "react";

interface GlassSurfaceProps {
  children: ReactNode;
  className?: string;
  interactive?: boolean;
  glow?: boolean;
  intensity?: "soft" | "medium" | "strong";
}

const intensityMap = {
  soft: { alpha: 0.22, glow: 0.18 },
  medium: { alpha: 0.31, glow: 0.26 },
  strong: { alpha: 0.40, glow: 0.34 },
};

export default function GlassSurface({
  children,
  className = "",
  interactive = true,
  glow = true,
  intensity = "medium",
}: GlassSurfaceProps) {
  const { alpha, glow: glowStrength } = intensityMap[intensity];

  const handlePointerMove = (event: PointerEvent<HTMLDivElement>) => {
    if (!interactive) return;
    const el = event.currentTarget;
    const rect = el.getBoundingClientRect();
    const x = Math.max(0, Math.min(100, ((event.clientX - rect.left) / rect.width) * 100));
    const y = Math.max(0, Math.min(100, ((event.clientY - rect.top) / rect.height) * 100));
    el.style.setProperty("--glass-x", `${x}%`);
    el.style.setProperty("--glass-y", `${y}%`);
    el.style.setProperty("--glass-alpha", "1");
  };

  const handlePointerLeave = (event: PointerEvent<HTMLDivElement>) => {
    if (!interactive) return;
    const el = event.currentTarget;
    el.style.setProperty("--glass-x", "50%");
    el.style.setProperty("--glass-y", "18%");
    el.style.setProperty("--glass-alpha", "0.62");
  };

  const style = {
    "--glass-x": "50%",
    "--glass-y": "18%",
    "--glass-alpha": "0.62",
    "--glass-bg": `rgba(255,255,255,${alpha})`,
  } as CSSProperties;

  return (
    <motion.div
      onPointerMove={handlePointerMove}
      onPointerLeave={handlePointerLeave}
      style={style}
      className={`glass-surface group relative overflow-hidden rounded-[30px] border border-white/80 ${interactive ? "will-change-transform" : ""} ${className}`}
      whileHover={interactive ? { y: -3, scale: 1.004 } : undefined}
      transition={{ type: "spring", stiffness: 320, damping: 28, mass: 0.65 }}
    >
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 rounded-[inherit]"
        style={{
          background: `radial-gradient(560px circle at var(--glass-x) var(--glass-y), rgba(255,255,255,0.60), transparent 40%), radial-gradient(440px circle at calc(var(--glass-x) + 8%) calc(var(--glass-y) + 10%), rgba(232,169,154,0.22), transparent 60%)`,
          opacity: "var(--glass-alpha)",
        }}
      />

      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 rounded-[inherit]"
        style={{
          background: "linear-gradient(125deg,rgba(255,255,255,.44),transparent 26%,transparent 66%,rgba(255,255,255,.12))",
          opacity: 0.9,
        }}
      />

      <div aria-hidden="true" className="glass-specular pointer-events-none absolute -inset-y-20 -left-1/2 w-[48%] rotate-[18deg]" />

      {glow ? (
        <div
          aria-hidden="true"
          className="pointer-events-none absolute -inset-28 rounded-full blur-3xl transition-opacity duration-500"
          style={{
            opacity: `calc(var(--glass-alpha) * ${glowStrength})`,
            background: "radial-gradient(circle at var(--glass-x) var(--glass-y), rgba(238,157,137,.48), rgba(238,157,137,.10) 35%, transparent 70%)",
          }}
        />
      ) : null}

      <div className="relative z-10">{children}</div>
    </motion.div>
  );
}

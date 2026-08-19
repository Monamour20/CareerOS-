"use client";

import { motion } from "motion/react";
import type { ReactNode } from "react";

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  interactive?: boolean;
}

export default function GlassCard({
  children,
  className = "",
  interactive = true,
}: GlassCardProps) {
  return (
    <motion.div
      className={[
        "relative overflow-hidden rounded-[24px]",
        "border border-white/70",
        "bg-white/45 backdrop-blur-2xl",
        "shadow-[0_18px_50px_rgba(40,30,30,0.12),inset_0_1px_0_rgba(255,255,255,0.9)]",
        interactive
          ? "transition-shadow duration-300 hover:shadow-[0_24px_60px_rgba(40,30,30,0.18),inset_0_1px_0_rgba(255,255,255,1)]"
          : "",
        className,
      ].join(" ")}
      initial={{ opacity: 0, y: 18, scale: 0.985 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{
        duration: 0.55,
        ease: [0.22, 1, 0.36, 1],
      }}
      whileHover={
        interactive
          ? {
              y: -3,
              scale: 1.008,
              transition: {
                duration: 0.25,
                ease: [0.22, 1, 0.36, 1],
              },
            }
          : undefined
      }
      whileTap={
        interactive
          ? {
              scale: 0.995,
            }
          : undefined
      }
    >
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-gradient-to-br from-white/55 via-transparent to-[#7d615e]/10"
      />

      <div className="relative z-10">{children}</div>
    </motion.div>
  );
}
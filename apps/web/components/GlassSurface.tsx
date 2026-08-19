"use client";

import { motion } from "motion/react";
import type { ReactNode } from "react";
import { useRef, useState } from "react";

interface GlassSurfaceProps {
  children: ReactNode;
  className?: string;
  interactive?: boolean;
}

export default function GlassSurface({
  children,
  className = "",
  interactive = true,
}: GlassSurfaceProps) {
  const ref = useRef<HTMLDivElement>(null);

  const [light, setLight] = useState({
    x: 50,
    y: 30,
  });

  function handlePointerMove(
    event: React.PointerEvent<HTMLDivElement>,
  ) {
    if (!interactive || !ref.current) return;

    const rect = ref.current.getBoundingClientRect();

    setLight({
      x: ((event.clientX - rect.left) / rect.width) * 100,
      y: ((event.clientY - rect.top) / rect.height) * 100,
    });
  }

  return (
    <motion.div
      ref={ref}
      onPointerMove={handlePointerMove}
      className={`relative overflow-hidden rounded-[26px] border border-white/65 bg-white/[0.36] shadow-[0_22px_60px_rgba(52,43,40,0.12),inset_0_1px_0_rgba(255,255,255,0.92)] backdrop-blur-2xl ${className}`}
      whileHover={
        interactive
          ? {
              y: -2,
              transition: {
                duration: 0.25,
              },
            }
          : undefined
      }
    >
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0"
        style={{
          background: `radial-gradient(circle at ${light.x}% ${light.y}%, rgba(255,255,255,0.48), transparent 32%)`,
        }}
      />

      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-gradient-to-br from-white/[0.42] via-transparent to-[#7d615e]/[0.09]"
      />

      <div className="relative z-10">
        {children}
      </div>
    </motion.div>
  );
}
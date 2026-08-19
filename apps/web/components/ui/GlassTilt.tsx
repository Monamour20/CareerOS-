"use client";

import { motion, useMotionValue, useSpring, useTransform } from "motion/react";
import type { PointerEvent, ReactNode } from "react";

interface GlassTiltProps {
  children: ReactNode;
  className?: string;
  intensity?: "soft" | "medium" | "strong";
}

const limits = { soft: 4.5, medium: 7.5, strong: 10 };

export default function GlassTilt({ children, className = "", intensity = "medium" }: GlassTiltProps) {
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const sx = useSpring(x, { stiffness: 220, damping: 25, mass: 0.45 });
  const sy = useSpring(y, { stiffness: 220, damping: 25, mass: 0.45 });
  const limit = limits[intensity];

  const rotateX = useTransform(sy, [-1, 1], [limit, -limit]);
  const rotateY = useTransform(sx, [-1, 1], [-limit, limit]);
  const lift = useTransform(sy, [-1, 0, 1], [1, 0, 1]);

  const handlePointerMove = (event: PointerEvent<HTMLDivElement>) => {
    const rect = event.currentTarget.getBoundingClientRect();
    x.set(((event.clientX - rect.left) / rect.width) * 2 - 1);
    y.set(((event.clientY - rect.top) / rect.height) * 2 - 1);
  };

  const reset = () => { x.set(0); y.set(0); };

  return (
    <motion.div
      className={`relative [perspective:1500px] ${className}`}
      onPointerMove={handlePointerMove}
      onPointerLeave={reset}
      style={{ transformStyle: "preserve-3d" }}
    >
      <motion.div
        className="relative transform-gpu [transform-style:preserve-3d]"
        style={{ rotateX, rotateY, y: lift }}
        transition={{ type: "spring", stiffness: 260, damping: 28 }}
      >
        {children}
      </motion.div>
    </motion.div>
  );
}

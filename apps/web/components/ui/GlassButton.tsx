"use client";

import { motion } from "motion/react";
import type { ReactNode } from "react";

interface GlassButtonProps {
  children: ReactNode;
  active?: boolean;
  className?: string;
  disabled?: boolean;
  onClick?: () => void;
}

export default function GlassButton({
  children,
  active = false,
  className = "",
  disabled = false,
  onClick,
}: GlassButtonProps) {
  return (
    <motion.button
      type="button"
      disabled={disabled}
      onClick={onClick}
      whileHover={
        disabled
          ? undefined
          : {
              y: -1,
              scale: 1.01,
            }
      }
      whileTap={
        disabled
          ? undefined
          : {
              scale: 0.98,
            }
      }
      transition={{
        type: "spring",
        stiffness: 400,
        damping: 25,
      }}
      className={[
        "relative overflow-hidden rounded-2xl border px-4 py-2.5 text-sm",
        "backdrop-blur-xl transition-colors",
        active
          ? "border-white/80 bg-white/[0.16] text-white shadow-[inset_0_1px_0_rgba(255,255,255,0.2)]"
          : "border-transparent text-white/65 hover:bg-white/[0.07] hover:text-white",
        disabled ? "cursor-not-allowed opacity-50" : "",
        className,
      ].join(" ")}
    >
      {active && (
        <span
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 bg-gradient-to-r from-[#d99a8c]/25 via-white/[0.04] to-transparent"
        />
      )}

      <span className="relative z-10 flex items-center gap-3">
        {children}
      </span>
    </motion.button>
  );
}
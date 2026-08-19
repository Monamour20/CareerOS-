export const spring = {
  type: "spring",
  stiffness: 280,
  damping: 28,
  mass: 0.7,
} as const;

export const softSpring = {
  type: "spring",
  stiffness: 190,
  damping: 24,
  mass: 0.8,
} as const;

export const fadeUp = {
  initial: { opacity: 0, y: 18 },
  animate: { opacity: 1, y: 0 },
  transition: {
    duration: 0.55,
    ease: [0.22, 1, 0.36, 1],
  },
} as const;
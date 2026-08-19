"use client";

import { FileSearch, Brain, Database } from "lucide-react";
import { motion } from "motion/react";
import GlassGlow from "@/components/ui/GlassGlow";
import GlassSurface from "@/components/ui/GlassSurface";

const stages = [
  {
    icon: FileSearch,
    title: "Reading your resume",
    description: "Extracting your professional information.",
  },
  {
    icon: Brain,
    title: "Understanding your career",
    description: "AI is identifying skills, experience, and direction.",
  },
  {
    icon: Database,
    title: "Building your profile",
    description: "Preparing your persistent CareerOS profile.",
  },
];

export default function ResumeAnalyzing() {
  return (
    <GlassGlow intensity="strong">
      <GlassSurface className="rounded-[32px] p-8 md:p-12">
        <div className="mx-auto max-w-3xl text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{
              duration: 5,
              repeat: Infinity,
              ease: "linear",
            }}
            className="mx-auto flex h-20 w-20 items-center justify-center rounded-full border border-white/80 bg-white/45 shadow-[0_18px_50px_rgba(60,40,40,0.14)]"
          >
            <Brain className="h-9 w-9 text-[#a06e65]" />
          </motion.div>

          <h2 className="mt-7 text-3xl font-medium text-[#302827]">
            Understanding your career
          </h2>

          <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-[#776663]">
            CareerOS is turning your resume into structured career
            intelligence. This may take a moment.
          </p>

          <div className="mt-10 space-y-4 text-left">
            {stages.map((stage, index) => {
              const Icon = stage.icon;

              return (
                <motion.div
                  key={stage.title}
                  initial={{ opacity: 0, x: -15 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{
                    delay: index * 0.35,
                    duration: 0.5,
                  }}
                  className="flex items-center gap-4 rounded-[22px] border border-white/70 bg-white/30 p-4"
                >
                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-[16px] bg-white/55">
                    <Icon className="h-5 w-5 text-[#94665e]" />
                  </div>

                  <div>
                    <p className="text-sm font-medium text-[#302827]">
                      {stage.title}
                    </p>
                    <p className="mt-1 text-xs text-[#776663]">
                      {stage.description}
                    </p>
                  </div>

                  <motion.div
                    className="ml-auto h-2 w-2 rounded-full bg-[#d58c7d]"
                    animate={{
                      opacity: [0.25, 1, 0.25],
                      scale: [0.8, 1.25, 0.8],
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                      delay: index * 0.25,
                    }}
                  />
                </motion.div>
              );
            })}
          </div>
        </div>
      </GlassSurface>
    </GlassGlow>
  );
}
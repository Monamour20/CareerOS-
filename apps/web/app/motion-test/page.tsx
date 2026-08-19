"use client";

import { useState } from "react";
import GlassCard from "@/components/ui/GlassCard";
import GlassGlow from "@/components/ui/GlassGlow";
import GlassTilt from "@/components/ui/GlassTilt";
import GlassToggle from "@/components/ui/GlassToggle";

export default function MotionTestPage() {
  const [active, setActive] = useState(false);

  return (
    <main className="min-h-screen bg-[#e8e0dc] p-12 text-[#211d1d]">
      <div className="mx-auto max-w-5xl">
        <p className="text-xs uppercase tracking-[0.3em] text-[#8a6b66]">
          CareerOS Motion Lab
        </p>

        <h1 className="mt-3 text-5xl font-semibold">
          Physical Glass System
        </h1>

        <p className="mt-4 max-w-2xl text-[#625856]">
          Testing the material, light and movement before applying them to
          CareerOS.
        </p>

        <div className="mt-14 grid gap-8 md:grid-cols-2">
          <GlassTilt intensity="medium">
            <GlassGlow intensity="strong">
              <GlassCard className="min-h-[280px] p-8">
                <p className="text-sm text-[#776663]">
                  Profile Completeness
                </p>

                <div className="mt-10 text-7xl font-light">
                  92%
                </div>

                <p className="mt-4 text-sm text-[#776663]">
                  Excellent! Keep it up.
                </p>
              </GlassCard>
            </GlassGlow>
          </GlassTilt>

          <GlassCard className="flex min-h-[280px] flex-col items-center justify-center p-8">
            <p className="mb-8 text-sm text-[#776663]">
              CareerOS Glass Toggle
            </p>

            <GlassToggle
              value={active}
              onChange={setActive}
              labels={["Overview", "Details"]}
            />

            <p className="mt-8 text-sm text-[#776663]">
              Active: {active ? "Details" : "Overview"}
            </p>
          </GlassCard>
        </div>
      </div>
    </main>
  );
}
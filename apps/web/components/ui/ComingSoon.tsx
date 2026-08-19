"use client";

import { Clock } from "lucide-react";

export function ComingSoon({ label }: { label: string }) {
  return (
    <div className="flex items-center gap-2 rounded-[8px] border border-white/40 bg-white/25 px-4 py-3 text-sm text-graphite/60">
      <Clock className="h-4 w-4" />
      <span>{label} — Coming soon</span>
    </div>
  );
}

"use client";

export function LoadingSpinner({ size = 20 }: { size?: number }) {
  return (
    <span
      style={{ width: size, height: size }}
      className="inline-block animate-spin rounded-full border-2 border-current border-t-transparent"
      aria-label="Loading"
    />
  );
}

export function LoadingOverlay({ label = "Loading..." }: { label?: string }) {
  return (
    <div className="flex min-h-[200px] flex-col items-center justify-center gap-3 text-graphite">
      <LoadingSpinner size={28} />
      <p className="text-sm">{label}</p>
    </div>
  );
}

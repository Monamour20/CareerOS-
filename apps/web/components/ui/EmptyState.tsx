"use client";

import { InboxIcon } from "lucide-react";

interface EmptyStateProps {
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export function EmptyState({ title, description, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-10 text-center text-graphite">
      <InboxIcon className="h-8 w-8 opacity-40" />
      <p className="font-medium">{title}</p>
      {description && <p className="max-w-xs text-sm opacity-70">{description}</p>}
      {action}
    </div>
  );
}

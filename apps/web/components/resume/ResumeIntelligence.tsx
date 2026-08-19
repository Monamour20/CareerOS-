"use client";

import { useState } from "react";
import { AlertCircle, ArrowLeft, Sparkles } from "lucide-react";
import { motion } from "motion/react";

import GlassSurface from "@/components/ui/GlassSurface";
import ResumeDropzone from "./ResumeDropzone";
import ResumeAnalyzing from "./ResumeAnalyzing";
import ResumeAnalysisResult from "./ResumeAnalysisResult";
import { api } from "@/lib/api";
import type { CareerProfile } from "@/lib/types";

interface ResumeIntelligenceProps {
  token: string;
  onBack?: () => void;
}

type Stage = "upload" | "analyzing" | "result";

export default function ResumeIntelligence({
  token,
  onBack,
}: ResumeIntelligenceProps) {
  const [file, setFile] = useState<File | null>(null);
  const [stage, setStage] = useState<Stage>("upload");
  const [profile, setProfile] = useState<CareerProfile | null>(null);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!file || !token) return;

    setError("");
    setStage("analyzing");

    try {
      const response = await api.analyzeResume(token, file);

      setProfile(response.career_profile);
      setStage("result");
    } catch (err) {
      setStage("upload");

      setError(
        err instanceof Error
          ? err.message
          : "CareerOS could not analyze this resume.",
      );
    }
  };

  const handleReset = () => {
    setFile(null);
    setProfile(null);
    setError("");
    setStage("upload");
  };

  return (
    <main className="min-h-screen px-4 py-6 md:px-8 md:py-8">
      <div className="mx-auto max-w-7xl">
        <div className="mb-8 flex items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs uppercase tracking-[0.25em] text-[#9a6b63]">
              <Sparkles className="h-4 w-4" />
              CareerOS Intelligence
            </div>

            <h1 className="mt-3 text-3xl font-medium tracking-tight text-[#302827] md:text-4xl">
              Resume Intelligence
            </h1>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-[#776663]">
              Turn your resume into a living career profile that CareerOS can
              use across your professional journey.
            </p>
          </div>

          {onBack && (
            <button
              type="button"
              onClick={onBack}
              className="inline-flex shrink-0 items-center gap-2 rounded-full border border-white/80 bg-white/45 px-4 py-2.5 text-sm text-[#625856] shadow-sm backdrop-blur-xl transition hover:bg-white/70"
            >
              <ArrowLeft className="h-4 w-4" />
              Dashboard
            </button>
          )}
        </div>

        {stage === "upload" && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <ResumeDropzone
              file={file}
              onFileChange={(selectedFile) => {
                setFile(selectedFile);
                setError("");
              }}
            />

            {error && (
              <GlassSurface className="mt-5 flex items-center gap-3 rounded-[20px] border-red-200/60 bg-red-50/35 p-4 text-sm text-red-800">
                <AlertCircle className="h-5 w-5 shrink-0" />
                <span>{error}</span>
              </GlassSurface>
            )}

            <div className="mt-6 flex justify-center">
              <button
                type="button"
                disabled={!file}
                onClick={handleAnalyze}
                className="rounded-full bg-[#302827] px-7 py-3.5 text-sm font-medium text-white shadow-[0_15px_35px_rgba(48,40,39,0.18)] transition hover:-translate-y-0.5 hover:bg-[#403533] disabled:cursor-not-allowed disabled:opacity-40"
              >
                Analyze my resume
              </button>
            </div>
          </motion.div>
        )}

        {stage === "analyzing" && <ResumeAnalyzing />}

        {stage === "result" && profile && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <ResumeAnalysisResult
              profile={profile}
              fileName={file?.name ?? "resume"}
              onAnalyzeAnother={handleReset}
            />
          </motion.div>
        )}
      </div>
    </main>
  );
}
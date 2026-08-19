"use client";

import { useCallback, useRef, useState } from "react";
import { FileText, Upload, X } from "lucide-react";
import { motion } from "motion/react";
import GlassGlow from "@/components/ui/GlassGlow";
import GlassSurface from "@/components/ui/GlassSurface";

interface ResumeDropzoneProps {
  file: File | null;
  onFileChange: (file: File | null) => void;
  disabled?: boolean;
}

const ACCEPTED_TYPES = [
  "application/pdf",
  "application/msword",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "text/plain",
];

const ACCEPTED_EXTENSIONS = [".pdf", ".doc", ".docx", ".txt"];

export default function ResumeDropzone({
  file,
  onFileChange,
  disabled = false,
}: ResumeDropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState("");

  const validateFile = useCallback((candidate: File) => {
    const lowerName = candidate.name.toLowerCase();
    const validExtension = ACCEPTED_EXTENSIONS.some((extension) =>
      lowerName.endsWith(extension),
    );

    const validType =
      !candidate.type || ACCEPTED_TYPES.includes(candidate.type);

    if (!validExtension || !validType) {
      setError("Please upload a PDF, DOC, DOCX, or TXT file.");
      return false;
    }

    if (candidate.size === 0) {
      setError("This file is empty. Please choose another file.");
      return false;
    }

    if (candidate.size > 15 * 1024 * 1024) {
      setError("File size must be 15 MB or smaller.");
      return false;
    }

    setError("");
    return true;
  }, []);

  const selectFile = useCallback(
    (candidate: File | undefined) => {
      if (!candidate || disabled) return;

      if (validateFile(candidate)) {
        onFileChange(candidate);
      }
    },
    [disabled, onFileChange, validateFile],
  );

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragging(false);
    selectFile(event.dataTransfer.files?.[0]);
  };

  return (
    <GlassGlow intensity="strong">
      <GlassSurface
        className={`relative overflow-hidden rounded-[32px] p-8 transition-all duration-300 md:p-12 ${
          dragging
            ? "scale-[1.01] border-[#ee9d89]/70 bg-white/55"
            : ""
        }`}
      >
        <div
          onDragEnter={(event) => {
            event.preventDefault();
            if (!disabled) setDragging(true);
          }}
          onDragOver={(event) => event.preventDefault()}
          onDragLeave={(event) => {
            event.preventDefault();
            setDragging(false);
          }}
          onDrop={handleDrop}
          onClick={() => {
            if (!disabled && !file) inputRef.current?.click();
          }}
          className={`relative flex min-h-[320px] cursor-pointer flex-col items-center justify-center rounded-[26px] border border-dashed border-white/80 bg-white/20 px-6 text-center ${
            disabled ? "cursor-not-allowed opacity-70" : ""
          }`}
        >
          <input
            ref={inputRef}
            type="file"
            hidden
            accept=".pdf,.doc,.docx,.txt"
            disabled={disabled}
            onChange={(event) => {
              selectFile(event.target.files?.[0]);
              event.target.value = "";
            }}
          />

          {file ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.94 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex w-full max-w-xl flex-col items-center"
            >
              <div className="flex h-20 w-20 items-center justify-center rounded-[24px] border border-white/80 bg-white/55 shadow-[0_15px_40px_rgba(60,40,40,0.12)]">
                <FileText className="h-9 w-9 text-[#8a625c]" />
              </div>

              <p className="mt-6 max-w-full truncate text-lg font-medium text-[#302827]">
                {file.name}
              </p>

              <p className="mt-2 text-sm text-[#776663]">
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>

              {!disabled && (
                <button
                  type="button"
                  onClick={(event) => {
                    event.stopPropagation();
                    onFileChange(null);
                  }}
                  className="mt-6 inline-flex items-center gap-2 rounded-full border border-white/80 bg-white/50 px-4 py-2 text-sm text-[#625856] transition hover:bg-white/75"
                >
                  <X className="h-4 w-4" />
                  Remove file
                </button>
              )}
            </motion.div>
          ) : (
            <>
              <motion.div
                animate={{
                  y: dragging ? -8 : [0, -5, 0],
                  rotate: dragging ? 0 : [0, 1.5, -1.5, 0],
                }}
                transition={{
                  duration: 3.5,
                  repeat: dragging ? 0 : Infinity,
                  ease: "easeInOut",
                }}
                className="flex h-20 w-20 items-center justify-center rounded-[26px] border border-white/90 bg-white/55 shadow-[0_18px_45px_rgba(60,40,40,0.14)]"
              >
                <Upload className="h-9 w-9 text-[#9b6a61]" />
              </motion.div>

              <h3 className="mt-7 text-2xl font-medium text-[#302827]">
                {dragging ? "Drop your resume here" : "Drop your resume here"}
              </h3>

              <p className="mt-3 text-sm text-[#776663]">
                or click to browse your computer
              </p>

              <div className="mt-5 flex flex-wrap justify-center gap-2">
                {["PDF", "DOC", "DOCX", "TXT"].map((type) => (
                  <span
                    key={type}
                    className="rounded-full border border-white/80 bg-white/35 px-3 py-1 text-xs text-[#776663]"
                  >
                    {type}
                  </span>
                ))}
              </div>
            </>
          )}
        </div>

        {error && (
          <p className="mt-4 text-center text-sm font-medium text-red-700">
            {error}
          </p>
        )}
      </GlassSurface>
    </GlassGlow>
  );
}
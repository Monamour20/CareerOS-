"use client";

import {
  Award,
  BriefcaseBusiness,
  GraduationCap,
  Rocket,
  Sparkles,
  UserRound,
} from "lucide-react";
import { motion } from "motion/react";

import GlassGlow from "@/components/ui/GlassGlow";
import GlassSurface from "@/components/ui/GlassSurface";
import type { CareerProfile } from "@/lib/types";

interface ResumeAnalysisResultProps {
  profile: CareerProfile;
  fileName: string;
  onAnalyzeAnother: () => void;
}

function getSkills(profile: CareerProfile): string[] {
  const groups = profile.skills;

  return Object.values(groups).flatMap((value) =>
    Array.isArray(value)
      ? value.filter(
          (item): item is string => typeof item === "string",
        )
      : [],
  );
}

export default function ResumeAnalysisResult({
  profile,
  fileName,
  onAnalyzeAnother,
}: ResumeAnalysisResultProps) {
  const skills = getSkills(profile);

  const experience = profile.experience ?? [];
  const education = profile.education ?? [];

  const personal = profile.personal_information;

  const summary =
    personal.summary ||
    "CareerOS has successfully created a structured career profile from your resume.";

  const firstName =
    personal.full_name ||
    personal.email ||
    "Your career profile";

  return (
    <div className="space-y-8">
      <GlassGlow intensity="strong">
        <GlassSurface className="overflow-hidden rounded-[32px] p-8 md:p-10">
          <div className="flex flex-col justify-between gap-6 md:flex-row md:items-center">
            <div>
              <div className="flex items-center gap-2 text-xs uppercase tracking-[0.25em] text-[#9a6b63]">
                <Sparkles className="h-4 w-4" />
                Career Intelligence
              </div>

              <h2 className="mt-4 text-3xl font-medium text-[#302827]">
                Your career profile is ready.
              </h2>

              <p className="mt-2 text-sm text-[#776663]">
                Built from{" "}
                <span className="font-medium">{fileName}</span>
              </p>
            </div>

            <button
              type="button"
              onClick={onAnalyzeAnother}
              className="rounded-full border border-white/80 bg-white/50 px-5 py-3 text-sm font-medium text-[#625856] shadow-sm transition hover:bg-white/75"
            >
              Analyze another resume
            </button>
          </div>
        </GlassSurface>
      </GlassGlow>

      <div className="grid gap-6 md:grid-cols-3">
        {[
          {
            icon: UserRound,
            label: "Identity",
            value: firstName,
          },
          {
            icon: Award,
            label: "Skills identified",
            value: String(skills.length),
          },
          {
            icon: BriefcaseBusiness,
            label: "Experience entries",
            value: String(experience.length),
          },
        ].map((metric, index) => {
          const Icon = metric.icon;

          return (
            <motion.div
              key={metric.label}
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.08 }}
            >
              <GlassSurface className="h-full rounded-[28px] p-7">
                <div className="flex h-11 w-11 items-center justify-center rounded-[16px] bg-white/55">
                  <Icon className="h-5 w-5 text-[#96665e]" />
                </div>

                <p className="mt-6 text-xs uppercase tracking-[0.18em] text-[#8c7772]">
                  {metric.label}
                </p>

                <p className="mt-2 truncate text-xl font-medium text-[#302827]">
                  {metric.value}
                </p>
              </GlassSurface>
            </motion.div>
          );
        })}
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
        <GlassSurface className="rounded-[28px] p-8">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-[16px] bg-white/55">
              <Sparkles className="h-5 w-5 text-[#96665e]" />
            </div>

            <div>
              <p className="text-sm font-medium text-[#302827]">
                Career Summary
              </p>

              <p className="text-xs text-[#8c7772]">
                AI-generated from your professional information
              </p>
            </div>
          </div>

          <p className="mt-7 text-base leading-8 text-[#514644]">
            {summary}
          </p>
        </GlassSurface>

        <GlassSurface className="rounded-[28px] p-8">
          <div className="flex items-center gap-3">
            <Rocket className="h-5 w-5 text-[#96665e]" />

            <p className="text-sm font-medium text-[#302827]">
              Career direction
            </p>
          </div>

          <div className="mt-6 space-y-3">
            {profile.career_interests.target_roles.length > 0 ? (
              profile.career_interests.target_roles.map((role) => (
                <div
                  key={role}
                  className="rounded-[18px] border border-white/70 bg-white/30 px-4 py-3 text-sm text-[#625856]"
                >
                  {role}
                </div>
              ))
            ) : (
              <p className="text-sm leading-7 text-[#625856]">
                Your CareerOS profile can now be used to guide future career
                decisions.
              </p>
            )}
          </div>
        </GlassSurface>
      </div>

      <GlassSurface className="rounded-[28px] p-8">
        <div className="flex items-center gap-3">
          <Award className="h-5 w-5 text-[#96665e]" />

          <h3 className="text-lg font-medium text-[#302827]">
            Skills identified
          </h3>
        </div>

        {skills.length > 0 ? (
          <div className="mt-6 flex flex-wrap gap-2">
            {skills.map((skill) => (
              <span
                key={skill}
                className="rounded-full border border-white/80 bg-white/40 px-4 py-2 text-sm text-[#625856]"
              >
                {skill}
              </span>
            ))}
          </div>
        ) : (
          <p className="mt-5 text-sm text-[#776663]">
            No structured skills were returned by the analysis.
          </p>
        )}
      </GlassSurface>

      <GlassSurface className="rounded-[28px] p-8">
        <div className="flex items-center gap-3">
          <BriefcaseBusiness className="h-5 w-5 text-[#96665e]" />

          <h3 className="text-lg font-medium text-[#302827]">
            Professional experience
          </h3>
        </div>

        {experience.length > 0 ? (
          <div className="mt-7 space-y-4">
            {experience.map((item, index) => (
              <motion.div
                key={`${item.company ?? "experience"}-${index}`}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.06 }}
                className="rounded-[22px] border border-white/70 bg-white/25 p-5"
              >
                <p className="font-medium text-[#302827]">
                  {item.title || "Professional experience"}
                </p>

                <p className="mt-1 text-sm text-[#776663]">
                  {item.company || ""}
                </p>

                {item.responsibilities.length > 0 && (
                  <ul className="mt-3 space-y-1 text-sm leading-6 text-[#625856]">
                    {item.responsibilities.map((responsibility) => (
                      <li key={responsibility}>
                        • {responsibility}
                      </li>
                    ))}
                  </ul>
                )}
              </motion.div>
            ))}
          </div>
        ) : (
          <p className="mt-5 text-sm text-[#776663]">
            No structured experience entries were returned.
          </p>
        )}
      </GlassSurface>

      {education.length > 0 && (
        <GlassSurface className="rounded-[28px] p-8">
          <div className="flex items-center gap-3">
            <GraduationCap className="h-5 w-5 text-[#96665e]" />

            <h3 className="text-lg font-medium text-[#302827]">
              Education
            </h3>
          </div>

          <div className="mt-6 space-y-3">
            {education.map((item, index) => (
              <div
                key={`${item.institution ?? "education"}-${index}`}
                className="rounded-[20px] border border-white/70 bg-white/25 p-5"
              >
                <p className="font-medium text-[#302827]">
                  {item.degree || "Education"}
                </p>

                <p className="mt-1 text-sm text-[#776663]">
                  {item.institution || ""}
                </p>
              </div>
            ))}
          </div>
        </GlassSurface>
      )}
    </div>
  );
}
"use client";

import { useCallback, useEffect, useState } from "react";
import {
  ArrowUpRight,
  BriefcaseBusiness,
  CheckCircle2,
  MapPin,
  RefreshCw,
  Sparkles,
  Target,
  XCircle,
} from "lucide-react";
import { motion } from "motion/react";

type JobSkill = {
  name: string;
  required: boolean;
};

type Job = {
  id: number;
  external_id: string | null;
  source: string;
  title: string;
  company: string;
  location: string | null;
  remote: boolean;
  employment_type: string | null;
  seniority: string | null;
  description: string;
  application_url: string | null;
  salary_min: number | null;
  salary_max: number | null;
  currency: string | null;
  posted_at: string | null;
  expires_at: string | null;
  skills: JobSkill[];
};

type Recommendation = {
  job: Job;
  score: number;
  category: string;
  matched_skills: string[];
  missing_skills: string[];
  reasons: string[];
};

type Props = {
  token: string;
};

const categoryLabels: Record<string, string> = {
  excellent: "Excellent Match",
  strong: "Strong Match",
  potential: "Potential Match",
  skill_gap: "Skill Gap",
};

function formatSalary(job: Job) {
  if (job.salary_min == null && job.salary_max == null) {
    return null;
  }

  const currency = job.currency === "INR" ? "₹" : job.currency || "";

  const format = (value: number) =>
    new Intl.NumberFormat("en-IN", {
      maximumFractionDigits: 0,
    }).format(value);

  if (job.salary_min != null && job.salary_max != null) {
    return `${currency}${format(job.salary_min)} – ${currency}${format(
      job.salary_max,
    )}`;
  }

  if (job.salary_min != null) {
    return `From ${currency}${format(job.salary_min)}`;
  }

  return `Up to ${currency}${format(job.salary_max!)}`;
}

function getScoreLabel(score: number) {
  if (score >= 85) return "Excellent";
  if (score >= 70) return "Strong";
  if (score >= 40) return "Potential";
  return "Low";
}

export default function JobRecommendations({ token }: Props) {
  const [recommendations, setRecommendations] = useState<Recommendation[]>(
    [],
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadRecommendations = useCallback(async () => {
    if (!token) {
      setLoading(false);
      setError("Please sign in again to load job recommendations.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/jobs/recommended", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        cache: "no-store",
      });

      if (!response.ok) {
        throw new Error("Unable to load job recommendations.");
      }

      const data = (await response.json()) as Recommendation[];
      setRecommendations(data);
    } catch (err) {
      setRecommendations([]);
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load job recommendations.",
      );
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    void loadRecommendations();
  }, [loadRecommendations]);

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <div className="mb-2 inline-flex items-center gap-2 rounded-full border border-white/70 bg-white/55 px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.18em] text-[#7a5b54] shadow-sm backdrop-blur-xl">
            <Sparkles size={13} />
            AI Career Matching
          </div>

          <h1 className="text-3xl font-semibold tracking-tight text-[#292525] sm:text-4xl">
            Recommended Jobs
          </h1>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-[#716a66] sm:text-base">
            Jobs ranked against your Career Vault, skills, target roles,
            seniority, and experience.
          </p>
        </div>

        <button
          type="button"
          onClick={() => void loadRecommendations()}
          disabled={loading}
          className="inline-flex h-11 items-center justify-center gap-2 rounded-xl border border-white/80 bg-white/60 px-4 text-sm font-semibold text-[#393332] shadow-[0_10px_30px_rgba(80,60,50,0.08)] backdrop-blur-xl transition hover:bg-white/80 disabled:cursor-not-allowed disabled:opacity-60"
        >
          <RefreshCw
            size={16}
            className={loading ? "animate-spin" : ""}
          />
          Refresh
        </button>
      </div>

      {loading ? (
        <div className="grid gap-5 xl:grid-cols-2">
          {[1, 2, 3, 4].map((item) => (
            <div
              key={item}
              className="animate-pulse rounded-[28px] border border-white/70 bg-white/45 p-6 shadow-[0_20px_60px_rgba(80,60,50,0.08)] backdrop-blur-2xl"
            >
              <div className="h-5 w-28 rounded-full bg-[#d9d0c9]" />
              <div className="mt-5 h-7 w-3/4 rounded-lg bg-[#d9d0c9]" />
              <div className="mt-3 h-4 w-1/2 rounded-lg bg-[#ddd5cf]" />
              <div className="mt-7 h-16 rounded-2xl bg-[#e2dad4]" />
              <div className="mt-5 flex gap-2">
                <div className="h-7 w-20 rounded-full bg-[#d9d0c9]" />
                <div className="h-7 w-24 rounded-full bg-[#d9d0c9]" />
              </div>
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="rounded-[28px] border border-red-200/80 bg-red-50/60 p-6 shadow-lg backdrop-blur-xl">
          <div className="flex items-start gap-3">
            <XCircle className="mt-0.5 text-red-500" size={20} />
            <div>
              <h2 className="font-semibold text-red-800">
                Recommendations unavailable
              </h2>
              <p className="mt-1 text-sm text-red-700">{error}</p>
              <button
                type="button"
                onClick={() => void loadRecommendations()}
                className="mt-4 rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white"
              >
                Try again
              </button>
            </div>
          </div>
        </div>
      ) : recommendations.length === 0 ? (
        <div className="rounded-[30px] border border-white/70 bg-white/50 px-6 py-14 text-center shadow-[0_20px_60px_rgba(80,60,50,0.08)] backdrop-blur-2xl">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border border-white/80 bg-white/70 shadow-sm">
            <BriefcaseBusiness size={25} className="text-[#9a7067]" />
          </div>

          <h2 className="mt-5 text-xl font-semibold text-[#302b29]">
            No strong matches yet
          </h2>

          <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-[#746d69]">
            Add more skills, projects, experience, or target roles to your
            Career Vault to improve recommendations.
          </p>
        </div>
      ) : (
        <>
          <div className="flex items-center gap-2 text-sm text-[#746d69]">
            <Target size={16} />
            <span>
              Showing {recommendations.length} personalized recommendation
              {recommendations.length === 1 ? "" : "s"}.
            </span>
          </div>

          <div className="grid gap-5 xl:grid-cols-2">
            {recommendations.map((recommendation, index) => {
              const salary = formatSalary(recommendation.job);

              return (
                <motion.article
                  key={recommendation.job.id}
                  initial={{ opacity: 0, y: 14 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{
                    duration: 0.35,
                    delay: Math.min(index * 0.06, 0.3),
                  }}
                  className="group relative overflow-hidden rounded-[28px] border border-white/75 bg-white/55 p-6 shadow-[0_22px_70px_rgba(80,60,50,0.09)] backdrop-blur-2xl transition duration-300 hover:-translate-y-1 hover:bg-white/65"
                >
                  <div className="pointer-events-none absolute -right-20 -top-20 h-48 w-48 rounded-full bg-[#e8b8ac]/20 blur-3xl transition group-hover:bg-[#e8b8ac]/30" />

                  <div className="relative">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <span className="inline-flex rounded-full border border-[#d9c2bb] bg-[#f8eeeb]/80 px-3 py-1 text-xs font-bold text-[#8b5f56]">
                          {categoryLabels[recommendation.category] ??
                            "Recommended"}
                        </span>

                        <h2 className="mt-4 text-xl font-semibold leading-tight text-[#2d2927]">
                          {recommendation.job.title}
                        </h2>

                        <p className="mt-1 font-medium text-[#716963]">
                          {recommendation.job.company}
                        </p>
                      </div>

                      <div className="shrink-0 text-center">
                        <div className="flex h-16 w-16 items-center justify-center rounded-full border border-white/80 bg-white/70 shadow-inner">
                          <span className="text-lg font-bold text-[#6f514a]">
                            {Math.round(recommendation.score)}
                          </span>
                        </div>

                        <span className="mt-1 block text-[10px] font-semibold uppercase tracking-wider text-[#8a817c]">
                          {getScoreLabel(recommendation.score)}
                        </span>
                      </div>
                    </div>

                    <div className="mt-5 flex flex-wrap gap-2 text-xs text-[#716a66]">
                      {recommendation.job.location && (
                        <span className="inline-flex items-center gap-1.5 rounded-full bg-white/65 px-3 py-1.5">
                          <MapPin size={13} />
                          {recommendation.job.location}
                        </span>
                      )}

                      {recommendation.job.remote && (
                        <span className="rounded-full bg-white/65 px-3 py-1.5">
                          Remote
                        </span>
                      )}

                      {recommendation.job.employment_type && (
                        <span className="rounded-full bg-white/65 px-3 py-1.5">
                          {recommendation.job.employment_type}
                        </span>
                      )}

                      {recommendation.job.seniority && (
                        <span className="rounded-full bg-white/65 px-3 py-1.5">
                          {recommendation.job.seniority}
                        </span>
                      )}
                    </div>

                    {salary && (
                      <p className="mt-4 text-sm font-semibold text-[#6c554e]">
                        {salary}
                      </p>
                    )}

                    {recommendation.reasons.length > 0 && (
                      <div className="mt-5 rounded-2xl border border-white/70 bg-white/45 p-4">
                        <p className="mb-2 text-xs font-bold uppercase tracking-[0.14em] text-[#8a7973]">
                          Why this matches
                        </p>

                        <ul className="space-y-2">
                          {recommendation.reasons.slice(0, 3).map((reason) => (
                            <li
                              key={reason}
                              className="flex gap-2 text-sm leading-5 text-[#5f5955]"
                            >
                              <CheckCircle2
                                size={15}
                                className="mt-0.5 shrink-0 text-[#8b6a62]"
                              />
                              {reason}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    <div className="mt-5">
                      <p className="mb-2 text-xs font-bold uppercase tracking-[0.14em] text-[#8a7973]">
                        Matched skills
                      </p>

                      <div className="flex flex-wrap gap-2">
                        {recommendation.matched_skills.length > 0 ? (
                          recommendation.matched_skills.map((skill) => (
                            <span
                              key={skill}
                              className="rounded-full border border-emerald-200/70 bg-emerald-50/70 px-3 py-1.5 text-xs font-semibold text-emerald-700"
                            >
                              {skill}
                            </span>
                          ))
                        ) : (
                          <span className="text-sm text-[#817a76]">
                            No direct skill matches detected.
                          </span>
                        )}
                      </div>
                    </div>

                    {recommendation.missing_skills.length > 0 && (
                      <div className="mt-4">
                        <p className="mb-2 text-xs font-bold uppercase tracking-[0.14em] text-[#8a7973]">
                          Skills to improve
                        </p>

                        <div className="flex flex-wrap gap-2">
                          {recommendation.missing_skills
                            .slice(0, 6)
                            .map((skill) => (
                              <span
                                key={skill}
                                className="rounded-full border border-amber-200/80 bg-amber-50/70 px-3 py-1.5 text-xs font-semibold text-amber-700"
                              >
                                {skill}
                              </span>
                            ))}
                        </div>
                      </div>
                    )}

                    <div className="mt-6 flex items-center justify-between gap-3 border-t border-white/60 pt-5">
                      <span className="text-xs text-[#8a817c]">
                        Source: {recommendation.job.source}
                      </span>

                      {recommendation.job.application_url ? (
                        <a
                          href={recommendation.job.application_url}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-2 rounded-xl bg-[#302a28] px-4 py-2.5 text-sm font-semibold text-white shadow-lg transition hover:-translate-y-0.5 hover:bg-[#201c1a]"
                        >
                          View Job
                          <ArrowUpRight size={15} />
                        </a>
                      ) : (
                        <span className="rounded-xl bg-white/70 px-4 py-2.5 text-sm font-semibold text-[#746b67]">
                          No application link
                        </span>
                      )}
                    </div>
                  </div>
                </motion.article>
              );
            })}
          </div>
        </>
      )}
    </section>
  );
}

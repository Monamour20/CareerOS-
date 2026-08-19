"use client";

import {
  ArrowUpRight,
  BriefcaseBusiness,
  ChevronRight,
  Clock3,
  FolderKanban,
  GraduationCap,
  Sparkles,
  Target,
} from "lucide-react";
import { motion } from "motion/react";
import { useEffect, useState } from "react";

import type { CareerProfile, User } from "@/lib/types";
import { profileCompleteness, totalSkills } from "@/lib/profile";
import GlassGlow from "@/components/ui/GlassGlow";
import GlassSurface from "@/components/ui/GlassSurface";
import GlassTilt from "@/components/ui/GlassTilt";
import GlassToggle from "@/components/ui/GlassToggle";

interface DashboardProps {
  profile: CareerProfile | null;
  user: User;
  onOpenVault: () => void;
}

function AnimatedNumber({ value, suffix = "" }: { value: number; suffix?: string }) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    let frame = 0;
    const start = performance.now();
    const duration = 850;

    const tick = (now: number) => {
      const progress = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplay(Math.round(value * eased));
      if (progress < 1) frame = requestAnimationFrame(tick);
    };

    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [value]);

  return (
    <motion.span
      key={`${value}-${suffix}`}
      initial={{ opacity: 0.45 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.35 }}
    >
      {display}{suffix}
    </motion.span>
  );
}

export default function Dashboard({ profile, user, onOpenVault }: DashboardProps) {
  const [details, setDetails] = useState(false);
  const completion = profileCompleteness(profile);
  const skills = totalSkills(profile);
  const projects = profile?.projects.length ?? 0;
  const experience = profile?.experience.length ?? 0;

  const stats = [
    { label: "Profile health", value: completion, suffix: "%", icon: Target, detail: completion >= 80 ? "Excellent" : "Needs attention" },
    { label: "Total skills", value: skills, icon: Sparkles, detail: "Across 4 categories" },
    { label: "Projects", value: projects, icon: FolderKanban, detail: "Career evidence" },
    { label: "Experience", value: experience, icon: BriefcaseBusiness, detail: "Career entries" },
  ];

  const skillGroups = [
    ["Technical", profile?.skills.technical ?? []],
    ["Tools", profile?.skills.tools ?? []],
    ["Languages", profile?.skills.languages ?? []],
    ["Soft skills", profile?.skills.soft_skills ?? []],
  ] as const;

  const projectsList = profile?.projects ?? [];
  const roles = profile?.career_interests.target_roles ?? [];

  return (
    <div className="space-y-6 pb-8">
      <motion.div
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1] }}
        className="flex flex-col gap-5 xl:flex-row xl:items-end xl:justify-between"
      >
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.26em] text-[#9b6258]">Career overview</p>
          <h1 className="mt-2 text-4xl font-semibold tracking-[-0.035em] text-[#242222] sm:text-5xl">
            Your career, in motion.
          </h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-[#6b605d]">
            A living view of your professional identity, evidence, skills, and direction.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <GlassToggle value={details} onChange={setDetails} labels={["Overview", "Details"]} />
          <button
            type="button"
            onClick={onOpenVault}
            className="group inline-flex items-center gap-2 rounded-full border border-white/75 bg-white/[0.32] px-4 py-3 text-sm font-medium text-[#403735] shadow-[0_12px_30px_rgba(52,43,40,0.1),inset_0_1px_0_rgba(255,255,255,0.9)] backdrop-blur-xl transition hover:bg-white/[0.48]"
          >
            Open Career Vault
            <ChevronRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
          </button>
        </div>
      </motion.div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 22, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ delay: index * 0.07, duration: 0.55, ease: [0.22, 1, 0.36, 1] }}
            >
              <GlassTilt intensity="soft">
                <GlassGlow intensity={index === 0 ? "medium" : "soft"}>
                  <GlassSurface className="min-h-[190px] p-5">
                    <div className="flex items-start justify-between">
                      <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-white/60 bg-white/[0.36] text-[#9b6258] shadow-[inset_0_1px_0_rgba(255,255,255,0.9)]">
                        <Icon className="h-5 w-5" />
                      </div>
                      <span className="rounded-full border border-white/60 bg-white/25 px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.16em] text-[#8a7b77]">
                        Live
                      </span>
                    </div>
                    <p className="mt-7 text-sm text-[#756966]">{stat.label}</p>
                    <p className="mt-1 text-4xl font-semibold tracking-[-0.04em] text-[#242222]">
                      <AnimatedNumber value={stat.value} suffix={stat.suffix} />
                    </p>
                    <p className="mt-2 text-xs text-[#8a7b77]">{stat.detail}</p>
                  </GlassSurface>
                </GlassGlow>
              </GlassTilt>
            </motion.div>
          );
        })}
      </div>

      {!details ? (
        <motion.div
          key="overview"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
          className="grid gap-5 xl:grid-cols-[1.15fr_0.85fr]"
        >
          <GlassSurface className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[#9b6258]">Career evidence</p>
                <h2 className="mt-1 text-xl font-semibold">Recent projects</h2>
              </div>
              <FolderKanban className="h-5 w-5 text-[#9b6258]" />
            </div>
            <div className="mt-6 space-y-3">
              {projectsList.length ? projectsList.slice(0, 4).map((project, index) => (
                <motion.div
                  key={`${project.name}-${index}`}
                  whileHover={{ x: 3, scale: 1.005 }}
                  transition={{ duration: 0.2 }}
                  className="rounded-2xl border border-white/55 bg-white/[0.27] p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.72)]"
                >
                  <div className="flex items-start gap-3">
                    <div className="mt-1.5 h-2 w-2 rounded-full bg-[#c98070] shadow-[0_0_16px_rgba(201,128,112,0.8)]" />
                    <div className="min-w-0 flex-1">
                      <div className="flex items-start justify-between gap-3">
                        <h3 className="font-medium text-[#302a28]">{project.name || "Untitled project"}</h3>
                        <ArrowUpRight className="h-4 w-4 shrink-0 text-[#a88a84]" />
                      </div>
                      <p className="mt-1 line-clamp-2 text-sm leading-5 text-[#756966]">{project.description || "No project description yet."}</p>
                      <div className="mt-3 flex flex-wrap gap-2">
                        {(project.technologies ?? []).slice(0, 4).map((tech) => (
                          <span key={tech} className="rounded-full border border-white/60 bg-white/[0.4] px-2.5 py-1 text-xs text-[#6e625e]">{tech}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                </motion.div>
              )) : (
                <div className="rounded-2xl border border-dashed border-white/65 bg-white/20 p-5 text-sm text-[#80736f]">Add projects to strengthen your career evidence.</div>
              )}
            </div>
          </GlassSurface>

          <GlassSurface className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[#9b6258]">Skill map</p>
                <h2 className="mt-1 text-xl font-semibold">Skills breakdown</h2>
              </div>
              <Sparkles className="h-5 w-5 text-[#9b6258]" />
            </div>
            <div className="mt-6 space-y-5">
              {skillGroups.map(([name, values]) => (
                <div key={name}>
                  <div className="mb-2 flex justify-between text-xs">
                    <span className="text-[#655a57]">{name}</span>
                    <span className="text-[#8a7b77]">{values.length}</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {values.length ? values.slice(0, 8).map((value) => (
                      <span key={value} className="rounded-full border border-white/65 bg-white/[0.4] px-3 py-1.5 text-xs text-[#514744]">{value}</span>
                    )) : <span className="text-xs text-[#9a8c88]">Not set</span>}
                  </div>
                </div>
              ))}
            </div>
          </GlassSurface>
        </motion.div>
      ) : (
        <motion.div
          key="details"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
          className="grid gap-5 lg:grid-cols-2"
        >
          <GlassSurface className="p-6">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-white/60 bg-white/[0.36] text-[#9b6258]"><GraduationCap className="h-5 w-5" /></div>
              <div><p className="text-xs uppercase tracking-[0.18em] text-[#9b6258]">Career direction</p><h2 className="font-semibold">Target roles</h2></div>
            </div>
            <div className="mt-6 flex flex-wrap gap-2">
              {roles.length ? roles.map((role) => <span key={role} className="rounded-full border border-white/65 bg-white/[0.42] px-3 py-2 text-sm text-[#514744]">{role}</span>) : <span className="text-sm text-[#8a7b77]">No target roles set.</span>}
            </div>
            <p className="mt-7 text-xs uppercase tracking-[0.18em] text-[#9b6258]">Career goals</p>
            <p className="mt-2 text-sm leading-6 text-[#655a57]">{user.career_goals || "No career goal recorded yet."}</p>
          </GlassSurface>

          <GlassSurface className="p-6">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-white/60 bg-white/[0.36] text-[#9b6258]"><Clock3 className="h-5 w-5" /></div>
              <div><p className="text-xs uppercase tracking-[0.18em] text-[#9b6258]">Career preferences</p><h2 className="font-semibold">Your working style</h2></div>
            </div>
            <div className="mt-6 grid gap-4 sm:grid-cols-2">
              <div className="rounded-2xl border border-white/55 bg-white/[0.25] p-4"><p className="text-xs text-[#8a7b77]">Work mode</p><p className="mt-2 text-lg font-medium">{user.preferred_work_mode || "Not set"}</p></div>
              <div className="rounded-2xl border border-white/55 bg-white/[0.25] p-4"><p className="text-xs text-[#8a7b77]">Seniority</p><p className="mt-2 text-lg font-medium">{profile?.career_interests.seniority || "Not set"}</p></div>
            </div>
          </GlassSurface>
        </motion.div>
      )}

      <div className="grid gap-5 lg:grid-cols-[1.1fr_0.9fr]">
        <GlassSurface className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.18em] text-[#9b6258]">Experience timeline</p>
              <h2 className="mt-1 text-xl font-semibold">Career journey</h2>
            </div>
            <BriefcaseBusiness className="h-5 w-5 text-[#9b6258]" />
          </div>
          <div className="mt-6 space-y-5">
            {profile?.experience?.length ? profile.experience.slice(0, 3).map((item, index) => (
              <div key={`${item.company}-${index}`} className="relative pl-6">
                {index < Math.min(profile.experience.length, 3) - 1 ? <div className="absolute left-[5px] top-4 h-[calc(100%+1.25rem)] w-px bg-gradient-to-b from-[#d79a8c] to-transparent" /> : null}
                <div className="absolute left-0 top-1.5 h-3 w-3 rounded-full border-2 border-[#f8eee9] bg-[#c98070] shadow-[0_0_14px_rgba(201,128,112,0.65)]" />
                <p className="text-xs text-[#8a7b77]">{item.start_date || "Career entry"} {item.end_date ? `— ${item.end_date}` : "— Present"}</p>
                <p className="mt-1 font-medium text-[#302a28]">{item.title || "Role"}</p>
                <p className="mt-1 text-sm text-[#756966]">{item.company || "Company not set"}</p>
              </div>
            )) : <p className="text-sm text-[#8a7b77]">No experience entries yet.</p>}
          </div>
        </GlassSurface>

        <GlassSurface className="p-6">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-white/60 bg-white/[0.36] text-[#9b6258]"><Target className="h-5 w-5" /></div>
            <div><p className="text-xs uppercase tracking-[0.18em] text-[#9b6258]">Profile signal</p><h2 className="font-semibold">Career intent</h2></div>
          </div>
          <p className="mt-6 text-sm text-[#655a57]">Career goal</p>
          <p className="mt-2 text-lg leading-7 text-[#302a28]">{user.career_goals || profile?.personal_information.summary || "Keep building your professional identity."}</p>
          <div className="mt-6 flex flex-wrap gap-2">
            {roles.slice(0, 3).map((role) => <span key={role} className="rounded-full border border-white/65 bg-white/[0.42] px-3 py-2 text-xs text-[#514744]">{role}</span>)}
          </div>
        </GlassSurface>
      </div>
    </div>
  );
}

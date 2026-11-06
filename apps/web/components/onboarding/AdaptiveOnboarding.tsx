"use client";

import { ArrowLeft, ArrowRight, Check, FileText, GraduationCap, BriefcaseBusiness, Sparkles } from "lucide-react";
import { FormEvent, useMemo, useState, type ReactNode } from "react";
import { motion } from "motion/react";

import { api } from "@/lib/api";
import { buildCareerProfile, resumeCreationRequested, type CareerStatus, type OnboardingDraft, type ResumeDecision } from "@/lib/onboarding";
import type { CareerProfile, User } from "@/lib/types";
import GlassGlow from "@/components/ui/GlassGlow";
import GlassSurface from "@/components/ui/GlassSurface";

const statusOptions: Array<{ value: CareerStatus; label: string; hint: string }> = [
  { value: "student", label: "Student", hint: "Studying and building early career evidence." },
  { value: "recent_graduate", label: "Recent graduate", hint: "Recently finished education and entering the market." },
  { value: "working_professional", label: "Working professional", hint: "Currently working and growing your career." },
  { value: "career_switcher", label: "Career switcher", hint: "Moving into a new role, field, or industry." },
  { value: "freelancer", label: "Freelancer", hint: "Building a career through independent work." },
  { value: "entrepreneur", label: "Entrepreneur", hint: "Building or running a business." },
  { value: "returning_to_work", label: "Returning to work", hint: "Coming back after a career break." },
  { value: "other", label: "Other", hint: "A different career situation." },
];

const initialDraft: OnboardingDraft = {
  careerStatus: "", workMode: "Hybrid", phone: "", location: "", summary: "", school: "", degree: "", field: "", educationStart: "", educationEnd: "",
  company: "", title: "", jobLocation: "", experienceStart: "", experienceEnd: "", responsibilities: "", technologies: "",
  technical: "", tools: "", soft: "", project: "", projectDescription: "", projectTech: "", projectLinks: "",
  roles: "", industries: "", seniority: "", goals: "", resumeDecision: "continue_without",
};

export default function AdaptiveOnboarding({
  token, user, setUser, setProfile, onDone, onOpenResume,
}: {
  token: string;
  user: User;
  setUser: (user: User) => void;
  setProfile: (profile: CareerProfile) => void;
  onDone: () => Promise<void>;
  onOpenResume: () => void;
}) {
  const [draft, setDraft] = useState<OnboardingDraft>(initialDraft);
  const [step, setStep] = useState(0);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");

  const backgroundTitle = useMemo(() => {
    if (draft.careerStatus === "student") return "Education & projects";
    if (draft.careerStatus === "entrepreneur" || draft.careerStatus === "freelancer") return "Work & projects";
    if (draft.careerStatus === "returning_to_work") return "Experience & re-entry";
    return "Education & experience";
  }, [draft.careerStatus]);

  const steps = [
    "Career status",
    "About you",
    backgroundTitle,
    "Skills",
    "Direction",
    "Resume",
    "Review",
  ];

  const update = <K extends keyof OnboardingDraft>(key: K, value: OnboardingDraft[K]) =>
    setDraft((current) => ({ ...current, [key]: value }));

  function next() {
    setMessage("");
    if (step === 0 && !draft.careerStatus) {
      setMessage("Choose your current career status to continue.");
      return;
    }
    setStep((current) => Math.min(current + 1, steps.length - 1));
  }

  async function submit(event?: FormEvent) {
    event?.preventDefault();
    setBusy(true);
    setMessage("");
    try {
      const profile = buildCareerProfile(user, draft);
      await api.saveOnboarding(token, {
        career_status: draft.careerStatus || null,
        preferred_work_mode: draft.workMode.trim() || null,
        career_goals: draft.goals.trim() || null,
        resume_creation_requested: resumeCreationRequested(draft.resumeDecision),
        career_profile: profile,
      });
      setProfile(profile);
      setUser({ ...user, onboarding_completed: true, career_status: draft.careerStatus || null, preferred_work_mode: draft.workMode.trim() || null, career_goals: draft.goals.trim() || null, resume_creation_requested: resumeCreationRequested(draft.resumeDecision) });
      await onDone();
      if (draft.resumeDecision === "upload_now") onOpenResume();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Onboarding failed.");
    } finally {
      setBusy(false);
    }
  }

  const progress = ((step + 1) / steps.length) * 100;

  return (
    <form onSubmit={submit} className="space-y-5">
      <GlassGlow intensity="medium">
        <GlassSurface className="p-5 sm:p-7">
          <div className="flex flex-col gap-5">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[#9b6258]">Career setup</p>
                <h3 className="mt-2 text-2xl font-semibold tracking-[-0.03em]">Build your career memory.</h3>
                <p className="mt-2 max-w-2xl text-sm leading-6 text-[#756966]">CareerOS asks only the questions that matter for your current career situation. You can edit everything later.</p>
              </div>
              <div className="hidden h-12 w-12 items-center justify-center rounded-2xl border border-white/70 bg-white/35 text-[#9b6258] sm:flex"><Sparkles className="h-5 w-5" /></div>
            </div>

            <div>
              <div className="flex items-center justify-between text-xs text-[#8a7b77]"><span>Step {step + 1} of {steps.length}</span><span>{Math.round(progress)}%</span></div>
              <div className="mt-2 h-2 overflow-hidden rounded-full bg-white/45"><motion.div className="h-full rounded-full bg-gradient-to-r from-[#c98070] to-[#e5b2a7]" animate={{ width: `${progress}%` }} transition={{ type: "spring", stiffness: 260, damping: 30 }} /></div>
              <div className="mt-3 flex flex-wrap gap-2">{steps.map((item, index) => <span key={item} className={`rounded-full px-2.5 py-1 text-[10px] uppercase tracking-[0.12em] ${index === step ? "bg-[#302a28] text-white" : index < step ? "bg-white/55 text-[#655a57]" : "bg-white/30 text-[#9a8c88]"}`}>{item}</span>)}</div>
            </div>
          </div>
        </GlassSurface>
      </GlassGlow>

      <GlassSurface className="p-5 sm:p-7">
        {step === 0 ? <CareerStatusStep value={draft.careerStatus} onChange={(value) => update("careerStatus", value)} /> : null}
        {step === 1 ? <AboutStep draft={draft} update={update} /> : null}
        {step === 2 ? <BackgroundStep draft={draft} update={update} status={draft.careerStatus} /> : null}
        {step === 3 ? <SkillsStep draft={draft} update={update} /> : null}
        {step === 4 ? <DirectionStep draft={draft} update={update} /> : null}
        {step === 5 ? <ResumeStep value={draft.resumeDecision} onChange={(value) => update("resumeDecision", value)} /> : null}
        {step === 6 ? <ReviewStep draft={draft} user={user} /> : null}

        {message ? <p className="mt-5 rounded-2xl border border-red-200/60 bg-red-50/55 p-3 text-sm text-red-700">{message}</p> : null}

        <div className="mt-7 flex items-center justify-between gap-3">
          <button type="button" onClick={() => { setMessage(""); setStep((current) => Math.max(0, current - 1)); }} disabled={step === 0 || busy} className="inline-flex items-center gap-2 rounded-full border border-white/70 bg-white/45 px-4 py-2.5 text-sm text-[#655a57] disabled:opacity-40"><ArrowLeft className="h-4 w-4" />Back</button>
          {step < steps.length - 1 ? <button type="button" onClick={next} className="inline-flex items-center gap-2 rounded-full bg-[#302a28] px-5 py-2.5 text-sm font-medium text-white shadow-lg">Continue<ArrowRight className="h-4 w-4" /></button> : <button type="submit" disabled={busy} className="inline-flex items-center gap-2 rounded-full bg-[#302a28] px-5 py-2.5 text-sm font-medium text-white shadow-lg disabled:opacity-60"><Check className="h-4 w-4" />{busy ? "Saving..." : "Complete CareerOS setup"}</button>}
        </div>
      </GlassSurface>
    </form>
  );
}

function CareerStatusStep({ value, onChange }: { value: OnboardingDraft["careerStatus"]; onChange: (value: CareerStatus) => void }) {
  return <div><SectionHeading icon={<Sparkles className="h-5 w-5" />} title="Where are you right now?" description="This decides which questions CareerOS shows next." /><div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">{statusOptions.map((item) => <button key={item.value} type="button" onClick={() => onChange(item.value)} className={`rounded-2xl border p-4 text-left transition ${value === item.value ? "border-[#c98070] bg-[#fff4ef] shadow-[0_12px_30px_rgba(201,128,112,0.14)]" : "border-white/70 bg-white/30 hover:bg-white/50"}`}><p className="font-medium text-[#302a28]">{item.label}</p><p className="mt-1 text-xs leading-5 text-[#80736f]">{item.hint}</p></button>)}</div></div>
}

function AboutStep({ draft, update }: { draft: OnboardingDraft; update: <K extends keyof OnboardingDraft>(key: K, value: OnboardingDraft[K]) => void }) {
  return <div><SectionHeading title="A little about you" description="These details help CareerOS keep your identity accurate." /><div className="grid gap-4 md:grid-cols-2"><Field label="Preferred work mode" value={draft.workMode} onChange={(value) => update("workMode", value)} /><Field label="Phone" value={draft.phone} onChange={(value) => update("phone", value)} /><Field label="Location" value={draft.location} onChange={(value) => update("location", value)} /></div><TextArea label="Professional summary" value={draft.summary} onChange={(value) => update("summary", value)} /></div>
}

function BackgroundStep({ draft, update, status }: { draft: OnboardingDraft; update: <K extends keyof OnboardingDraft>(key: K, value: OnboardingDraft[K]) => void; status: OnboardingDraft["careerStatus"] }) {
  const showExperience = status !== "student";
  return <div><SectionHeading icon={showExperience ? <BriefcaseBusiness className="h-5 w-5" /> : <GraduationCap className="h-5 w-5" />} title={status === "student" ? "Education first" : "Your background"} description="Only add information you already know. You can expand it later in Career Vault." /><div className="grid gap-4 md:grid-cols-2"><Field label="Institution" value={draft.school} onChange={(value) => update("school", value)} /><Field label="Degree" value={draft.degree} onChange={(value) => update("degree", value)} /><Field label="Field of study" value={draft.field} onChange={(value) => update("field", value)} /><Field label="Education start" value={draft.educationStart} onChange={(value) => update("educationStart", value)} type="date" /><Field label="Education end" value={draft.educationEnd} onChange={(value) => update("educationEnd", value)} type="date" /></div>{showExperience ? <div className="mt-7 border-t border-white/60 pt-6"><p className="mb-4 text-sm font-semibold text-[#302a28]">Recent or current experience</p><div className="grid gap-4 md:grid-cols-2"><Field label="Company" value={draft.company} onChange={(value) => update("company", value)} /><Field label="Title" value={draft.title} onChange={(value) => update("title", value)} /><Field label="Work location" value={draft.jobLocation} onChange={(value) => update("jobLocation", value)} /><Field label="Start date" value={draft.experienceStart} onChange={(value) => update("experienceStart", value)} type="date" /><Field label="End date" value={draft.experienceEnd} onChange={(value) => update("experienceEnd", value)} type="date" /></div><TextArea label="Responsibilities / achievements" value={draft.responsibilities} onChange={(value) => update("responsibilities", value)} placeholder="One item per line" /><TextArea label="Technologies used" value={draft.technologies} onChange={(value) => update("technologies", value)} placeholder="Python, SQL, ..." /></div> : null}<div className="mt-7 border-t border-white/60 pt-6"><p className="mb-4 text-sm font-semibold text-[#302a28]">Project evidence</p><div className="grid gap-4 md:grid-cols-2"><Field label="Project name" value={draft.project} onChange={(value) => update("project", value)} /><Field label="Project technologies" value={draft.projectTech} onChange={(value) => update("projectTech", value)} /><Field label="Project links" value={draft.projectLinks} onChange={(value) => update("projectLinks", value)} /></div><TextArea label="Project description" value={draft.projectDescription} onChange={(value) => update("projectDescription", value)} /></div></div>
}

function SkillsStep({ draft, update }: { draft: OnboardingDraft; update: <K extends keyof OnboardingDraft>(key: K, value: OnboardingDraft[K]) => void }) {
  return <div><SectionHeading icon={<Sparkles className="h-5 w-5" />} title="What can you do?" description="Use commas or new lines to separate skills." /><div className="grid gap-4 md:grid-cols-2"><TextArea label="Technical skills" value={draft.technical} onChange={(value) => update("technical", value)} placeholder="Python, TypeScript, SQL" /><TextArea label="Tools" value={draft.tools} onChange={(value) => update("tools", value)} placeholder="FastAPI, Git, Docker" /><TextArea label="Soft skills" value={draft.soft} onChange={(value) => update("soft", value)} placeholder="Communication, Ownership" /></div></div>
}

function DirectionStep({ draft, update }: { draft: OnboardingDraft; update: <K extends keyof OnboardingDraft>(key: K, value: OnboardingDraft[K]) => void }) {
  return <div><SectionHeading title="Where do you want to go?" description="CareerOS will use these preferences later for opportunity matching." /><div className="grid gap-4 md:grid-cols-2"><TextArea label="Target roles" value={draft.roles} onChange={(value) => update("roles", value)} placeholder="AI Engineer, Product Engineer" /><TextArea label="Industries" value={draft.industries} onChange={(value) => update("industries", value)} placeholder="HR Tech, SaaS" /><Field label="Seniority" value={draft.seniority} onChange={(value) => update("seniority", value)} /></div><TextArea label="Career goals" value={draft.goals} onChange={(value) => update("goals", value)} /></div>
}

function ResumeStep({ value, onChange }: { value: ResumeDecision; onChange: (value: ResumeDecision) => void }) {
  const options: Array<{ value: ResumeDecision; title: string; text: string }> = [
    { value: "upload_now", title: "Upload now", text: "Finish onboarding and go straight to Resume Intelligence." },
    { value: "create_later", title: "Create later", text: "Save your career profile first and create a resume later." },
    { value: "continue_without", title: "Continue without a resume", text: "Keep using CareerOS without a resume for now." },
  ];
  return <div><SectionHeading icon={<FileText className="h-5 w-5" />} title="What should we do about your resume?" description="Your choice is saved with your Career Vault. Uploading itself happens in Resume Intelligence." /><div className="grid gap-3 md:grid-cols-3">{options.map((item) => <button key={item.value} type="button" onClick={() => onChange(item.value)} className={`rounded-2xl border p-5 text-left ${value === item.value ? "border-[#c98070] bg-[#fff4ef]" : "border-white/70 bg-white/30 hover:bg-white/50"}`}><p className="font-medium text-[#302a28]">{item.title}</p><p className="mt-2 text-xs leading-5 text-[#80736f]">{item.text}</p></button>)}</div></div>
}

function ReviewStep({ draft, user }: { draft: OnboardingDraft; user: User }) {
  const profile = buildCareerProfile(user, draft);
  return <div><SectionHeading icon={<Check className="h-5 w-5" />} title="Review your setup" description="Check the main facts before they are saved to Career Vault." /><div className="grid gap-3 sm:grid-cols-2"><Review label="Career status" value={statusOptions.find((item) => item.value === draft.careerStatus)?.label ?? "Not set"} /><Review label="Work mode" value={draft.workMode || "Not set"} /><Review label="Target roles" value={profile.career_interests.target_roles.join(", ") || "Not set"} /><Review label="Skills" value={String(profile.skills.technical.length + profile.skills.tools.length + profile.skills.soft_skills.length)} /><Review label="Education entries" value={String(profile.education.length)} /><Review label="Experience entries" value={String(profile.experience.length)} /><Review label="Projects" value={String(profile.projects.length)} /><Review label="Resume choice" value={draft.resumeDecision.replaceAll("_", " ")} /></div></div>
}

function SectionHeading({ icon, title, description }: { icon?: ReactNode; title: string; description: string }) { return <div className="mb-6 flex gap-3">{icon ? <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl border border-white/70 bg-white/40 text-[#9b6258]">{icon}</div> : null}<div><h4 className="text-xl font-semibold text-[#302a28]">{title}</h4><p className="mt-1 text-sm leading-6 text-[#80736f]">{description}</p></div></div>; }
function Review({ label, value }: { label: string; value: string }) { return <div className="rounded-2xl border border-white/65 bg-white/30 p-4"><p className="text-xs uppercase tracking-[0.12em] text-[#9a8c88]">{label}</p><p className="mt-1 text-sm font-medium text-[#403735]">{value}</p></div>; }

function Field({
  label,
  value,
  onChange,
  type = "text",
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
  placeholder?: string;
}) {
  return (
    <label className="block text-sm font-medium text-[#514744]">
      {label}
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        type={type}
        placeholder={placeholder}
        className="mt-2 w-full rounded-2xl border border-white/70 bg-white/55 px-3 py-3 text-sm text-[#302a28] outline-none focus:border-[#c98070]"
      />
    </label>
  );
}
function TextArea({ label, value, onChange, placeholder }: { label: string; value: string; onChange: (value: string) => void; placeholder?: string }) { return <label className="mt-4 block text-sm font-medium text-[#514744]">{label}<textarea value={value} onChange={(event) => onChange(event.target.value)} placeholder={placeholder} className="mt-2 min-h-24 w-full rounded-2xl border border-white/70 bg-white/55 px-3 py-3 text-sm text-[#302a28] outline-none focus:border-[#c98070]" /></label>; }

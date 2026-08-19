"use client";

import {
  BarChart3,
  Bell,
  BriefcaseBusiness,
  Check,
  ChevronRight,
  Database,
  GraduationCap,
  LayoutDashboard,
  LinkIcon,
  LogOut,
  Pencil,
  Rocket,
  Save,
  Search,
  Sparkles,
  UserRound,
  X,
} from "lucide-react";
import { FormEvent, useMemo, useState } from "react";
import { motion } from "motion/react";

import { api } from "@/lib/api";
import { emptyCareerProfile } from "@/lib/profile";
import type { AuthResponse, CareerProfile, User } from "@/lib/types";

import Dashboard from "@/components/dashboard/Dashboard";
import ResumeIntelligence from "@/components/resume/ResumeIntelligence";

const navItems = [
  ["Dashboard", LayoutDashboard],
  ["Career Vault", Database],
  ["Resume Intelligence", Sparkles],
  ["Jobs & Opportunities", BriefcaseBusiness],
  ["Learning Hub", GraduationCap],
  ["Roadmap", Rocket],
  ["Analytics", BarChart3],
  ["AI Assistant", Sparkles],
  ["Settings", UserRound],
] as const;

type Mode = "login" | "signup";
type View = "dashboard" | "vault" | "resume";

const splitList = (value: string) =>
  value
    .split(/\n|,/)
    .map((item) => item.trim())
    .filter(Boolean);

export default function Home() {
  const [auth, setAuth] = useState<AuthResponse | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<CareerProfile | null>(null);

  const [view, setView] = useState<View>("dashboard");

  const [mode, setMode] = useState<Mode>("signup");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  const token = auth?.token ?? "";

  async function handleAuth(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setBusy(true);
    setMessage("");

    const form = new FormData(event.currentTarget);

    try {
      const response =
        mode === "signup"
          ? await api.signup({
              full_name: String(form.get("fullName")),
              email: String(form.get("email")),
              password: String(form.get("password")),
            })
          : await api.login({
              email: String(form.get("email")),
              password: String(form.get("password")),
            });

      setAuth(response);
      setUser(response.user);

      localStorage.setItem("careeros_token", response.token);

      setProfile(
        emptyCareerProfile(
          response.user.full_name ?? "",
          response.user.email ?? "",
        ),
      );
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Request failed.");
    } finally {
      setBusy(false);
    }
  }

  async function refreshProfile() {
    if (!token) return;

    try {
      const [nextUser, stored] = await Promise.all([
        api.me(token),
        api.getMyProfile(token),
      ]);

      setUser(nextUser);
      setProfile(stored.career_profile);
    } catch {
      setProfile(
        (current) =>
          current ??
          emptyCareerProfile(
            user?.full_name ?? "",
            user?.email ?? "",
          ),
      );
    }
  }

  function logout() {
    setAuth(null);
    setUser(null);
    setProfile(null);
    setView("dashboard");

    localStorage.removeItem("careeros_token");
  }

  function navigate(label: string) {
    if (label === "Dashboard") {
      setView("dashboard");
      return;
    }

    if (label === "Career Vault") {
      setView("vault");
      return;
    }

    if (label === "Resume Intelligence") {
      setView("resume");
      return;
    }

    // Other sections are not implemented yet.
    setView("dashboard");
  }

  if (!auth || !user) {
    return (
      <main className="min-h-screen px-4 py-8 sm:px-8">
        <section className="mx-auto grid min-h-[calc(100vh-4rem)] max-w-6xl items-center gap-8 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="space-y-8">
            <div className="inline-flex items-center gap-3 rounded-full bg-white/55 px-4 py-2 text-sm text-graphite shadow-sm">
              <Sparkles className="h-4 w-4 text-rose" />
              AI-first professional identity
            </div>

            <div className="space-y-5">
              <h1 className="max-w-3xl text-5xl font-semibold leading-tight text-ink sm:text-6xl">
                CareerOS
              </h1>

              <p className="max-w-2xl text-lg leading-8 text-graphite">
                Build an account, complete adaptive onboarding, and land
                inside a persistent Career Vault powered by your profile data.
              </p>
            </div>
          </div>

          <form onSubmit={handleAuth} className="glass rounded-[8px] p-6">
            <div className="mb-6 flex rounded-[8px] bg-white/50 p-1">
              {(["signup", "login"] as const).map((item) => (
                <button
                  key={item}
                  type="button"
                  onClick={() => setMode(item)}
                  className={`flex-1 rounded-[6px] px-4 py-2 text-sm font-medium ${
                    mode === item
                      ? "bg-ink text-white"
                      : "text-graphite"
                  }`}
                >
                  {item === "signup" ? "Sign up" : "Log in"}
                </button>
              ))}
            </div>

            <div className="space-y-4">
              {mode === "signup" ? (
                <Field
                  label="Full name"
                  name="fullName"
                  defaultValue="CareerOS Test User"
                />
              ) : null}

              <Field
                label="Email"
                name="email"
                type="email"
                defaultValue="careeros.test@example.com"
              />

              <Field
                label="Password"
                name="password"
                type="password"
                defaultValue="CareerOS-Test-123"
              />

              {message ? (
                <p className="text-sm text-clay">{message}</p>
              ) : null}

              <button
                disabled={busy}
                className="flex w-full items-center justify-center gap-2 rounded-[8px] bg-ink px-4 py-3 font-medium text-white disabled:opacity-60"
              >
                <ChevronRight className="h-4 w-4" />

                {busy
                  ? "Working..."
                  : mode === "signup"
                    ? "Create account"
                    : "Enter CareerOS"}
              </button>
            </div>
          </form>
        </section>
      </main>
    );
  }

  return (
    <main className="relative min-h-screen overflow-hidden px-3 py-3 text-[#242222] sm:px-5 sm:py-5">
      {/* Background lighting */}
      <div
        aria-hidden="true"
        className="pointer-events-none fixed inset-0 overflow-hidden"
      >
        <motion.div
          className="absolute -left-32 top-[-10rem] h-[34rem] w-[34rem] rounded-full bg-[#e8a99b]/18 blur-3xl"
          animate={{
            x: [0, 70, 0],
            y: [0, 35, 0],
            scale: [1, 1.08, 1],
          }}
          transition={{
            duration: 14,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />

        <motion.div
          className="absolute right-[-12rem] top-[12rem] h-[30rem] w-[30rem] rounded-full bg-white/55 blur-3xl"
          animate={{
            x: [0, -55, 0],
            y: [0, 45, 0],
          }}
          transition={{
            duration: 17,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />

        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(255,255,255,0.6),transparent_38%)]" />
      </div>

      <div className="relative mx-auto flex min-h-[calc(100vh-1.5rem)] max-w-[1700px] gap-4 lg:min-h-[calc(100vh-2.5rem)] lg:gap-5">
        {/* SIDEBAR */}
        <aside className="glass-panel hidden w-[248px] shrink-0 flex-col rounded-[32px] p-4 lg:flex">
          <div className="flex items-center gap-3 px-3 py-3">
            <div className="relative flex h-11 w-11 items-center justify-center rounded-[16px] border border-white/80 bg-white/45 text-[#9b6258] shadow-[inset_0_1px_0_rgba(255,255,255,0.95),0_10px_30px_rgba(50,40,38,0.1)]">
              <Sparkles className="h-5 w-5" />

              <span className="absolute -right-0.5 -top-0.5 h-2.5 w-2.5 rounded-full bg-[#d28b7c] shadow-[0_0_12px_rgba(210,139,124,0.85)]" />
            </div>

            <div>
              <p className="text-lg font-semibold tracking-[-0.02em]">
                CareerOS
              </p>

              <p className="text-[11px] uppercase tracking-[0.18em] text-[#8a7b77]">
                Career intelligence
              </p>
            </div>
          </div>

          <div className="my-3 h-px bg-gradient-to-r from-transparent via-white/70 to-transparent" />

          <nav className="flex-1 space-y-1.5">
            <p className="px-3 pb-2 pt-3 text-[10px] font-semibold uppercase tracking-[0.22em] text-[#9b6258]">
              Workspace
            </p>

            {navItems.map(([label, Icon]) => {
              const active =
                (label === "Dashboard" && view === "dashboard") ||
                (label === "Career Vault" && view === "vault") ||
                (label === "Resume Intelligence" && view === "resume");

              return (
                <button
                  key={label}
                  type="button"
                  onClick={() => navigate(label)}
                  className={`group relative flex w-full items-center gap-3 overflow-hidden rounded-2xl px-3 py-2.5 text-left text-[13px] transition duration-300 ${
                    active
                      ? "text-[#302a28]"
                      : "text-[#756966] hover:bg-white/[0.28] hover:text-[#302a28]"
                  }`}
                >
                  {active ? (
                    <motion.span
                      layoutId="active-nav"
                      className="absolute inset-0 rounded-2xl border border-white/75 bg-white/[0.52] shadow-[0_10px_25px_rgba(50,40,38,0.08),inset_0_1px_0_rgba(255,255,255,0.95)]"
                      transition={{
                        type: "spring",
                        stiffness: 420,
                        damping: 34,
                      }}
                    />
                  ) : null}

                  <span className="relative z-10 flex h-8 w-8 items-center justify-center rounded-xl bg-white/[0.24]">
                    <Icon
                      className={`h-4 w-4 ${
                        active
                          ? "text-[#9b6258]"
                          : "text-[#8a7b77]"
                      }`}
                    />
                  </span>

                  <span className="relative z-10 truncate">
                    {label}
                  </span>
                </button>
              );
            })}
          </nav>

          <div className="rounded-[22px] border border-white/70 bg-white/[0.28] p-3 shadow-[inset_0_1px_0_rgba(255,255,255,0.88)]">
            <p className="text-[10px] uppercase tracking-[0.18em] text-[#9b6258]">
              Profile state
            </p>

            <p className="mt-1 text-sm font-medium">
              {user.onboarding_completed
                ? "Career memory active"
                : "Onboarding in progress"}
            </p>

            <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-white/45">
              <motion.div
                initial={{ width: 0 }}
                animate={{
                  width: user.onboarding_completed
                    ? "100%"
                    : "55%",
                }}
                transition={{ duration: 0.9 }}
                className="h-full rounded-full bg-gradient-to-r from-[#c98070] to-[#e5b2a7]"
              />
            </div>
          </div>

          <button
            type="button"
            onClick={logout}
            className="mt-3 flex w-full items-center gap-3 rounded-2xl px-3 py-2.5 text-sm text-[#756966] transition hover:bg-white/[0.3] hover:text-[#302a28]"
          >
            <LogOut className="h-4 w-4" />
            Logout
          </button>
        </aside>

        {/* MAIN AREA */}
        <section className="min-w-0 flex-1">
          <header className="glass-panel sticky top-3 z-30 mb-5 flex min-h-[76px] items-center gap-3 rounded-[28px] px-4 py-3 sm:px-5">
            <div className="flex min-w-0 flex-1 items-center gap-3">
              <div className="hidden h-10 w-10 items-center justify-center rounded-2xl border border-white/70 bg-white/[0.3] text-[#9b6258] sm:flex">
                <Sparkles className="h-4 w-4" />
              </div>

              <div className="min-w-0">
                <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-[#9b6258]">
                  CareerOS
                </p>

                <h2 className="truncate text-lg font-semibold tracking-[-0.02em]">
                  {user.full_name}
                </h2>
              </div>
            </div>

            <div className="hidden w-full max-w-[430px] items-center gap-2 rounded-full border border-white/70 bg-white/[0.26] px-4 py-2.5 shadow-[inset_0_1px_0_rgba(255,255,255,0.88)] md:flex">
              <Search className="h-4 w-4 text-[#8a7b77]" />

              <span className="text-sm text-[#8a7b77]">
                Search anything...
              </span>

              <span className="ml-auto rounded-md border border-white/70 bg-white/30 px-1.5 py-0.5 text-[10px] text-[#9a8c88]">
                ⌘ K
              </span>
            </div>

            <div className="ml-auto flex items-center gap-2">
              <button
                type="button"
                className="relative flex h-11 w-11 items-center justify-center rounded-full border border-white/70 bg-white/[0.28] text-[#756966] shadow-[inset_0_1px_0_rgba(255,255,255,0.9)] transition hover:bg-white/[0.42]"
              >
                <Bell className="h-4 w-4" />

                <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-[#c98070] shadow-[0_0_10px_rgba(201,128,112,0.8)]" />
              </button>

              <div className="hidden items-center gap-2 rounded-full border border-white/70 bg-white/[0.28] py-1 pl-1 pr-3 sm:flex">
                <div className="flex h-9 w-9 items-center justify-center rounded-full border border-white/80 bg-gradient-to-br from-[#d9a79b] via-[#f2ddd5] to-[#b9847b] text-xs font-semibold text-[#513c37]">
                  {(user.full_name || "C")
                    .slice(0, 1)
                    .toUpperCase()}
                </div>

                <div className="max-w-[120px] truncate text-xs font-medium">
                  {user.full_name}
                </div>
              </div>
            </div>
          </header>

          {/* MOBILE NAVIGATION */}
          <div className="mb-4 overflow-x-auto rounded-2xl border border-white/70 bg-white/[0.28] p-1.5 shadow-[0_12px_30px_rgba(52,43,40,0.08)] backdrop-blur-xl lg:hidden">
            <div className="flex min-w-max gap-1">
              {navItems.slice(0, 5).map(([label, Icon]) => {
                const active =
                  (label === "Dashboard" &&
                    view === "dashboard") ||
                  (label === "Career Vault" &&
                    view === "vault") ||
                  (label === "Resume Intelligence" &&
                    view === "resume");

                return (
                  <button
                    key={label}
                    type="button"
                    onClick={() => navigate(label)}
                    className={`flex items-center gap-2 rounded-xl px-3 py-2 text-xs ${
                      active
                        ? "bg-white/60 text-[#302a28] shadow-sm"
                        : "text-[#756966]"
                    }`}
                  >
                    <Icon className="h-3.5 w-3.5" />
                    {label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* CONTENT */}
          {!user.onboarding_completed ? (
            <Onboarding
              token={token}
              user={user}
              setUser={setUser}
              setProfile={setProfile}
              onDone={refreshProfile}
            />
          ) : view === "vault" ? (
            <Vault
              token={token}
              profile={profile}
              setProfile={setProfile}
            />
          ) : view === "resume" ? (
            <ResumeIntelligence
              token={token}
              onBack={() => setView("dashboard")}
            />
          ) : (
            <Dashboard
              profile={profile}
              user={user}
              onOpenVault={() => setView("vault")}
            />
          )}
        </section>
      </div>
    </main>
  );
}

function Field({
  label,
  name,
  type = "text",
  defaultValue = "",
}: {
  label: string;
  name: string;
  type?: string;
  defaultValue?: string;
}) {
  return (
    <label className="block text-sm font-medium text-graphite">
      {label}

      <input
        name={name}
        type={type}
        defaultValue={defaultValue}
        required
        className="mt-2 w-full rounded-[8px] border border-white/60 bg-white/62 px-3 py-3 outline-none focus:border-rose"
      />
    </label>
  );
}

function Onboarding({
  token,
  user,
  setUser,
  setProfile,
  onDone,
}: {
  token: string;
  user: User;
  setUser: (user: User) => void;
  setProfile: (profile: CareerProfile) => void;
  onDone: () => Promise<void>;
}) {
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setBusy(true);
    setMessage("");

    const form = new FormData(event.currentTarget);

    const profile = emptyCareerProfile(
      user.full_name ?? "",
      user.email ?? "",
    );

    profile.personal_information.phone =
      String(form.get("phone") || "") || null;

    profile.personal_information.location =
      String(form.get("location") || "") || null;

    profile.personal_information.summary =
      String(form.get("summary") || "") || null;

    profile.personal_information.links = splitList(
      String(form.get("links") || ""),
    );

    profile.education = [
      {
        institution:
          String(form.get("school") || "") || null,
        degree:
          String(form.get("degree") || "") || null,
        field_of_study:
          String(form.get("field") || "") || null,
        start_date: null,
        end_date: null,
        details: splitList(
          String(form.get("educationDetails") || ""),
        ),
      },
    ];

    profile.experience = [
      {
        company:
          String(form.get("company") || "") || null,
        title:
          String(form.get("title") || "") || null,
        location:
          String(form.get("jobLocation") || "") || null,
        start_date: null,
        end_date: null,
        responsibilities: splitList(
          String(form.get("responsibilities") || ""),
        ),
        technologies: splitList(
          String(form.get("technologies") || ""),
        ),
      },
    ];

    profile.skills.technical = splitList(
      String(form.get("technical") || ""),
    );

    profile.skills.tools = splitList(
      String(form.get("tools") || ""),
    );

    profile.skills.soft_skills = splitList(
      String(form.get("soft") || ""),
    );

    profile.projects = [
      {
        name:
          String(form.get("project") || "") || null,
        description:
          String(form.get("projectDescription") || "") || null,
        technologies: splitList(
          String(form.get("projectTech") || ""),
        ),
        links: [],
      },
    ];

    profile.certifications = [
      {
        name:
          String(form.get("certification") || "") || null,
        issuer:
          String(form.get("issuer") || "") || null,
        date: null,
      },
    ];

    profile.achievements = [
      {
        title:
          String(form.get("achievement") || "") || null,
        description:
          String(form.get("achievementDescription") || "") || null,
      },
    ];

    profile.career_interests.target_roles = splitList(
      String(form.get("roles") || ""),
    );

    profile.career_interests.industries = splitList(
      String(form.get("industries") || ""),
    );

    profile.career_interests.seniority =
      String(form.get("seniority") || "") || null;

    try {
      await api.saveOnboarding(token, {
        career_status:
          String(form.get("careerStatus") || "") || null,
        preferred_work_mode:
          String(form.get("workMode") || "") || null,
        career_goals:
          String(form.get("goals") || "") || null,
        resume_creation_requested:
          form.get("resumeHelp") === "on",
        career_profile: profile,
      });

      setProfile(profile);
      setUser({
        ...user,
        onboarding_completed: true,
      });

      await onDone();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Onboarding failed.",
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="glass rounded-[8px] p-5">
      <div className="mb-5 flex items-center gap-3">
        <Sparkles className="h-5 w-5 text-rose" />

        <h3 className="text-xl font-semibold">
          Adaptive onboarding
        </h3>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Field
          label="Career status"
          name="careerStatus"
          defaultValue="Early-career builder"
        />

        <Field
          label="Preferred work mode"
          name="workMode"
          defaultValue="Hybrid"
        />

        <Field
          label="Phone"
          name="phone"
          defaultValue="+1 555 0100"
        />

        <Field
          label="Location"
          name="location"
          defaultValue="Austin, TX"
        />

        <Field
          label="School"
          name="school"
          defaultValue="CareerOS Test University"
        />

        <Field
          label="Degree"
          name="degree"
          defaultValue="B.S. Computer Science"
        />

        <Field
          label="Field"
          name="field"
          defaultValue="Software Engineering"
        />

        <Field
          label="Company"
          name="company"
          defaultValue="Synthetic Labs"
        />

        <Field
          label="Title"
          name="title"
          defaultValue="Product Engineering Intern"
        />

        <Field
          label="Job location"
          name="jobLocation"
          defaultValue="Remote"
        />

        <Field
          label="Target roles"
          name="roles"
          defaultValue="Product Engineer, AI Engineer"
        />

        <Field
          label="Industries"
          name="industries"
          defaultValue="HR Tech, Developer Tools"
        />

        <Field
          label="Seniority"
          name="seniority"
          defaultValue="Entry Level"
        />

        <Field
          label="Technical skills"
          name="technical"
          defaultValue="Python, TypeScript, SQL"
        />

        <Field
          label="Tools"
          name="tools"
          defaultValue="FastAPI, PostgreSQL, Next.js"
        />

        <Field
          label="Soft skills"
          name="soft"
          defaultValue="Communication, Ownership"
        />

        <Field
          label="Project"
          name="project"
          defaultValue="CareerOS Synthetic Profile Builder"
        />

        <Field
          label="Project tech"
          name="projectTech"
          defaultValue="React, FastAPI"
        />

        <Field
          label="Certification"
          name="certification"
          defaultValue="Synthetic Cloud Fundamentals"
        />

        <Field
          label="Issuer"
          name="issuer"
          defaultValue="CareerOS Academy"
        />

        <Field
          label="Achievement"
          name="achievement"
          defaultValue="Built a test onboarding workflow"
        />

        <Field
          label="Links"
          name="links"
          defaultValue="https://github.com/careeros-test, https://linkedin.com/in/careeros-test"
        />
      </div>

      <TextField
        label="Summary"
        name="summary"
        defaultValue="Synthetic test user focused on AI-assisted career tooling."
      />

      <TextField
        label="Responsibilities"
        name="responsibilities"
        defaultValue="Built typed frontend workflows, Validated API integration"
      />

      <TextField
        label="Education details"
        name="educationDetails"
        defaultValue="Dean's List, Capstone in applied AI"
      />

      <TextField
        label="Project description"
        name="projectDescription"
        defaultValue="A realistic synthetic profile used to verify CareerOS onboarding."
      />

      <TextField
        label="Achievement description"
        name="achievementDescription"
        defaultValue="Confirmed profile persistence through PostgreSQL."
      />

      <TextField
        label="Career goals"
        name="goals"
        defaultValue="Grow into an AI product engineering role."
      />

      <label className="mt-4 flex items-center gap-3 text-sm text-graphite">
        <input
          name="resumeHelp"
          type="checkbox"
          className="h-4 w-4 accent-rose"
        />

        Resume creation requested
      </label>

      {message ? (
        <p className="mt-4 text-sm text-clay">{message}</p>
      ) : null}

      <button
        disabled={busy}
        className="mt-5 flex items-center gap-2 rounded-[8px] bg-ink px-4 py-3 font-medium text-white disabled:opacity-60"
      >
        <Check className="h-4 w-4" />

        {busy ? "Saving..." : "Complete onboarding"}
      </button>
    </form>
  );
}

function TextField({
  label,
  name,
  defaultValue = "",
}: {
  label: string;
  name: string;
  defaultValue?: string;
}) {
  return (
    <label className="mt-4 block text-sm font-medium text-graphite">
      {label}

      <textarea
        name={name}
        defaultValue={defaultValue}
        className="mt-2 min-h-20 w-full rounded-[8px] border border-white/60 bg-white/62 px-3 py-3 outline-none focus:border-rose"
      />
    </label>
  );
}

function Vault({
  token,
  profile,
  setProfile,
}: {
  token: string;
  profile: CareerProfile | null;
  setProfile: (profile: CareerProfile) => void;
}) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(
    JSON.stringify(profile ?? emptyCareerProfile(), null, 2),
  );
  const [message, setMessage] = useState("");

  const sections = useMemo(
    () =>
      profile
        ? [
            [
              "Personal information",
              [
                profile.personal_information.full_name,
                profile.personal_information.email,
                profile.personal_information.location,
              ],
            ],
            [
              "Education",
              profile.education.map(
                (item) =>
                  `${item.degree ?? ""} ${item.institution ?? ""}`,
              ),
            ],
            [
              "Experience",
              profile.experience.map(
                (item) =>
                  `${item.title ?? ""} ${item.company ?? ""}`,
              ),
            ],
            [
              "Projects",
              profile.projects.map((item) => item.name),
            ],
            [
              "Certifications",
              profile.certifications.map((item) => item.name),
            ],
            [
              "Achievements",
              profile.achievements.map((item) => item.title),
            ],
            [
              "Links",
              profile.personal_information.links,
            ],
          ]
        : [],
    [profile],
  );

  async function save() {
    try {
      const parsed = JSON.parse(draft) as CareerProfile;

      const response = await api.updateMyProfile(
        token,
        parsed,
      );

      setProfile(response.career_profile);
      setEditing(false);
      setMessage("Saved");
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Save failed.",
      );
    }
  }

  if (!profile) {
    return (
      <Panel title="Career Vault">
        <p className="text-sm text-graphite">
          No CareerProfile has been saved yet.
        </p>
      </Panel>
    );
  }

  return (
    <div className="grid gap-5">
      <div className="glass flex items-center justify-between rounded-[8px] p-4">
        <h3 className="text-xl font-semibold">
          Career Vault
        </h3>

        <div className="flex gap-2">
          {editing ? (
            <>
              <button
                onClick={save}
                className="rounded-[8px] bg-ink p-2 text-white"
                title="Save"
              >
                <Save className="h-4 w-4" />
              </button>

              <button
                onClick={() => setEditing(false)}
                className="rounded-[8px] bg-white/60 p-2 text-graphite"
                title="Cancel"
              >
                <X className="h-4 w-4" />
              </button>
            </>
          ) : (
            <button
              onClick={() => {
                setDraft(
                  JSON.stringify(profile, null, 2),
                );
                setEditing(true);
              }}
              className="rounded-[8px] bg-ink p-2 text-white"
              title="Edit"
            >
              <Pencil className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>

      {message ? (
        <p className="text-sm text-clay">{message}</p>
      ) : null}

      {editing ? (
        <textarea
          value={draft}
          onChange={(event) =>
            setDraft(event.target.value)
          }
          className="min-h-[36rem] rounded-[8px] border border-white/70 bg-white/70 p-4 font-mono text-sm outline-none focus:border-rose"
        />
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {sections.map(([title, values]) => (
            <Panel key={title as string} title={title as string}>
              <Tags
                values={
                  (values as Array<string | null>).filter(
                    Boolean,
                  ) as string[]
                }
              />
            </Panel>
          ))}
        </div>
      )}
    </div>
  );
}

function Panel({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="glass rounded-[8px] p-5">
      <h3 className="mb-4 text-lg font-semibold text-ink">
        {title}
      </h3>

      {children}
    </section>
  );
}

function Tags({ values }: { values: string[] }) {
  if (values.length === 0) {
    return (
      <p className="text-sm text-graphite">
        Not set
      </p>
    );
  }

  return (
    <div className="flex flex-wrap gap-2">
      {values.map((value) => (
        <span
          key={value}
          className="inline-flex items-center gap-2 rounded-full bg-white/65 px-3 py-1.5 text-sm text-graphite"
        >
          <LinkIcon className="h-3 w-3 text-rose" />
          {value}
        </span>
      ))}
    </div>
  );
}
import { describe, expect, it } from "vitest";
import { buildCareerProfile, resumeCreationRequested, splitList, type OnboardingDraft } from "./onboarding";
import type { User } from "./types";

const user: User = { id: 1, full_name: "Test User", email: "test@example.com", account_type: "standard", career_status: null, preferred_work_mode: null, career_goals: null, onboarding_completed: false, resume_creation_requested: false };
const draft: OnboardingDraft = { careerStatus: "student", workMode: "Hybrid", phone: "", location: "", summary: "", school: "RAIT", degree: "B.Tech", field: "Computer Science", educationStart: "2022-08-01", educationEnd: "2026-05-01", company: "", title: "", jobLocation: "", experienceStart: "", experienceEnd: "", responsibilities: "", technologies: "", technical: "Python, SQL", tools: "Git\nDocker", soft: "Communication", project: "CareerOS", projectDescription: "Career platform", projectTech: "Next.js", projectLinks: "https://example.com", roles: "AI Engineer, Product Engineer", industries: "SaaS", seniority: "Entry Level", goals: "Build AI products", resumeDecision: "upload_now" };

describe("adaptive onboarding profile builder", () => {
  it("splits list input without empty values", () => { expect(splitList("Python, SQL\n Git,,")).toEqual(["Python", "SQL", "Git"]); });
  it("builds only populated career records", () => { const profile=buildCareerProfile(user,draft); expect(profile.education).toHaveLength(1); expect(profile.experience).toHaveLength(0); expect(profile.projects).toHaveLength(1); expect(profile.skills.technical).toEqual(["Python","SQL"]); });
  it("maps resume decisions to the existing backend boolean", () => { expect(resumeCreationRequested("upload_now")).toBe(true); expect(resumeCreationRequested("create_later")).toBe(true); expect(resumeCreationRequested("continue_without")).toBe(false); });
});

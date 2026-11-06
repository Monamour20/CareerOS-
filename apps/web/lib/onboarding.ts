import type { CareerProfile, User } from "./types";

export type CareerStatus =
  | "student"
  | "recent_graduate"
  | "working_professional"
  | "career_switcher"
  | "freelancer"
  | "entrepreneur"
  | "returning_to_work"
  | "other";

export type ResumeDecision = "upload_now" | "create_later" | "continue_without";

export type OnboardingDraft = {
  careerStatus: CareerStatus | "";
  workMode: string;
  phone: string;
  location: string;
  summary: string;
  school: string;
  degree: string;
  field: string;
  educationStart: string;
  educationEnd: string;
  company: string;
  title: string;
  jobLocation: string;
  experienceStart: string;
  experienceEnd: string;
  responsibilities: string;
  technologies: string;
  technical: string;
  tools: string;
  soft: string;
  project: string;
  projectDescription: string;
  projectTech: string;
  projectLinks: string;
  roles: string;
  industries: string;
  seniority: string;
  goals: string;
  resumeDecision: ResumeDecision;
};

export const splitList = (value: string): string[] =>
  value
    .split(/\n|,/)
    .map((item) => item.trim())
    .filter(Boolean);

const hasAny = (...values: Array<string | null | undefined>) =>
  values.some((value) => Boolean(value?.trim()));

export function buildCareerProfile(user: User, draft: OnboardingDraft): CareerProfile {
  const profile: CareerProfile = {
    personal_information: {
      full_name: user.full_name || null,
      email: user.email || null,
      phone: draft.phone.trim() || null,
      location: draft.location.trim() || null,
      links: [],
      summary: draft.summary.trim() || null,
    },
    education: [],
    experience: [],
    skills: { technical: splitList(draft.technical), tools: splitList(draft.tools), languages: [], soft_skills: splitList(draft.soft) },
    projects: [],
    certifications: [],
    achievements: [],
    career_interests: {
      target_roles: splitList(draft.roles),
      industries: splitList(draft.industries),
      seniority: draft.seniority.trim() || null,
      strengths: [],
      growth_areas: [],
    },
  };

  if (hasAny(draft.school, draft.degree, draft.field, draft.educationStart, draft.educationEnd)) {
    profile.education.push({
      institution: draft.school.trim() || null,
      degree: draft.degree.trim() || null,
      field_of_study: draft.field.trim() || null,
      start_date: draft.educationStart.trim() || null,
      end_date: draft.educationEnd.trim() || null,
      details: [],
    });
  }

  if (hasAny(draft.company, draft.title, draft.jobLocation, draft.experienceStart, draft.experienceEnd, draft.responsibilities, draft.technologies)) {
    profile.experience.push({
      company: draft.company.trim() || null,
      title: draft.title.trim() || null,
      location: draft.jobLocation.trim() || null,
      start_date: draft.experienceStart.trim() || null,
      end_date: draft.experienceEnd.trim() || null,
      responsibilities: splitList(draft.responsibilities),
      technologies: splitList(draft.technologies),
    });
  }

  if (hasAny(draft.project, draft.projectDescription, draft.projectTech, draft.projectLinks)) {
    profile.projects.push({
      name: draft.project.trim() || null,
      description: draft.projectDescription.trim() || null,
      technologies: splitList(draft.projectTech),
      links: splitList(draft.projectLinks),
    });
  }

  return profile;
}

export const resumeCreationRequested = (decision: ResumeDecision): boolean =>
  decision !== "continue_without";

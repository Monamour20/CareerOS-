import type { CareerProfile } from "./types";

export const emptyCareerProfile = (fullName = "", email = ""): CareerProfile => ({
  personal_information: {
    full_name: fullName || null,
    email: email || null,
    phone: null,
    location: null,
    links: [],
    summary: null
  },
  education: [],
  experience: [],
  skills: { technical: [], tools: [], languages: [], soft_skills: [] },
  projects: [],
  certifications: [],
  achievements: [],
  career_interests: {
    target_roles: [],
    industries: [],
    seniority: null,
    strengths: [],
    growth_areas: []
  }
});

export const profileCompleteness = (profile: CareerProfile | null): number => {
  if (!profile) return 0;
  const checks = [
    Boolean(profile.personal_information.full_name),
    Boolean(profile.personal_information.email),
    Boolean(profile.personal_information.summary),
    profile.education.length > 0,
    profile.experience.length > 0,
    profile.skills.technical.length + profile.skills.tools.length + profile.skills.soft_skills.length > 0,
    profile.projects.length > 0,
    profile.certifications.length > 0,
    profile.achievements.length > 0,
    profile.career_interests.target_roles.length > 0
  ];
  return Math.round((checks.filter(Boolean).length / checks.length) * 100);
};

export const totalSkills = (profile: CareerProfile | null): number => {
  if (!profile) return 0;
  return Object.values(profile.skills).reduce((total, items) => total + items.length, 0);
};

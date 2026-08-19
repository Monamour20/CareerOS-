export type PersonalInformation = {
  full_name: string | null;
  email: string | null;
  phone: string | null;
  location: string | null;
  links: string[];
  summary: string | null;
};

export type EducationItem = {
  institution: string | null;
  degree: string | null;
  field_of_study: string | null;
  start_date: string | null;
  end_date: string | null;
  details: string[];
};

export type ExperienceItem = {
  company: string | null;
  title: string | null;
  location: string | null;
  start_date: string | null;
  end_date: string | null;
  responsibilities: string[];
  technologies: string[];
};

export type Skills = {
  technical: string[];
  tools: string[];
  languages: string[];
  soft_skills: string[];
};

export type ProjectItem = {
  name: string | null;
  description: string | null;
  technologies: string[];
  links: string[];
};

export type CertificationItem = {
  name: string | null;
  issuer: string | null;
  date: string | null;
};

export type AchievementItem = {
  title: string | null;
  description: string | null;
};

export type CareerInterests = {
  target_roles: string[];
  industries: string[];
  seniority: string | null;
  strengths: string[];
  growth_areas: string[];
};

export type CareerProfile = {
  personal_information: PersonalInformation;
  education: EducationItem[];
  experience: ExperienceItem[];
  skills: Skills;
  projects: ProjectItem[];
  certifications: CertificationItem[];
  achievements: AchievementItem[];
  career_interests: CareerInterests;
};

export type User = {
  id: number;
  full_name: string | null;
  email: string | null;
  account_type: string | null;
  career_status: string | null;
  preferred_work_mode: string | null;
  career_goals: string | null;
  onboarding_completed: boolean;
  resume_creation_requested: boolean;
};

export type AuthResponse = {
  token: string;
  expires_at: string;
  user: User;
};

export type StoredCareerProfileResponse = {
  user_id: number;
  career_profile: CareerProfile;
};

export type ResumeAnalysisResponse = {
  career_profile: CareerProfile;
};

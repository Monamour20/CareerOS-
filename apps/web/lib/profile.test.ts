import { describe, expect, it } from "vitest";
import { emptyCareerProfile, profileCompleteness, totalSkills } from "./profile";

describe("profile metrics", () => {
  it("counts skills across all skill groups", () => {
    const profile = emptyCareerProfile("CareerOS Test User", "careeros.test@example.com");
    profile.skills.technical = ["Python", "FastAPI"];
    profile.skills.tools = ["PostgreSQL"];
    profile.skills.soft_skills = ["Communication"];

    expect(totalSkills(profile)).toBe(4);
  });

  it("calculates completion from populated profile sections", () => {
    const profile = emptyCareerProfile("CareerOS Test User", "careeros.test@example.com");
    profile.personal_information.summary = "Synthetic profile.";
    profile.education.push({ institution: "Test University", degree: "BS", field_of_study: "CS", start_date: null, end_date: null, details: [] });
    profile.career_interests.target_roles = ["Product Engineer"];

    expect(profileCompleteness(profile)).toBe(50);
  });
});

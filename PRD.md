# CareerOS — Product Requirements Document

## Product Definition
CareerOS is an AI-powered Career Operating System that understands a user's professional identity, stores it in a personal Career Vault, discovers and evaluates opportunities, prepares personalized applications, assists with approved application actions, tracks outcomes, and turns career activity into better decisions.

Core loop:
`User Identity → Career Vault → Career Intelligence → Opportunities → Application Intelligence → Approved Action → Outcomes → Better Recommendations`

## Primary Users
Students, recent graduates, working professionals, career switchers, freelancers, entrepreneurs, returning-to-work users, and other job seekers.

Onboarding is adaptive to the user's career status.

## Initial User Journey
`Sign up → Career status → Education/experience/goals → Resume decision → Career Profile → Career Vault → Dashboard`

Resume is optional.

If the user has a resume:
`Upload → document processing → AI analysis → validated CareerProfile → merge with onboarding data → Career Vault`

If the user has no resume:
CareerOS asks whether they want to create one and records that intent. They can continue without a resume.

## Career Vault
The persistent source of truth for:
- Identity
- Education
- Experience
- Skills
- Projects
- Certifications
- Achievements
- Career goals
- Career preferences
- Target roles
- Resume metadata and versions
- Applications
- Interviews
- Outcomes

Do not use one giant JSON document as the primary data model.

## CareerProfile
A structured representation of professional identity. It is not simply a parsed resume and can combine resume evidence, onboarding information, education, experience, projects, skills, certifications, achievements, goals, and preferences.

AI output must be validated before persistence.

## Opportunity Intelligence
`Source → Fetch → Normalize → Deduplicate → Enrich → Match → Rank → Present`

Users receive ranked opportunities with match explanations, strengths, missing requirements, risks, and recommended actions. User feedback improves ranking.

## JD Intelligence
`JD → Structured Job Profile → Requirement Analysis → CareerProfile Comparison`

Possible fields: role, company, location, experience, education, required/preferred skills, responsibilities, technologies, domain, soft skills, eligibility, and reliable compensation data.

## Resume Studio
Two engines:

### Content Intelligence
May reorder relevant information, improve clarity, align terminology with a JD, emphasize supported evidence, improve bullet structure, and recommend missing evidence.

Never invent jobs, companies, projects, skills, technologies, certifications, achievements, metrics, or experience.

### Design Intelligence
Professional templates such as ATS Safe, Modern Tech, Executive, Consulting, and Creative/Portfolio.

User controls template, typography, accent, section order, spacing, and layout.

Quality dimensions:
- Truthfulness
- JD alignment
- Content quality
- ATS compatibility
- Visual quality

## Application Intelligence
`Selected Job → JD Analysis → Resume-JD Comparison → Tailored Resume → ATS Validation → Cover Letter → Application Answers → Readiness Review`

User reviews before consequential action.

## Application Automation
Supported external applications may use browser automation:
`CareerOS → Website/ATS Detection → Adapter → Browser Agent → Form Mapping → Career Vault → User Review → User Approval → Submit → Confirmation → Track`

Never claim submission without confirmation. Stop for CAPTCHA, MFA, unsupported flows, unexpected security controls, or missing human-only steps. Never bypass security controls.

## Application Tracking
Statuses:
Saved, Applied, Assessment, Interview, Technical Round, HR Round, Offer, Rejected, Withdrawn, Closed.

Track job, company, application date, resume version, cover letter, answers, events, interviews, and outcome.

## Interview Intelligence
Uses JD + company context + CareerProfile + submitted resume + application to prepare likely questions, technical topics, behavioral/STAR preparation, weak areas, and questions for the interviewer.

## Career Analytics
Analyze structured outcomes such as response rates, recurring skill gaps, resume performance, industries, application funnel, and interview patterns. Do not pretend to know an exact rejection reason.

## Product Principles
1. User owns career data.
2. AI assists; user controls consequential actions.
3. AI never invents career facts.
4. Validate before persistence.
5. PostgreSQL is the system of record.
6. Career Vault is central career memory.
7. Preserve working functionality.
8. Implement incrementally and test.
9. Do not add technologies without a real requirement.
10. Do not silently replace frozen technology decisions.

## Implementation Order
1. Resume/document intelligence
2. Career Vault/database
3. Adaptive onboarding
4. Career Profile UI
5. Opportunity intelligence
6. JD intelligence
7. Resume Studio
8. Application preparation/tracking
9. Interview intelligence
10. Career analytics
11. Controlled application automation
12. Production deployment

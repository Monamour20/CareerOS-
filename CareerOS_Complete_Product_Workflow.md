# CareerOS — Complete Product Workflow & Project Navigation

> **Purpose:** Canonical end-to-end workflow and navigation document for CareerOS.
>
> If project context is ever lost, read this document together with `PRD.md`, `Architecture.md`, `Rules.md`, `Phases.md`, `Design.md`, and `Memory.md`.
>
> The repository remains the source of truth for actual implementation state.

---

# 1. CareerOS Product Definition

CareerOS is an AI-powered Career Operating System.

It understands a user's professional identity, stores it in a persistent Career Vault, discovers and evaluates opportunities, prepares personalized applications, assists with approved application actions, tracks outcomes, and uses those outcomes to improve future career decisions.

## Core Loop

```text
User Identity
      ↓
Career Vault
      ↓
Career Intelligence
      ↓
Opportunities
      ↓
Application Intelligence
      ↓
Approved Action
      ↓
Outcomes
      ↓
Better Recommendations
      ↓
Career Vault
2. Complete User Journey
LANDING / ENTRY
      ↓
SIGNUP / LOGIN
      ↓
CAREER STATUS
      ↓
ADAPTIVE ONBOARDING
      ↓
EDUCATION
      ↓
EXPERIENCE
      ↓
SKILLS / PROJECTS
      ↓
GOALS
      ↓
CAREER PREFERENCES
      ↓
RESUME DECISION
      ↓
 ┌───────────────┐
 │               │
Upload Resume    Continue Without Resume
 │               │
 ↓               ↓
Resume           Career Profile
Intelligence         │
 │                    │
 └────────┬───────────┘
          ↓
    VALIDATED CAREER PROFILE
          ↓
      CAREER VAULT
          ↓
    CAREER DASHBOARD
          ↓
   CAREER INTELLIGENCE
          ↓
 OPPORTUNITY DISCOVERY
          ↓
     SELECT JOB
          ↓
    JD INTELLIGENCE
          ↓
   SKILL GAP ANALYSIS
          ↓
      RESUME STUDIO
          ↓
 APPLICATION INTELLIGENCE
          ↓
      USER REVIEW
          ↓
     USER APPROVAL
          ↓
 APPLICATION / TRACKING
          ↓
 INTERVIEW INTELLIGENCE
          ↓
 NETWORKING INTELLIGENCE
          ↓
    CAREER ANALYTICS
          ↓
       OUTCOMES
          ↓
BETTER RECOMMENDATIONS
          ↓
      CAREER VAULT
3. Technical Architecture
Frozen Stack
Frontend
Next.js
React
TypeScript
Tailwind CSS
shadcn/ui
Framer Motion
Lucide
Backend
Python 3.13
FastAPI
Pydantic
SQLAlchemy 2.x
Alembic
psycopg
Database
PostgreSQL 17
AI
Ollama
Qwen3.5 9B
Documents
PyMuPDF
python-docx
Pillow
pytesseract / Tesseract
LibreOffice where required
Browser Automation
Playwright
Chromium

Do not silently replace frozen technologies.

4. System Architecture
                         ┌──────────────────┐
                         │      Browser     │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │ Next.js / React  │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │     FastAPI      │
                         └────────┬─────────┘
                                  ↓
                    ┌────────────────────────────┐
                    │    Application Services   │
                    │                            │
                    │ Career Vault              │
                    │ Career Intelligence       │
                    │ Opportunity Intelligence  │
                    │ Resume Intelligence       │
                    │ Application Intelligence  │
                    │ Analytics                  │
                    └────────────┬───────────────┘
                                 ↓
                    ┌────────────────────────────┐
                    │       Infrastructure       │
                    │                            │
                    │ PostgreSQL                 │
                    │ Ollama                     │
                    │ Document Processing        │
                    │ File/Object Storage        │
                    │ Playwright                 │
                    └────────────────────────────┘
Backend Layering
Route
 ↓
Application Service
 ↓
Domain
 ↓
Repository / Infrastructure

Routes remain thin.

Business logic belongs in application/domain layers.

Database orchestration belongs in repositories/infrastructure.

5. AI Boundary

The LLM never directly accesses PostgreSQL.

API
 ↓
Application Service
 ↓
AI Workflow
 ↓
LLM Interface
 ↓
Ollama
 ↓
Qwen3.5 9B
Persistence Boundary
LLM
 ↓
Parser
 ↓
Pydantic Validation
 ↓
Business Validation
 ↓
Validated Domain Object
 ↓
Application Service
 ↓
Repository
 ↓
SQLAlchemy
 ↓
PostgreSQL

Never:

LLM → Database
6. Career Vault

Career Vault is the central persistent career memory.

It is the source of truth used by all major CareerOS intelligence modules.

Core Entities
User
UserProfile
CareerProfile
Education
Experience
Skill
Project
Certification
Achievement
CareerGoal
CareerPreference
TargetRole
Resume
ResumeVersion
Opportunity
Application
ApplicationEvent
Interview
CareerMetric
Important Principle

CareerProfile is NOT simply a parsed resume.

It can combine:

onboarding information
resume evidence
education
experience
skills
projects
certifications
achievements
goals
preferences
target roles

Use normalized relational tables.

Do not make the complete career profile one giant JSON document.

7. Milestone 1 — Universal Resume Intelligence
Status

COMPLETE / FROZEN

Workflow
Upload
 ↓
Validation
 ↓
Signature Detection
 ↓
Extraction / OCR
 ↓
Normalization
 ↓
Qwen3.5 9B
 ↓
Pydantic Validation
 ↓
Business Validation
 ↓
CareerProfile
 ↓
Persistence
Supported Inputs
PDF
DOC
DOCX
TXT
PNG
JPG
JPEG
WEBP
Requirements
Scanned PDFs use OCR fallback.
AI output must be validated.
Raw LLM output must never be persisted.
Resume facts are merged into Career Vault as supported evidence.
CHECKPOINT 1 — Resume Intelligence Frozen

Verify:

document input works
extraction works
OCR works
AI workflow works
validation works
persistence works
tests remain green

Next:

Do not redesign this milestone unless a later integration defect requires a minimal fix.

8. Milestone 2 — Career Vault Foundation
Status

COMPLETE / FROZEN

Workflow
Validated CareerProfile
 ↓
Repository
 ↓
SQLAlchemy
 ↓
PostgreSQL
Foundation
PostgreSQL
SQLAlchemy
Alembic
User
CareerProfile
Education
Experience
Skills
Projects
Certifications
Achievements
Career Preferences
Resume metadata
Repository layer
CareerProfile persistence
Retrieval API
Resume → AI → CareerProfile → PostgreSQL integration
CHECKPOINT 2 — Career Vault Frozen

Verify:

PostgreSQL connection
Alembic migration
CareerProfile persistence
CareerProfile retrieval
invalid-profile rejection
resume integration
pytest
Ruff

Next:

Use Career Vault as the central foundation for onboarding.

9. Milestone 3 — Account + Adaptive Onboarding + Career Vault UI
Status

CURRENT MAJOR BUILD TARGET

This milestone must be completed before moving to Milestone 4.

User Flow
Signup
 ↓
Login
 ↓
Career Status
 ↓
Adaptive Questions
 ↓
Education
 ↓
Experience
 ↓
Skills
 ↓
Projects
 ↓
Goals
 ↓
Preferences
 ↓
Resume Decision
 ↓
Career Profile
 ↓
Career Vault
 ↓
Dashboard
Adaptive Onboarding

CareerOS should not show every user the same giant questionnaire.

Example:

Career Status
      ↓
 ┌───────────────┬────────────────┐
 │ Student       │ Professional   │
 └───────┬───────┴────────┬───────┘
         ↓                ↓
     Education         Experience
     Projects          Experience
         ↓                ↓
         └───────┬────────┘
                 ↓
                Goals
                 ↓
            Preferences
                 ↓
          Resume Decision
Required Features
Authentication
Signup
Login
Secure session
Protected routes/data
Logout
Career Status

Support appropriate career states such as:

student
recent graduate
working professional
career switcher
freelancer
entrepreneur
returning to work
other
Education

Capture supported:

degree
institution
field
dates
relevant evidence
Experience

Capture supported:

employer
title
dates
responsibilities
achievements
Goals

Capture:

target roles
career direction
goals
Preferences

Capture:

seniority
location preferences
other supported job preferences
Resume Decision

User can:

Upload now.
Create later.
Continue without a resume.
Career Vault UI

Editable sections:

Personal
Education
Experience
Skills
Projects
Certifications
Achievements
Goals
Preferences
Resumes

AI-extracted information must remain editable.

Dashboard

Surface:

Career health
Recommended next action
Top opportunities
Skill gaps
Application status
Upcoming interviews
Recent AI insights

Do not create a wall of cards.

CHECKPOINT 3 — Milestone 3 Complete

Verify that a new user can:

Sign up.
Log in.
Complete adaptive onboarding.
Persist their career information.
Upload or skip a resume.
Open Career Vault.
Edit career information.
Return later and see the same data.
View the dashboard.

Next:

Freeze Milestone 3 and start Milestone 4.

10. Milestone 4 — Opportunity Intelligence
Workflow
Source
 ↓
Fetch
 ↓
Normalize
 ↓
Deduplicate
 ↓
Enrich
 ↓
Match
 ↓
Rank
 ↓
Present
Features
Source Adapters

Each external job provider should have an isolated adapter.

Fetch

Retrieve supported jobs.

Normalize

Convert different provider formats into the CareerOS Job model.

Deduplicate

Use stable provider identity and safe additional signals.

Enrich

Extract and structure requirements where supported.

Match

Compare jobs against CareerProfile.

Rank

Rank using:

skills
experience
goals
preferences
career fit
other explainable signals
Opportunity UI

Show:

role
company
location
match score
why it matches
strengths
missing requirements
risks
recommended action

Actions:

Save
Reject
Interested
CHECKPOINT 4 — Opportunity Intelligence Complete

Verify:

A user can discover ranked opportunities, understand why they match, see missing requirements, and provide feedback.

Next:

Milestone 5 — JD Intelligence.

11. Milestone 5 — JD Intelligence
Workflow
Job Description
 ↓
Structured Job Profile
 ↓
Requirement Analysis
 ↓
CareerProfile Comparison
 ↓
Gap Analysis
 ↓
Recommendations
Extract

Potential fields:

role
company
location
experience
education
required skills
preferred skills
responsibilities
technologies
domain
soft skills
eligibility
reliable compensation data
Requirement Comparison
Requirement
 ↓
CareerProfile Evidence
 ↓
Classification

Classifications:

Matched
Partial
Missing
Unknown / insufficient evidence
Skill Gap Analysis

CareerOS must answer:

What am I missing for this role?

and:

What should I work on next?

Prioritize meaningful gaps rather than dumping a long list of missing keywords.

Recommendations

Possible actions:

learn a skill
strengthen an existing skill
build a project
improve evidence
improve resume evidence
prepare for interview topics

Recommendations must be grounded in Career Vault data.

CHECKPOINT 5 — JD Intelligence Complete

Verify:

JD parsing works
requirements are structured
CareerProfile comparison works
matched/partial/missing requirements work
explanations work
gap analysis works
recommendations work

Next:

Milestone 6 — Resume Studio.

12. Milestone 6 — Resume Studio
Workflow
CareerProfile + JD
 ↓
Content Intelligence
 ↓
User Review
 ↓
Design Intelligence
 ↓
ATS Validation
 ↓
Preview
 ↓
Export
 ↓
ResumeVersion
Content Intelligence

Allowed:

reorder relevant information
improve clarity
align terminology
emphasize supported evidence
improve bullet structure
recommend missing evidence

Forbidden:

invent employers
invent titles
invent dates
invent skills
invent technologies
invent projects
invent certifications
invent achievements
invent metrics
invent experience
Design Intelligence

Templates:

ATS Safe
Modern Tech
Executive
Consulting
Creative / Portfolio

User controls:

template
typography
accent
section order
spacing
layout
Quality Dimensions
Truthfulness
JD alignment
Content quality
ATS compatibility
Visual quality
UI
Editor | Preview

Include:

AI suggestions
JD tailoring
ATS analysis
version history
PDF export
DOCX export
CHECKPOINT 6 — Resume Studio Complete

Verify:

User can create, edit, tailor, validate, preview, export, and retrieve truthful resume versions.

Next:

Milestone 7 — Application Intelligence.

13. Milestone 7 — Application Intelligence
Workflow
Selected Job
 ↓
JD Analysis
 ↓
Resume-JD Comparison
 ↓
Tailored Resume
 ↓
ATS Validation
 ↓
Cover Letter
 ↓
Application Answers
 ↓
Readiness Review
 ↓
User Review
 ↓
Application Record
Application Package
tailored resume
cover letter
application answers
readiness review
Tracking Statuses
Saved
Applied
Assessment
Interview
Technical Round
HR Round
Offer
Rejected
Withdrawn
Closed

Track:

job
company
application date
resume version
cover letter
answers
events
interviews
outcome
CHECKPOINT 7 — Application Intelligence Complete

Verify:

A user can prepare, review, record, and track an application.

Next:

Milestone 8 — Interview + Networking Intelligence.

14. Milestone 8 — Interview + Networking Intelligence
Interview Workflow
JD
 +
Company Context
 +
CareerProfile
 +
Submitted Resume
        ↓
Interview Intelligence
        ↓
Preparation Workspace
Interview Features
technical questions
technical topics
behavioral questions
STAR preparation
weak areas
company preparation
role preparation
questions for interviewer

Everything must be grounded in the user's real career information.

Networking Workflow
Contact
 ↓
Relationship Context
 ↓
Networking Goal
 ↓
Personalized Outreach
 ↓
User Review
 ↓
Follow-up Tracking
CHECKPOINT 8 — Interview + Networking Complete

Verify:

Users can prepare for interviews and manage networking assistance.

Next:

Milestone 9 — Career Analytics.

15. Milestone 9 — Career Analytics
Data Flow
Applications
 +
Opportunities
 +
Interviews
 +
Resume Versions
 +
Outcomes
 +
Skill Gaps
        ↓
Career Metrics
        ↓
Recommendations
Analytics

Analyze:

application funnel
response rates
interview rates
offer rates
recurring skill gaps
role trends
industry trends
resume performance
interview patterns
Truthfulness Rule

Do not pretend to know an exact rejection reason without evidence.

CHECKPOINT 9 — Career Analytics Complete

Verify:

Analytics use structured data and clearly separate facts from inference.

Next:

Milestone 10 — Controlled Application Automation.

16. Milestone 10 — Controlled Application Automation
Workflow
CareerOS
 ↓
Website / ATS Detection
 ↓
Adapter
 ↓
Browser Agent
 ↓
Form Mapping
 ↓
Career Vault
 ↓
User Review
 ↓
User Approval
 ↓
Submit
 ↓
External Confirmation
 ↓
Track
Rules

Automation must:

use ATS/site adapters
map form fields to Career Vault
stop for unsupported flows
require user review
require explicit approval
verify external confirmation
record confirmed application state

Stop for:

CAPTCHA
MFA
security controls
unsupported workflows
human-only steps

Never:

bypass CAPTCHA
bypass MFA
bypass security
bypass authorization
bypass consent
claim submission without confirmation
CHECKPOINT 10 — Controlled Automation Complete

Verify:

Supported automation is safe, consent-driven, and truthful.

Next:

Milestone 11 — Production.

17. Milestone 11 — Production
Workflow
Docker
 ↓
Production Containers
 ↓
CI/CD
 ↓
Secret Management
 ↓
Managed PostgreSQL
 ↓
Object Storage
 ↓
Monitoring
 ↓
Logging
 ↓
HTTPS
 ↓
Backups
 ↓
Deployment
Requirements
production containers
production configuration
CI/CD
secret management
managed PostgreSQL
object storage
monitoring
logging
HTTPS
backups
recovery
deployment
CHECKPOINT 11 — Production Complete

Verify:

deployment works
critical user journeys work
secrets are protected
monitoring works
logging works
backups work
recovery is tested
security requirements pass

Next:

CareerOS enters maintenance and product-growth mode.

18. Cross-Feature AI Rules

These rules apply everywhere.

User Control

AI assists.

The user controls consequential actions.

No Fabrication

AI must never invent:

employers
titles
dates
skills
technologies
metrics
certifications
projects
achievements
experience
Validation

Always:

LLM
 ↓
Parser
 ↓
Pydantic
 ↓
Business Validation
 ↓
Persistence
No Hidden Reasoning

Never expose hidden model reasoning.

Show:

status
useful results
evidence
match explanations
missing requirements
risks
recommendations
Central Memory

Career Vault remains the central persistent career memory.

19. User Experience Principles

CareerOS should feel like a premium professional operating system.

Design
clean
modern
premium
professional
calm
data-focused
AI-native
Navigation
Overview
Career Vault
Opportunities
Resume Studio
Applications
Interviews
Networking
Analytics
Settings
AI Status Messages

Examples:

Reading resume
Extracting career information
Checking profile
Analyzing opportunity
Preparing application
Waiting for approval
Accessibility
semantic HTML
keyboard navigation
visible focus
labels
accessible dialogs
sufficient contrast
clear errors
20. Engineering Protocol

Every milestone follows:

INSPECT
   ↓
PLAN
   ↓
IMPLEMENT
   ↓
TEST
   ↓
REPAIR
   ↓
INTEGRATION TEST
   ↓
FINAL REPORT
   ↓
FREEZE
Inspect

Read:

repository structure
dependencies
routes
services
domain models
repositories
database models
frontend
tests
configuration
Plan

Define:

files
database changes
API contracts
domain logic
UI states
data flow
acceptance criteria
Implement

Build the complete vertical feature.

Do not create disconnected mock features.

Test

Preserve all existing tests.

Add tests for new behavior.

Run:

pytest
Ruff
frontend typecheck
frontend tests
frontend build
important integration tests
Repair

Fix real defects.

Never:

delete tests
weaken tests
hide failures
use temporary hacks
Integration Test

Test the actual flow:

User
 ↓
Frontend
 ↓
API
 ↓
Application Service
 ↓
Repository
 ↓
PostgreSQL
 ↓
Response
 ↓
Frontend
Final Report

Record:

changed files
architecture changes
database changes
API changes
frontend changes
tests
lint
build
integration verification
limitations
acceptance status
next milestone
Freeze

When acceptance criteria pass, freeze the milestone.

21. Project Recovery Checkpoint

When context is lost:

READ THIS FILE
      ↓
READ MEMORY.md
      ↓
CHECK git status
      ↓
CHECK recent git log
      ↓
IDENTIFY LAST CHECKPOINT
      ↓
IDENTIFY CURRENT MILESTONE
      ↓
CHECK ACCEPTANCE CRITERIA
      ↓
INSPECT EXISTING IMPLEMENTATION
      ↓
CONTINUE FROM FIRST INCOMPLETE STEP
Never Do This

Do not:

restart the project
rebuild completed milestones
guess the current state
replace frozen technologies
skip acceptance criteria
start a later milestone before the current one is complete
22. Current Project Checkpoint
Repository
Project: CareerOS
Branch: main

Known latest repository checkpoint:

8e5a42e
fix career profile persistence
Current Local Changes
services/ai-service/app/infrastructure/database/repositories/career_profile.py

services/ai-service/tests/test_career_profile_repository.py
Latest Known Backend Verification
43 tests passed
Current Product Position
Milestone 1
Resume Intelligence
        ↓
COMPLETE

Milestone 2
Career Vault Foundation
        ↓
COMPLETE

Milestone 3
Account + Adaptive Onboarding + Career Vault UI
        ↓
CURRENT BUILD TARGET

Milestone 4
Opportunity Intelligence
        ↓
NEXT

Milestone 5
JD Intelligence + Skill Gap Analysis
        ↓
LATER
CHECKPOINT 12 — Current Resume Point

Before starting new product work:

Preserve the working CareerProfile persistence fix.
Verify repository status.
Commit clean bug-fix changes when appropriate.
Complete Milestone 3.
Do not jump directly to JD Intelligence.
Do not restart completed milestones.
23. Complete Dependency Graph
                    USER IDENTITY
                         │
                         ↓
                   CAREER VAULT
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
     EXPERIENCE       SKILLS         GOALS
          │              │              │
          └──────────────┼──────────────┘
                         ↓
               CAREER INTELLIGENCE
                         ↓
              OPPORTUNITY ENGINE
                         ↓
                    SELECT JOB
                         ↓
                  JD INTELLIGENCE
                         ↓
                 SKILL GAP ANALYSIS
                         ↓
                   RESUME STUDIO
                         ↓
             APPLICATION INTELLIGENCE
                         ↓
                   USER APPROVAL
                         ↓
              APPLICATION TRACKING
                         ↓
              INTERVIEW INTELLIGENCE
                         ↓
             NETWORKING INTELLIGENCE
                         ↓
                CAREER ANALYTICS
                         ↓
                      OUTCOMES
                         ↓
              BETTER RECOMMENDATIONS
                         ↓
                   CAREER VAULT
24. Whole-Product Definition of Done

CareerOS is complete when:

all planned milestones are implemented
all milestone acceptance criteria pass
critical user journeys work end-to-end
Career Vault is the central source of truth
AI output is validated before persistence
AI never invents career facts
opportunities are normalized, matched, ranked, and explained
JD intelligence works
skill gaps are actionable
Resume Studio works
applications can be prepared and tracked
interview preparation works
networking assistance works
analytics work
automation is consent-driven
external submission is never falsely claimed
production deployment works
monitoring works
backups work
recovery works
tests pass
lint passes
typecheck passes
builds pass
critical integration flows pass
CHECKPOINT 13 — WHOLE CAREEROS COMPLETE
Milestone 1  ✅
Milestone 2  ✅
Milestone 3  ✅
Milestone 4  ✅
Milestone 5  ✅
Milestone 6  ✅
Milestone 7  ✅
Milestone 8  ✅
Milestone 9  ✅
Milestone 10 ✅
Milestone 11 ✅

Then verify the complete loop:

Identity
 → Career Vault
 → Career Intelligence
 → Opportunities
 → JD Intelligence
 → Skill Gap
 → Resume Studio
 → Application Intelligence
 → User Approval
 → Application Tracking
 → Interview Intelligence
 → Networking
 → Outcomes
 → Career Analytics
 → Better Recommendations
 → Career Vault

Only after this checkpoint should CareerOS move into normal post-launch development.

25. Quick Recovery Card

If either the user or assistant becomes confused about the project:

WHAT ARE WE BUILDING?
→ CareerOS

WHAT IS THE CENTRAL SYSTEM?
→ Career Vault

WHAT IS THE CURRENT MILESTONE?
→ Check the latest checkpoint in this file + repository state

WHAT DO WE DO NEXT?
→ Complete the first incomplete acceptance criterion

DO WE RESTART COMPLETED WORK?
→ NO

DO WE JUMP TO A LATER MILESTONE?
→ NO

WHAT IS THE BUILD PROCESS?
→ Inspect → Plan → Implement → Test → Repair → Integration Test → Final Report → Freeze

WHAT IS THE FINAL GOAL?
→ Complete the entire CareerOS product loop
26. Relationship With Other Project Documents

This file does not replace the existing project documents.

PRD.md
   ↓
What CareerOS must do

Architecture.md
   ↓
How CareerOS is technically structured

Rules.md
   ↓
How CareerOS must be engineered safely

Phases.md
   ↓
What must be built and in what order

Design.md
   ↓
How CareerOS should look and behave

Memory.md
   ↓
Historical/current implementation memory

CareerOS_Complete_Product_Workflow.md
   ↓
How the complete product connects
+ user journey
+ technical workflow
+ checkpoints
+ recovery process

The repository code remains the final source of truth for actual implementation state.

END OF CAREEROS MASTER WORKFLOW


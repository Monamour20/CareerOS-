from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app.core.errors import DatabaseOperationError
from app.domain.career_profile.models import (
    AchievementItem,
    CareerInterests,
    CareerProfile,
    CertificationItem,
    EducationItem,
    ExperienceItem,
    PersonalInformation,
    ProjectItem,
    Skills,
)
from app.infrastructure.database.models import (
    AchievementRecord,
    CareerPreferenceItemRecord,
    CareerPreferenceRecord,
    CareerProfileRecord,
    CertificationRecord,
    EducationDetailRecord,
    EducationRecord,
    ExperienceRecord,
    ExperienceResponsibilityRecord,
    ExperienceTechnologyRecord,
    ProjectLinkRecord,
    ProjectRecord,
    ProjectTechnologyRecord,
    SkillRecord,
    UserRecord,
)


class CareerProfileRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, profile: CareerProfile, user_id: int | None = None) -> int:
        try:
            user = self._get_or_create_user(profile, user_id)
            if user.career_profile is not None:
                self.session.delete(user.career_profile)
                self.session.flush()

            user.full_name = profile.personal_information.full_name
            if profile.personal_information.email:
                user.email = profile.personal_information.email

            record = self._to_record(profile)
            user.career_profile = record
            self.session.add(user)
            self.session.commit()
            return user.id
        except SQLAlchemyError as exc:
            self.session.rollback()
            raise DatabaseOperationError("Could not save CareerProfile.") from exc

    def get_by_user_id(self, user_id: int) -> CareerProfile | None:
        statement = (
            select(UserRecord)
            .where(UserRecord.id == user_id)
            .options(
                selectinload(UserRecord.career_profile).selectinload(CareerProfileRecord.education),
                selectinload(UserRecord.career_profile)
                .selectinload(CareerProfileRecord.education)
                .selectinload(EducationRecord.details),
                selectinload(UserRecord.career_profile).selectinload(CareerProfileRecord.experience),
                selectinload(UserRecord.career_profile)
                .selectinload(CareerProfileRecord.experience)
                .selectinload(ExperienceRecord.responsibilities),
                selectinload(UserRecord.career_profile)
                .selectinload(CareerProfileRecord.experience)
                .selectinload(ExperienceRecord.technologies),
                selectinload(UserRecord.career_profile).selectinload(CareerProfileRecord.skills),
                selectinload(UserRecord.career_profile).selectinload(CareerProfileRecord.projects),
                selectinload(UserRecord.career_profile)
                .selectinload(CareerProfileRecord.projects)
                .selectinload(ProjectRecord.technologies),
                selectinload(UserRecord.career_profile)
                .selectinload(CareerProfileRecord.projects)
                .selectinload(ProjectRecord.links),
                selectinload(UserRecord.career_profile).selectinload(CareerProfileRecord.certifications),
                selectinload(UserRecord.career_profile).selectinload(CareerProfileRecord.achievements),
                selectinload(UserRecord.career_profile)
                .selectinload(CareerProfileRecord.career_preference)
                .selectinload(CareerPreferenceRecord.items),
            )
        )
        user = self.session.scalars(statement).first()
        if user is None or user.career_profile is None:
            return None
        return self._from_record(user)

    def _get_or_create_user(self, profile: CareerProfile, user_id: int | None) -> UserRecord:
        if user_id is not None:
            user = self.session.get(UserRecord, user_id)
            if user is None:
                user = UserRecord(id=user_id)
            return user

        email = profile.personal_information.email
        if email:
            user = self.session.scalars(select(UserRecord).where(UserRecord.email == email)).first()
            if user is not None:
                return user

        return UserRecord()

    def _to_record(self, profile: CareerProfile) -> CareerProfileRecord:
        linkedin, github = self._extract_profile_links(profile.personal_information.links)
        record = CareerProfileRecord(
            phone=profile.personal_information.phone,
            location=profile.personal_information.location,
            linkedin=linkedin,
            github=github,
            summary=profile.personal_information.summary,
        )

        record.education = [
            EducationRecord(
                institution=item.institution,
                degree=item.degree,
                field_of_study=item.field_of_study,
                start_date=item.start_date,
                end_date=item.end_date,
                sort_order=index,
                details=[
                    EducationDetailRecord(detail=detail, sort_order=detail_index)
                    for detail_index, detail in enumerate(item.details)
                ],
            )
            for index, item in enumerate(profile.education)
        ]
        record.experience = [
            ExperienceRecord(
                company=item.company,
                title=item.title,
                location=item.location,
                start_date=item.start_date,
                end_date=item.end_date,
                sort_order=index,
                responsibilities=[
                    ExperienceResponsibilityRecord(
                        responsibility=responsibility,
                        sort_order=responsibility_index,
                    )
                    for responsibility_index, responsibility in enumerate(item.responsibilities)
                ],
                technologies=[
                    ExperienceTechnologyRecord(technology=technology, sort_order=technology_index)
                    for technology_index, technology in enumerate(item.technologies)
                ],
            )
            for index, item in enumerate(profile.experience)
        ]
        record.skills = self._skill_records(profile.skills)
        record.projects = [
            ProjectRecord(
                name=item.name,
                description=item.description,
                sort_order=index,
                technologies=[
                    ProjectTechnologyRecord(technology=technology, sort_order=technology_index)
                    for technology_index, technology in enumerate(item.technologies)
                ],
                links=[
                    ProjectLinkRecord(url=link, sort_order=link_index)
                    for link_index, link in enumerate(item.links)
                ],
            )
            for index, item in enumerate(profile.projects)
        ]
        record.certifications = [
            CertificationRecord(
                name=item.name,
                issuer=item.issuer,
                date=item.date,
                sort_order=index,
            )
            for index, item in enumerate(profile.certifications)
        ]
        record.achievements = [
            AchievementRecord(
                title=item.title,
                description=item.description,
                sort_order=index,
            )
            for index, item in enumerate(profile.achievements)
        ]
        record.career_preference = CareerPreferenceRecord(
            seniority=profile.career_interests.seniority,
            items=self._preference_items(profile.career_interests),
        )
        return record

    def _from_record(self, user: UserRecord) -> CareerProfile:
        record = user.career_profile
        assert record is not None
        links = [link for link in (record.linkedin, record.github) if link]

        return CareerProfile(
            personal_information=PersonalInformation(
                full_name=user.full_name,
                email=user.email,
                phone=record.phone,
                location=record.location,
                links=links,
                summary=record.summary,
            ),
            education=[
                EducationItem(
                    institution=item.institution,
                    degree=item.degree,
                    field_of_study=item.field_of_study,
                    start_date=item.start_date,
                    end_date=item.end_date,
                    details=[
                        detail.detail for detail in sorted(item.details, key=lambda detail: detail.sort_order)
                    ],
                )
                for item in sorted(record.education, key=lambda item: item.sort_order)
            ],
            experience=[
                ExperienceItem(
                    company=item.company,
                    title=item.title,
                    location=item.location,
                    start_date=item.start_date,
                    end_date=item.end_date,
                    responsibilities=[
                        detail.responsibility
                        for detail in sorted(
                            item.responsibilities, key=lambda detail: detail.sort_order
                        )
                    ],
                    technologies=[
                        technology.technology
                        for technology in sorted(
                            item.technologies, key=lambda technology: technology.sort_order
                        )
                    ],
                )
                for item in sorted(record.experience, key=lambda item: item.sort_order)
            ],
            skills=self._skills_from_record(record.skills),
            projects=[
                ProjectItem(
                    name=item.name,
                    description=item.description,
                    technologies=[
                        technology.technology
                        for technology in sorted(
                            item.technologies, key=lambda technology: technology.sort_order
                        )
                    ],
                    links=[link.url for link in sorted(item.links, key=lambda link: link.sort_order)],
                )
                for item in sorted(record.projects, key=lambda item: item.sort_order)
            ],
            certifications=[
                CertificationItem(name=item.name, issuer=item.issuer, date=item.date)
                for item in sorted(record.certifications, key=lambda item: item.sort_order)
            ],
            achievements=[
                AchievementItem(title=item.title, description=item.description)
                for item in sorted(record.achievements, key=lambda item: item.sort_order)
            ],
            career_interests=self._career_interests_from_record(record.career_preference),
        )

    def _skill_records(self, skills: Skills) -> list[SkillRecord]:
        records: list[SkillRecord] = []
        for category, values in (
            ("technical", skills.technical),
            ("tools", skills.tools),
            ("languages", skills.languages),
            ("soft_skills", skills.soft_skills),
        ):
            records.extend(
                SkillRecord(category=category, name=value, sort_order=index)
                for index, value in enumerate(values)
            )
        return records

    def _skills_from_record(self, records: list[SkillRecord]) -> Skills:
        grouped = {"technical": [], "tools": [], "languages": [], "soft_skills": []}
        for record in sorted(records, key=lambda item: item.sort_order):
            if record.category in grouped:
                grouped[record.category].append(record.name)
        return Skills(**grouped)

    def _preference_items(self, interests: CareerInterests) -> list[CareerPreferenceItemRecord]:
        items: list[CareerPreferenceItemRecord] = []
        for category, values in (
            ("target_roles", interests.target_roles),
            ("industries", interests.industries),
            ("strengths", interests.strengths),
            ("growth_areas", interests.growth_areas),
        ):
            items.extend(
                CareerPreferenceItemRecord(category=category, value=value, sort_order=index)
                for index, value in enumerate(values)
            )
        return items

    def _career_interests_from_record(
        self, record: CareerPreferenceRecord | None
    ) -> CareerInterests:
        if record is None:
            return CareerInterests()

        grouped = {"target_roles": [], "industries": [], "strengths": [], "growth_areas": []}
        for item in sorted(record.items, key=lambda item: item.sort_order):
            if item.category in grouped:
                grouped[item.category].append(item.value)
        return CareerInterests(seniority=record.seniority, **grouped)

    def _extract_profile_links(self, links: list[str]) -> tuple[str | None, str | None]:
        linkedin = next((link for link in links if "linkedin" in link.lower()), None)
        github = next((link for link in links if "github" in link.lower()), None)
        return linkedin, github

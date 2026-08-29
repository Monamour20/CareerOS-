from dataclasses import dataclass


@dataclass(frozen=True)
class CareerContext:
    summary: str
    skills: tuple[str, ...]
    experiences: tuple[str, ...]
    education: tuple[str, ...]
    projects: tuple[str, ...]
    certifications: tuple[str, ...]
    preferences: tuple[str, ...]

    def to_prompt_context(self) -> str:
        """Convert career data into controlled AI context."""

        sections = [
            f"SUMMARY:\n{self.summary or 'Not provided'}",
            self._format_section("SKILLS", self.skills),
            self._format_section("EXPERIENCE", self.experiences),
            self._format_section("EDUCATION", self.education),
            self._format_section("PROJECTS", self.projects),
            self._format_section("CERTIFICATIONS", self.certifications),
            self._format_section("PREFERENCES", self.preferences),
        ]

        return "\n\n".join(sections)

    @staticmethod
    def _format_section(
        title: str,
        values: tuple[str, ...],
    ) -> str:
        if not values:
            return f"{title}:\nNot provided"

        return f"{title}:\n" + "\n".join(
            f"- {value}" for value in values
        )
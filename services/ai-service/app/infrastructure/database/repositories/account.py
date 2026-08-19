from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app.core.errors import AuthenticationError, ConflictError, DatabaseOperationError
from app.core.security import (
    create_session_token,
    hash_password,
    hash_session_token,
    verify_password,
)
from app.infrastructure.database.models import AuthSessionRecord, UserRecord

SESSION_TTL_DAYS = 14


class AccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, *, full_name: str, email: str, password: str) -> UserRecord:
        user = UserRecord(
            full_name=full_name,
            email=email.lower(),
            password_hash=hash_password(password),
            account_type="standard",
        )
        self.session.add(user)
        try:
            self.session.commit()
            self.session.refresh(user)
            return user
        except IntegrityError as exc:
            self.session.rollback()
            raise ConflictError("An account already exists for this email.") from exc
        except SQLAlchemyError as exc:
            self.session.rollback()
            raise DatabaseOperationError("Could not create account.") from exc

    def authenticate_user(self, *, email: str, password: str) -> UserRecord:
        user = self.session.scalars(
            select(UserRecord).where(UserRecord.email == email.lower())
        ).first()
        if user is None or not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid email or password.")
        return user

    def create_session(self, user: UserRecord) -> tuple[str, datetime]:
        token = create_session_token()
        expires_at = datetime.now(UTC) + timedelta(days=SESSION_TTL_DAYS)
        session_record = AuthSessionRecord(
            user_id=user.id,
            token_hash=hash_session_token(token),
            expires_at=expires_at,
        )
        self.session.add(session_record)
        try:
            self.session.commit()
        except SQLAlchemyError as exc:
            self.session.rollback()
            raise DatabaseOperationError("Could not create auth session.") from exc
        return token, expires_at

    def get_user_by_session_token(self, token: str) -> UserRecord | None:
        token_hash = hash_session_token(token)
        now = datetime.now(UTC)
        statement = (
            select(AuthSessionRecord)
            .where(AuthSessionRecord.token_hash == token_hash)
            .where(AuthSessionRecord.expires_at > now)
            .options(selectinload(AuthSessionRecord.user))
        )
        session_record = self.session.scalars(statement).first()
        if session_record is None:
            return None
        return session_record.user

    def delete_session(self, token: str) -> None:
        token_hash = hash_session_token(token)
        try:
            self.session.execute(delete(AuthSessionRecord).where(AuthSessionRecord.token_hash == token_hash))
            self.session.commit()
        except SQLAlchemyError as exc:
            self.session.rollback()
            raise DatabaseOperationError("Could not end auth session.") from exc

    def update_onboarding(
        self,
        user: UserRecord,
        *,
        career_status: str | None,
        preferred_work_mode: str | None,
        career_goals: str | None,
        resume_creation_requested: bool,
    ) -> None:
        user.career_status = career_status
        user.preferred_work_mode = preferred_work_mode
        user.career_goals = career_goals
        user.resume_creation_requested = resume_creation_requested
        user.onboarding_completed = True
        try:
            self.session.add(user)
            self.session.commit()
        except SQLAlchemyError as exc:
            self.session.rollback()
            raise DatabaseOperationError("Could not update onboarding state.") from exc

from sqlmodel import Session, select

from ..models import User


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()

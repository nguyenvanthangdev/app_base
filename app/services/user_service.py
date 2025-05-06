from app.db.session import get_session
from app.models.user import User
from sqlmodel import select


def get_all_users():
    with get_session() as session:
        return session.exec(select(User)).all()


def add_user(name: str, email: str):
    with get_session() as session:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def delete_user(user_id: int):
    with get_session() as session:
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            session.commit()

def update_user(user_id: int, name: str, email: str):
    with get_session() as session:
        user = session.get(User, user_id)
        if user:
            user.name = name
            user.email = email
            session.commit()
            session.refresh(user)
            return user
        return None


from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


engine = create_engine('sqlite:///taskdb.db', echo=True)

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String)
    users = relationship(
        'Roles',
        secondary='users_roles'
    )


class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    roles = relationship(
        'Users',
        secondary='users_roles'
    )


class UsersRoles(Base):
    __tablename__ = 'users_roles'
    users_id = Column(
        Integer,
        ForeignKey('users.id', ondelete="CASCADE"),
        primary_key=True,
    )

    roles_id = Column(
        Integer,
        ForeignKey('roles.id'),
        primary_key=True)

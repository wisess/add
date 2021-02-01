from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Users, Roles, UsersRoles, Base

engine = create_engine('sqlite:///taskdb.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


def get_user_data(user_name: str):
    user = session.query(Users).filter_by(name=user_name).one()
    user_roles_id = session.query(UsersRoles).filter_by(users_id=user.id).all()
    user_roles = []
    for role_id in user_roles_id:
        user_roles.append(session.query(Roles).filter_by(id=role_id.roles_id).one().name)
    user_data = {
        "user_id": user.id,
        "user_name": user.name,
        "phone_number": user.phone_number,
        "roles": user_roles,
    }
    return user_data


def get_all_users_data():
    all_users_data = []
    users = session.query(Users).all()
    for user in users:
        all_users_data.append(get_user_data(user.name))
    return all_users_data


def add_user(user_name: str, phone_number: str, role: str):
    user_to_add = Users(name=user_name, phone_number=phone_number)
    session.add(user_to_add)
    session.commit()
    add_role_for_user(user_name, role)


def delete_user(user_name: str):
    user_to_delete = session.query(Users).filter_by(name=user_name).one()
    session.delete(user_to_delete)
    session.commit()


def update_user_data(user_name: str, new_data: Dict[str, str]):
    user_to_update = session.query(Users).filter_by(name=user_name).one()
    user_to_update.name = new_data["new_user_name"]
    if new_data["new_user_phone_number"] != "":
        user_to_update.phone_number = new_data["new_user_phone_number"]
    session.add(user_to_update)
    session.commit()


def add_role_for_user(user_name: str, role: str):
    user_id = session.query(Users).filter_by(name=user_name).one().id
    role_id = session.query(Roles).filter_by(name=role).one().id
    user_role_to_add = UsersRoles(users_id=user_id, roles_id=role_id)
    session.add(user_role_to_add)
    session.commit()


def delete_user_role(user_name: str, role: str):
    user_id = session.query(Users).filter_by(name=user_name).one().id
    role_id = session.query(Roles).filter_by(name=role).one().id
    user_role_to_delete = session.query(UsersRoles).filter_by(users_id=user_id).filter_by(roles_id=role_id).one()
    session.delete(user_role_to_delete)
    session.commit()


def add_role(role_name: str):
    role_to_add = Roles(name=role_name)
    session.add(role_to_add)
    session.commit()


def delete_role(role_name: str):
    role_to_delete = session.query(Roles).filter_by(name=role_name).one()
    session.delete(role_to_delete)
    session.commit()


def user_is_exist(user_name: str):
    user = session.query(Users).filter_by(name=user_name).first()
    return user


def role_is_exist(role_name: str):
    role = session.query(Roles).filter_by(name=role_name).first()
    return role


def user_has_role(user_name: str, role_name: str):
    user_id = session.query(Users).filter_by(name=user_name).one().id
    role_id = session.query(Roles).filter_by(name=role_name).one().id
    user_role = session.query(UsersRoles).filter_by(users_id=user_id).filter_by(roles_id=role_id).first()
    if user_role:
        return user_role
    else:
        return None

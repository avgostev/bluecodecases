from sqlalchemy import MetaData, select, create_engine, func, delete, case, extract, text
from sqlalchemy.orm import Session
from app.config import SQLALCHEMY_DATABASE_URI
from app import lm
from app.models import User, SLRCase, Sex, Result, Place, Locate
import math

engine = create_engine(url=SQLALCHEMY_DATABASE_URI)

@lm.user_loader
def load_user(user_id):
    with Session(engine) as session:
        sttmnt = select(User).where(User.id == user_id)
        return session.scalars(sttmnt).one_or_none()


def get_user_from_login(login):
    with Session(engine) as session:
        sttmnt = select(User).where(User.email == login)
        return session.scalars(sttmnt).one_or_none()


def register_user(user_dict):
    with Session(engine) as session:
        user = User(name = user_dict["name"],
                    email = user_dict["email"]
                    )
        user.set_password(user_dict["password"])
        session.add(user)
        session.commit()


def get_slrcases_count(user_id):
    cases = 0
    with Session(engine) as session:
        if user_id:
            sttmnt = select(func.count(SLRCase.id)).select_from(SLRCase).where(SLRCase.user_id == user_id)
        else:
            sttmnt = select(func.count(SLRCase.id)).select_from(SLRCase)
        cases = session.execute(sttmnt).scalars().one_or_none()
    
    return cases


def get_slrcases_result(user_id):
    cases = [0, 0]
    with Session(engine) as session:
        if user_id:
            sttmnt = select(func.count(case((SLRCase.result_id == 1, SLRCase.id), else_ = None)).label("cnt_1"), func.count(SLRCase.id).label("cnt_all")).select_from(SLRCase).where(SLRCase.user_id == user_id)
        else:
            sttmnt = select(func.count(case((SLRCase.result_id == 1, SLRCase.id), else_ = None)).label("cnt_1"), func.count(SLRCase.id).label("cnt_all")).select_from(SLRCase)
        cases = session.execute(sttmnt).fetchone()
    
    if cases[1] == 0:
        return 0
    else:
        return cases[0] / cases[1] * 100


def get_slrcases(user_id, offset = 0, limit = 100):
    cases = []
    with Session(engine) as session:
        sttmnt = select(SLRCase).where(SLRCase.user_id == user_id).order_by(SLRCase.d_slr.desc()).offset(offset).limit(limit)
        for slr_case in session.scalars(sttmnt):
            cases.append(slr_case)
    return cases


def get_slrcase(id, user_id):
    slrcase = None
    with Session(engine) as session:
        sttmnt = select(SLRCase).where(SLRCase.id == id).where(SLRCase.user_id == user_id)
        slrcase = session.scalars(sttmnt).one_or_none()
        
    return slrcase

def delete_slrcase(id, user_id):
    slrcase = None
    with Session(engine) as session:
        sttmnt = select(SLRCase).where(SLRCase.id == id).where(SLRCase.user_id == user_id)
        slrcase = session.scalars(sttmnt).one_or_none()
        if slrcase is not None:
            session.delete(slrcase)
            session.commit()
        
    return True

def save_slrcase(slrcase: dict):
    if slrcase is None:
        return False
    
    with Session(engine) as session:
        sttmnt = select(SLRCase).where(SLRCase.id == slrcase['id'])
        item = session.scalars(sttmnt).one_or_none()
        if item is not None:
            if item.user_id == slrcase['user_id']:
                item.d_slr = slrcase['d_slr']
                item.sex_id = slrcase['sex']
                item.result_id = slrcase['result']
                item.place_id = slrcase['place']
                item.locate_id = slrcase['locate']
                item.d_bdate = slrcase['d_bdate']
            else:
                return False
        else:
            item = SLRCase(d_slr = slrcase['d_slr'],
                           sex_id = slrcase['sex'],
                           result_id = slrcase['result'],
                           place_id = slrcase['place'],
                           locate_id = slrcase['locate'],
                           d_bdate = slrcase['d_bdate'],
                           user_id = slrcase['user_id'])
            session.add(item)
        session.commit()
    return True


def get_genders():
    genders = []
    with Session(engine) as session:
        sttmnt = select(Sex).order_by(Sex.s_name.asc())
        for gender in session.scalars(sttmnt):
            genders.append(gender)
    return genders


def get_results():
    results = []
    with Session(engine) as session:
        sttmnt = select(Result).order_by(Result.s_name.asc())
        for result in session.scalars(sttmnt):
            results.append(result)
    return results


def get_places():
    places = []
    with Session(engine) as session:
        sttmnt = select(Place).order_by(Place.s_name.asc())
        for place in session.scalars(sttmnt):
            places.append(place)
    return places


def get_locates():
    locates = []
    with Session(engine) as session:
        sttmnt = select(Locate).order_by(Locate.s_name.asc())
        for locate in session.scalars(sttmnt):
            locates.append(locate)
    return locates

from fastapi import APIRouter
from schemas import OurTeamModel, StatusModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status, Depends
from db.models import Comments, Users, OurTeam, Status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT


team_router = APIRouter(prefix="/team")
session = Session(bind=ENGINE)


@team_router.get("/")
def get_all_teams(Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    data = session.query(OurTeam).all()
    return jsonable_encoder(data)


@team_router.post("/create")
def create_team(team: OurTeamModel, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if exist_user.is_staff:
        user = session.query(Users).filter(Users.id == team.employee_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
        statuse = session.query(Status).filter(Status.id == team.status_id).first()
        if not statuse:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the status does not exist")
        new_team = OurTeam(
            employee_id=team.employee_id,
            photo=team.photo,
            status_id=team.status_id
        )
        session.add(new_team)
        session.commit()
        session.refresh(new_team)
        return HTTPException(status_code=status.HTTP_201_CREATED, detail="successful")


@team_router.get("/{id}")
def get_employee(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    employee = session.query(OurTeam).filter(OurTeam.id == id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The employee does not exist")
    return jsonable_encoder(employee)


@team_router.put("/{id}")
def update_employee(id: int, team: OurTeamModel, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    employee = session.query(OurTeam).filter(OurTeam.id == id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the employee does not exist")
    employee.employee_id = team.employee_id
    employee.status_id = team.status_id
    employee.photo = team.photo
    session.commit()
    return jsonable_encoder(employee)

@team_router.delete("/{id}")
async def delete_employee(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    exist_employee = session.query(OurTeam).filter(OurTeam.id == id).first()
    if not exist_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the employee does not exist")
    session.delete(exist_employee)
    session.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="successful deleted")

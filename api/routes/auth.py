from fastapi import APIRouter

router = APIRouter()

# Add authentication endpoints here
@router.post("/login/")
def login():
    return {"message": "Login endpoint (to be implemented)"}

@router.post("/register/")
def register():
    return {"message": "Register endpoint (to be implemented)"}

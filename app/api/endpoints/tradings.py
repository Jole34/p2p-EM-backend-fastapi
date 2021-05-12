from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from app import db

from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from datetime import datetime, timedelta
import schemas
import crud
from db.session import SessionLocal
from settings.common import verify_token  
from models import User
import traceback
import re

router = APIRouter()


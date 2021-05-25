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

@router.get('/user-me/', response_model=schemas.UserOutput)
def get_user_me(user: User = Depends(verify_token)):
    return user

@router.post('/create-user/', response_model=schemas.UserOutput)
def create_user(user: schemas.User) -> Any:
        if user.role_id_1 == 0 and user.role_id_2 == 0 and user.role_id_3:
            raise HTTPException(
                status_code=400,
                detail="Invalid role IDS"
            )              

        if user.role_id_1 > 4  or user.role_id_2 > 4 or user.role_id_3 > 4:
            raise HTTPException(
                status_code=400,
                detail="Invalid role"
            )       
        
        if len(user.password) < 8:
            raise HTTPException(
                status_code=400,
                detail="Short password"
            )             

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", user.email):
            raise HTTPException(
                status_code=400,
                detail="Not a valid email."
            )           
        db = SessionLocal()
        user = crud.user.create(db, obj_in=user)
        db.close()
        if not user:
            raise HTTPException(
                status_code=400,
                detail="Invalid data"
            )
        return user

@router.put('/balance/')
def update_user_balance(user: User = Depends(verify_token), balance: schemas.Balance = None):
        db = SessionLocal()
        balance_update = crud.billing.get_billing_by_user_id(db, user.id)
       
        if not balance_update:
            raise HTTPException(
                status_code=400,
                detail="Invalid data"
            )
        

        balance_update.money_amount = balance.money_amount+balance.money_amount
        updated = crud.billing.update(db, balance_update)
        db.close()

        if not updated:
            raise HTTPException(
                status_code=400,
                detail="Error while adding balance."
            )
        return balance_update.money_amount

@router.post('/billing/')
def create_user_billing(user: User = Depends(verify_token), billing: schemas.Billing = None):
        db = SessionLocal()
        obj_in = billing
        countries = ['Afghanistan', 'Åland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia (Plurinational State of)', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'United States Minor Outlying Islands', 'Virgin Islands (British)', 'Virgin Islands (U.S.)', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cabo Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo (Democratic Republic of the)', 'Cook Islands', 'Costa Rica', 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', "Côte d'Ivoire", 'Iran (Islamic Republic of)', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'North Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia (Federated States of)', 'Moldova (Republic of)', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', "Korea (Democratic People's Republic of)", 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine, State of', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Korea (Republic of)', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom of Great Britain and Northern Ireland', 'United States of America', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela (Bolivarian Republic of)', 'Viet Nam', 'Wallis and Futuna', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']
        
        if billing.country not in countries:
            raise HTTPException(
                status_code=400,
                detail="Invalid data, there is no country like that."
            )
        if not billing.address_line or not billing.city or not billing.country or not billing.zip_code:
            raise HTTPException(
                status_code=400,
                detail="All values most be populated."
            )                    
              
        biling_obj = schemas.BillingIn(
            address_line=billing.address_line,
            city=billing.city,
            country=billing.country,
            zip_code=billing.zip_code,
            user_id=user.id
        )
        billing_update = crud.billing.create(db, obj_in=biling_obj)
        db.close()
        if not billing_update:
            raise HTTPException(
                status_code=400,
                detail="Invalid data"
            )
        return billing_update

@router.get('/billing/')
def get_billing(user: User = Depends(verify_token)):
        db = SessionLocal()
        billing = crud.billing.get_billing_by_user_id(db, user.id)
        db.close()
        if not billing:
            raise HTTPException(
                status_code=404,
                detail="Not found"
            )
        return billing

@router.get('/balance/')
def get_balance(user: User = Depends(verify_token)):
        db = SessionLocal()
        billing = crud.billing.get_balance_by_user_id(db, user.id)
        db.close()
        if not billing:
            raise HTTPException(
                status_code=404,
                detail="Not found"
            )
        return {'money': billing.money_amount, 'energy': billing.energy_amount}

@router.post('/billing/update/')
def update_billing(user: User = Depends(verify_token), billing: schemas.BillingUpdate = None):
        db = SessionLocal()
        billing_db = crud.billing.get_billing_by_user_id(db, user.id)
        if not billing_db:
            raise HTTPException(
                status_code=404,
                detail="Not found"
            )
            
        if billing.address_line:
           billing_db.addres=billing.address_line
        if billing.city:
           billing_db.city=billing.city
        if billing.country:
           billing_db.country=billing.country
        if billing.zip_code:
           billing_db.zip_code=billing.zip_code        
        if billing.zip_code:
           billing_db.zip_code=billing.zip_code    
        if billing.discount:
           billing_db.discount=billing.discount 
        if billing.energy_amount:
           billing_db.discount=billing.energy_amount 
        if billing.money_amount:
           billing_db.discount=billing.money_amount
            
        updated = crud.billing.update(db, billing_db)
        if not updated:
            raise HTTPException(
                status_code=400,
                detail="Update error"
            )
        db.close()
        return updated


@router.put('/energy-balance/')
def update_energy_balance(user: User = Depends(verify_token), balance: schemas.BalanceEnergy = None):
        db = SessionLocal()
        balance_update = crud.billing.get_billing_by_user_id(db, user.id)
       
        if not balance_update:
            raise HTTPException(
                status_code=400,
                detail="Invalid data"
            )
       
        balance_update.energy_amount = balance.energy_amount+balance_update.energy_amount
        updated = crud.billing.update(db, balance_update)
        db.close()

        if not updated:
            raise HTTPException(
                status_code=400,
                detail="Error while adding balance."
            )
        return balance_update.energy_amount
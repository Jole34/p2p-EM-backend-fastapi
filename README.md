# p2p-energy-backend-fastapi

# To install all requirements:
pip install -r requirments-dev.txt

## Additional info:
    Alembic used for automatic migrations
    Postgres db on local/production
    
## To run on local:
    uvicorn main:app --reload --app-dir app
## Run alembic migrations
    alembic revision --autogenerate -m "Migration message"
    alembic upgrade head
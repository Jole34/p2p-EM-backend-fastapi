# p2p-energy-backend-fastapi
    Create local python env
# To install all requirements:
    pip install -r requirements-dev.txt
    pip install -r requirements.txt

## Additional info:
    Alembic used for automatic migrations
    Postgres db on local/production
    
## To run on local:
    uvicorn main:app --reload --app-dir app (running on port 800)
## Run alembic migrations
    alembic revision --autogenerate -m "Migration message"
    alembic upgrade head
    DB for local localhost else ec2-54-74-156-137.eu-west-1.compute.amazonaws.com
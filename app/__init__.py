from app.models.base import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine) 
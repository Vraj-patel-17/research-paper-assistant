from database import Base,engine
from models.user import User
from models.paper import Paper
Base.metadata.create_all(bind=engine)
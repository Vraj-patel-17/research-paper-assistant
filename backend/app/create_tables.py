from app.database import Base,engine
from app.models.user import User
from app.models.paper import Paper
from app.models.bookmark import Bookmark
Base.metadata.create_all(bind=engine)
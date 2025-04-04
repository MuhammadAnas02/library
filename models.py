from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, LargeBinary, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///library.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

book_borrowers = Table(
    'book_borrowers',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    uploaded_books = relationship("Book", back_populates="uploader", foreign_keys="Book.uploader_user_id")
    borrowed_books = relationship("Book", secondary=book_borrowers, back_populates="borrowers")
    managed_members = relationship("Member", back_populates="managing_user")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)
    pdf_filename = Column(String, nullable=True)
    pdf_data = Column(LargeBinary, nullable=True)
    uploader_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploader = relationship("User", back_populates="uploaded_books", foreign_keys=[uploader_user_id])
    borrowers = relationship("User", secondary=book_borrowers, back_populates="borrowed_books")

class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    managing_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    managing_user = relationship("User", back_populates="managed_members")

Base.metadata.create_all(engine)

def get_all_books():
    try:
        books = session.query(Book).all()
        return books
    except Exception as e:
        print(f"Error fetching books: {e}")
        return []

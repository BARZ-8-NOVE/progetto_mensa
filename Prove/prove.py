from sqlalchemy import create_engine,MetaData, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from BackEnd.Classi.ClasseDB.config import DATABASE_URI

meta = MetaData
from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Define naming convention for foreign keys and constraints
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

# Use the updated Base with metadata
Base = declarative_base(metadata=metadata)

# Define an explicit association table for many-to-many relationship
dev_company_association = Table(
    "dev_company_association",
    Base.metadata,
    Column("dev_id", Integer, ForeignKey("devs.id"), primary_key=True),
    Column("company_id", Integer, ForeignKey("companies.id"), primary_key=True),
)

# Freebie Model (Entity Table, not a pure association table)
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    # Define relationships
    dev = relationship("Dev", back_populates="freebies")
    company = relationship("Company", back_populates="freebies")

# Company Model
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    founding_year = Column(Integer, nullable=False)

    freebies = relationship("Freebie", back_populates="company")
    
    # Corrected many-to-many relationship
    devs = relationship(
        "Dev",
        secondary=dev_company_association,
        back_populates="companies"
    )

# Developer Model
class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    freebies = relationship("Freebie", back_populates="dev")
    
    # Corrected many-to-many relationship
    companies = relationship(
        "Company",
        secondary=dev_company_association,
        back_populates="devs"
    )

# Set up database connection
engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()  # Create a session instance

# Ensure `session` is available for import
__all__ = ["Company", "Dev", "Freebie", "session"]

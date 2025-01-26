from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    custom_groups_permissions = relationship('CustomGroupPermission', back_populates='permission')

    def __repr__(self):
        return f"<Permission(id={self.id}, name={self.name})>"


class CustomGroup(Base):
    __tablename__ = 'custom_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    custom_groups_permissions = relationship('CustomGroupPermission', back_populates='custom_group')
    users = relationship('User', back_populates='custom_group')

    def __repr__(self):
        return f"<CustomGroup(id={self.id}, name={self.name})>"


class CustomGroupPermission(Base):
    __tablename__ = 'custom_group_permission'

    id = Column(Integer, primary_key=True)
    custom_group_id = Column(Integer, ForeignKey('custom_groups.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False)

    custom_group = relationship('CustomGroup', back_populates='custom_groups_permissions')
    permission = relationship('Permission', back_populates='custom_groups_permissions')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    employee_number = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    creation_date = Column(DateTime, default=func.now())

    clients = relationship('Client', back_populates='sales_contact')
    events = relationship('Event', back_populates='support_contact')

    custom_group_id = Column(Integer, ForeignKey('custom_groups.id'))
    custom_group = relationship('CustomGroup', back_populates='users')

    def get_permissions(self, session):
        if not self.custom_group:
            return []

        permissions = session.query(Permission).join(CustomGroupPermission).filter(
            CustomGroupPermission.custom_group_id == self.custom_group_id
        ).all()

        return [permission.name for permission in permissions]

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, first_name={self.first_name}, last_name={self.last_name})>"


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    company_name = Column(String(100), nullable=False)
    creation_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())

    contracts = relationship('Contract', back_populates='client')

    sales_contact_id = Column(Integer, ForeignKey('users.id'))
    sales_contact = relationship('User', back_populates='clients')

    def __repr__(self):
        return f"<Client(id={self.id}, email={self.email}, company_name={self.company_name})>"


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    contract_number = Column(String(50), unique=True, nullable=False)
    total_amount = Column(Integer, nullable=False)
    remaining_amount = Column(Integer, nullable=False)
    creation_date = Column(DateTime, default=func.now())
    is_signed = Column(Boolean, default=False)

    events = relationship('Event', back_populates='contract')

    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship('Client', back_populates='contracts')

    def __repr__(self):
        return f"<Contract(id={self.id}, contract_number={self.contract_number}, total_amount={self.total_amount})>"


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=True)
    attendees = Column(Integer, nullable=False)
    notes = Column(String(500), nullable=True)

    contract_id = Column(Integer, ForeignKey('contracts.id'))
    contract = relationship('Contract', back_populates='events')

    support_contact_id = Column(Integer, ForeignKey('users.id'))
    support_contact = relationship('User', back_populates='events')

    def __repr__(self):
        return f"<Event(id={self.id}, name={self.name}, date_start={self.date_start})>"




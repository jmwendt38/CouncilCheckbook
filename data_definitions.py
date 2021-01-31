from sqlalchemy import Table, Column, Integer, Numeric, String, Boolean, Date
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

conn_string = r'sqlite:///test.db'
Base = declarative_base()

class Payee(Base):
    __tablename__ = 'payees'
    payee_name = Column(String(50))
    address_1 = Column(String(50), nullable=False)
    address_2 = Column(String(50), nullable=True)
    address_3 = Column(String(50), nullable=True)
    active = Column(Boolean, default=True)
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return "Payee(payee_name='{self.payee_name}', " \
               "address_1='{self.address_1}'," \
               "address_2='{self.address_2}'," \
               "address_3='{self.address_3}'".format(self=self)

"""
check status is 'outstanding, 'paid', 'void'
"""
class Check(Base):
    __tablename__ = 'checks'

    def __init__(self, check_as_dict):
        self.check_id = check_as_dict['check_number']
        self.check_number = check_as_dict['check_number']
        self.check_date = check_as_dict['check_date']
        self.payee_name = check_as_dict['payee_name']
        self.address_1 = check_as_dict['address_1']
        self.address_2 = check_as_dict['address_2']
        self.address_3 = check_as_dict['address_3']
        self.amount = check_as_dict['amount']
        self.memo = check_as_dict['memo']
        self.fund = check_as_dict['fund']
        self.status = 'outstanding'

    check_id = Column(Integer(), primary_key=True)
    check_number = Column(Integer())
    check_date = Column(Date, nullable=False)
    payee_name = Column(String(50), nullable=False)
    address_1 = Column(String(50), nullable=True)
    address_2 = Column(String(50), nullable=True)
    address_3 = Column(String(50), nullable=True)
    amount = Column(Integer(), nullable=False)
    fund = Column(String(10), nullable=False)
    memo = Column(String(50), nullable=False)
    paid_date = Column(Date, nullable=True)
    status = Column(String(15))

    def __str__(self):
        return 'ID = {} {} {} {} {} {} Paid {}'.format(self.check_id, self.check_number, self.payee_name, self.amount,self.fund, self.memo, self.paid_date)

"""
fund is 'council', 'yyyy' for EAF year
"""
class Balance(Base):
    __tablename__ = 'balances'

    def __init__(self, fund, amount):
        self.fund = fund
        self.amount = amount

    fund = Column(String(7), primary_key=True)
    amount = Column(Integer(), nullable=False)

class Deposit(Base):
    __tablename__ = 'deposits'

    def __init__(self, date, amount):
        self.date = date
        self.amount = amount

    id = Column(Integer(), primary_key=True)
    date = Column(Date)
    amount = Column(Integer)

class DataAccessLayer:
    def __init__(self):
        self.engine = None
        self.session = None
        self.conn_string = r'sqlite:///test.db'

    def connect(self, conn_string):
        self.engine = create_engine(conn_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

dal = DataAccessLayer()

if __name__ == "__main__":
    pass
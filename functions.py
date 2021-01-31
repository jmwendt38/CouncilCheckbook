from data_definitions import Payee, Check, Balance, dal
from sqlalchemy import func

from decimal import Decimal
# from checks_as_pdf import checks_as_pdf
# from currency import *
from num2words import num2words


def add_payee(payee_name, address_1, address_2, address_3):
    p = Payee(payee_name=payee_name, address_1=address_1, address_2=address_2, address_3=address_3, active=True)
    this_session = dal.session
    this_session.add(p)
    this_session.commit()


def get_payee_names():
    n = dal.session.query(Payee.payee_name).all()
    list = []
    for name in n:
        #       print(name[0])
        list.append(name[0])

    return list


def get_payee_by_name(input_name):
    p = dal.session.query(Payee).filter(Payee.payee_name == input_name).first()
    return p

# Checks that have not been assigned a printed number (<= 3000)
def get_unnumbered_checks():
    cks = dal.session.query(Check.check_id, Check.check_number, Check.payee_name, Check.amount).filter(Check.check_number < 2000).all()
    return cks

"""
def new_check(check_number, check_date, payee_name, address_1, address_2, address_3, amount, memo, fund):

"""
def new_check(check_as_dict, to_pdf=True):
    print(f'Write to disk {check_as_dict}')
    ck = Check(check_as_dict)
    this_session = dal.session
    this_session.add(ck)
    this_session.commit()

    # format check elements as text for printing
    if to_pdf:
        # Format things
        # dollars = check_as_dict["amount"]/100
        # cents = checks_as_pdf["amount"] - dollars
        # check_as_dict['words'] = dollars_to_words(dollars, cents)
        # check_as_dict["dollar_amount"] = 'TBD'
        # check_as_dict["words"] = 'TBD'

        # Print the check
        the_list = []
        the_list.append(check_as_dict)
        p_name = check_as_dict['payee_name']
        p_name = p_name.replace(' ', '_')
        the_file_name = r"C:\Users\John M. Wendt\Documents\Checks_WVN\{}_{}.pdf".format(
            check_as_dict['check_date'].isoformat(), p_name)
        print('File name is {}'.format(the_file_name))
        print(the_list)
        if to_pdf:
            checks_as_pdf(the_list, the_file_name)


def get_check_by_number(check_number):
    ck = dal.session.query(Check).filter(Check.check_number == check_number).first()
    return ck


def get_check_by_id(id):
    ck = dal.session.query(Check).filter(Check.check_id == id).first()
    return ck


def total_by_fund(target_fund):
    total = dal.session.query(func.sum(Check.amount)).filter_by(fund=target_fund).scalar()
    if total == None:
        total = Decimal(0.0)
    return total


def get_status_of_a_check(check_number):
    ck = dal.session.query(Check).filter(Check.check_number == check_number).first()
    return ck.status


def set_status_of_a_check(check_number, new_status):
    session = dal.session
    q = session.query(Check)
    q = q.filter(Check.check_number == check_number)

    if q != None:
        q.update({Check.status: new_status})
        session.commit()


def set_check_number(the_id, new_number):
    session = dal.session
    q = session.query(Check)
    q = q.filter(Check.check_id == the_id)

    if q != None:
        q.update({Check.check_number: new_number})
        session.commit()

def set_check_paid_date(check_number, paid_date):
    session = dal.session
    q = session.query(Check)
    q = q.filter(Check.check_number == check_number)

    if q != None:
        q.update({Check.paid_date: paid_date})
        session.commit()


def total_by_fund_and_status(target_fund, target_status):
    total = dal.session.query(func.sum(Check.amount)).filter_by(fund=target_fund, status=target_status).scalar()
    if total == None:
        total = Decimal(0.0)
    return total


def count_by_fund_and_status(target_fund, status):
    count = dal.session.query([func.count(Check)]).filter_by(fund=target_fund, status=status).scalar()
    if count == 0:
        count = Decimal(0.0)
    return count


"""
123.45 -> 12345
456 or 456. > 45600
"""

def currency_string_as_1nteger(amount):
    pos = amount.find('.')

    if pos < 0: # no decimal point
        return int(amount)

    if pos > 0: #decimal point
        dollars, cents = amount.split('.')
        return int(dollars) * 100 + int(cents)

def format_thousands(amount):
    fmt = "{:,}"
    return fmt.format(amount)

"""
>>> '{:,}'.format(1234567890)
'1,234,567,890'

Input: cents as integer
Returns: String('ddd.cc')
"""


def format_name(name):
    last, first = name.split(', ')
    formatted_name = first + ' ' + last
    return formatted_name
def split_currency(amount_as_cents):
    amount_as_cents = int(amount_as_cents)
    dollars = (int)(amount_as_cents/100)
    cents = amount_as_cents - dollars*100
    return[dollars, cents]

def dollars_to_words(dollars, cents):
    if cents > 0:
        return num2words(dollars).upper().replace('AND ', '') + " AND {}/100".format(cents)
    else:
        return num2words(dollars).upper().replace('AND ', '') + " AND 00/100".format(cents)

# from openpyxl import load_workbook
# def excel_to_dicts(file_name, sheet, fund:int, check_date, first_employee, last_employee):
#     workbook = load_workbook(file_name, data_only=True)
#     sheet = workbook[sheet]
#
#     the_list = []
#
#     # column indices
#     CHECK_NUMBER_COLUMN = 1
#     PAYEE_NAME_COLUMN = 2
#     ADDRESS_1_COLUMN = 4
#     AMOUNT_COLUMN = 10
#
#     for j in range(first_employee, last_employee):
#         check_as_dict = {}
#
#         integer_amount = int(sheet.cell(j, AMOUNT_COLUMN).value ) #  As integer dollars
#
#         check_as_dict['check_number'] = sheet.cell(j, CHECK_NUMBER_COLUMN).value
#         check_as_dict['check_id'] = check_as_dict['check_number']
#         check_as_dict['check_date'] = check_date
#         check_as_dict['date_as_characters'] = check_as_dict['check_date'].strftime("%b %d, %Y")
#         check_as_dict['payee_name'] = format_name(sheet.cell(j, PAYEE_NAME_COLUMN).value)
#         check_as_dict['address_1'] = sheet.cell(j, ADDRESS_1_COLUMN).value
#         check_as_dict['address_2'] = ''
#         check_as_dict['address_3'] = ''
#         check_as_dict['amount'] = integer_amount * 100  #Add two zeroes to the amoint
#         s = split_currency(integer_amount)
#         check_as_dict['words'] = dollars_to_words(s[0], s[1])
#         check_as_dict["amount_as_characters"] = format(integer_amount) + '.00'
#         check_as_dict["dollar_amount_as_characters"] = '$' + format(integer_amount ) + '.00'
# #        check_as_dict['words'] = sheet.cell(j, WORDS_COLUMN).value
#         check_as_dict['fund'] = fund
#         check_as_dict['memo'] = 'Employee Appreciation'
#         check_as_dict['status'] = 'outstanding'
#
#         the_list.append(check_as_dict)
#
#     return the_list

def dicts_to_checks(the_dict_list):
    the_check_list = []
    for d in the_dict_list:
        c = Check(d)
        the_check_list.append(c)

    return the_check_list

def save_checks_to_database(the_check_list):
    session = dal.session
    session.bulk_save_objects(the_check_list)
    session.commit()

def get_balance(target_fund):
    this_session = dal.session
    b = this_session.query(Balance).filter(Balance.fund == target_fund).first()
    return b.amount

def add_to_balance(target_fund, amount_added):
    session = dal.session
    query = session.query(Balance)
    current_balance = query.filter(Balance.fund == target_fund).first()
    current_balance.amount = current_balance.amount + amount_added
    session.commit()


def subtract_from_balance(target_fund, amount_subtracted):
    session = dal.session
    query = session.query(Balance)
    current_balance = query.filter(Balance.fund == target_fund).first()
    current_balance.amount = current_balance.amount - amount_subtracted
    session.commit()


def set_balance(target_fund, new_amount):
    session = dal.session
    query = session.query(Balance)
    the_balance = query.filter(Balance.fund == target_fund).first()
    the_balance.amount = new_amount
    session.commit()




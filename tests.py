import pytest
from datetime import date
from data_definitions import Base, Payee, Check, Balance, dal
from functions import *
# from checks_from_sheet import combine_spreadsheet_pages, checks_from_spreadsheet
#
# from read_html import get_check_numbers_from_html
# from currency import *


@pytest.fixture
def setup():
    conn_string = r'sqlite:///test2.db'
    dal.connect(conn_string)
    session = dal.session

    add_payee(payee_name='Loren Ipsum', address_1='76 Wistful Vista', address_2='', address_3='')
    add_payee(payee_name='Dolores Set Amet', address_1='5 Main St.', address_2='Cicero IN', address_3='')
    add_payee(payee_name='Qualis Non Sum', address_1='5 Main St.', address_2='Cicero IN', address_3='')

    # file_name = r"C:\Users\John M. Wendt\Documents\WVN_Council\EAF\2019\EAF_2019_Working\EAF_2019_Working.xlsx"
    # the_dict_file = excel_to_dicts(file_name, 'Test Sheet', '2019', date(2019, 12, 13), 2, 304)
    # the_check_list = dicts_to_checks(the_dict_file)
    # save_checks_to_database(the_check_list)

    try:
        a_new_balance = Balance(fund='council', amount=12000)
        session.add(a_new_balance)
        session.commit()
    except:
        e =""

    yield

    # Teardown
    session = dal.session
    Base.metadata.drop_all(bind=dal.engine)
    session.commit()

def test_payee(setup):
    names = get_payee_names()
    the_name = names[0]
    assert the_name == "Loren Ipsum"

def test_payee_by_name(setup):
    p = get_payee_by_name('Loren Ipsum')
    assert p.address_1 == '76 Wistful Vista'

# 03
def test_get_check_by_id(setup):
    ck = get_check_by_id(12)
    assert ck.check_number == 3182
    ck = get_check_by_id(190)
    assert ck.check_number == 3360

# 04
def test_check_data(setup):
    ck = get_check_by_number(3453)
    assert ck.payee_name == 'Steven Shaw'

# 05
def test_add_eaf(setup):
    #   file_name = r"C:\Users\John M. Wendt\Documents\EAF_2019\EAF_2019_Working\EAF_2019_Working.xlsm"
    #  excel_to_db(file_name, 'Test Sheet', '2019', date(2019, 12, 13), 2, 304)
    ck = get_check_by_number(3175)
    assert ck.payee_name == 'Sharon Rowland'
    assert ck.fund == '2019'

# 06
def test_sum_by_fund_db(setup):
    s = total_by_fund('2019')
    assert s == 6988000

# 07
def test_change_status(setup):
    s = get_status_of_a_check(3456)
    assert s == 'outstanding'
    set_status_of_a_check(3456, 'paid')
    #    ck = dal.session.query(Check).filter(Check.check_number==3456).first()
    s = get_status_of_a_check(3456)
    assert s == 'paid'

# 08
def test_total_by_fund_and_status(setup):
    set_status_of_a_check(3456, 'paid')
    set_status_of_a_check(3459, 'paid')
    t = total_by_fund_and_status('2019', 'outstanding')
    assert t == 6927000

# 09
def test_missing_check(setup):
    ck = get_check_by_number(5000)
    assert ck == None

#10
def test_empty_fund(setup):
    t = total_by_fund(1000)
    assert t == 0

#11
def test_change_nonexistent_check(setup):
    set_status_of_a_check(9000, 'x')

#12
def test_check_paid_date():
    pass

#13
# def test_paid_checks_from_html(setup):
#     the_list = get_check_numbers_from_html()
#     n = len(the_list)
#     tot = total_by_fund_and_status('2019', 'paid')
#     tot2 = total_by_fund_and_status('2019', 'outstanding')
#     #    m = count_by_fund_and_status('2019','paid')
#     assert tot == 6000000  # Some unnumbered in bank html?
#     assert tot2 == 988000
#     assert n == 243
#
# #14
# def test_check_paid_date(setup):
#     ck1 = get_check_by_number(3425)
#     ck2 = get_check_by_number(3195)
#
#     get_check_numbers_from_html()
#     assert ck1.paid_date == date(2019, 12, 19)
#     assert ck2.paid_date == date(2019, 12, 16)
#
# #15
# def test_set_check_number(setup):
#     ck = get_check_by_number(3175)
#     id = ck.check_id
#     print(id)
#     set_check_number(id, 5678)
#     ck1 = get_check_by_number(5678)
#     assert ck1.payee_name == 'Sharon Rowland'
#
# #16
# def test_string_to_currency(setup):
#     c = string_to_currency('316.48')
#     assert c == 31648
#
#     c = string_to_currency('456')
#     assert c == 45600
#
#     c = string_to_currency('456.')
#     assert c == 45600
#
# #17
# def test_currency_to_string(setup):
#     s = currency_to_string(567356)
#     assert s == '5,673.56'
#
# #18
# def test_cents_to_decimal(setup):
#     dec = cents_to_decimal(1298)
#     assert dec['dollars'] == '12'
#     assert dec['cents'] == '98'
#     assert dec['decimal'] == '12.98'
# #19
# def test_get_balance(setup):
#     set_balance('council', 27000)
#     b = get_balance('council')
#     assert b == 27000
#
# #20
# def test_set_balance(setup):
#     set_balance('council', 25000)
#     b = get_balance('council')
#     assert b == 25000
#
# def test_add_to_balance(setup):
#     set_balance('council', 22000)
#     add_to_balance('council', 4000)
#     b = get_balance('council')
#     assert b == 26000
#
# def test_subtract_from_balance(setup):
#     set_balance('council', 22000)
#     subtract_from_balance('council', 4000)
#     b = get_balance('council')
#     assert b == 18000
#
# def test_format_thousands(setup):
#     str = format_thousands(12345)
#     assert str == '12,345'

#def test_checks_from_spreadsheet():
#    checks_from_spreadsheet()




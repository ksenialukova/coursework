import cx_Oracle
import config
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
from fpdf import FPDF

# add_user             insert update  +
# check_user           select         +
# set_state                           +
# get_current_state                   +
# temp_table_expense                  +
# add_expense                         +
# drop_table           drop           +


def add_user(user_id, first_name, last_name, username):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                if check_user(cur, user_id):
                    cur.execute('update Users set state = 0 where id = {0}'.format(user_id))
                    print('Update {}'.format(username))
                else:
                    cur.execute('insert into Users values ({0}, {1}, \'{2}\', \'{3}\', \'{4}\')'.format(str(user_id),
                                                                                                        config.State.S_START, first_name, last_name, username))
                    print('Add new user: {}'.format(username))
                con.commit()
                pass
            except cx_Oracle.IntegrityError:
                print("Start error by {}".format(username))


def check_user(cur, user_id):
    u = cur.execute('select id from Users').fetchall()
    for i in u:
        if user_id in i:
            return True
    return False


def get_current_state(user_id):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                cur.execute('select state from users where id={}'.format(user_id))
                state = cur.fetchall()[0][0]
            except IndexError:
                state = config.State.S_START
    return state


def set_state(user_id, value, username):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                cur.execute('update Users set state = {0} where id = {1}'.format(value, user_id))
                con.commit()
                print("Update state {}".format(username))
                return True
            except cx_Oracle.IntegrityError:
                return False


def drop_table(user_id):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                cur.execute('drop table TMP_T{}'.format(user_id))
                con.commit()
            except:
                print("Error")


def add_expense(user_id, price):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                ex_type = cur.execute('select type from TMP_T{}'.format(user_id)).fetchall()[0][0]
                date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                cur.execute('insert into Outcome values (outcome_seq.nextval, TO_DATE(\'{0}\', \'dd.mm.yy hh24:mi:ss\'),{1}, {2}, {3})'
                            .format(date, ex_type, user_id, price))
                cur.execute('drop table TMP_T{}'.format(user_id))
                con.commit()
            except cx_Oracle.IntegrityError:
                print("Error")


def temp_table_expense(user_id, ex_type):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                cur.execute('''CREATE TABLE TMP_T{}     
                               (
                               ID NUMBER,
                               TYPE NUMBER       
                               )'''.format(user_id))

            except cx_Oracle.IntegrityError:
                print("Error")
            finally:
                cur.execute('insert into TMP_T{0} values({0}, {1})'.format(user_id, get_type_expense_id(ex_type)))
                con.commit()


def get_type_expense_id(type_expense):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                type_id = cur.execute('select id from Outcometype where name = \'{}\''.format(str(type_expense).upper())).fetchall()[0][0]
                return type_id
            except cx_Oracle.IntegrityError:
                return False


def temp_table_income(user_id, in_type):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                cur.execute('''CREATE TABLE TMP_T{}     
                               (
                               ID NUMBER,
                               TYPE NUMBER       
                               )'''.format(user_id))

            except cx_Oracle.IntegrityError:
                print("Error")
            finally:
                cur.execute('insert into TMP_T{0} values({0}, {1})'.format(user_id, get_type_income_id(in_type)))
                con.commit()


def get_type_income_id(type_income):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                type_id = cur.execute('select id from Incometype where name = \'{}\''.format(str(type_income).upper())).fetchall()[0][0]
                return type_id
            except cx_Oracle.IntegrityError:
                return False


def add_income(user_id, price):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                in_type = cur.execute('select type from TMP_T{}'.format(user_id)).fetchall()[0][0]
                date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                cur.execute('insert into Income values (income_seq.nextval, TO_DATE(\'{0}\', \'dd.mm.yy hh24:mi:ss\'),{1}, {2}, {3})'
                            .format(date, in_type, user_id, price))
                cur.execute('drop table TMP_T{}'.format(user_id))
                con.commit()
            except cx_Oracle.IntegrityError:
                print("Error")


def del_info(user_id):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                cur.execute('delete from users where id={}'.format(user_id))
            except:
                print('Error')

            try:
                cur.execute('delete from outcome where user_id={}'.format(user_id))
            except:
                print('Error')

            try:
                cur.execute('delete from income where user_id={}'.format(user_id))
            except:
                print('Error')

            try:
                cur.execute('delete from broarderprice where user_id={}'.format(user_id))
            except:
                print('Error')

            con.commit()


def add_board(user_id, price):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                ex_type = cur.execute('select type from TMP_T{}'.format(user_id)).fetchall()[0][0]
                cur.execute('insert into Boarderprice values (boarderprice_seq.nextval,{0}, {1}, {2})'
                            .format(ex_type, user_id, price))
                cur.execute('drop table TMP_T{}'.format(user_id))
                con.commit()
            except cx_Oracle.IntegrityError:
                print("Error")


def print_board(user_id):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                res = cur.execute('select name, price from BoarderPrice inner join OutcomeType on BoarderPrice.type_id = OutcomeType.ID where user_id = {}'.format(user_id)).fetchall()
                return res
            except cx_Oracle.IntegrityError:
                print("Error")
                return


def income_stat(user_id):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                res = cur.execute('select name, p.v from (select type_id, sum(price) v from Income where user_id={} group by type_id) p inner join IncomeType on IncomeType.ID = p.type_id'.format(user_id)).fetchall()
                return res
            except cx_Oracle.IntegrityError:
                print("Error")
                return


def outcome_stat(user_id):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                res = cur.execute('''select name, p.v
from
     (select type_id, sum(price) v
from Outcome
where user_id={0}
group by type_id) p inner join OutcomeType on OutcomeType.ID = p.type_id'''.format(user_id)).fetchall()
                return res
            except cx_Oracle.IntegrityError:
                print("Error")
                return


def statpdf1(user_id):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                res = cur.execute('''select OutcomeType.NAME, p.v
from
     (SELECT distinct type_id, user_id, AVG(price) OVER (partition by type_id, user_id) v FROM Outcome
where user_id = {}) p inner join OutcomeType on OutcomeType.ID = p.type_id'''.format(user_id)).fetchall()
                return res
            except cx_Oracle.IntegrityError:
                print("Error")
                return False


def statpdf2(user_id):
    with cx_Oracle.connect(user='botdb', password='botdb') as con:
        with con.cursor() as cur:
            try:
                res = cur.execute('''select OutcomeType.NAME, p.t
from
     (SELECT type_id, RATIO_TO_REPORT(v) OVER (partition by user_id) t
FROM
     (SELECT distinct type_id, user_id, sum(price) OVER (partition by user_id, type_id) v FROM Outcome
where user_id = {})) p inner join OutcomeType on OutcomeType.ID = p.type_id'''.format(user_id)).fetchall()
                return res
            except cx_Oracle.IntegrityError:
                print("Error")
                return False

def createPDF(user_id):
    data_values = []
    data_names = []

    pdf = FPDF(orientation='P', format='A4')
    pdf.set_font("Arial", size=20)
    pdf.add_page()
    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    pdf.cell(col_width, row_height, txt='Financial report(outcome)')
    pdf.ln(2*row_height)
    pdf.set_font("Arial", size=15)

    if statpdf1(user_id):
        pdf.cell(col_width, row_height, txt='Average by every item')
        pdf.ln(2*row_height)
        pdf.set_font("Arial", size=8)
        res = statpdf1(user_id)
        for i in res:
            name, val = i
            val = round(float(val), 1)
            pdf.cell(50, row_height, txt=name)
            pdf.cell(20, row_height, txt=str(val))
            pdf.ln(row_height)

    pdf.ln(2*row_height)

    if statpdf2(user_id):
        pdf.set_font("Arial", size=15)
        pdf.cell(col_width, row_height, txt='Ratio by every item')
        pdf.ln(2*row_height)
        pdf.set_font("Arial", size=8)
        res = statpdf2(user_id)
        print(res)
        for i in res:
            name, val = i
            val = round(float(val), 3)
            pdf.cell(50, row_height, txt=name)
            pdf.cell(20, row_height, txt=str(val))
            pdf.ln(row_height)
            data_values.append(val)
            data_names.append(name)


    mpl.rcParams.update({'font.size': 9})
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    plt.title('')
    plt.pie(
        data_values, autopct='%.1f', radius=1.1,
        explode=[0.15] + [0 for _ in range(len(data_names) - 1)])

    plt.legend(
        bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
        loc='lower left', labels=data_names)

    fig.savefig('pie.png')
    pdf.image('pie.png')
    pdf.output('report{}.pdf'.format(user_id))

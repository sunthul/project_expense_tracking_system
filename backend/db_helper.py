from backend.logging_setup import setup_logger
import mysql.connector
from contextlib import contextmanager

logger = setup_logger(__name__, r'backend\server.log')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='expense_manager'
    )

    if connection.is_connected():
        logger.info('Connection Successful')
    else:
        logger.error('Connection Failed')

    cursor = connection.cursor(dictionary=True)

    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def fetch_all_record():
    try:
        with get_db_cursor() as cursor:
            cursor.execute('SELECT * FROM expenses')
            expenses = cursor.fetchall()
            return expenses
    except Exception as e:
        logger.error(f"Error in fetch_all_record: {e}")
        return None

def fetch_expenses_for_date(expense_date):
    logger.info(f'fetch_expenses_for_date called with {expense_date}')

    try:
        with get_db_cursor() as cursor:
            cursor.execute('SELECT * FROM expenses WHERE expense_date = %s', (expense_date,))
            expenses = cursor.fetchall()
            return expenses
    except Exception as e:
        logger.error(f"Error in fetch_expenses_for_date: {e}")
        return None

def insert_expense(expense_date, amount, category, notes=None):
    logger.info(f'insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}')

    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute('INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s,%s,%s,%s)',
                           (expense_date, amount, category, notes))
    except Exception as e:
        logger.error(f'Error in insert_expense: {e}')

def delete_expense_for_date(expense_date):
    logger.info(f'delete_expense_for_date called with {expense_date}')

    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute('DELETE FROM expenses WHERE expense_date = %s', (expense_date,))
    except Exception as e:
        logger.error(f'Error in delete_expense_for_date: {e}')

def fetch_expenses_by_category_summary(date1, date2):
    logger.info(f'fetch_expenses_by_category_summary called with date1: {date1} and date2: {date2}')

    try:
        with get_db_cursor() as cursor:
            cursor.execute('''SELECT sum(amount) as total, category FROM expenses
                            WHERE expense_date BETWEEN %s AND %s
                            GROUP BY category;''', (date1, date2))
            expenses = cursor.fetchall()
            return expenses
    except Exception as e:
        logger.error(f'Error in fetch_expenses_by_category_summary: {e}')
        return None

def fetch_expenses_by_monthly_summary():
    logger.info(f'fetch_expenses_by_monthly_summary called')

    try:
        with get_db_cursor() as cursor:
            cursor.execute('''SELECT 
                                    DATE_FORMAT(expense_date, '%Y-%m') AS month,
                                    SUM(amount) AS total
                                    FROM 
                                    expenses
                                    GROUP BY 
                                    month
                                    ORDER BY 
                                    month;''',)
            expenses = cursor.fetchall()
            return expenses
    except Exception as e:
        logger.error(f'Error in fetch_expenses_by_monthly_summary: {e}')
        return None
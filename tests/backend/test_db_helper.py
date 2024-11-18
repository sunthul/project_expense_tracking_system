from backend import db_helper

def test_fetch_expense_for_date_aug_15():
    expenses = db_helper.fetch_expense_for_date('2024-08-15')

    assert len(expenses) == 1
    assert expenses[0]['amount'] == 10.0
    assert expenses[0]['category'].lower() == 'shopping'
    assert expenses[0]['id'] == 62

def test_fetch_expense_for_date_invalid_date():
    expenses = db_helper.fetch_expense_for_date('9999-08-15')

    assert len(expenses) == 0

def test_fetch_expenses_summary_invalid_range():
    expenses = db_helper.fetch_expenses_by_category_summary('2024-09-06','2024-09-07')

    assert len(expenses) == 0

from sys import breakpointhook

from fastapi import FastAPI, HTTPException
from datetime import date
from typing import List
from pydantic import BaseModel

from backend import db_helper


class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date:date


app = FastAPI()

@app.get('/expenses/{expense_date}', response_model=List[Expense])
def get_expenses(expense_date: date):
    try:
        expenses = db_helper.fetch_expenses_for_date(expense_date)
        if not expenses:
            raise HTTPException(status_code=404, detail="No expenses found for the given date")
        return expenses
    except Exception as e:
        print(f"Error fetching expenses: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post('/expenses/{expense_date}')
def add_or_update_expense(expense_date: date, expenses:List[Expense]):
    db_helper.delete_expense_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date,
                                expense.amount,
                                expense.category,
                                expense.notes)
    return {"message": "Expenses updated successfully"}


@app.post('/analytics_category/')
def get_analytics(date_range: DateRange):
    data = db_helper.fetch_expenses_by_category_summary(date1=date_range.start_date,
                                     date2=date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500,
                            detail='Failed to retrieve expense summary from the database')

    total = sum([row['total'] for row in data])
    breakdown = {}

    for row in data:
        percentage = (row['total']/total)*100 if total != 0 else 0
        breakdown[row['category']] = {'total':row['total'],
                                      'percentage':percentage}
    return breakdown

@app.get('/analytics_monthly/')
def get_analytics_monthly():
    data = db_helper.fetch_expenses_by_monthly_summary()
    if data is None:
        raise HTTPException(status_code=500,
                            detail='Failed to retrieve expense summary from the database')

    total = sum([row['total'] for row in data])
    breakdown = {}

    for row in data:
        month = row['month']
        amount = row['total']
        percentage = (amount / total) * 100 if total != 0 else 0
        breakdown[month] = {'total': amount, 'percentage': percentage}

    return breakdown

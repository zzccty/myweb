from .models import Category_by_date
import datetime
from . import db

def get_years():
    years = str(datetime.date.today().year) + str(datetime.date.today().month)
    years_instance = Category_by_date(date=years)
    db.session.add(years_instance)
    db.session.commit()
    return years_instance

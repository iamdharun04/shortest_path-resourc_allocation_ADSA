# forms.py

from django import forms
from .models import TouringPlace
import pymysql as mysql

# Database connection details (moved here for simplicity)
db_config = {
    'user': 'root',
    'password': '0000',
    'host': 'localhost',
    'database': 'touring_places_db'
}

def fetch_cities_from_db():
    connection = mysql.connect(user=db_config['user'], password=db_config['password'], host=db_config['host'], database=db_config['database'])
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT city FROM touring_places")
    cities = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return cities

class CityForm(forms.Form):
    city = forms.CharField(label='Select a City', widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CityForm, self).__init__(*args, **kwargs)
        self.fields['city'].widget.choices = [(city, city) for city in fetch_cities_from_db()]

import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('cleaned_hotel_bookings.csv')

engine = create_engine('sqlite:///Hotel_project.db',echo = False)

df.to_sql("Hotel_project",con = engine,index = False,if_exists= "replace")

print("data have successfully loaded.")
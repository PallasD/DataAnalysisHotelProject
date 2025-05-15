
import pandas as pd


df = pd.read_csv('hotel_bookings.csv')
#print(df.shape)

print(df.head()) #taking a picture of the first 5 rows
print(df.info()) # see some basic information for the dataset
print(df.isnull().sum()) # see how many null has the dataset and where

df['children'].fillna(0, inplace = True) # we have only 4 nulls we can apply 0 here.
df['country'].fillna("Unknown", inplace = True) # we have only 488 nulls we can apply for unknown.
df['agent'].fillna(0, inplace = True) # we apply for 0 here because we may use them later.
df['company'].fillna(0, inplace = True) # --\\--

#we have 3 kind of dates so it's better to make it 1 full date.

df['arrival_date'] = pd.to_datetime(
    df['arrival_date_year'].astype(str) + "-" +
    df['arrival_date_month'] + "-" +
    df['arrival_date_day_of_month'].astype(str),
    format = '%Y-%B-%d'
)
# check
print(df[["arrival_date","arrival_date_year","arrival_date_month","arrival_date_day_of_month"]])

#remove the 0 data
df = df[(df['adults'] > 0) | (df['children'] > 0) | (df['babies'] > 0)]

#check
print("bookings with problem:",df[(df['adults'] == 0) & (df['children'] == 0) & (df['babies'] == 0)])


#check for duplicates
print("duplicate lines:" , df.duplicated().sum())

#check the duplicates (I need to take a decision if I will need the data for later or not)
duplicates = df[df.duplicated()]
duplicates.to_csv('duplicates_only.csv',index = False)

#I extract a mini description of the data
describe1 = df.describe(include="all")
describe1.to_csv('describe.csv')

#we need to check the outliers for all the columns

outColCheck = df.select_dtypes(include=['int64','float64']).columns
outliers = pd.DataFrame()
for col in outColCheck:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lowerBound = Q1 - 1.5 * IQR
    upperBound = Q3 + 1.5 * IQR

    outliers1 = df[(df[col] < lowerBound) | (df[col] > upperBound)]
    numOutliers = outliers1.shape[0]
    total = df.shape[0]
    percentage = (numOutliers / total ) * 100

    print(f"Column: {col}")
    print(f"lower accepted bound : {lowerBound:.2f}")
    print(f"upper accepted bound : {upperBound:.2f}")
    print(f"outliers {numOutliers} from total {total} rows ({percentage:.2f}%)\n")

    outliers = pd.concat([outliers, outliers1])
outliers.to_csv('Outliers.csv', index = False)

#we need to remove the entries where adults are 0
df = df[df['adults'] > 0]

df.to_csv('cleaned_hotel_bookings.csv', index = False)
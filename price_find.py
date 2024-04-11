
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas
import itertools
import streamlit as st
#Cash flow — The profit each month after paying everything (mortgage, property management, repair allowances, vacancy expense)
#Cap rate — The net income per year divided by the price of the asset (in percent)
#Cash on cash return rate — Net income per year divided by the down payment used for the asset (in percent)


def net_operating(rent, tax_rate, price):
     #Takes input as monthly mortgage amount and monthly rental amount
    #Uses management expense, amount for repairs, vacancies
    mortgage_amt = mortgage_monthly(price, 20, 3)
    prop_management = rent * 0.10
    prop_tax = (price * (tax_rate/100) / 12)
    prop_repairs = (price * 0.02) / 12
    vacancy = (rent * 0.02)
    #These sections are a list of all the expenses used and formulas for each
    net_income = rent - prop_management - prop_tax - prop_repairs - vacancy - mortgage_amt
    
      #Sum of expenses
    
    output = [prop_management, prop_tax, prop_repairs, vacancy, net_income]
    
    return output

def down_payment(price, percent):
    
#This function takes the price and the downpayment rate and returns the downpayment amount 
    #EX: down_payment(100,20) returns 20
    amt_down = price * (percent/100)
    return amt_down

def mortgage_monthly(price, years, percent):
    
    #This implements an approach to finding a monthly mortgage amount from the purchase price,
    #years and percent. 
    #EX: (300000,20,4) = 2422
    
    percent = percent / 100
    down = down_payment(price, 20)
    loan = price - down
    months = years * 12
    interest_monthly = percent / 12
    interest_plus = interest_monthly + 1
    exponent = (interest_plus) ** (-1 * months)
    subtract = 1 - exponent
    division = interest_monthly / subtract
    payment = division * loan
    
    return payment

def price_mine(url):
    #this function takes an input of a URL and returns the listing prices 
    #The site it mines is remax
    try:
       
        headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'}
        url = 'https://www.remax.com'
        response = get(url, headers=headers)
        response_text = response.text
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the URL. Status code: {response.status_code}")
        
        html_soup = BeautifulSoup(response.text, 'html.parser')
        price_element = html_soup.find('h2', class_='price')
        
        if price_element is None:   
            raise Exception("Price element not found on the webpage.")
        
        price = price_element.text.strip().replace(',', '').replace('$', '').replace(' ', '')
        price = float(price)
        
        return price
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def cap_rate(monthly_income, price):
    #This function takes net income, and price and calculates the cap rate
    cap_rate = ((monthly_income * 12) / price) * 100
    return cap_rate

def cash_on_cash(monthly_income, down_payment):
    
#Net income per year divided by the down payment used for the asset (in percent)
    cash_return = ((monthly_income * 12) / down_payment) * 100
    return cash_return

st.write("""# Real Estate Investment Analysis Tool""")

trial = st.sidebar.text_input("Enter the listing URL: ")
rent_amt = st.sidebar.text_input("Enter the monthly mortgage price: ")
property_tax = st.sidebar.text_input("Enter the tax rate: ")

try:
    rent_amt = float(rent_amt)
    property_tax = float(property_tax)
    listing_notice = price_mine(str(trial))
    
    if listing_notice:
        mortgage = mortgage_monthly(listing_notice, 20, 3)
        cash = down_payment(listing_notice, 20)
        net_income = net_operating(rent_amt, property_tax, listing_notice)
        monthly_cash = net_income[4]
        cap_return = cap_rate(monthly_cash, listing_notice)
        cash_percent = cash_on_cash(monthly_cash, cash)
        
        st.write("The monthly cashflow is: ", monthly_cash)
        st.write("The cap rate is: ", cap_return)
    
except ValueError:
    st.error("Please enter valid numerical values for mortgage price and tax rate.")


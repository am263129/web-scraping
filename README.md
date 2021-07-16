# web-scraping
getting product name, price, ASIN 


This script has basic feature.
import keyword from csv file
and search it from eshop site.
and get product's name, price, ASIN.

using python selenium and bs4.

! download chromedriver and save in project directory to run amazone_selenium.py


# How to run

first, install packages.
you should install python.
download from https://www.python.org/downloads/ and setup.
after install python, you should add python directory to your environment variable.

for example:
	C:\Users\User name\AppData\Local\Programs\Python\Python39
	C:\Users\User name\AppData\Local\Programs\Python\Python39\Scripts

and install pip
follow this link https://pip.pypa.io/en/stable/installing/

after that, install packages from requirements.txt

	pip install requirements.txt

now you are ready.
input keywords to keywords.csv 
and run scripts.
	py amazone_bs.py
	or
	py amazone_selenium.py

this will download product information and save it to products.csv
that's all.	
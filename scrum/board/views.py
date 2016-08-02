from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions, viewsets,filters
from django.shortcuts import render_to_response, render
from .models import Product
from .forms import ProductFilter
from .serializers import ProductSerializer
from django.shortcuts import render_to_response, render
from postgres_copy import CopyMapping
from .models import Product
import csv, json, requests, psycopg2
from bs4 import BeautifulSoup
from itertools import chain
data = []

    
class ProductViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (
            filters.DjangoFilterBackend,
            filters.SearchFilter,
            filters.OrderingFilter,
    )
    filter_class = ProductFilter
    search_fields = ('name','category')
    ordering_fields = ('name', 'price',)


def index(requet):
    return render(requet,'index.html',{})


def web_crawler(requet):
    print "web crawler"
    url = 'http://www.justbake.in/bangalore'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    top = soup.find('div',{'class':'col-lg-12'})
    top_div = top.findAll('div',{'class':'col-lg-2'})
    links = [div.findAll('a') for div in top_div]
    for a in chain.from_iterable(links):
        href = "http://www.justbake.in" + a.get('href')
        # print href
        category = a.string
        # print category
        get_single_item_data(href,category)
    # writing data into json file
    with open('data.json', 'w') as f:
        json.dump(data, f)
    # writing csv from json
    json_to_csv()
    return render(requet,'crawler.html',{})

def get_single_item_data(item_url,category):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    for item_name in soup.findAll('div',{'class':'col-lg-4'}):

        newItem= {}
        newItem['category']=category;

        image_url= item_name.find('div',{'class':'pimg'})
        a = image_url.find('a')
        img = a.find('img')
        newItem['image'] = "http://www.justbake.in/"+ img.get('src')[3:]
        
        cake_name= item_name.find('a',{'class':'black2'})
        newItem['name'] = cake_name.string[4:]
        
        cake_price= item_name.find('div',{'class':'green1'})
        newItem['price'] = int(cake_price.contents[0][16:])
        
        data.append(newItem);

def json_to_csv():
    f = open('data.json')
    data = json.load(f)
    f.close()

    f = csv.writer(open('file.csv', 'wb+'))
    f.writerow(data[0].keys())
    for item in data:
        f.writerow(item.values())



def insertRecords(requet):
    # save the data into model of Django
    c = CopyMapping(
            # Give it the model
            Product,
            # The path to your CSV
            'file.csv',
            # And a dict mapping the  model fields to CSV headers
            dict(category='category', name='name', image='image', price='price')
    )
    # Then save it.
    c.save()

    # save the record into postgresql database 
    conn = psycopg2.connect("dbname='testdb' user='postgres' host='localhost' password='anand1993tiwari'")
    cur = conn.cursor()
    filesource = 'file.csv'
    reader = csv.reader(open(filesource, 'rb'))
    i=0
    
    for row in reader:
        if(i!=0):
            cur.execute("INSERT INTO test_table (category, image, price, name) VALUES(%s, %s, %s, %s)",(row[0],row[1],row[2],row[3]))
        i=1
        conn.commit()
    conn.close()
    
    # used for accesing data from postgresql database
    conn = psycopg2.connect("dbname='testdb' user='postgres' host='localhost' password='anand1993tiwari'")
    cur = conn.cursor()
    cur.execute("""
        select * from test_table
        """)
    results = []
    rows = cur.fetchall()
    for row in rows:
        results.append(row)

    return render(requet,'insert.html',{})
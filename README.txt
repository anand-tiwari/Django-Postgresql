
How to use :

http://localhost:8000/  - this url open home page
http://localhost:8000/crawler  - get the data from the website and store them into json and csv format

http://localhost:8000/post  -  data is stored into Django admin model and postgresql database

http://localhost:8000/api/ - open Django rest framework api

it contains another link - http://localhost:8000/api/products/  it will open new page with all data
	and with several functionality:-
		1. post 
		2. get
		3. filter on field
		4. search 
		5. ordering 

http://localhost:8000/admin - it opens Django Admin page 

contains Products model 


Project structure :- 

scrum
	board  			- app inside project
		migrations
		model
		view
		urls
		forms
	env  			- virtual environment 
	scrum  
		setting
		url
		views
	templates  		 - contains template like html file
		base
			base.hmtl
		index.html
		insert.html
		crawler.html
	manage.py   


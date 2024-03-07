# FE&P Projections Tool

A Django web application designed port facility expenses into a sqLite databse to be mapped into a Tableau worksheet for graphical reference. I helped develop and maintain this for Rice University DE&P staff to manage projections for each month



## Important Commands
Load the Organization and Account models into the database using the following command:
```
python manage.py runserver
python manage.py loaddata data_upload_system/fixtures/organization_data.json data_upload_system/fixtures/organization_data.json
python manage.py loaddata data_upload_system/fixtures/organization_data.json data_upload_system/fixtures/accountParentLevelE_data.json
python setup.py
```


## Guide to run 
1. First of all install python and postgresql in the system.
2. Open project folder in vscode
3. install virtualenv : <code>pip install virtualenv</code>
4. create a virtualenv : <code>virtualenv venv</code>
5. activate virtualev  :
   1. In window <code>./venv/script/activate</code>
   2. in linux and mac : <code>source ./venv/bin/activate</code>
6. install requirement.txt  :<code>pip install requirement.txt</code>
7. change database setting in setting.py according to your system.
8. Now enter some command for django:
   1. <code>python manage.py makemigrations</code>
   2. <code>python manage.py migrate</code>
   3. Create a superuser: 
      1. <code>python manage.py createsuperuser</code>
      2. enter email address
      3. enter password
9. Now run server by <code>python manage.py runserver</code>
10. Now webpage running on 127.0.0.1:8000

@echo off

..\.env\scripts\activate
timeout 20 /nobreak  
python manage.py runserver
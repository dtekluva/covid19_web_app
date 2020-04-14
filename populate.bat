@echo off

..\.env\scripts\activate
python manage.py update_data

for /L %%a in (1,1,10) do (     
python manage.py update_data
timeout 20 /nobreak                                                        
)
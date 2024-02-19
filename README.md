## Установка




1. **Клонувати репозиторій**

git clone https://github.com/Eugen1y/test_website.git
2.   **створити змінне середовище**

cd test_website

pip install venv

python -m venv venv

3. **Активувати змінне середовище**

source venv/Scripts/activate

4. **Встановити залежності**

pip install -r requirements.txt

5. **Мігрувати базу даних**

python manage.py migrate

5. **Завантажити дані в базу даних**


python manage.py loaddata user_data.json


6. **запустити проект** 

python manage.py runserver

7. **Перейти за адресою**

http://127.0.0.1:8000/

8. Паролі до юзерів у файлі pswrds.txt
   
login: admin password: qwerty  - суперюзер 
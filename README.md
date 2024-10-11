## Demo Video

https://github.com/user-attachments/assets/a68fc70a-380c-4612-9799-09800271b687

<h2>Setup :</h2>

Clone the repository to your local machine:
```sh
$ git clone https://github.com/jay-arora31/AuthProject.git
$ cd AuthProject
```
Install the required dependencies:
```sh
$ virtualenv venv
```
```sh
$ venv\scripts\activate


```
```sh
$ pip install -r requirements.txt


```

Apply database migrations:
```sh
$ python manage.py makemigrations


```
```sh
$ python manage.py migrate


```

Start the development server:
```sh
$ python manage.py runserver


```

# finin_test
Getting invoive details from Gmail Account.

Environment setup details

1. we need to clone the repository from github.com
    git@github.com:justincletus/finin_test.git

2. we need to create virtual environment inside the clone repository
    python3 -m venv venv

3. using pip to install all required depenancy
    pip3 install -r requirements.txt

4. Migrate database model and create super user for admin

    python3 manage.py migrate

    python3 manage.py createsuperuser

5. We created API for getting transaction details from Gmail
    request the /transaction api for invoice, subscription and bill details

6. We created API for user account
    create post request for /user_login_register/signup/ It required paload with username, email, and password

7. Get the user access and refresh token request the /api/token/ endpoint



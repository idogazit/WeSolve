# WeSolve

Data-Centered Crowd Sourcing Project by:

- Nir Swartz
- Guy Shnaider
- Ido Gazit
- Itai Weiss

Please read our documentation file ("WeSolve Documentation.pdf") and go over "Project's Related Files" folder for more important information about the project (including our presentations).

## Instructions for Windows set up
```python -m venv venv
call ./Scripts/activate.bat
pip install -r ./requirements.txt
```

for client side:
```
cd WeSolve/frontend
npm install
npm install axios --save
npm run serve
```

for server side:
```
cd WeSolve
python manage.py migrate
python manage.py runserver
```
#### Open up Chrome and go to 127.0.0.1:8000 and the app is now running in development mode!


## Instructions for Mac/Ubuntu set up

#### Download the code to your PC, unpack the zip and move inside the folder.

#### Create a new Python Virtual Environment:
```
python3 -m venv venv
```

#### Activate the environment and install all the Python/Django dependencies:

```
source ./venv/bin/activate
pip install -r ./requirements.txt
```


#### Time to install the Vue JS dependencies:
```
cd WeSolve/frontend
npm install
npm install axios --save
```

#### Run Vue JS Development Server:
```
npm run serve
```

#### Run Django's development server:
```
# cd to the folder which contains the "manage.py" file
# do the first two steps again
# might need do to (if an error is raised): python -m pip install Pillow
python manage.py migrate
python manage.py runserver
```
#### Open up Chrome and go to 127.0.0.1:8000 and the app is now running in development mode!

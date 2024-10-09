## Tasks

A task manager is an app let cerate, delete, update, retrieve your only own tasks.



## Set up the requirements to run the on your browser

First, you‘ll need to have Python installed, which you can download from the official Python website if you don‘t have it already. Then create a folder on your desktop (Tasks)

Create a virtual environment to isolate its packages from your computer:

```terminal(powershell)
python -m venv venva
```

Activate the virtual environment:

```terminal(powershell)
venva\Scripts\activate.ps1
```

With the virtual environment active, install Django using pip:

```terminal(powershell)
pip install django
pip install djangorestframework
```

# Creating the Django Project

django-admin startproject (handle_tasks)

## This will create a new directory called piggyhandle_tasksbank with the basic structure of a Django project. Let‘s also create a new app within our project that will handle the core handle_tasks functionality:

```terminal(powershell)
cd (handle_tasks)
python manage.py startapp (tarea)
```

The created app(tarea) is where we‘ll put most of our project settings file code. Make sure to add it to the list of installed apps in the your handle_tasks/settings.py file:

```python
INSTALLED_APPS = [
    ...
    'tarea',
]
```

# Designing the Database Models

Next, let‘s consider what database models we‘ll need for our your project app. We‘ll define models for:

User: the built-in Django user model, extended with a custom user profile.
Task: where stores the data entered

Here‘s an example of what model might look like (tarea/models.py):

```python 
from django.db import models
from django.contrib.auth.models import User



class Task(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    task_type  = models.CharField(max_length=255, null=False, blank=False)
    task_highlites = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
```


### We can define similar models for any other app you want to create.  After creating the models, we need to create a migration and sync the database:

```terminal(powershell)
python manage.py makemigrations 
python manage.py migrate
```


## Then write the logic of your app here an example:

### tarea.views.py

```python 
from rest_framework import viewsets
from .serializers import  UserSerializer
from django.contrib.auth.models import  User



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

```

This operate the CRUD operations create, delete, update and retrieve.


## Then create a serializers file to transform/recreate data objects to/from a portable format.

### tarea.serializers.py 


```python
from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id','username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

```

## After creating the serializers.py, create the urls.py file to get the endpoint directory 

### tarea.urls.py

```python
from .views import UserViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
```

## In order to be able to execute the operations and read the changes you have done, you must set the the urls of the app(tarea) in the urls.py of the project(handle_tasks):

### handle_tasks.urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tarea.urls')),
]
```

## How to Perform CRUD Operations with Postman

To perform CRUD operations, such as Create new user, you can use Postman. 

### Step 1: Open Postman

Make sure you have Postman installed on your computer.

### Step 2: Create a New Request

In Postman, create a new request.

### Step 3: Enter the URL

To create new user, enter the following URL: http://127.0.0.1:8000/api/users/

### step 4: enter the user's data. So, select Body then raw

```python
{
    "username": "mostafa",
    "email": "mostafa@app.com",
    "password": "123456",
    "password2": "123456",
    "first_name": "mostafa",
    "last_name": "mostafa"
}
```

### Step 5: Send the Request

Select the **POST** method and click **Send**.

You should see a list of all currencies in the response.
---
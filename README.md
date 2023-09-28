# Blog Application

### Features at a Glance:
* Sign Up
* Log In
* Log Out
* Post what is on your mind
* Edit your Posts
* Fetch all Posts from all Users
* Fetch a specific Post if you have its ID
* Delete each of your Posts

## How to Use

### Intsall the required packages
Install the required packages with:

```python
pip install -r requirements.txt
```
### Create your DateBase
Run the following commands in the terminal of the project directory.
```python
python manage.py makemigrations
```
```python
python manage.py migrate
```

### Run the Application on your Local Machine
You can run the project on your local machine using the command below.

```python
python manage.py runserver
```

### Connect through the APIs in Examples

#### Register User
Register a new User in the app according to the following example.

```python
url = 'http://127.0.0.1:8000/signup/'

data = {
    'username': 'myUserName',
    'password': 'myPassword',
}

response = requests.post(url, json=data)
print(response.status_code, ">>>", response.text)
```

#### Log in and retrieve your authentication TOKEN
Use your valid username and password to log in the system and receive your authentication token.

```python
url = 'http://127.0.0.1:8000/login/'

data = {
    'username': 'myUserName',
    'password': 'myPassword',
}

response = requests.post(url, json=data)
token = json.loads(response.text)['token']

print(response.status_code, ">>>", response.text)
```

#### Log out to invalidate your TOKEN when you are done
Remember to log out of your account when you are done to ensure that the created token for your session is invalidated. Otherwise, your account privacy would be at risk of abusing.

```python
url = 'http://127.0.0.1:8000/logout/'

headers = {
    'Authorization': f'Token {token}',
}

response = requests.post(url, headers=headers)

print(response.status_code, ">>>", response.text)
```

#### Create a Post
Post your content using the template below. We consider that you already have logged in and retrieved your token as `token`.

```python
url = 'http://127.0.0.1:8000/create-post/'

data = {
    'title': 'Huawei is on Fire',
    'content': 'Huawei have just released their latest Mate XS flagship smartphone with surprising adjustable screen size feature.',
}
headers = {
    'Authorization': f'Token {token}',
}

response = requests.post(url, json=data, headers=headers)

print(response.status_code, ">>>", response.text)
```

#### Fetch the App Feed
Get all the avaialble posts on the app using the following example. It is assumed that the user is logged in and the token is received and valid.

```python
url = 'http://127.0.0.1:8000/get-all-posts/'

headers = {
    'Authorization': f'Token {token}',
}

response = requests.get(url, headers=headers)

print(response.status_code, ">>>", response.text)
```

Also, you can fetch a specific post from the server if you set the ID value for it. The assumption on logging status of the user is still considered.

```python
post_id = 1
url = 'http://127.0.0.1:8000/get-post/post_id'

headers = {
    'Authorization': f'Token {token}',
}

response = requests.get(url, headers=headers)

print(response.status_code, ">>>", response.text)
```

#### Edit your Posts
Edit your post title and/or content as you wish.

```python
post_id = 1
url = 'http://127.0.0.1:8000/update-post/post_id'

headers = {
    'Authorization': f'Token {token}',
}

data = {
    "title": "Huawei is on Fire" // drop the line if you don't seek to edit the title
    "content": "New Content Here" // drop the line if you don't seek to edit the content
}

response = requests.post(url, json=data, headers=headers)

print(response.status_code, ">>>", response.text)
```

#### Delete your Posts
Delete your post using the post ID.

```python
post_id = 1
url = 'http://127.0.0.1:8000/delete-post/post_id'

headers = {
    'Authorization': f'Token {token}',
}

response = requests.post(url, headers=headers)

print(response.status_code, ">>>", response.text)
```

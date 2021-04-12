# Face swap flask REST API

## Simple request to the api

Using the python requests library, you can get access to the API.

```python
import requests

url = 'http://localhost:5000/predict'
response = requests.post(url, files={'img': open('path_to_image.jpg', 'rb')})
```

The API returns link with the results of the face swap for both male and female.

Results are stored on the following link:

```
http://localhost:5000/result/ + generated link
```

## Before the app configuring

Firstly, download the weights for models and extract model_weights folder to the main directory

[Download weights](https://drive.google.com/file/d/1U2BonClMqnDvTNEaBPtFYG5IqMICc18z/view?usp=sharing)


## Local run

To run locally, firstly install requirements:

```
pip install -r requirements.txt
```

Then, run app.py file:

```
python app.py
```

The application will be configured at the following link:

```
http://localhost:5000
```

# Run in docker container
 
Firstly, build a docker container:

```
docker build -t faceswap-flask-restapi .
```

It will take some time to build the container, as the dlib python module takes 5-7 minutes to build.

To run docker container execute following command:

```
docker run -d -p 5000:5000 faceswap-flask-restapi
```


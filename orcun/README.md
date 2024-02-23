APIDON-BRIDGE

MODEL HOSTING WITH FASTAPI
--These are apis that provide us hosting in remote servers Pytorch and Tensorflow models. 

REQUIREMENTS
--Python 3.8+(Recommended 3.10)
--FastAPI
--An HTTP client to interact with the applications (e.g., Postman)

RUNNING
--The dependencies in requirements.txt should be downloaded in your computer.
>>pip install -r requirements.txt
--The server can be started with the following code typed into the terminal:
>>uvicorn hosting.main:app --reload

POSTMAN etc. 
--You can test the api with postman and the others.While doing this, you should use first 
this request http://127.0.0.1:8000. You will face this answer : "message":"Welcome to APIDON".
Then you should test the other request by changing paths.Please be aware of prefixes.
the paths:
root --> /
tensorflow message --> /tensorflow
pytorch message --> /pytorch
tensorflow classify --> /tensorflow/classify
pytorch classify --> /pytorch/classify

PROBLEMS
--Tensorflow model may make trouble with packages problem. So we advice Python3.10 or 3.11 version. 
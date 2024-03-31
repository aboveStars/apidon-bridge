
## MODEL DOWNLOAD AND STORAGE FEATURE

APIDON-BRIDGE now includes an API endpoint that allows you to download your Pytorch or Tensorflow model files and save them to a specified directory on your computer. This feature facilitates the management and deployment of machine learning models by providing an automated process for handling model files.

### HOW TO USE

To utilize this feature, make a request to the following endpoint, replacing <model_type> with either pytorch or tensorflow, and specify your desired save location in the request body. 

The endpoint:"http://127.0.0.1:8000/upload_model"

#### RAW CODE
```bash
curl --location 'http://127.0.0.1:8000/upload_model' \
--form 'url="<your_url>"' \
--form 'path="<your_path>"'
```
This API call will download the specified model and save it to the provided directory path on your machine.

#### TESTING WITH POSTMAN

To test the API endpoints using Postman, follow the steps below. Ensure that you select the form-data option when sending POST requests where you need to upload files or specify parameters. Details for each relevant endpoint are provided for clarity.

It is convenient that using the menu in Postman application. First select 'Body' option under request bar. Then by using new menu that includes "none,raw,form-data,binary" options, you can send the POST request. 



For the /upload_model endpoint, use the form-data option in Postman. You need to specify the following parameters:

url: The URL where the model file is located.
path: The local directory path where you want to save the model file.

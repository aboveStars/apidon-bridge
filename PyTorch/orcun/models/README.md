
## CLASSIFY ENDPOINTS

### HOW TO USE CLASSIFY

You should send the post request the following endpoint by using postman or raw code and you will take predictions of image of models  
The endpoint:"http://127.0.0.1:8000"


#### RAW CODE
Example cURL template for classify endpoints:

```bash
curl --location 'http://127.0.0.1:8000/pytorch/classify' \
--form 'image_url="https://yourdomain.com/path/to/image.png"'
```
Be sure to replace pytorch with tensorflow or tensorflow_lite in the URL if you are using the TensorFlow or TensorFlowLite model.



#### TESTING WITH POSTMAN 

For the /pytorch/classify ,/tensorflow/classify, /tensorflow_lite/classify endpoints, when sending a POST request, you should use the form-data option and include the parameter named **image_url**. This parameter should contain the URL of the image you wish to classify. When using Postman ,you should follow the same steps with Model Downloading and Storage Feature.
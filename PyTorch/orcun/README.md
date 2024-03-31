## TABLE OF CONTENTS
- [APIDON-BRIDGE](#apidon-bridge)
 - [REQUIREMENTS](##requirements)
 -[SETUP AND INSTALLATION](##setup-and-installation)
  -[INSTALL THE NECESSARY PYTHON PACKAGES](###install-the-necessary-python-packages)
  -[START THE FASTAPI SERVER WITH THIS COMMAND](###start-the-fastapi-server-with-this-command)
 -[DOCKER CONTAINER SET-UP](##docker-container-set-up)
  -[HOW TO USE DOCKERFILE](###how-to-use-dockerfile)
 -[KNOWN ISSUES](##known-issues) 
 -[CONCLUSION](#conclusion) 



# APIDON-BRIDGE
APIDON-BRIDGE allows for easy deployment of Pytorch,TensorFlow_Lite and Tensorflow models with a FastAPI backend, including features like automatic model download and save functionality.
## REQUIREMENTS


Python 3.8 or higher (recommended: 3.10 for optimal compatibility)
FastAPI
An HTTP client for API interaction (e.g., Postman, cURL)


## SETUP AND INSTALLATION

First, clone the repository or download the source code to your local machine. Then, follow these steps to set up your environment:

### INSTALL THE NECESSARY PYTHON PACKAGES
```bash
pip install -r requirements.txt
```
### START THE FASTAPI SERVER WITH THIS COMMAND
```bash
uvicorn hosting.main:app --reload
```
This command starts a local development server that automatically reloads upon any file changes, making it ideal for development purposes.

## DOCKER CONTAINER SET-UP

For deploying APIDON-BRIDGE on a remote server using Docker, use the provided Dockerfile to build and run the container. The Dockerfile contains all necessary instructions to create a containerized environment for the API.


### HOW TO USE DOCKERFILE ###

Follow these steps to build and run your Docker container:

Ensure Docker is installed on your machine.
Navigate to the project directory containing the Dockerfile.
Build the Docker image:
```bash
docker build -t <container-name> .
```
Run the Docker container:
```bash
docker run -d --name -p 8000:8000 <container-name>
```
### DEPLOYMENT ON DIGITAL OCEAN DROPLET WITH BIND-MOUNT###

For deploying APIDON-BRIDGE on a Digital Ocean droplet using Docker and ensuring persistent storage through bind-mount:

Prepare the Droplet:

Install Docker on your Digital Ocean droplet.
Ensure you have SSH access to the droplet.
 Using Bind-Mount:

Identify the local directory on your droplet where you want to persist data.
Utilize Docker's -v or --mount flag to bind-mount the local directory to a directory within the container.
Example command:

```bash
docker run -d --name <container-name> -p 8000:8000 -v /path/on/droplet:/path/in/container -it <image-name>
```
This ensures that data saved in /path/in/container within the container is also accessible in /path/on/droplet on your droplet, facilitating persistent storage and ease of management.








## KNOWN ISSUES


Users may encounter package-related issues when using the Tensorflow model. To avoid these problems, it is recommended to use Python version 3.10 or 3.11.

## CONCLUSION

APIDON-BRIDGE offers a streamlined approach to deploying machine learning models, ensuring ease of access and reliability. The additional feature for downloading and saving model files broadens the utility of the service, making it even more convenient for users managing multiple models. For further assistance or to report issues, please consult the documentation or raise an issue on the project repository.
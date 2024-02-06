
---    FastAPI Image Converter & Analyser   ---

This FastAPI application is designed to convert images to JPEG format and, optionally, analyze them using a predefined AI model. It fetches images from specified URLs, converts them to the RGB color space, and saves the JPEGs locally. When integrated with an AI model, it can also analyze the images and provide relevant results.

1- Features:
 - Fetch images via URL
 - Convert images to JPEG format
 - Validate image content type and size constraints
 - (Optional) Analyze images using an AI model
 - Save converted images locally

2- Requirements
 - FastAPI
 - Uvicorn (for running the application)
 - Pillow (for image processing)
 - Requests (for fetching images from URLs)
 - Your custom AI model (if analysis functionality is utilized)

Note: Ensure you have Python 3.6+ installed on your machine.

3- Installation

1. Clone the Repository:

    First, clone this repository to your local machine.
        "git clone <repository_url>"

2. Install Dependencies:

    Navigate to the project directory and install the required dependencies.
       " cd <project_directory>"
       " pip install pydantic ,uvicorn , fastapi , Pillow , Requests"

3. Set Up Environment:

(Optional) If your project requires environment variables (e.g., for your AI model), set them up accordingly.

4. Running the Application:

    Run the application using Uvicorn:
        "uvicorn main.con_img:app --reload" 
    Note: If you are planning to use this code in another file you should add the directory before running it (Example : This code file in "Example" directory then you shold change "uvicorn main.con_img:app --reload" to  "uvicorn Example.Kaan.main.con_img:app --reload")
    The application will be accessible at http://127.0.0.1:8000.

4- Usage:

    Convert Images to JPEG:

    To convert an image to JPEG, send a POST request to the http://127.0.0.1:8000/classify endpoint with the image URL in the request body.

        Request Example:
        doc.type (json)
        Body:Raw

        {
          "image_url": "http://example.com/image.png"
        }

        Response Example:
        doc.type (json)
        Body:Raw

        {
          "message": "Image converted, saved, and analyzed successfully.",
          "url": "/images/123456789_converted.jpg"
          "results": ["example_1", "example_2" "example_3","example_4","example_5"]
        }

5- Extending the Application
    To add image analysis functionality:

        1. Import your AI model module at the top of the main.py file.

        2. Uncomment the lines related to the AI model prediction in the convert_image function.

6- Troubleshooting & FAQ

    - Ensure image URLs are valid and accessible.

    - Verify that the server running the application can access external URLs if running behind a proxy or firewall.

    - Check that your AI model is correctly integrated and that its dependencies are included in requirements.txt.

8- Contributing
    
    Contributions to improve FastAPI Image Converter & Analyser are welcome.

9- Updates & Relases    

    V0.1.1:
            # First demo relase

    V0.1.2:  
            # README updated 
            # Directory comment added for better understanding and running code
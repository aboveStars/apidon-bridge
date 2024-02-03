from fastapi.testclient import TestClient
import pytest
from apidon_bridge.convert_jpg import app


client = TestClient(app)

def test_convert_jpg():
    with open('image/aa.jpg','rb') as img_fil:
        response= client.post("/convert_jpg/", files = {"file":img_fil})

        assert response.status_code == 200
        assert "application/json" in response.headers['content-type']

        
            



from app.main import app
from fastapi.testclient import TestClient


class TestAccountsRouter:
    client = TestClient(app)

    def test_index_no_auth(self):
        response = self.client.get('/accounts')
        assert response.status_code != 200          # negative case
        # Unprocessable Entity response status code
        assert response.status_code == 422

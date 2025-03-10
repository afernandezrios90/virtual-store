# Virtual Store
Repository for deploying a really simple e-commerce site. The idea of this app is to make load testing, logging, etc.

## Functionality

- The app exposes an API endpoint on port 5000
- It simulates product listing if you make a `GET` request to `/products`
- It simulates a purchase of a product if you make a `POST` request to `/buy/<id>`.
    - If product ID is not valid, returns 404

## Repo structure
```bash
virtual-store/
│── app/
│   ├── main.py  # Main API code
│   ├── requirements.txt  # Python dependencies
│── test/
│   ├── test_requests.http  # Sample requests for testing the Virtual Store

│── Dockerfile  # Docker image to build
│── docker-compose.yml  # Docker Compose file to use for deployment
│── README.md  # Repo explanation
```

## Considerations
-

## Installation
1. Clone the repository
```bash
git clone https://github.com/afernandezrios90/virtual-store.git
```
2. Adjust the content of the app if desired
3. Run using Docker compose
```bash
docker-compose up -d
```
4. Start sending requests to simulate activity
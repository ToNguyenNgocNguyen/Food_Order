# Deployment option

## Deploy as Image

```bash
docker build -t nto218145/food_order:latest .
docker run -d --name my_app_container -p 3000:3000 -p 5000:5000 nto218145/food_order:latest
```

## Deploy as container

```bash
docker compose up -d
```

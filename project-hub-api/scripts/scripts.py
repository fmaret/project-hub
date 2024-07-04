import subprocess


def local():
    subprocess.run(["docker-compose", "up", "project-hub-db", "-d"])
    subprocess.run(["sh", "-c", "PGPASSWORD=test psql -h localhost --port 8015 -U test db -f init_db.sql"])
    subprocess.run(["sh", "-c", "poetry run uvicorn client:create_app --host 0.0.0.0 --port 8014 --factory --reload"])
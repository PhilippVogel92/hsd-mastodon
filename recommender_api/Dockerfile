FROM tiangolo/meinheld-gunicorn-flask:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app/recommender_api/

ENV MODULE_NAME="recommender_api.main"

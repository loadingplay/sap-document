FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY ./ /app/

RUN pip install -r requirements.txt
RUN pip install --no-cache-dir newrelic

ENTRYPOINT ["newrelic-admin", "run-program"]
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "/gunicorn_conf.py", "api:api"]

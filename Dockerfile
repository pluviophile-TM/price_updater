FROM python:3.7-alpine
WORKDIR /app
COPY price_updater.py .
RUN pip install redis
CMD ["python", "price_updater.py"]

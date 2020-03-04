FROM python:3.7
RUN pip install pipenv

WORKDIR /app
COPY . .

RUN pipenv install --dev --system --deploy --skip-lock          

CMD [ "python", "./app.py" ]
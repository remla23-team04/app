FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# EXPOSE lets other containers access the server at port 5000
EXPOSE 5000

COPY . .

CMD [ "python", "./src/app.py" ]

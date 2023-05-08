FROM python:3.9

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y cron
RUN pip install python-dotenv
RUN pip install -r requirements.txt

RUN echo "* * * * * root rm -rf /app/uploads/*" >> /etc/crontab

EXPOSE 5000

RUN chmod +x start.sh

CMD [ "./start.sh" ]

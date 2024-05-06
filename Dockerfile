FROM python:3.10

WORKDIR /app

COPY . /app

RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"

ENV TZ=Asia/Tashkent
RUN ls -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install --no-cache-dir -r requirements.txt

ENV NAME World

CMD ["python", "./main.py"]

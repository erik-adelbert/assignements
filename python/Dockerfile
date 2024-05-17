FROM python:3.11.0

# working directory
WORKDIR /usr/src/app

# copy requirement file to working directory
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest
RUN pip install pytest-asyncio

COPY . .

RUN chmod +x ./entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
CMD ["./entrypoint.sh", "."]
FROM mageai/mageai:latest
ARG PROJECT_NAME
ENV PROJECT_NAME=${PROJECT_NAME}
RUN mage init ${PROJECT_NAME}
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT mage start orchestratrator

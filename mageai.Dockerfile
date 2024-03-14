FROM mageai/mageai:latest
RUN mage init orchestratrator
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT mage start orchestratrator

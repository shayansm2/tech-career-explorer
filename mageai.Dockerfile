FROM mageai/mageai:latest
RUN mage init orchestrator
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT mage start orchestrator

FROM mageai/mageai:latest
ARG PROJECT_NAME
# todo fix this
ENTRYPOINT mage start $PROJECT_NAME

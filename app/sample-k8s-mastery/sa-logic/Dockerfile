# https://betterprogramming.pub/6-concepts-to-master-when-dockerizing-python-applications-e5f5a6a87845
# https://pythonspeed.com/articles/base-image-python-docker-images/
# https://towardsdatascience.com/how-to-build-slim-docker-images-fast-ecc246d7f4a7
# We want to enjoy the same freedom of installing private packages inside our Docker build
# We want to get the $PIP_EXTRA_INDEX_URL variable from our build agent host and pass it to our Docker build context.
# see task: PipAuthenticate@1 in azure-pipelines.yml
# ARG PIP_EXTRA_URL
# RUN pip3 install -r /requirements.txt --extra-index-url $PIP_EXTRA_URL

# ARG is only available during the build of a Docker image (RUN etc)
# ENV values are available to containers
# RUN is an image build step, the state of the container after a RUN command will be committed to the container image.
# CMD is the command the container executes by default when you launch the built image.
# ENTRYPOINT is also closely related to CMD and can modify the way a container is started from an image.

# ARG INFA_EDC_AUTH
# ENV INFA_EDC_AUTH=$INFA_EDC_AUTH
# demo

FROM python:3.6-slim
COPY sa /app
WORKDIR /app
RUN pip3 install -r requirements.txt && \
    python3 -m textblob.download_corpora
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["sentiment_analysis.py"]

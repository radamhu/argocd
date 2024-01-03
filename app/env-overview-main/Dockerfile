FROM node:18 AS build

# args
ARG codeartifact_token
ARG version
ARG versionHash

# env variables
ENV CODEARTIFACT_AUTH_TOKEN=${codeartifact_token}


# update
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install bash dos2unix wget -y

COPY . /app
WORKDIR /app

# install dependencies
#RUN npm install
RUN yarn install

RUN yarn run build

# start app
#CMD [ "npm start" ]
#ENTRYPOINT ["sh","/app/docker-entrypoint.sh"]

#
# runtime
#
FROM alpine:3.18 as runtime

# add nodejs and yarn (will be nodejs 16)
RUN apk add --update nodejs yarn

# update apk
RUN apk update && apk upgrade

RUN apk add tzdata \
    && cp /usr/share/zoneinfo/Europe/Berlin /etc/localtime \
    && echo "Europe/Berlin" >  /etc/timezone

# add nodejs and yarn (will be nodejs 14)
RUN apk add --update nodejs yarn npm

RUN yarn global add serve

# create extra www user and www group
RUN addgroup -g 1000 www
RUN adduser -D -G www -u 1000 www

RUN apk add openssl curl jq

# copy docu
#COPY docu/openapi /docs
RUN mkdir -p /app
RUN mkdir -p /docs

# app permission
RUN chown -R www:www /app && \
    chown -R www:www /docs


WORKDIR /app

# copy build files
COPY --chown=www:www .npmrc ./
COPY --chown=www:www package.json ./
COPY --chown=www:www --from=build /app/node_modules ./node_modules
COPY --chown=www:www --from=build /app/build ./build

# copy own docker entrypoint
COPY --chown=www:www docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# run as user www
USER www

ENTRYPOINT ["sh","/app/docker-entrypoint.sh"]
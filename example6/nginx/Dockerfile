FROM alpine

RUN apk add --update \
    nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY index.html /www/

EXPOSE 8080

CMD nginx -g 'pid /tmp/nginx.pid;'
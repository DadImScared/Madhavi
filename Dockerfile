FROM node:carbon as base

ADD /server/static /server/static

COPY /client/ /client/

WORKDIR /client/

RUN yarn && yarn build

FROM python:3.5.2-onbuild

RUN pip install gunicorn

COPY --from=base /server/static /usr/src/app/server/static

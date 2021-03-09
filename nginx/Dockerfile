FROM nginx:1.14.0

RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir staticfiles
COPY /django_core/staticfiles/ /staticfiles/
COPY nginx.conf /etc/nginx/conf.d

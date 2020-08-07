FROM python:3.7-buster

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/finin
RUN cd /opt/finin/
RUN python3 -m venv venv
RUN cd ../../
RUN mkdir -p /opt/finin/src
RUN mkdir -p /opt/finin/pip_cache
#RUN mkdir -p /opt/finin/finin_test
#COPY requirements.txt /opt/finin/pip_cache/
COPY start-server.sh /opt/finin/src/

#COPY src/manage.py /opt/finin/src
COPY .pip_cache /opt/finin/pip_cache/
COPY src /opt/finin/
# WORKDIR /opt/finin/src/
RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt

# RUN ls -l /opt/finin/pip_cache/
#RUN cd /opt/finin/pip_cache/
#RUN pip install -r requirements.txt --cache-dir /opt/finin/pip_cache
RUN chown -R www-data:www-data /opt/finin

# start server
EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["/opt/finin/src/start-server.sh"]





FROM debian:stretch

# 1. Install dependencies
RUN apt update
RUN apt install -y libxml2 python git python-pip libxslt-dev python-dev zlib1g-dev libpq-dev nginx uwsgi uwsgi-plugin-python python-virtualenv

# 2. Setup the runtime for the app
# 2.1. Create user and directories
RUN useradd -m annuaire

USER annuaire:annuaire
WORKDIR /home/annuaire

# 2.2. Install the project in a virtualenv
RUN git clone https://github.com/Kehrlann/annuaire.git
RUN virtualenv venv \
    && . venv/bin/activate \
    && cd annuaire \
    && python setup.py install \
    && deactivate

# 2.3. Add runtime configs
ADD start_app.sh start_app.sh
ADD uwsgi.ini uwsgi.ini
ADD annuaire.conf /etc/nginx/sites-enabled/

# 2.4. Set correct permissions on those files
USER root:root
WORKDIR /
RUN chown annuaire:annuaire /home/annuaire
RUN chmod +x /home/annuaire/start_app.sh

# 4. Custom entrypoint
COPY entrypoint.sh /usr/local/bin/
RUN ln -s /usr/local/bin/entrypoint.sh / 
RUN chmod +x entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["entrypoint.sh"]

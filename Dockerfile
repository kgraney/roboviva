FROM python

RUN apt -y update
RUN apt -y --no-install-recommends install texlive-base
RUN apt -y --no-install-recommends install texlive-latex-extra
RUN apt -y --no-install-recommends install texlive-fonts-extra
RUN apt -y --no-install-recommends install texlive-fonts-recommended

RUN python -m venv venv
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install flask Flask-Shelve

COPY roboviva /roboviva/roboviva
COPY run.py /roboviva/run.py
COPY config.py /roboviva/config.py

RUN mkdir -p /tmp/pdf_cache

EXPOSE 5000
CMD /venv/bin/python /roboviva/run.py

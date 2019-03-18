FROM python:3
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN sed --in-place --regexp-extended "s/(\/\/)(archive\.ubuntu)/\1br.\2/" /etc/apt/sources.list
WORKDIR /usr/src/app

RUN chmod go-w ~
COPY . .
RUN pip3 install --no-cache-dir -r pip_requirements.txt
CMD [ "bash", "/usr/src/app/runner.sh" ]
# получаем image для нашего питона
FROM python:3.9.1

# добавляем пользователя djangocore
RUN useradd djangocore -m

# устанавливаем рабочую директорию
ENV HOME=/home/djangocore
ENV APP_HOME=/home/djangocore/django_core
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# docker-compose-wait tool
ENV WAIT_VERSION 2.7.3
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

# задаём переменные окружения, чтобы
# предотвратить ряд событий, а именно:
# создания .pyc файлов и использования
# питоном буффера для stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ставим зависимости
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# копируем проект
COPY . .

# даём право на доступ пользователю djangocore
RUN chown -R djangocore:djangocore $APP_HOME

# меняем пользователя на djangocore
USER djangocore

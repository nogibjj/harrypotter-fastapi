FROM public.ecr.aws/lambda/python:3.9

RUN mkdir -p /app
COPY . . /app/
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["app.py"]
ENTRYPOINT [ "python" ]
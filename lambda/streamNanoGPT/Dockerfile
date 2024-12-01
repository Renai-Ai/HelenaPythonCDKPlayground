#FROM public.ecr.aws/docker/library/python:3.12.0-slim-bullseye
FROM continuumio/miniconda3:main
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter
ENV AWS_LWA_INVOKE_MODE=RESPONSE_STREAM
ADD . .
RUN conda install -y conda-forge::pytorch-cpu
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
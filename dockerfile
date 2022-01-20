FROM python:3
USER root
WORKDIR /home

RUN apt-get update -y
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8


RUN pip install --upgrade pip setuptools wheel&&\
    pip install pygithub pyproject.toml numpy requests slack-sdk tqdm chardet argparse matplotlib seaborn pandas numexpr scikit_posthocs pingouin
RUN pip install git+https://github.com/opencv/opencv-python
CMD ["/bin/bash"]
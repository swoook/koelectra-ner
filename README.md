# KOELECTRA for NER

- This repository contains what I've learned for fine-tuning PLMs from monologg/KOELECTRA to named entity recognition for Korean corpus

## Environments

1. Build an image from the `Dockerfile` at the `<repository_root_directory>`

    ```Bash
    docker build -t <image_name>:<tag_name> .
    ```
    
    - E.g.,
    
    ```Bash
    docker build -t koelectra-ner:latest .
    ```
    
2. Run a container from the image `<image_name>:<tag_name>` built in step 1

    ```Bash
    docker run -itd --rm --shm-size=<shared_memory_size> --gpus all \
    --entrypoint /bin/bash \
    -v <host_volume>:<container_volume> \
    -p <host_port>:<container_port> \
    --name <container_name> \
    <image>:<tag>
    ```
    
    - E.g.,
    
    ```Bash
    docker run -itd --rm --shm-size=32G --gpus all \
    --entrypoint /bin/bash \
    -v /data/:/host_volume \
    -p 8888:8888 \
    --name FinNER \
    koelectra-ner:latest
    ```

## Datasets

1. 국립국어원 개체명 분석 말뭉치 개체 연결 2021
2. 전문분야 말뭉치
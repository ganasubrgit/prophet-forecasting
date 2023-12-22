# prophet-forecasting
Reference https://research.facebook.com/blog/2017/2/prophet-forecasting-at-scale/

### System Requirement 
- Docker (or) Rancher Desktop

### Build and run jupyter notebook with prophet localy with Docker

- clone the repo
- `cd` to the repo directory 
- `docker buildx build --tag prophet:latest --load .`

### Start the container from the newly built image
- `docker run -p 8888:8888 -v $(pwd)/data/tmp:/tmp prophet:latest`

### Web login to Jupyter notebook using the console printed URL with token similar as below.

   `http://127.0.0.1:8888/lab?token=edb8c3ef75276103421ccdbb6ff0d3d9911c5b5b3e803531`
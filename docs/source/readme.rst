readme
======
This repo builds a docker image of the COPASI Simulator for BioSimulations web application.

The docker image is eventually converted to Singularity image in CRBM service user at HPC which further is used to perform actual simulation. The image is created automatically on  **crbmapi.cam.uchc.edu** server via service root user using cron jobs (cronjob scheduled with the latest docker hub image tag)

Make sure to have all env variables placed in root dir for singularity image

To push latest image to docker hub
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Create a new release tag version that pushes latest and version images to docker hub

To check it manually with docker image locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. ```docker pull crbm/biosimulations_copasi_api:latest```
2. use env.sample as `.env` file with all variables filled
3. run this command  ```docker run -v <LOCAL_DIR_WITH_SEDML AND SBML>:/usr/local/app/copasi/<SUB_ID>/<SIM_ID> --env-file <PATH_OF_ENV_FILE> <DOCKER_IMAGE>```
4. Make sure to bind sedml file inbound directory

VERSION=v1
FUNCTION_NAME=tradelens-onboarding/tradelens_unlocodes
IMAGE_NAME=marek5050/pumpkin-eating-chocolate
ORG=Zonar
SPACE=prod

include .env

build:
	echo "Using ${IMAGE_NAME} as the image name"; \
	docker build -t ${IMAGE_NAME} .

publish:
	echo "Publishing ${IMAGE_NAME}"; \
	docker push ${IMAGE_NAME}

updatefunc:
	echo "Updating the cloud function"; \
	ibmcloud target -o ${ORG} -s ${SPACE}; \
	ibmcloud fn action update ${FUNCTION_NAME} --docker ${IMAGE_NAME} --param MYSQL_EP ${MYSQL_EP}

fn_test:
	ibmcloud fn action invoke ${FUNCTION_NAME} --param unlocode USHOU --param timestamp 1549367920

fn_logs:
	bx fn activation logs -l

run_docker:
	docker run ${IMAGE_NAME}

test_unocode:
	@ ./exec '{"MYSQL_FILE":"dataset/unlocode_list_with_gps.csv","unlocode":"USHOU","timestamp":1549367920000}'

test_unocode_with_db:
	@ ./exec '{"MYSQL_EP":${MYSQL_EP},"unlocode":"USHOU","timestamp":1549367920000}'
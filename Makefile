VERSION=v1
FUNCTION_NAME=tradelens-onboarding/tradelens_unlocodes
IMAGE_NAME=jamesltpz/pumpkin-eating-chocolate
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
	ibmcloud fn action update ${FUNCTION_NAME} --docker ${IMAGE_NAME} \
	--param MYSQL_EP ${MYSQL_EP} --param unlocode "USHOU"

fn_daily_prod:
	ibmcloud fn action invoke ${FUNCTION_NAME} --param days 3 --param function daily_prod_stats

fn_daily_sandbox:
	ibmcloud fn action invoke ${FUNCTION_NAME} --param days 3 --param function daily_sandbox_stats

fn_logs:
	bx fn activation logs -l

run_docker:
	docker run ${IMAGE_NAME}

test_health_check:
	@ ./exec '{"apiKey":"${ORG_APIKEY}","orgId":"${ORG_ID}","MYSQL_EP":"${MYSQL_EP}","size":10,"before_n_days":30,"function":"daily_health_check","org":"TEST_ORG"}'

test_daily_prod:
	@ ./exec '{"PROD_EP":"${PROD_EP}","PROD_APIKEY":"${PROD_APIKEY}","MYSQL_EP":"${MYSQL_EP}","days":30,"function":"daily_prod_stats"}'

test_daily_sandbox:
	@ ./exec '{"SANDBOX_EP":"${SANDBOX_EP}","MYSQL_EP":"${MYSQL_EP}","days":15,"function":"daily_sandbox_stats"}'

test_daily_orphans_sandbox:
	@ ./exec '{"SANDBOX_EP":"${SANDBOX_EP}","MYSQL_EP":"${MYSQL_EP}","days":30,"function":"daily_sandbox_orphan_stats"}'
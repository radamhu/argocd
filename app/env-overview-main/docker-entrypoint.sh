#!/bin/sh

echo "1/2>>creating log folders and exporting variables"
mkdir -p  "${APP_LOG_DIR}"

# Start app
echo "2/2>>starting app" | tee -a "${APP_LOG_DIR}/${APP_NAME}.log"
echo "starting ${APP_NAME} with command: npm run ${APP_START}" | tee -a "${APP_LOG_DIR}/${APP_NAME}.log"
#npm run "${APP_START}" | tee -a "${APP_LOG_DIR}/${APP_NAME}.log"
serve -s build | tee -a "${APP_LOG_DIR}/${APP_NAME}.log"
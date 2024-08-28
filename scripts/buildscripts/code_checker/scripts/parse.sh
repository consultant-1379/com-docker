#!/bin/bash -x

# These environment variables must be set:
#
# ${PROJECT_NAME} - Project name
# ${PROJECT_WORKSPACE_DIR} - Workspace directory
# ${CONFIG_DIR} - Where Skip file for analysis and others are stored.
# ${PROJECT_URL} - URL where the project accessible.
# ${CODECHECKER_USER} - User name who are permitted to store the result of
#        parsing in the web server.
# Arguments:
# $1 - Name of the project similar to name in codechecker server
# $2 and $3 - Username and Password for login to codechecker server
# $4 - Git project, needed to generate Version tag
# $5 - Commit Hash value of the HEAD in the project
# $6 - Base code, optional parameter


# These variables are consts. The demo environment needs them but fixes.
export PROJECT_NAME="$1"
export CODECHECKER_USER="$2"

standard_output=1
standard_error=2

script_cleanup() {
    local result=$?

    echo "Cleaning up..." >&${standard_error}
    return ${result}
}

print_usage() {
    local output_stream=${1}

    cat <<EOF >&${output_stream}
Usage: $(basename "$0") -h
       $(basename "$0") options
Options:
    -h              This help message.
    -s server_host  Host name of the CodeChecker web server. Optional. The default is "localhost".
    -r RSTATE       RSTATE.
EOF
}

trap script_cleanup EXIT

# Uncomment when needed
#set -e

webserver_host="codechecker.gic.ericsson.se"

scriptdir=$(readlink -e "$(dirname "$(which "$0")")")

export CONFIG_DIR="${scriptdir}/../config"

workspace_dir="/"
export PROJECT_WORKSPACE_DIR=$workspace_dir
export CLONE=$4

export RUN_NAME="${PROJECT_NAME}-$5"

if [ $# -eq 6 ] ; then
   export BASE_CODE=$6
else
   export BASE_CODE=$RUN_NAME
fi

export PROJECT_URL="https://${webserver_host}/${PROJECT_NAME}"

export URL_PATH="${PROJECT_URL}/#is-unique=on&tab=${RUN_NAME}"

echo "BASE_CODE : $BASE_CODE"
echo "CONFIG_DIR: $CONFIG_DIR"
echo "PROJECT_URL: $PROJECT_URL"

cc_credential_file_name="${HOME}/.codechecker.passwords.json"
user_credential_file_name="${CONFIG_DIR}/.codechecker.passwords.json"

# The pre-installed credential file provides user's password so no
# interaction necessary with the user during parsing.
if [[ -e "${user_credential_file_name}" ]]; then
        rm -f "${cc_credential_file_name}"
        sed -i "s#user:password#$2:$3#g" "${user_credential_file_name}"
        chmod 0600 ${user_credential_file_name}
        ln -s "${user_credential_file_name}" "${cc_credential_file_name}"
else
    echo "Error: The CodeChecker user's credential file does not exist." >&${standard_error}
    exit 4
fi

source "${scriptdir}/project_specific.sh"

# Set up development environment of the project
# The sciptdir parameter helps the function to find other parts of the
# project specific things.

COMPILATION_DATABASE=$(get_compilation_database "${PROJECT_WORKSPACE_DIR}")


#Build the project
if is_logging_necessary; then
    echo "Start logging of compile commands..."
    # Create compilation database for parsing. This section builds the project
    # completely.
    export CC_LOGGER_GCC_LIKE="$(get_compiler_pattern)"
fi


FILTERED_COMPILATION_DATABASE=$(filter_compilation_database "${scriptdir}"    \
    "${COMPILATION_DATABASE}")
echo "The ${FILTERED_COMPILATION_DATABASE} will be used for analyzing."
REPORTS_DIR="${PROJECT_WORKSPACE_DIR}/reports"
CHECKER_FLAGS=""
SKIP_FILE_OPTION=$(generate_skipfile_option "${CONFIG_DIR}")

while read FLAG; do
    CHECKER_FLAGS="${CHECKER_FLAGS} ${FLAG}";
done < <(get_analyze_flags_array "${scriptdir}")


#Analyzing
echo "Analyzing started..."
CodeChecker analyze --name "${PROJECT_NAME}" --jobs 8 --add-compiler-defaults  \
  --output "${REPORTS_DIR}" ${SKIP_FILE_OPTION} ${CHECKER_FLAGS}               \
  "${FILTERED_COMPILATION_DATABASE}"
if [ $? -ne 0 ]; then
    echo "Error: CodeChecker Analyzing failed"
    exit 1
fi

echo "Analyzing finished successfully."


#Parsing
echo "Parsing started"
PARSE_OUTPUT=$(CodeChecker parse "${REPORTS_DIR}"  --suppress suppressfile --export-source-suppress)
if [ $? -ne 0 ]; then
    echo "Error: CodeChecker Parsing failed"
    exit 1
fi
echo "$PARSE_OUTPUT" > "${REPORTS_DIR}/parse_results.txt"
echo "Parsing completed"

TAG_OPTION=$(generate_run_tag "${PROJECT_WORKSPACE_DIR}" "${CLONE}")

echo "BASE_CODE: $BASE_CODE"
echo "RUN_NAME: $RUN_NAME"


CodeChecker cmd login --url "${PROJECT_URL}" "${CODECHECKER_USER}"
if [ $? -ne 0 ]; then
    echo "Error: Login to CodeChecker server failed"
    exit 1
fi


CodeChecker store --force --name "$RUN_NAME"  --url "${PROJECT_URL}" ${TAG_OPTION} "${REPORTS_DIR}"
if [ $? -ne 0 ]; then
    echo "Error: Storing results to CodeChecker server failed"
    exit 1
fi


echo "import suppressfile to server"
CodeChecker cmd suppress   -i suppressfile  --url "${PROJECT_URL}"  $RUN_NAME
if [ $? -ne 0 ]; then
    echo "Error: import suppressfile to server failed"
    exit 1
fi
echo "importing suppressfile completed"



echo "URL_PATH: $URL_PATH"
echo "$URL_PATH" > "${REPORTS_DIR}/serverpath.txt"

# Check if base run exists.
PREVIOUS_EXISTS=$(CodeChecker cmd runs --url "${PROJECT_URL}" --output csv | grep "${BASE_CODE}")
if [ -z "${PREVIOUS_EXISTS}" ]
then
  echo "Can't check if new bugs were introduced."
  echo "Error: Previous run \"${BASE_CODE}\" does not exist."
  CodeChecker cmd login --logout --url "${PROJECT_URL}" "${CODECHECKER_USER}"
  exit 1
fi


# Execute the diff command and handle its output.
DIFF_CMD=$(CodeChecker cmd diff --url ${PROJECT_URL}  --basename ${BASE_CODE}  --newname  "${REPORTS_DIR}"   --new)
if [ $? -ne 0 ]; then
    echo "Error: CodeChecker diff failed"
    CodeChecker cmd login --logout --url "${PROJECT_URL}" "${CODECHECKER_USER}"
    exit 1
fi
echo "DIFF_CMD: $DIFF_CMD"
DIFF_CMD_ERRORS=1

if echo "$DIFF_CMD" | grep -q " No results"; then
    DIFF_CMD_ERRORS=0
    echo "No bugs found "
fi
echo "$DIFF_CMD" > "${REPORTS_DIR}/bugs.txt"

# Investigate the below command
DIFF_CMD=$(CodeChecker cmd results --url ${PROJECT_URL} ${RUN_NAME})
echo "$DIFF_CMD" > "${REPORTS_DIR}/results.txt"


DIFF_CMD=$(CodeChecker cmd sum --url ${PROJECT_URL} -n ${RUN_NAME})
echo "$DIFF_CMD" > "${REPORTS_DIR}/summary.txt"



if [ $DIFF_CMD_ERRORS -eq 1 ]; then
  echo "New bugs introduced!"
  CodeChecker cmd login --logout --url "${PROJECT_URL}" "${CODECHECKER_USER}"
  exit 1
else
  echo "No new bugs! :)"
  CodeChecker cmd login --logout --url "${PROJECT_URL}" "${CODECHECKER_USER}"
  exit 0
fi

#!/bin/sh

ENV_FILE=$1

[ ! -f "${ENV_FILE}" ] && touch "${ENV_FILE}" || source "${ENV_FILE}"

replace_var() {
  FILE=$1
  VAR=$2
  VAL=$3
  touch "${FILE}"
  tmpfile=$(mktemp)
  awk "index(\$0, \"${VAR}=\") != 1 { print \$0 } END { print \"${VAR}=${VAL}\" }" "${FILE}" > $tmpfile
  mv "${tmpfile}" "${FILE}"
}

echo "FAIRshake API Key can be obtained by visiting https://fairshake.cloud/accounts/api_access/ when logged in you should have access to your key."
echo -n "FAIRSHAKE_API_KEY (current: \"$FAIRSHAKE_API_KEY\"): "
read FAIRSHAKE_API_KEY
[ "$FAIRSHAKE_API_KEY" != "" ] && replace_var "${ENV_FILE}" "FAIRSHAKE_API_KEY" "${FAIRSHAKE_API_KEY}"

echo "Github's API has strict limits and so you'll need to authenticate with your account. This can be done by creating a personal access token here: https://github.com/settings/tokens"
echo "The privileges I used were public_repo, read:org, and read:user"

echo -n "Github Username (current: \"$GITHUB_USERNAME\"): "
read GITHUB_USERNAME
[ "$GITHUB_USERNAME" != "" ] && replace_var "${ENV_FILE}" "GITHUB_USERNAME" "${GITHUB_USERNAME}"

echo -n "Github OAUTH Token (current: \"$GITHUB_OAUTH\"): "
read GITHUB_OAUTH
[ "$GITHUB_OAUTH" != "" ] && replace_var "${ENV_FILE}" "GITHUB_OAUTH" "${GITHUB_OAUTH}"

exit 0

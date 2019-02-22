#!/bin/sh
# depends:
# - curl
# - jq
# - python extruct

# Enumerate all repos from a github organization
org_repos() {
  ORG=$1
  CREDENTIALS=$2
  let N_REPOS=$(curl -u ${CREDENTIALS} "https://api.github.com/orgs/${ORG}" | jq '.public_repos')
  let CURRENT_PAGE=1
  let PER_PAGE=100
  while [ "$N_REPOS" -gt 0 ]; do
    curl -u ${CREDENTIALS} "https://api.github.com/orgs/${ORG}/repos?page=${CURRENT_PAGE}&per_page=${PER_PAGE}" \
      | jq -c '.[]'
    let N_REPOS="${N_REPOS}-${PER_PAGE}"
    let CURRENT_PAGE="${CURRENT_PAGE}+1"
  done
}

# Given repo JSON from github, crawl page for more JSON-LD
repo_extruct() {
  REPO=$1
  REPO_HTML_URL=$(echo "${REPO}" | jq -r '.html_url')
  python -m extruct "${REPO_HTML_URL}"
}

# Given repo JSON from github, obtain the root directory file list
repo_ls() {
  REPO=$1
  CREDENTIALS=$2
  REPO_API_URL=$(echo "${REPO}" | jq -r '.url')
  curl -u ${CREDENTIALS} "${REPO_API_URL}/contents/"
}

# Given an github organization, obtain all github and json-ld metadata available.
org_repo_metadata() {
  ENV_FILE=$1
  ORG=$2

  source "${ENV_FILE}"
  CREDENTIALS="${GITHUB_USERNAME}:${GITHUB_OAUTH}"

  org_repos "${ORG}" "${CREDENTIALS}" | jq -c '.' | while read REPO; do
    cat << EOF | jq -c '.'
{
  "github": ${REPO},
  "extruct": $(repo_extruct "${REPO}"),
  "ls": $(repo_ls "${REPO}" "${CREDENTIALS}")
}
EOF
  done
}

org_repo_metadata $@

# NCBI-Hackathon FAIR Assessment with FAIRshake

This project allows you to perform a automated FAIR assessment of the NCBI-Hackathon repositories on github with FAIRshake. It does so by crawling different parts of github.

A `Dockerfile`, `docker-compose.yml` and `Makefile` have all been designed to make running this project simple.

A `create_env.sh` walks you through building a `.env` file needed to perform the assessment; a [FAIRshake API Key](https://fairshake.cloud/accounts/api_access/) and a [Github OAuth Token](https://github.com/settings/tokens) will both be necessary.

A `github.sh` script extracts metadata for all repos in a github organization (in this case, NCBI-Hackathons as defined in the Makefile).

An `assessment.js` script uses the extracted github metadata to perform the assessment.

Finally the `fairshake.py` repurposed from FAIRshake's demo assessments, takes the resulting assessments and registers them on FAIRshake.

## docker-compose
```bash
docker-compose build
# Note that the other make arguments can be specified here
docker-compose run assessment commit
# Answer any prompts on screen until assessment is complete
```

## Dockerfile
```bash
docker build -t ncbi-hackathons-assessment .
# Note that the other make arguments can be specified here
docker run -it ncbi-hackathons-assessment commit
```

## Makefile
All dependencies need to be available to use the Makefile on your own system, these include; it may be simpler to use the Dockerfile which work with the same makefile commands at the end of it.

system deps:
- bash
- jq
- curl
- python3

python deps:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

javascript deps:
```
npm install
```

```bash
# Construct the env-file
make env

# Crawl github repos, creating a metadata.json
make work/metadata.json

# Use assess the fields available in metadata.json, constructing an assessment.json
make work/assessment.json

# Send the assessmens to FAIRshake
make commit
```

### Future Direction

This model can be formalized into a general framework for anyone to perform an automated assessment.

ORG=NCBI-Hackathons

.PRECIOUS: work/
workdir:
	mkdir -p work

.PRECIOUS: work/.env
work/.env: workdir
	./create_env.sh work/.env

.PHONY: env
env: work/.env

.PRECIOUS: work/metadata.json
work/metadata.json: work/.env github.sh
	./github.sh work/.env "$(ORG)" > work/metadata.json

.PRECIOUS: work/assessment.json
work/assessment.json: assessment.js work/metadata.json
	npx babel-node assessment.js < work/metadata.json > work/assessment.json

commit: work/.env work/assessment.json
	ENV_FILE=work/.env python ./fairshake.py work/assessment.json

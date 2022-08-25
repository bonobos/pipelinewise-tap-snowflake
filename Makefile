
deploy_package:
	@poetry build
	@s3pypi --bucket deg-shared-services-pypi-us-east-1 --private --secret ${S3PYPI_SECRET} --dist-path dist

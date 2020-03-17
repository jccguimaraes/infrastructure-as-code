```bash
aws cloudformation package \
  --template-file main.yaml \
  --s3-bucket io.yld.cf.joao \
  --output-template-file packaged.yaml \
  --profile $AWS_PROFILE

aws cloudformation deploy \
  --stack-name stack-demo \
  --template-file packaged.yaml \
  --capabilities CAPABILITY_IAM \
  --profile $AWS_PROFILE

aws cloudformation deploy \
  --stack-name stack-demo-test \
  --template-file test.yaml \
  --capabilities CAPABILITY_IAM \
  --profile $AWS_PROFILE
```

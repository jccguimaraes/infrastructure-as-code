exports.handler = async evt => {
  const requestId = evt.requestId
  const status = 'SUCCESS'

  const fragment = {
    Resources: {
      MyVPC: {
        Type: 'AWS::EC2::VPC',
        Properties: {
          CidrBlock: '10.1.0.0/16',
          Tags: [{
            Key: 'Name',
            Value: 'my-vpc'
          }]
        }
      }
    }
  }

	return { requestId, status, fragment }
}
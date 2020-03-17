# Google Cloud Platform - Cloud Development Manager - Step 2

This iteration consists on adding a subnetwork `my_subnet` to an already existing vpc `my_vpc` as the previous [Step 1](https://github.com/jccguimaraes/infrastructure-as-code/tree/master/gcp/cdm-example-01) with the exception we will acquire the `my_vpc` resource into the deployment.

This demo has the following Deployment Manager configuration:

```yaml
resources:
- name: my-vpc
  type: compute.v1.network
  properties:
    autoCreateSubnetworks: false
- name: my-subnet
  type: compute.v1.subnetwork
  properties:
    region: europe-west3
    ipCidrRange: 10.2.0.0/16
    network: $(ref.my_vpc.selfLink)
```

or

```json
{
  "resources": [
    {
      "name": "my_vpc",
      "type": "compute.v1.network",
      "properties": {
        "autoCreateSubnetworks": false
      }
    },
    {
      "name": "my_subnet",
      "type": "compute.v1.subnetwork",
      "properties": {
        "region": "europe-west3",
        "ipCidrRange": "10.2.0.0/16",
        "network": "$(ref.my_vpc.selfLink)"
      }
    }
  ]
}
```

```bash
gcloud deployment-manager deployments create cdm-example-02 --config main.yaml --preview
```

or

```bash
gcloud deployment-manager deployments create cdm-example-02 --config main.json --preview
```

<pre>
The fingerprint of the deployment is zBQM97eP8KLkuBBHDszweQ==
Waiting for create [operation-1584232735236-5a0d9ed6ce22f-1df74e8c-ff2592cb]...done.
Create operation operation-1584232735236-5a0d9ed6ce22f-1df74e8c-ff2592cb completed successfully.
NAME       TYPE                   STATE       ERRORS  INTENT
my_subnet  compute.v1.subnetwork  IN_PREVIEW  []      CREATE_OR_ACQUIRE
my_vpc     compute.v1.network     IN_PREVIEW  []      CREATE_OR_ACQUIRE
</pre>

> Keep in mind that we will take ownership of (acquire the) `my_vpc` resource.

```bash
gcloud deployment-manager deployments update cdm-example-02
```

<pre>
The fingerprint of the deployment is mHIcAlc5DVXSPPbLtLAlkA==
Waiting for update [operation-1584233608869-5a0da217f7844-0c71d40a-0f587aba]...done.
Update operation operation-1584233608869-5a0da217f7844-0c71d40a-0f587aba completed successfully.
NAME       TYPE                   STATE      ERRORS  INTENT
my_subnet  compute.v1.subnetwork  COMPLETED  []
my_vpc     compute.v1.network     COMPLETED  []
</pre>

> Keep in mind that we took ownership of (acquire the) `my_vpc` resource.

```bash
gcloud deployment-manager deployments delete cdm-example-02
```

<pre>
The following deployments will be deleted:
- cdm-example-02

Do you want to continue (y/N)?  y

Waiting for delete [operation-1584233736618-5a0da291cc107-44463ef2-f56be12e]...done.
Delete operation operation-1584233736618-5a0da291cc107-44463ef2-f56be12e completed successfully.
</pre>
# Google Cloud Platform - Cloud Development Manager - Step 1

This iteration consists on adding a subnetwork `my-subnet` to an already existing vpc `my-vpc`.

This VPC network was created through the GCP console as per the following images.

On the left menu go to `VPC network` and click on the `Create VPC network`.

![step-1][step-1]

Add `my-vpc` as the name and leave the rest as per the next image.

![step-1][step-2]

Validate the vpc was created.

![step-1][step-3]
![step-1][step-4]

Initial setup (will be valid for all other steps / examples):

In order to use `gcloud` we create a service account with the following `Compute Network Admin` role.

![step-0-0][step-0-0]
![step-0-1][step-0-1]
![step-0-2][step-0-2]
![step-0-3][step-0-3]

For simplicity, download the JSON credentials from the service account and set the following environment variables:

![step-0-4][step-0-4]

Configure the `gcloud` CLI.

```bash
# set accordingly with your settings
gcloud auth activate-service-account --key-file path/to/credentials
gcloud config set core/project personal-265109

gcloud config list
```

Which should output something close to:

```text
[core]
account = terraform-automation@personal-265109.iam.gserviceaccount.com
disable_usage_reporting = True
project = personal-265109

Your active configuration is: [default]
```

> If you don't create a VPC network as above, you'll get this error when deploying.
>
> <pre>
> The fingerprint of the deployment is 4geOghpV3CvGzk1dBDoIJg==
> Waiting for create [operation-1584231360600-5a0d99b7d987a-6102a252-fa0a163c]...failed.
> ERROR: (gcloud.deployment-manager.deployments.create) Error in Operation [operation-1584231360600-5a0d99b7d987a-6102a252-fa0a163c]: errors:
> - code: RESOURCE_ERROR
>   location: /deployments/deployment-demo-1/resources/my-subnet
>   message: '{"ResourceType":"compute.v1.subnetwork","ResourceErrorCode":"404","ResourceErrorMessage":{"code":404,"message":"Requested
>     entity was not found.","status":"NOT_FOUND","statusMessage":"Not Found","requestPath":"https://compute.googleapis.com/compute/v1/projects/personal-265109/regions/europe-
> west3/subnetworks","httpMethod":"POST"}}'
> </pre>

This demo has the following Deployment Manager configuration:

```yaml
resources:
- name: my-subnet
  type: compute.v1.subnetwork
  properties:
    region: europe-west3
    ipCidrRange: 10.2.0.0/16
    network: "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my-vpc"
```

or the JSON alternative:

```json
{
  "resources": [
    {
      "name": "my-subnet",
      "type": "compute.v1.subnetwork",
      "properties": {
        "region": "europe-west3",
        "ipCidrRange": "10.2.0.0/16",
        "network": "https://www.googleapis.com/compute/v1/projects/personal-265109/global/networks/my-vpc"
      }
    }
  ]
}
```

In order to preview what will be created, run the following command:

```bash
gcloud deployment-manager deployments create cdm-example-01 --config main.yaml --preview
```

or

```bash
gcloud deployment-manager deployments create cdm-example-01 --config main.json --preview
```

> You may need to switch from `create` to `update` if you already created the deployment (which throwed an error).

This will output the following:

<pre>
The fingerprint of the deployment is 8eHnt6HjwuvGjjCWSJ6lUw==
Waiting for create [operation-1584231636887-5a0d9abf56845-1b42dc3d-4f3dab24]...done.  
Create operation operation-1584231636887-5a0d9abf56845-1b42dc3d-4f3dab24 completed successfully.
NAME       TYPE                   STATE       ERRORS  INTENT
my-subnet  compute.v1.subnetwork  IN_PREVIEW  []      CREATE_OR_ACQUIRE
</pre>

This means that it will try to `create` or `acquire` if the resource does not exists already. In this case will the first case.

![step-6][step-6]

Running:

```bash
gcloud deployment-manager deployments update cdm-example-01
```

Will deploy the subnet as the output confirms it.

<pre>
The fingerprint of the deployment is 6JmkucS5_f5KduZpgPUtHw==
Waiting for update [operation-1584231859017-5a0d9b932d572-07742ec7-158ffca3]...done.
Update operation operation-1584231859017-5a0d9b932d572-07742ec7-158ffca3 completed successfully.
NAME       TYPE                   STATE      ERRORS  INTENT
my-subnet  compute.v1.subnetwork  COMPLETED  []
</pre>

![step-5][step-5]
![step-7][step-7]
![step-8][step-8]

Destroying the `my-subnet` is easy as simply deleting the deployment itself.

```bash
gcloud deployment-manager deployments delete cdm-example-01
```

As per the output:

<pre>
The following deployments will be deleted:
- deployment-demo-1

Do you want to continue (y/N)?  y

Waiting for delete [operation-1584231337249-5a0d99a194a82-f6aa6b22-0d2f968d]...done.

Delete operation operation-1584231337249-5a0d99a194a82-f6aa6b22-0d2f968d completed successfully.
</pre>

Next go to [Step 2](https://github.com/jccguimaraes/infrastructure-as-code/tree/master/gcp/cdm-example-02)!

[step-0-0]: ./assets/step-0-0.jpg "step 0-0"
[step-0-1]: ./assets/step-0-1.jpg "step 0-1"
[step-0-2]: ./assets/step-0-2.jpg "step 0-2"
[step-0-3]: ./assets/step-0-3.jpg "step 0-3"
[step-0-4]: ./assets/step-0-4.jpg "step 0-4"
[step-1]: ./assets/step-1.jpg "step 1"
[step-2]: ./assets/step-2.jpg "step 2"
[step-3]: ./assets/step-3.jpg "step 3"
[step-4]: ./assets/step-4.jpg "step 4"
[step-5]: ./assets/step-5.jpg "step 5"
[step-6]: ./assets/step-6.jpg "step 6"
[step-7]: ./assets/step-7.jpg "step 7"
[step-8]: ./assets/step-8.jpg "step 8"
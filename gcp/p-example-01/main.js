const gcp = require('@pulumi/gcp');

const network = new gcp.compute.Network("network");
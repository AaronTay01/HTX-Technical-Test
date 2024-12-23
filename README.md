# HTX-Technical-Test

This project contains a deployment setup with Docker for **Elasticsearch** and **Kibana** running on an EC2 instance. The application uses Amazon Elastic Container Registry (ECR) for container management.

## Deployment Overview

The deployment consists of the following services:

- **Elasticsearch** (2 nodes)
- **Kibana**
- **Frontend (Node.js app)**

The containers are deployed on an EC2 instance, and the services are exposed through ports 80 and 8000 for public access.

## Deployment URL

You can access the deployed services via the following URL:

- **Frontend App**: `http://<EC2_PUBLIC_IP>:80`
- **Kibana**: `http://<EC2_PUBLIC_IP>:5601`
- **Elasticsearch**: `http://<EC2_PUBLIC_IP>:9200`

**Note**: Replace `52.221.197.118` with the actual public IP address of your EC2 instance.

## Setting Up the Environment

### Prerequisites

1. **EC2 Instance** running in AWS with Docker installed.
2. **AWS CLI** configured on your EC2 instance to access Amazon ECR.
3. **Security Group Configuration**: Ensure that the required ports (80, 8000, 9200, 5601) are open to the public in your EC2 instance's security group.

### Steps for Deployment

1. **Log into your EC2 instance**:

   Ensure you have SSH access to your EC2 instance.

   ```bash
   ssh -i <your-key.pem> ec2-user@<EC2_PUBLIC_IP>

2. **Authenticate Docker with ECR**:

    ```bash
    aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com

3. **Pull the Docker Image from ECR**:

    ```bash
    docker pull <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com/htx-technical-test

4. **Run the Docker Container**:

    ```bash
    docker run -d \
    --name my-container \
    -p 80:80 \
    -p 8000:8000 \
    <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com/htx-technical-test

5. **Verify the Deployment**:

    ```bash
    docker ps

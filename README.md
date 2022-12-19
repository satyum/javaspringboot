# A custom Cloud Template Generator in python and java spring end to end deployment


## deploying Image by building and pushing it to ecr in jenkins
```
* docker build -t awsaccountnumber.dkr.ecr.us-east-1.amazonaws.com/springboot:latest . 
* aws ecr create-repository --repository-name springboot --region us-east-1
* aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 6xxxxxxxxx2.dkr.ecr.us-east-1.amazonaws.com
* docker push awsaccountnumber.dkr.ecr.us-east-1.amazonaws.com/springboot:latest
```
## Templates
* Network cloudformation template [network Template](https://github.com/satyum/javaspringboot/blob/master/templates/vpc.yml)
* rds cloudformation template [rds Template](https://github.com/satyum/javaspringboot/blob/master/templates/rds.yml)



### Steps For deploying on AWS ECS

Use Region <b>us-east-1</b> or you can change accordingly
-----------------------------------------------------------------------------------------------------------------------------------------------
### Now run cloud formtion template for creating VPC
```
aws cloudformation create-stack --stack-name vpc --template-body file://vpc.yml --region=us-east-1
```
By this stack, get some Export value
So, use that values to any resource from this VPC
```
Outputs:
  VPCid:
    Description: The VPCid
    Value: !Ref VPC
    Export:
      Name: VPC

  PublicSub1:
    Description: public subnet 1
    Value: !Ref PublicSubnet1
    Export:
      Name: PublicSubnet1

  PublicSub2:
    Description: public subnet  2
    Value: !Ref PublicSubnet2
    Export:
      Name: PublicSubnet2

  PrivateSub1:
    Description: private subnet 1
    Value: !Ref PrivateSubnet1
    Export:
      Name: PrivateSubnet1

  PrivateSub2:
    Description: private subnet 2
    Value: !Ref PrivateSubnet2
    Export:
      Name: PrivateSubnet2
```
### Run another cloud formation for RDS 
```
aws cloudformation create-stack --stack-name rds --template-body file://rds.yml  --region=us-east-1 --capabilities CAPABILITY_NAMED_IAM
```
From this , got the Endpoint of RDS and store that in Export
```
  DBEndpoint:
    Description: The connection endpoint for the database.
    Value: !GetAtt  DBinstance.Endpoint.Address
    Export:
      Name: DBEndPoint 
```
### Now Run the final stack for deploying the ECS Infra using following CLI command 
```
aws cloudformation create-stack --stack-name ecs --template-body file://ecs.yml --parameters ParameterKey=ImageUrl,ParameterValue=<image> --capabilities CAPABILITY_NAMED_IAM --region=us-east-1
```


## Check loadbalancer for hiting spring app api
* Add /swagger-ui.html at the end of the dns to hit the main url


![image](https://user-images.githubusercontent.com/54767390/208317697-1b7a81c5-de64-4a49-97d4-98839d87421a.png)



![image](https://user-images.githubusercontent.com/54767390/208317833-808b591f-1c2c-4adf-b57e-729a6af953ba.png)






## install all the required packages 

``` pip install -r requirements.txt```

# ecs custom parameter template to auto-populate the ecs service file by using python script mentioned above
*  ecs custom parameter template [ecs Template](https://github.com/satyum/javaspringboot/blob/master/parameters/ecs.yml)

## Parameters for ecs template passing through custom parameter file
* Image
* ServiceName
* ContainerPort
* LoadBalancerPort
* HealthCheckPath
* MinContainers
* MaxContainers

## deploy the pipeline for ecs service
```groovy
pipeline {
    agent any
     stages {
        stage('Git checkout1') {
          steps{
                git branch: 'master', credentialsId: '', url: 'https://github.com/satyum/javaspringboot.git'
                sh'ls -lat'
            }
        }

        
        stage('validation') {
          steps{
              sh 'python3 templ.py ecs.yml'
              sh 'cat output/ecs.yml'
              sh'aws cloudformation  validate-template --template-body file://output/ecs.yml'              
            }
        }
               
    }
}
```

___________________________________________________________________________________________________________________________________

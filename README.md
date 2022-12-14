# A custom Cloud Template Generator in python and java spring end to end deployment
![alt text](https://www.python.org/static/img/python-logo.png)


 Python code for [Template generator](https://github.com/satyum/javaspringboot/blob/master/templ.py)
 
 ## Feature
 
 * Detect templates according to the parameter file automatically
 * For example : sns-param.yml will automatically detect and generate the sns template


## Note : 
* you can change username and password of springboot application from application.yml before deploying the image

![sring_config](https://github.com/satyum/javaspringboot/blob/master/pictures/conf.png)

## deploying Image by building and pushing it to ecr in jenkins
```
* docker build -t awsaccountnumber.dkr.ecr.us-east-1.amazonaws.com/spring:latest . 
* aws ecr create-repository --repository-name springboot --region us-east-1
* aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 6xxxxxxxxx2.dkr.ecr.us-east-1.amazonaws.com
* docker push awsaccountnumber.dkr.ecr.us-east-1.amazonaws.com/spring:latest
```
## deploy network and rds for any application using network and rds template in templates folder
* Network cloudformation template [network Template](https://github.com/satyum/javaspringboot/blob/master/templates/rds.yml)
* rds cloudformation template [rds Template](https://github.com/satyum/javaspringboot/blob/master/templates/vpc.yml)


## Now things needed to be installed in jenkins server

* python 
* pip (for installing requirement.txt)
* aws cli

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
## Check loadbalancer for hiting spring app api
* Add /swagger-ui.html at the end of the dns to hit the main url

# A custom Cloud Template Generator in python and java spring end to end deployment
![alt text](https://www.python.org/static/img/python-logo.png)


 Python code for [Template generator](https://github.com/satyum/javaspringboot/blob/master/templ.py)
 
 ## Feature
 
 * Detect templates according to the parameter file automatically
 * For example : sns-param.yml will automatically detect and generate the sns template

## Things needed to be installed in jenkins server

* python 
* pip (for installing requirement.txt)
* aws cli

## install all the required packages 

``` pip install -r requirements.txt```

## Parameters for ecs template 
* Image
* ServiceName
* ContainerPort
* LoadBalancerPort
* HealthCheckPath
* MinContainers
* MaxContainers

## deploying Image by building and pushing it to ecr in jenkins
```
pipeline {
    agent any
     stages {
        stage('Git checkout1') {
          steps{
                git branch: 'master', credentialsId: '', url: 'https://github.com/satyum/javaspringboot.git'
            }
        }
         stage('build image') {
          steps{
              sh'docker build -t 607966531582.dkr.ecr.us-east-1.amazonaws.com/spring:${BUILD_NUMBER} . '
                }
        }
        stage('push image') {
          steps{
             sh'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 607966531582.dkr.ecr.us-east-1.amazonaws.com'
             sh'docker push 607966531582.dkr.ecr.us-east-1.amazonaws.com/spring:${BUILD_NUMBER}'
                }
        }  
        stage('validation') {
          steps{
              sh 'python3 templ.py ecs.yml'
              sh'aws cloudformation validate-template --template-body file://output/ecs.yml'              
            }
        }
        stage('submit stack') {
          steps{               
              sh'aws cloudformation create-stack --stack-name ecs --template-body file://output/ecs.yml --parameters ParameterKey=Image1,ParameterValue=${image}:${BUILD_NUMBER} --capabilities CAPABILITY_NAMED_IAM'
            }
        }                
    }
}
```
## deploy network and rds for any application using network and rds template in templates folder
* Network cloudformation template [network Template](https://github.com/satyum/javaspringboot/blob/master/templates/rds.yml)
* rds cloudformation template [rds Template](https://github.com/satyum/javaspringboot/blob/master/templates/vpc.yml)

## Note : 
* you can change username and password of application from application.yml

![sring_config](https://github.com/satyum/javaspringboot/blob/master/pictures/conf.png)

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

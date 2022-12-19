#  Java springboot and rds end to end deployment


## deploying Image by building and pushing it to ecr 
```
 aws account number = 6xxxxxxxxx2
 
Use this command to build the image where dockerfile is:
* docker build -t 6xxxxxxxxx2.dkr.ecr.us-east-1.amazonaws.com/springboot:latest . 

Create ecr repository
* aws ecr create-repository --repository-name springboot --region us-east-1

Get Login access for ecr for few hours to push image
* aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 6xxxxxxxxx2.dkr.ecr.us-east-1.amazonaws.com

push the image to the ecr
* docker push 6xxxxxxxxx2.dkr.ecr.us-east-1.amazonaws.com/springboot:latest
```
## Templates
* Network cloudformation template [network Template](https://raw.githubusercontent.com/satyum/javaspringboot/master/templates/vpc.yml)
* rds cloudformation template [rds Template](https://raw.githubusercontent.com/satyum/javaspringboot/master/templates/rds.yml)
* ecs cloudformation template [ecs Template](https://raw.githubusercontent.com/satyum/javaspringboot/master/templates/ecs.yml)
 
 ## Note
please change the parameter for dnsendpoint,database,database user and database password with your aws account number in  rds cloudformation template [rds Template](https://raw.githubusercontent.com/satyum/javaspringboot/master/templates/rds.yml)


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


![dns](https://github.com/satyum/javaspringboot/blob/master/pictures/Screenshot%20from%202022-12-19%2012-33-28.png)



![mainroute](https://github.com/satyum/javaspringboot/blob/master/pictures/Screenshot%20from%202022-12-19%2012-33-28.png)



___________________________________________________________________________________________________________________________________

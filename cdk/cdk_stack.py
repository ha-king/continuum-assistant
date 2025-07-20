import json
from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_cognito as cognito,
    aws_secretsmanager as secretsmanager,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_elasticloadbalancingv2 as elbv2,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    Duration,
    RemovalPolicy,
    SecretValue,
    CfnOutput,
)
from constructs import Construct
from docker_app.config_file import Config

CUSTOM_HEADER_NAME = "X-Custom-Header"

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env_name: str = "prod", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.env_name = env_name

        # Define prefix that will be used in some resource names
        prefix = f"{Config.STACK_NAME}{env_name.title()}"

        # Create Cognito user pool
        user_pool = cognito.UserPool(self, f"{prefix}UserPool")

        # Create Cognito client
        user_pool_client = cognito.UserPoolClient(self, f"{prefix}UserPoolClient",
                                                  user_pool=user_pool,
                                                  generate_secret=True
                                                  )

        # Always use existing secret if it exists
        secret_name = f"{Config.SECRETS_MANAGER_ID}-{env_name}"
        
        # Use a different logical ID to avoid conflict with existing resource
        # This is the key change - using ExistingParamCognitoSecret instead of ParamCognitoSecret
        secret = secretsmanager.Secret.from_secret_name_v2(
            self, f"{prefix}ExistingParamCognitoSecret",
            secret_name=secret_name
        )
        
        # Note: We're not updating the secret automatically anymore.
        # After deployment, you'll need to manually update the secret with the new Cognito details:
        # - User pool ID: {user_pool.user_pool_id}
        # - App client ID: {user_pool_client.user_pool_client_id}
        # This can be done through the AWS Console or using the AWS CLI.


        # VPC for ALB and ECS cluster
        vpc = ec2.Vpc(
            self,
            f"{prefix}AppVpc",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            vpc_name=f"{prefix}-stl-vpc",
            nat_gateways=1,
        )

        ecs_security_group = ec2.SecurityGroup(
            self,
            f"{prefix}SecurityGroupECS",
            vpc=vpc,
            security_group_name=f"{prefix}-stl-ecs-sg",
        )

        alb_security_group = ec2.SecurityGroup(
            self,
            f"{prefix}SecurityGroupALB",
            vpc=vpc,
            security_group_name=f"{prefix}-stl-alb-sg",
        )

        ecs_security_group.add_ingress_rule(
            peer=alb_security_group,
            connection=ec2.Port.tcp(8501),
            description="ALB traffic",
        )

        # ECS cluster and service definition
        cluster = ecs.Cluster(
            self,
            f"{prefix}Cluster",
            enable_fargate_capacity_providers=True,
            vpc=vpc)

        # ALB to connect to ECS
        alb = elbv2.ApplicationLoadBalancer(
            self,
            f"{prefix}Alb",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name=f"{prefix}-stl",
            security_group=alb_security_group,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )

        fargate_task_definition = ecs.FargateTaskDefinition(
            self,
            f"{prefix}WebappTaskDef",
            memory_limit_mib=1024,
            cpu=512,
        )

        # Build Dockerfile from local folder and push to ECR
        image = ecs.ContainerImage.from_asset('docker_app')

        fargate_task_definition.add_container(
            f"{prefix}WebContainer",
            # Use an image from DockerHub
            image=image,
            port_mappings=[
                ecs.PortMapping(
                    container_port=8501,
                    protocol=ecs.Protocol.TCP)],
            logging=ecs.LogDrivers.aws_logs(stream_prefix="WebContainerLogs"),
            environment={
                "ENVIRONMENT": env_name,
                "CONVERSATION_TABLE": "user-conversations",
                "CONVERSATION_BUCKET": f"user-conversations-data-{self.account}-{self.region}",
                "USER_PROFILES_TABLE": "user-profiles",
                "RESPONSE_CACHE_TABLE": "response-cache",
                "AWS_REGION": self.region
            }
        )

        service = ecs.FargateService(
            self,
            f"{prefix}ECSService",
            cluster=cluster,
            task_definition=fargate_task_definition,
            service_name=f"{prefix}-stl-front",
            security_groups=[ecs_security_group],
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
        )

        # Grant access to Bedrock
        bedrock_policy = iam.Policy(
            self,
            f"{prefix}BedrockPolicy",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "bedrock:InvokeModel",
                        "bedrock:InvokeModelWithResponseStream",
                        "bedrock:RetrieveAndGenerate",
                        "bedrock:Retrieve",
                        "ssm:GetParameter"
                    ],
                    resources=["*"]
                )
            ]
        )
        task_role = fargate_task_definition.task_role
        task_role.attach_inline_policy(bedrock_policy)

        # Grant access to read the secret in Secrets Manager
        secret.grant_read(task_role)
        
        # Create DynamoDB tables
        # 1. User Conversations table
        conversation_table = dynamodb.Table(
            self, f"{prefix}ConversationTable",
            table_name="user-conversations",
            partition_key=dynamodb.Attribute(
                name="conversation_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN,  # Retain data when stack is deleted
            time_to_live_attribute="expiry_time"
        )
        
        # 2. User Profiles table
        profiles_table = dynamodb.Table(
            self, f"{prefix}UserProfilesTable",
            table_name="user-profiles",
            partition_key=dynamodb.Attribute(
                name="user_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN  # Retain data when stack is deleted
        )
        
        # 3. Response Cache table
        cache_table = dynamodb.Table(
            self, f"{prefix}ResponseCacheTable",
            table_name="response-cache",
            partition_key=dynamodb.Attribute(
                name="cache_key",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,  # Cache can be safely destroyed
            time_to_live_attribute="ttl"  # Enable TTL for automatic cleanup
        )
        
        # 4. Create S3 bucket for conversation data storage
        conversation_bucket = s3.Bucket(
            self, f"{prefix}ConversationBucket",
            bucket_name=f"user-conversations-data-{self.account}-{self.region}",
            removal_policy=RemovalPolicy.RETAIN,  # Retain data when stack is deleted
            lifecycle_rules=[
                s3.LifecycleRule(
                    expiration=Duration.days(30),  # Auto-delete after 30 days
                    enabled=True
                )
            ],
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )
        
        # Add policy for DynamoDB access to all tables
        dynamodb_policy = iam.Policy(
            self,
            f"{prefix}DynamoDBPolicy",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "dynamodb:PutItem",
                        "dynamodb:GetItem",
                        "dynamodb:DeleteItem",
                        "dynamodb:Query",
                        "dynamodb:Scan"
                    ],
                    resources=[
                        conversation_table.table_arn,
                        f"{conversation_table.table_arn}/index/*",
                        profiles_table.table_arn,
                        f"{profiles_table.table_arn}/index/*",
                        cache_table.table_arn,
                        f"{cache_table.table_arn}/index/*"
                    ]
                )
            ]
        )
        task_role.attach_inline_policy(dynamodb_policy)
        
        # Add policy for S3 access
        s3_policy = iam.Policy(
            self,
            f"{prefix}S3Policy",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "s3:PutObject",
                        "s3:GetObject",
                        "s3:DeleteObject",
                        "s3:ListBucket"
                    ],
                    resources=[
                        conversation_bucket.bucket_arn,
                        f"{conversation_bucket.bucket_arn}/*"
                    ]
                )
            ]
        )
        task_role.attach_inline_policy(s3_policy)

        # Add ALB as CloudFront Origin
        origin = origins.LoadBalancerV2Origin(
            alb,
            custom_headers={CUSTOM_HEADER_NAME: Config.CUSTOM_HEADER_VALUE},
            origin_shield_enabled=False,
            protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
        )

        cloudfront_distribution = cloudfront.Distribution(
            self,
            f"{prefix}CfDist",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origin,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,
                origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER,
            ),
        )

        # ALB Listener
        http_listener = alb.add_listener(
            f"{prefix}HttpListener",
            port=80,
            open=True,
        )

        http_listener.add_targets(
            f"{prefix}TargetGroup",
            target_group_name=f"{prefix}-tg",
            port=8501,
            priority=1,
            conditions=[
                elbv2.ListenerCondition.http_header(
                    CUSTOM_HEADER_NAME,
                    [Config.CUSTOM_HEADER_VALUE])],
            protocol=elbv2.ApplicationProtocol.HTTP,
            targets=[service],
        )
        # add a default action to the listener that will deny all requests that
        # do not have the custom header
        http_listener.add_action(
            "default-action",
            action=elbv2.ListenerAction.fixed_response(
                status_code=403,
                content_type="text/plain",
                message_body="Access denied",
            ),
        )

        # Output CloudFront URL
        CfnOutput(self, "CloudFrontDistributionURL",
                  value=cloudfront_distribution.domain_name)
        # Output Cognito pool id
        CfnOutput(self, "CognitoPoolId",
                  value=user_pool.user_pool_id)

        # CI/CD Pipeline for both environments
        # GitHub token secret
        github_token = secretsmanager.Secret.from_secret_name_v2(
            self, f"{prefix}GitHubToken",
            secret_name="github-token"
        )

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        # CodeBuild project
        build_project = codebuild.Project(
            self, f"{prefix}Build",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "install": {
                        "runtime-versions": {
                            "python": "3.12",
                            "nodejs": "20"
                        },
                        "commands": [
                            "npm install -g aws-cdk",
                            "pip install aws-cdk-lib constructs"
                        ]
                    },
                    "build": {
                        "commands": [
                            f"cdk deploy {construct_id} --app 'python3 app_dev.py' --require-approval never" if env_name == "dev" else "cdk deploy --require-approval never"
                        ]
                    }
                }
            }),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_7_0,
                privileged=True
            )
        )

        # Add permissions for CDK deployment
        build_project.add_to_role_policy(iam.PolicyStatement(
            actions=["*"],
            resources=["*"]
        ))

        # Pipeline
        pipeline = codepipeline.Pipeline(
            self, f"{prefix}Pipeline",
            stages=[
                codepipeline.StageProps(
                    stage_name="Source",
                    actions=[
                        codepipeline_actions.GitHubSourceAction(
                            action_name="GitHub_Source",
                            owner="ha-king",
                            repo="continuum-assistant",
                            branch="main" if env_name == "prod" else "dev",
                            oauth_token=github_token.secret_value,
                            output=source_output
                        )
                    ]
                ),
                codepipeline.StageProps(
                    stage_name="Build",
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            action_name="Build",
                            project=build_project,
                            input=source_output,
                            outputs=[build_output]
                        )
                    ]
                )
            ]
        )

        CfnOutput(self, "PipelineArn", value=pipeline.pipeline_arn)
        
        CfnOutput(self, "Environment", value=env_name)

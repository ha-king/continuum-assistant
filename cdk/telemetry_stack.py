"""
Telemetry Stack - AWS resources for telemetry
"""

from aws_cdk import (
    Stack,
    aws_logs as logs,
    aws_cloudwatch as cloudwatch,
    aws_kinesisfirehose as firehose,
    aws_iam as iam,
    aws_s3 as s3,
    aws_glue as glue,
    aws_athena as athena,
    RemovalPolicy,
    Duration,
)
from constructs import Construct

class TelemetryStack(Stack):
    """CDK Stack for telemetry resources"""
    
    def __init__(self, scope: Construct, construct_id: str, env_name: str = "prod", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Define prefix for resource names
        prefix = f"continuum-assistant-{env_name}"
        
        # Create S3 bucket for telemetry data
        telemetry_bucket = s3.Bucket(
            self, 
            f"{prefix}-telemetry-bucket",
            bucket_name=f"{prefix}-telemetry",
            removal_policy=RemovalPolicy.RETAIN,
            lifecycle_rules=[
                s3.LifecycleRule(
                    transitions=[
                        s3.Transition(
                            storage_class=s3.StorageClass.INTELLIGENT_TIERING,
                            transition_after=Duration.days(30)
                        ),
                        s3.Transition(
                            storage_class=s3.StorageClass.GLACIER,
                            transition_after=Duration.days(90)
                        )
                    ],
                    expiration=Duration.days(365)
                )
            ]
        )
        
        # Create CloudWatch Log Group
        log_group = logs.LogGroup(
            self,
            f"{prefix}-log-group",
            log_group_name=f"/aws/lambda/{prefix}",
            retention=logs.RetentionDays.ONE_MONTH,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # Create IAM role for Firehose
        firehose_role = iam.Role(
            self,
            f"{prefix}-firehose-role",
            assumed_by=iam.ServicePrincipal("firehose.amazonaws.com")
        )
        
        # Grant permissions to the role
        telemetry_bucket.grant_write(firehose_role)
        
        # Create Firehose delivery stream
        delivery_stream = firehose.CfnDeliveryStream(
            self,
            f"{prefix}-delivery-stream",
            delivery_stream_name=f"{prefix}-telemetry",
            s3_destination_configuration=firehose.CfnDeliveryStream.S3DestinationConfigurationProperty(
                bucket_arn=telemetry_bucket.bucket_arn,
                role_arn=firehose_role.role_arn,
                prefix="telemetry/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/",
                error_output_prefix="errors/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/!{firehose:error-output-type}/",
                buffering_hints=firehose.CfnDeliveryStream.BufferingHintsProperty(
                    interval_in_seconds=60,
                    size_in_m_bs=5
                ),
                compression_format="GZIP"
            )
        )
        
        # Create Glue Database
        glue_database = glue.CfnDatabase(
            self,
            f"{prefix}-glue-database",
            catalog_id=self.account,
            database_input=glue.CfnDatabase.DatabaseInputProperty(
                name=f"{prefix.replace('-', '_')}_telemetry"
            )
        )
        
        # Create Glue Table for user interactions
        user_interactions_table = glue.CfnTable(
            self,
            f"{prefix}-user-interactions-table",
            catalog_id=self.account,
            database_name=glue_database.ref,
            table_input=glue.CfnTable.TableInputProperty(
                name="user_interactions",
                storage_descriptor=glue.CfnTable.StorageDescriptorProperty(
                    location=f"s3://{telemetry_bucket.bucket_name}/telemetry/",
                    input_format="org.apache.hadoop.mapred.TextInputFormat",
                    output_format="org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                    serde_info=glue.CfnTable.SerdeInfoProperty(
                        serialization_library="org.openx.data.jsonserde.JsonSerDe"
                    ),
                    columns=[
                        glue.CfnTable.ColumnProperty(name="event_id", type="string"),
                        glue.CfnTable.ColumnProperty(name="timestamp", type="bigint"),
                        glue.CfnTable.ColumnProperty(name="user_id", type="string"),
                        glue.CfnTable.ColumnProperty(name="event_type", type="string"),
                        glue.CfnTable.ColumnProperty(name="query_length", type="int"),
                        glue.CfnTable.ColumnProperty(name="query_type", type="string"),
                        glue.CfnTable.ColumnProperty(name="assistant_used", type="string"),
                        glue.CfnTable.ColumnProperty(name="response_time_ms", type="int"),
                        glue.CfnTable.ColumnProperty(name="environment", type="string"),
                        glue.CfnTable.ColumnProperty(name="app_version", type="string")
                    ]
                ),
                partition_keys=[
                    glue.CfnTable.ColumnProperty(name="year", type="string"),
                    glue.CfnTable.ColumnProperty(name="month", type="string"),
                    glue.CfnTable.ColumnProperty(name="day", type="string")
                ]
            )
        )
        
        # Create Athena Workgroup
        athena_workgroup = athena.CfnWorkGroup(
            self,
            f"{prefix}-athena-workgroup",
            name=f"{prefix}-analytics",
            description="Workgroup for analyzing telemetry data",
            state="ENABLED",
            work_group_configuration=athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                result_configuration=athena.CfnWorkGroup.ResultConfigurationProperty(
                    output_location=f"s3://{telemetry_bucket.bucket_name}/athena-results/"
                ),
                publish_cloud_watch_metrics_enabled=True
            )
        )
        
        # Create CloudWatch Dashboard
        dashboard = cloudwatch.Dashboard(
            self,
            f"{prefix}-dashboard",
            dashboard_name=f"{prefix}-telemetry"
        )
        
        # Add widgets to dashboard
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="Response Times by Assistant",
                left=[
                    cloudwatch.Metric(
                        namespace=f"continuum-assistant/AssistantPerformance",
                        metric_name="ResponseTime",
                        dimensions_map={
                            "Environment": env_name,
                            "AssistantName": assistant
                        },
                        statistic="Average",
                        period=Duration.minutes(5)
                    )
                    for assistant in ["financial", "universal", "aviation", "formula1", "tech"]
                ]
            ),
            cloudwatch.GraphWidget(
                title="Query Count by Type",
                left=[
                    cloudwatch.Metric(
                        namespace=f"continuum-assistant/UserInteractions",
                        metric_name="QueryCount",
                        dimensions_map={
                            "Environment": env_name,
                            "QueryType": query_type
                        },
                        statistic="Sum",
                        period=Duration.minutes(5)
                    )
                    for query_type in ["crypto", "finance", "aviation", "formula1", "tech", "general"]
                ]
            )
        )
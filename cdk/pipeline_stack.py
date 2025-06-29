from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_iam as iam,
)
from constructs import Construct

class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Source artifact
        source_output = codepipeline.Artifact()

        # Build artifact
        build_output = codepipeline.Artifact()

        # CodeBuild project
        build_project = codebuild.Project(
            self, "StreamlitBuild",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "install": {
                        "runtime-versions": {
                            "python": "3.12",
                            "nodejs": "20"
                        },
                        "commands": [
                            "npm install -g aws-cdk"
                        ]
                    },
                    "build": {
                        "commands": [
                            "cd docker_app",
                            "pip install -r requirements.txt",
                            "cd ..",
                            "cdk deploy --require-approval never"
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
            self, "StreamlitPipeline",
            stages=[
                codepipeline.StageProps(
                    stage_name="Source",
                    actions=[
                        codepipeline_actions.CodeStarConnectionsSourceAction(
                            action_name="GitHub_Source",
                            owner="ha-king",
                            repo="continuum-assistant",
                            branch="main",
                            connection_arn="arn:aws:codestar-connections:us-west-2:540257590858:connection/github",
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
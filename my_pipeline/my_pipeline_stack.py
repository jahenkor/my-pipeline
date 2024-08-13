import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from my_pipeline.my_pipeline_app_stage import MyPipelineAppStage

class MyPipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        synth_step = ShellStep("Synth",
                input=CodePipelineSource.git_hub("OWNER/REPO", "main"),
                commands=["npm install -g aws-cdk",
                  "python -m pip install -r requirements.txt",
                  "cdk synth"])

        pipeline = CodePipeline(self, "Pipeline",
                pipeline_name="MyPipeline",
                synth=synth_step)
        
        stage = pipeline.add_stage(MyPipelineAppStage(self, "test",
            env=cdk.Environment(account="654654214598", region="us-east-2")))

        stage.add_post(ShellStep("validate", input=synth_step, commands=["node test/validate.js"],))

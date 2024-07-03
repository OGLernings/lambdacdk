import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import {
  CodePipeline,
  CodePipelineSource,
  ShellStep,
} from "aws-cdk-lib/pipelines";
import { ManualApprovalStep } from "aws-cdk-lib/pipelines";
import { GCStage } from "./stage-stack";

export class OgpipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const demoCICD = new CodePipeline(this, "demoPipeline", {
      synth: new ShellStep("Synth", {
        input: CodePipelineSource.gitHub("OGLernings/GC_CICD", "main"),
        commands: ["npm ci", "npm run build", "npx cdk synth"],
      }),
      pipelineName: "GCPipeline",
    });

    const devStage = demoCICD.addStage(
      new GCStage(this, "dev", {
        env: { account: "862165548342", region: "us-east-1" },
      })
    );
    devStage.addPost(
      new ManualApprovalStep("Manual Approval before production")
    );

    const prodStage = demoCICD.addStage(
      new GCStage(this, "prod", {
        env: { account: "862165548342", region: "us-east-1" },
      })
    );
  }
}

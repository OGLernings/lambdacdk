import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as iam from "aws-cdk-lib/aws-iam";
import * as lambda from "aws-cdk-lib/aws-lambda";
import path = require("path");

export class infraStack extends cdk.Stack {
  constructor(
    scope: Construct,
    id: string,
    stageName: string,
    props?: cdk.StackProps
  ) {
    super(scope, id, props);

    const gcIamRole = new iam.Role(this, "gcIamLogicalId", {
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
      roleName: stageName + "gcIamRoleForLambda030724",
    });
    gcIamRole.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName("CloudWatchFullAccess")
    );

    const getGcLambda = new lambda.Function(this, "getGcLambdaLogicalId", {
      handler: "lambda_function.lambda_handler",
      role: gcIamRole,
      runtime: lambda.Runtime.PYTHON_3_11,
      code: lambda.Code.fromAsset(path.join(__dirname, "services")),
      environment: {
        StageName: stageName,
        Region: "us-east-1",
      },
      functionName: stageName + "gcGetLambda030724",
    });
  }
}

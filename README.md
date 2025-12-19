# Serverless Random Data API (AWS Infrastructure)

## Project Overview

This project implements a fully managed serverless HTTP API designed to explore low-level interactions between core AWS services (AWS Lambda and AWS API Gateway). The goal was not only to produce a working endpoint, but to develop a deep, practical understanding of request flow, security boundaries, and observability.

By utilizing an event-driven model where Amazon API Gateway serves as the ingress and AWS Lambda executes the business logic, the system inherits high-availability characteristics from AWS managed services, requires no server management, and scales automatically based on demand.

## Technical Highlights
- Implemented a serverless REST API using AWS Lambda and API Gateway with proxy integration.
- Designed IAM roles and resource-based policies following the principle of least privilege.
- Deployed and managed infrastructure using AWS CLI to understand low-level service interactions.
- Used CloudWatch Logs to debug runtime and permission-related issues in a stateless environment.
- Performed full resource cleanup to avoid residual cloud costs.

## System Architecture and Rationale
The architecture centers on a Python 3.12 runtime within AWS Lambda, chosen for its cost-efficiency and performance in a stateless execution model. A critical design decision was the implementation of Lambda Proxy Integration. This approach allows API Gateway to pass the raw HTTP context, including headers and query string parameters, directly to the application layer.

This design shifts request parsing and response shaping into the codebase, keeping the infrastructure configuration minimal, explicit, and portable.

Security is enforced through strict adherence to the Principle of Least Privilege. The Lambda execution role is scoped exclusively to CloudWatch logging permissions, while resource-based policies ensure that the function can only be invoked by the designated API Gateway instance. This layered security model prevents unauthorized invocation and limits the blast radius of potential failures.

## Engineering Challenges and Problem Solving
The development process highlighted several challenges specific to serverless systems. Initial deployments surfaced runtime errors that were only observable through CloudWatch Log Streams, reinforcing the importance of structured logging in a stateless execution environment. Resolving these issues required detailed inspection of execution logs to trace event context and runtime behavior.

Additionally, encountering AccessDenied errors during the cleanup phase provided practical insight into AWS permission boundaries. Differentiating between identity-based policies and resource-based policies proved essential for managing the infrastructure lifecycle correctly. These challenges emphasized the value of a CLI-first approach, which offered a more granular understanding of AWS primitives than the web console alone.

## Results and Future Trajectory
The final API delivers consistent performance, with an observed latency of approximately 50–100 ms per request during manual testing, while remaining entirely within AWS Free Tier limits. The current implementation supports multiple data types through a single endpoint by dynamically interpreting the request context.

The architecture is intentionally designed to evolve. Potential enhancements include integrating Amazon DynamoDB for persistent storage, introducing AWS Cognito for authentication, and formalizing deployments using Infrastructure as Code with Terraform or the AWS Cloud Development Kit (CDK).

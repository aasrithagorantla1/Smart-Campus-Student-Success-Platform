# Cost assumptions and AWS deployment preflight

## Guiding constraint
The prototype seeks to remain at approximately £0 infrastructure spend while free allowances remain available, with no guaranteed permanent zero-cost claim.

## Typical AWS resource review
- CloudFront default HTTPS domain under free-tier eligible account conditions
- Lambda Function URLs with on-demand execution only
- DynamoDB standard table with provisioned capacity and autoscaling disabled
- Minimal CloudWatch log retention
- No API Gateway, EC2, ALB, NAT, RDS, or paid AI endpoints

## Cost categories
- Recurring: minimal Lambda execution, DynamoDB usage, and CloudFront edge traffic within free tier
- Usage-dependent: request volume, data transfers, and read/write units
- Credit-dependent: temporary free-tier allowances and promotions may expire

## Expiry warning
Free allowances vary by account age, region, and service limits. If the account loses free-tier eligibility, the platform must be reviewed and revalidated before any deployment.

## Pre-deployment stop condition
If the proposed configuration cannot stay within the verified free allowance, deployment is paused and the assumptions are reported clearly.

# Deployment preflight checklist

- Confirm AWS account is eligible for CloudFront and Lambda free allowances.
- Confirm DynamoDB provisioned capacity fits within remaining free-tier limits.
- Verify no other workloads consume the available free allowances.
- Ensure CloudFront is configured with OAC and restricted origin invocation.
- Validate no local auth bypass is enabled in deployment mode.
- Review cloudformation template for strict regional configuration.
- Check that all demo/test data is excluded from real aggregates unless explicitly allowed.
- Confirm rollback and teardown procedure before any deployment.

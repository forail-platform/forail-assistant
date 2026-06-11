# Common Errors and Troubleshooting

## Job Failures

### "No inventory to run against"
The job template does not have an inventory assigned. Edit the template and select an inventory.

### "Playbook not found"
The selected playbook does not exist in the project. Sync the project first (Projects > Sync), then verify the playbook name.

### "Permission denied" on SSH connection
The machine credential does not have the correct SSH key or password. Verify:
- The SSH username is correct.
- The private key or password matches the target host.
- The target host allows SSH access from the Forail server.

### "Host key verification failed"
Add `host_key_checking = False` to your ansible.cfg, or add the host key to known_hosts on the Forail server.

### Job hangs in "Pending" status
- Check that the task worker is running (`forail-task` container).
- Check instance capacity at **Admin > Instances**.
- If using tenancy, verify the tenant queue has capacity.

### Job shows "Error" status
Check the job's stdout for the full error. Common causes:
- Syntax errors in playbooks.
- Missing required variables.
- Network connectivity issues to target hosts.

## Authentication Issues

### "CSRF verification failed"
The CSRF trusted origins are not configured. Add your domain to Settings > CSRF_TRUSTED_ORIGINS, or set the `FORAIL_CSRF_TRUSTED_ORIGINS` environment variable.

### "Invalid credentials"
- Verify username and password.
- Check if the user account is active.
- If using LDAP/SAML, verify the external auth configuration.

### MFA challenge not appearing
- WebAuthn MFA must be configured in Settings > Security.
- The user must have at least one registered security key.
- Check browser compatibility (WebAuthn requires HTTPS).

## Project Sync Issues

### "Authentication failed" on Git sync
- Verify the SCM credential has the correct token or SSH key.
- For GitHub/GitLab, ensure the token has repository read access.
- For SSH, ensure the key is not passphrase-protected (or use an SSH credential with passphrase).

### "Branch not found"
The specified branch does not exist in the remote repository. Check the branch name in the project settings.

## Inventory Issues

### "Could not resolve hostname"
DNS resolution failed for a host in the inventory. Verify:
- The hostname is spelled correctly.
- DNS is configured on the Forail server.
- The host is reachable from the Forail network.

## Policy/Scanner Issues

### "Policy denied launch"
A Policy-as-Code rule blocked the launch. Check **Compliance > Policy Decisions** for the specific deny reason.

### "Scanner blocked launch"
A scanner found findings above the severity threshold. Check **Compliance > Scan Results** for details. You can either fix the findings or adjust the scanner's severity threshold.

## Drift Detection Issues

### No drift detections appearing
- Ensure jobs run with `gather_facts: true` in playbooks.
- Check that the drift task is running (requires Celery worker).
- Verify the host has at least two fact snapshots for comparison.

## Service Catalog Issues

### Request stuck in "pending_approval"
- An authorized approver must approve the request.
- Check who can approve: the approver team, or org admins if no team is set.
- Superusers can always approve any request.

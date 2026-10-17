# Deployment Evidence and Troubleshooting

This guide documents the original Google Cloud, Jenkins, Docker, and website deployment sequence. These screenshots are historical evidence; the original cloud VM was later removed. They do not indicate that the old endpoint is currently online.

> **Security notice:** one historical screenshot contained a Jenkins agent secret. That command has been obscured in the copy included here. If the original credential could still be valid, invalidate it and remove any stale agent configuration.

## How to use this guide

- Read the step title before each image to understand what it demonstrates.
- Compare the expected outcome with the result visible in the screenshot.
- Use the troubleshooting notes if reproducing the step produces a different result.
- Do not reuse old IP addresses, agent secrets, passwords, or cloud settings without validating the current environment.

## Step 01 — Create the Google Cloud VM

This screen records the initial VM configuration used to host the Jenkins controller or build environment.

![Step 01: Create the Google Cloud VM](screenshots/01-gcp-vm-details.png)

**Expected outcome:** Confirm the chosen region, machine type, boot disk, and network before creating the instance.

**If something goes wrong:** If creation fails, check quota, selected zone capacity, IAM permissions, and whether the selected machine type is available.

## Step 02 — Review VM operating-system and storage settings

This step shows the selected operating system, disk, and instance configuration.

![Step 02: Review VM operating-system and storage settings](screenshots/02-gcp-instance-settings.png)

**Expected outcome:** Use a supported OS image, a disk size appropriate for the workload, and a documented instance name.

**If something goes wrong:** If SSH or package installation fails, confirm the VM is running, the boot disk has enough space, and the OS image matches the instructions.

## Step 03 — Configure the required network rule

This screenshot documents the firewall rule used to reach the service or Jenkins endpoint.

![Step 03: Configure the required network rule](screenshots/03-gcp-firewall-rule.png)

**Expected outcome:** Allow only required TCP ports and target only the intended VM using a network tag or service account.

**If something goes wrong:** If the page is unreachable, verify the VM has the matching network tag, the rule applies to the correct VPC, and the application is listening on that port. Avoid opening admin ports to the entire internet.

## Step 04 — Install Jenkins and its prerequisites

Terminal output documents the Jenkins installation and package setup.

![Step 04: Install Jenkins and its prerequisites](screenshots/04-jenkins-install-output.png)

**Expected outcome:** Package installation completes without unresolved dependency or repository errors.

**If something goes wrong:** If installation fails, check apt repository configuration, package indexes, disk space, and network connectivity; inspect the first error rather than retrying blindly.

## Step 05 — Install Java and supporting packages

This step records installation of packages required by Jenkins and its runtime.

![Step 05: Install Java and supporting packages](screenshots/05-jenkins-dependencies.png)

**Expected outcome:** The package manager finishes successfully and the required Java runtime is available.

**If something goes wrong:** If packages cannot be resolved, refresh package indexes, confirm repository availability, and check the supported Java version for the installed Jenkins release.

## Step 06 — Download the Jenkins inbound agent

This terminal output shows the agent JAR being downloaded from the Jenkins controller.

![Step 06: Download the Jenkins inbound agent](screenshots/06-jenkins-agent-download.png)

**Expected outcome:** The download completes and the file exists on the intended agent machine.

**If something goes wrong:** If the download returns an error, verify controller URL, DNS/network access, controller port, and the agent JAR path. Do not publish a raw agent launch command or secret.

## Step 07 — Verify Jenkins service state

This screenshot records service setup and/or runtime status on the host.

![Step 07: Verify Jenkins service state](screenshots/07-jenkins-service-status.png)

**Expected outcome:** The service is active and enabled, and the logs do not show a repeating startup failure.

**If something goes wrong:** Use `sudo systemctl status jenkins --no-pager` and `sudo journalctl -u jenkins -n 100 --no-pager`. Check Java version, memory pressure, and port conflicts.

## Step 08 — Review the Compute Engine instance

The cloud console overview shows the VM resource and its operational state.

![Step 08: Review the Compute Engine instance](screenshots/08-gcp-compute-overview.png)

**Expected outcome:** The expected instance is running and its name, zone, and network are correct.

**If something goes wrong:** If the instance is stopped or missing, inspect its lifecycle state, operation errors, quotas, and audit logs before recreating it.

## Step 09 — Unlock Jenkins securely

The initial Jenkins setup page prompts for the one-time administrator unlock secret.

![Step 09: Unlock Jenkins securely](screenshots/09-jenkins-unlock-screen.png)

**Expected outcome:** Retrieve the initial password from the host's protected Jenkins setup file and enter it directly in the trusted browser session.

**If something goes wrong:** If the password is unavailable, read it over SSH with appropriate permissions. Never commit it to source control or share a screenshot containing it.

## Step 10 — Choose the initial Jenkins plugins

This screen records the plugin selection during first-run setup.

![Step 10: Choose the initial Jenkins plugins](screenshots/10-jenkins-plugin-selection.png)

**Expected outcome:** Install only the plugins needed for the intended pipeline; avoid adding plugins without a clear use case.

**If something goes wrong:** If installation hangs, check controller internet access, plugin-center connectivity, proxy settings, and Jenkins logs. Restart only after reviewing the cause.

## Step 11 — Wait for plugin installation to finish

The setup screen shows progress while Jenkins installs selected plugins.

![Step 11: Wait for plugin installation to finish](screenshots/11-jenkins-plugin-installation.png)

**Expected outcome:** Required plugins complete installation and Jenkins proceeds to the next setup step.

**If something goes wrong:** If a plugin fails, inspect the failure details, update the plugin center metadata, and check version compatibility before retrying.

## Step 12 — Create the Jenkins administrator account

This screen documents the initial admin user setup.

![Step 12: Create the Jenkins administrator account](screenshots/12-jenkins-admin-setup.png)

**Expected outcome:** Use a unique admin username and strong password; store the credentials in an approved password manager.

**If something goes wrong:** If setup cannot continue, verify all required fields and confirm the controller can write to its Jenkins home directory. Never include the password in screenshots.

## Step 13 — Confirm the Jenkins dashboard is available

The dashboard confirms the controller is ready for job and node configuration.

![Step 13: Confirm the Jenkins dashboard is available](screenshots/13-jenkins-dashboard.png)

**Expected outcome:** The UI loads and the administrator can navigate to Nodes and Jobs.

**If something goes wrong:** If the dashboard is blank or unavailable, check service status, controller logs, browser console, reverse-proxy settings, and port 8080 reachability.

## Step 14 — Prepare the build agent

This terminal output documents agent-side setup and/or installation of build dependencies.

![Step 14: Prepare the build agent](screenshots/14-jenkins-agent-install-output.png)

**Expected outcome:** The agent has the tools required by the job: Git, Python 3, Docker CLI/daemon access, and curl.

**If something goes wrong:** If commands are missing, install the required packages and confirm the Jenkins service account has approved Docker access. Never make the Docker socket world-writable.

## Step 15 — Configure the Jenkins agent connection

This screen records the node's connection method and remote working directory.

![Step 15: Configure the Jenkins agent connection](screenshots/15-jenkins-agent-configuration.png)

**Expected outcome:** The node name, labels, launch method, and remote root match the host configuration.

**If something goes wrong:** If the node stays offline, verify the agent can reach the controller, the remote directory is writable, Java is installed, and the launch log has no authentication or WebSocket errors.

## Step 16 — Register the build node

The node creation screen defines the agent used for build execution.

![Step 16: Register the build node](screenshots/16-jenkins-node-creation.png)

**Expected outcome:** The node is created with an appropriate executor count, labels, and remote root directory.

**If something goes wrong:** If node creation or connection fails, check the remote root ownership and ensure the directory exists. Keep executors conservative on low-memory machines.

## Step 17 — Set job execution options

This screen documents the selected Jenkins job settings or build parameters.

![Step 17: Set job execution options](screenshots/17-jenkins-job-options.png)

**Expected outcome:** The job uses the correct SCM source and deployment mode; credentials are referenced by ID rather than embedded in scripts.

**If something goes wrong:** If a parameter is missing, save the job configuration and reload the job. Keep remote deployment disabled until credentials and target access are verified.

## Step 18 — Troubleshoot agent connection and workspace permissions

The original terminal showed an agent launch attempt and a workspace permission error. The credential-bearing command has been redacted.

![Step 18: Troubleshoot agent connection and workspace permissions](screenshots/18-agent-connection-debug-redacted.png)

**Expected outcome:** The agent should launch without exposing its secret, and the remote working directory should be writable by the Jenkins service account.

**If something goes wrong:** For `AccessDeniedException`, set the remote root to a dedicated writable directory and correct ownership. If a secret was ever exposed publicly, invalidate/rotate it and remove the stale agent.

## Step 19 — Configure the CI/CD job

This screen shows the job setup used to run the project's build and deployment workflow.

![Step 19: Configure the CI/CD job](screenshots/19-jenkins-job-configuration.png)

**Expected outcome:** The job points to the intended repository and branch, and its script source is version-controlled.

**If something goes wrong:** If checkout fails, verify the repository URL, branch name, SCM credentials, Git installation, and agent network access.

## Step 20 — Review the saved job configuration

This screenshot records the job's general or pipeline configuration after setup.

![Step 20: Review the saved job configuration](screenshots/20-jenkins-job-settings.png)

**Expected outcome:** The job configuration is saved and references the correct source and pipeline options.

**If something goes wrong:** If a build uses stale settings, save the job again, confirm the selected branch and Jenkinsfile path, then trigger a fresh build.

## Step 21 — Review build history and result

The build history shows the job's recorded executions and statuses.

![Step 21: Review build history and result](screenshots/21-jenkins-build-history.png)

**Expected outcome:** A successful run is marked green/Success and its console output matches the expected commit and build number.

**If something goes wrong:** If a build is red, open Console Output and locate the first failing stage. Fix the root cause and rerun; do not hide a failed check.

## Step 22 — Inspect build and deployment commands

The console output records source checkout, Docker build/deploy operations, and verification commands.

![Step 22: Inspect build and deployment commands](screenshots/22-jenkins-build-output.png)

**Expected outcome:** The log shows the expected repository revision, image build, container start, and HTTP response check.

**If something goes wrong:** If Docker reports permission denied, inspect daemon availability and service-account group/permissions. If a port is occupied, select a free port instead of killing unrelated services.

## Step 23 — Confirm the job summary

This screen records the configured job and its visible build status.

![Step 23: Confirm the job summary](screenshots/23-jenkins-job-summary.png)

**Expected outcome:** The job exists and the most recent successful build is easy to identify.

**If something goes wrong:** If no successful build is present, open the latest console log and confirm the agent is online, the correct branch was built, and the smoke test ran.

## Step 24 — Verify the deployed ReleaseForge website

This browser screenshot records the website responding after the historical deployment.

![Step 24: Verify the deployed ReleaseForge website](screenshots/24-releaseforge-deployed-site.png)

**Expected outcome:** The page renders its ReleaseForge title, primary message, and pipeline content without a browser network error.

**If something goes wrong:** If the browser cannot reach the site, check container health, host port mapping, firewall target tags, and whether the VM still exists. This screenshot is historical, not a current uptime claim.

## Step 25 — Verify the running container and port mapping

This terminal output documents the named container, published port, and/or health status after deployment.

![Step 25: Verify the running container and port mapping](screenshots/25-container-health-status.png)

**Expected outcome:** The expected container is running, health reports `healthy`, and the published port points to container port 80.

**If something goes wrong:** If health is `starting` or `unhealthy`, run `docker logs releaseforge-website`, `docker inspect releaseforge-website`, and `curl -i http://127.0.0.1:8082/healthz`. Confirm the image contains the expected health route.

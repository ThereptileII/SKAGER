# SKAGER public source and production publishing

This document defines the release boundary for the public source repository and
the desktop update feed. It is deliberately separate from development and CI
evidence workflows.

## Public source repository

Every distributed SKAGER desktop build must be traceable to a public source
revision. The source publication contains the complete corresponding source,
build recipes, pinned dependency manifests, OpenCPN integration documentation,
license texts and release metadata. It must not contain credentials, private
chart material, customer data, signed URLs, or local build output.

The public repository is a clean source snapshot repository. Its release commit
is the exact source revision used to create the binary. Do not publish a source
snapshot from a different commit or silently amend a release after publishing.

## Production-only publication rule

The normal push workflows are verification workflows. Their artifacts are CI
evidence and are not update-feed releases. They must never publish an installer,
portable package or update manifest to customers.

Only the manually invoked `SKAGER Production Release` workflow may publish a
desktop release. It runs against one explicit commit and one explicit version,
uses the native Win32/MSVC production build, and requires the GitHub `production`
environment. A protected environment review is required before the upload step.

The publication order is transactional:

1. verify the exact source commit and distribution inputs;
2. build and run the required production gates;
3. create the installer, recovery package, hashes, source archive and release
   metadata;
4. create the GitHub release in the public source repository as a draft;
5. upload the same bytes to the private update server;
6. read the objects back and compare SHA-256 values;
7. verify the signed update manifest through the public update endpoint;
8. publish the GitHub release only after server verification succeeds.

Any failure before step 8 leaves the GitHub release as a draft and the update
channel unchanged. No workflow may overwrite an existing version. Promotion to
the public beta remains a separate human decision.

## Required protected configuration

Values are stored only as GitHub Actions secrets or environment-protected
variables. They are never written to the repository, build logs or release
metadata.

| Secret | Purpose |
| --- | --- |
| `PRODUCTION_PUBLISH_TOKEN` | short-lived authorization for the update-server publication endpoint |
| `PRODUCTION_PUBLISH_URL` | HTTPS publication endpoint for the private update feed |
| `UPDATE_MANIFEST_SIGNING_KEY` | signing key held by the protected release environment |
| `PUBLIC_SOURCE_REPO` | canonical public source repository, for example `ThereptileII/SKAGER` |

The workflow must fail before building if the protected endpoint or signing key
is absent. A GitHub token may create the release only in the configured public
source repository; it is not used as an update-server credential.

## Server publication contract

The endpoint accepts a multipart publication containing the exact installer,
portable recovery package, corresponding source archive, `SHA256SUMS.txt`,
release metadata and signed update manifest. It must authenticate the request,
reject duplicate versions, validate all declared hashes, and publish objects
atomically. The response includes the publication id and the server-side hashes.

The workflow treats a non-2xx response, a missing object, a hash mismatch, an
unexpected version, or an unsigned manifest as a failed release. It never falls
back to a public bucket or an unauthenticated upload.

## Releasing a candidate

From the public source repository, use **Actions → SKAGER Production Release →
Run workflow**, enter the exact tested commit and version, and wait for the
protected production-environment review. Do not use a push-triggered workflow
for release publication. The release notes must identify the OpenCPN version,
upstream revision, application commit, installer hash, source archive hash and
remaining limitations.

## Rollback

Rollback is a new signed publication that points the updater to the last known
good release. Existing release objects are immutable. Never replace an object
in place and never delete the previous release before the replacement has been
verified by a client.

## License and corresponding source

The repository includes the GPL license and OpenCPN attribution. Third-party
licenses and notices are kept with the source release. The public release page
links to the exact source commit and source archive used by the binary.


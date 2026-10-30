# SKAGER build and release workflow

This is the operational runbook for maintainers. It replaces the earlier
staging-first publication habit for all new desktop releases.

## Three different outputs

* **Development checks** compile and test code. Their artifacts are disposable
  evidence and never reach users.
* **Qualification candidates** are exact-commit packages used for Windows,
  installer, boat and recovery testing. They remain unpublished.
* **Production releases** are the only packages eligible for the update feed.
  They are created by the protected production workflow and are published to
  both the public source repository and the update server.

Do not rename a development artifact or manually copy it into production. A
production workflow must rebuild or consume only an authenticated exact-commit
artifact whose provenance is recorded in the release metadata.

## Before starting a release

1. Confirm the worktree is clean and the source commit is pushed.
2. Run `python tools/verify-distribution-inputs.py`.
3. Confirm `Version.h`, the Windows compatibility manifest and the release
   metadata contain the same version.
4. Confirm the pinned OpenCPN revision and Win32/x86 ABI.
5. Confirm no credentials, chart files, profiles or build directories are
   tracked.
6. Confirm the candidate's Linux and native Windows results are attached to the
   same commit.
7. Confirm the boat test result and remaining limitations are recorded.

The checks above are preconditions, not approval to publish.

## Production workflow stages

The `SKAGER Production Release` workflow is manual and protected:

1. **Resolve**: checkout the requested commit, verify it is immutable and record
   the source SHA.
2. **Preflight**: validate release inputs, OpenCPN compatibility, dependency
   manifests and source-package cleanliness.
3. **Build**: run the native Windows MSVC Win32 production build and package the
   installer and recovery package. Linux checks may run in parallel but cannot
   replace native Windows qualification.
4. **Test**: run the focused production contract, installer lifecycle, update
   trust and package smoke checks required by the changed inputs. Release
   blockers fail the job.
5. **Assemble**: create `Setup.exe`, `Portable-Recovery.zip`, corresponding
   source, `SHA256SUMS.txt`, release notes, license notices and a signed update
   manifest.
6. **Draft**: create a draft GitHub release in the public source repository.
7. **Publish server**: send the exact bytes to the protected update endpoint.
8. **Verify**: read back each object, compare hashes, verify the signed feed and
   exercise an unauthenticated metadata request without exposing a download
   token.
9. **Finalize**: mark the GitHub release published only after the server checks
   pass. Record the CI run, source SHA and all hashes.

## What must never happen

* Do not publish from a dirty worktree.
* Do not publish a package from a different commit than the source archive.
* Do not use staging URLs, public R2 objects or unsigned manifests for a
  production release.
* Do not put signing keys, API keys, credentials or signed URLs in logs.
* Do not overwrite an existing version or mutate a released object.
* Do not treat a successful compile as a release gate.
* Do not open public payment/download access as part of this workflow.

## Routine after a release

Record the release URL, CI run, source revision, OpenCPN revision, package
hashes, server publication id, feed verification result and any rejected or
deferred checks. Keep the previous release available for rollback.


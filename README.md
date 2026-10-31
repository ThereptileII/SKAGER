# SKAGER

**A modern marine navigation interface built on OpenCPN.**

SKAGER brings a chart-first interface to the boat computer, with routes and
waypoints, AIS, vessel instruments, electric propulsion and battery information,
and advisory energy estimates. It retains OpenCPN’s chart engine, navigation
storage and plugin infrastructure, with Legacy and Safe modes available for
compatibility and recovery.

- [Product website](https://beta.skager.app/)
- [Installation requirements](https://beta.skager.app/install/)
- [Help and support](https://beta.skager.app/support/)
- [Source releases](https://github.com/ThereptileII/SKAGER/releases)
- [Open source and licences](https://beta.skager.app/open-source/)

## About this repository

This is SKAGER’s public source repository. It provides application source,
OpenCPN integration patches, build and installation scripts, dependency version
information, and licence material. Product development and release operations
are maintained separately.

For a particular distributed version, use its matching source archive and
source reference. The default branch is not a promise that it matches every
installed binary. See [Source releases](SOURCE_RELEASE.md) and
[Building from source](BUILDING.md).

## OpenCPN prerequisite

The supported Windows integration targets **OpenCPN 5.12.4**, preserving its
32-bit application and plugin ABI on 64-bit Windows. Install supported OpenCPN
separately before installing an official SKAGER package. The installer verifies
compatibility; a matching version label alone is insufficient.

SKAGER builds on the work of the [OpenCPN project](https://opencpn.org/) and its
contributors. It is an independent product and is not affiliated with or
endorsed by OpenCPN. The pinned upstream source is
[OpenCPN 5.12.4](https://github.com/OpenCPN/OpenCPN/tree/37fd0cddb7334fe489e9f18aa163977a9c5c84f7).

## Beta status and navigation

SKAGER is beta software. Hardware support and available readings depend on
connected equipment and the exact release. Missing or stale readings must not be
interpreted as valid navigation data. Energy and SmartNav predictions are advisory.
SKAGER does not provide autonomous steering.

Consult the limitations supplied with your exact version. Keep an independent
means of navigation and a recovery path available.

## Licensing

See [LICENSE](LICENSE) and the notices supplied with each component and release.
Third-party components retain their own licences and copyright notices; see
[Third-party notices](docs/release/THIRD_PARTY_NOTICES.md).

Source access does not require a SKAGER account. Paid services do not remove
rights granted by the applicable open-source licences. Commercial chart data
and chart-provider licences are separate and are not included here.

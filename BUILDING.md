# Building SKAGER from source

Use the source archive and dependency material matching the binary version you
want to inspect or rebuild. This repository is a source distribution, not an
installer for an existing navigation computer.

## Source layout

- `src/`: native interface, vessel data, advisory calculations and integration.
- `patches/`: changes applied to the pinned OpenCPN baseline.
- `resources/`: application and chart-presentation resources.
- `installer/windows/`: Windows integration and maintenance scripts.
- `tools/`: build, dependency preparation and packaging scripts.
- `tests/`: automated checks and fixtures.
- `upstream.lock.json`: upstream version and source revision.

Internal identifiers containing OpenNav or XNav are retained in code and build
scripts for compatibility; the customer-facing product is SKAGER.

## Get the source

```sh
git clone --recurse-submodules https://github.com/ThereptileII/SKAGER.git
cd SKAGER
git submodule update --init --recursive
python3 tools/verify-upstream.py
```

The pinned OpenCPN revision is
`37fd0cddb7334fe489e9f18aa163977a9c5c84f7`.
Do not substitute a different upstream revision when reproducing a release.

## Portable C++ components

Requirements include CMake 3.24 or newer, a C++17 compiler, Ninja (for the
commands below), and dependencies selected by the CMake configuration. Dependency
URLs and hashes are recorded in the supplied CMake and lock files.

```sh
cmake -S . -B build/contracts -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build/contracts
ctest --test-dir build/contracts --output-on-failure
```

These commands build the portable components and their checks, not the complete
OpenCPN application.

## Integrated Linux application

Install the dependencies required by the pinned OpenCPN source, including
wxWidgets/GTK, OpenGL and the relevant development libraries, plus Python 3,
Git, CMake and Ninja. Consult OpenCPN’s source build instructions for the chosen
distribution. The supplied scripts retain the required integration options:

```sh
bash tools/build-production-linux.sh --build-only
```

`tools/prepare-integration.py` prepares a separate patched source directory;
`tools/build-production-linux.sh` configures, builds and installs under `build/`.
It disables synthetic runtime fixtures. The optional `--build-only` argument
skips the script’s post-build checks.

## Integrated Windows application

Use a 64-bit Windows host with Visual Studio 2022 C++ build tools, the Windows
SDK, CMake, Python 3, Git, 7-Zip, and the dependencies specified by the supplied
Windows scripts and lock files. Use the **Win32** target to preserve OpenCPN’s
supported ABI:

```powershell
./tools/build-pristine-windows.ps1 -Architecture Win32 -Integration -Production
```

Dependency preparation scripts include `build-openssl-windows.ps1`,
`build-curl-windows.ps1` and `build-zlib-windows.ps1`. Consult the matching release
archive for dependency source, hashes, producer receipts and toolchain details.
A development build is not evidence that an official release was qualified.

## Installation and source mapping

The Windows installer sources are under `installer/windows/`; packaging scripts
are under `tools/`. Packaging requires the dependencies, resources and notices
for the exact release, not just a compiled executable.

Use a disposable profile when running a source build. Do not replace a working
OpenCPN installation manually. Keep the original navigation profile and charts
backed up, and use official installers for ordinary operation.

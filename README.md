# routergen
RouterGen is a safety-first topology compiler for building reproducible Linux and WSL2 router environments from declarative topology definitions.

=================================
RouterGen
=================================

RouterGen is a topology-driven network interface configuration generator for building Linux router instances, initially targeting WSL2 and Linux network namespaces.

RouterGen takes a logical topology definition and resolves it against the interfaces actually available on the host. It then produces a deterministic configuration plan for namespaces, router interfaces, Linux bridges, host-side SVIs, VLAN transports, and, in later lifecycle stages, FRRouting (FRR).

The project is designed around a simple principle:

Describe the router topology logically, discover the host physically, resolve the two safely, validate everything, and only then make network changes.

RouterGen is currently under active development. The v0.2 data model and read-only architecture are defined, while automated network application and FRR lifecycle management remain later implementation stages.

=================================
What problem does RouterGen solve?
=================================

Linux networking labs are easy to build manually, but become increasingly difficult to reproduce as the topology grows.

A router may require:

Linux network namespaces
veth interfaces
Linux bridges
VLAN subinterfaces
host-facing interfaces
static or DHCP addressing
multiple isolated Layer-2 segments
multiple routers on the same host
connections between different physical or virtual hosts
FRRouting instances with independent runtime state

Hard-coding interface names such as eth0, eth1, or br0 makes a topology dependent on a specific machine.

RouterGen separates the logical topology from the physical host implementation.

For example, the topology can describe:

Router interface
      |
      v
Dedicated Linux bridge
      |
      v
Transport
      |
      v
Detected host interface


The transport may subsequently resolve to:

local connectivity
VLAN transport
host-routed connectivity
an existing external bridge
a staged/unconnected interface

The actual host device is discovered at runtime rather than silently assumed.

This makes the same logical topology portable across different laptops, WSL2 instances, Linux hosts, and eventually multi-host router labs.

=================================
Supported platforms
=================================

/Initial target/

RouterGen is currently being developed and tested primarily for:

Windows 11
WSL2
Ubuntu 24.04
Linux network namespaces
Linux bridges
iproute2

Development uses a dedicated Python virtual environment.

/Architecture target/

The data model is intentionally Linux-oriented rather than WSL2-specific, so the architecture is intended to accommodate native Linux hosts as the project develops.

/ FRRouting /

FRRouting (FRR) integration is part of the architecture but is deliberately separated from initial network-interface provisioning.

Each RouterGen router is intended to have an independent FRR pathspace, for example:

frr -N r1
frr -N r2


This allows multiple logical routers on one Linux host while keeping their FRR configuration, PID, VTY, Zebra, and runtime state isolated.

The network underlay must validate successfully before FRR configuration or startup is attempted.

=================================
Architecture
=================================

RouterGen separates intent, host discovery, resolution, validation, planning, and eventually application.

Logical Topology JSON
        |
        v
JSON Schema Validation
        |
        v
Semantic Validation
        |
        +----------------+
        |                |
        v                v
Host Discovery      Saved Profiles
        |                |
        +-------+--------+
                |
                v
          Configuration
            Resolution
                |
                v
       Fully Resolved Router
                |
                v
      Deterministic Read-Only
              Plan
                |
                v
           Safety Gates
                |
                v
        Network Application
          [future stage]
                |
                v
       Post-Apply Validation
                |
                v
        FRR Lifecycle Layer
          [future stage]

=================================
Core data model
=================================

The v0.2 architecture models the system approximately as:

HOST
 └── detected physical/virtual interfaces

ROUTER
 ├── namespace
 ├── interfaces
 │    ├── router addressing
 │    ├── routing policy
 │    └── attachment
 │
 └── optional FRR intent

ATTACHMENT
 └── dedicated BRIDGE
      ├── optional host SVI
      └── TRANSPORT
           ├── local
           ├── vlan
           ├── host-routed
           ├── external-bridge
           └── staged

=================================
Important design rule
=================================

Each router attachment receives its own dedicated Linux bridge representing one logical Layer-2 segment.

Separate point-to-point VLANs must therefore not accidentally be collapsed onto a common bridge.

For example:

r1:eth1
   |
 br101
   |
 vlan 101
   |
 host interface

r1:eth2
   |
 br102
   |
 vlan 102
   |
 host interface


br101 and br102 represent different Layer-2 segments even if their VLAN transports ultimately use the same physical host interface.

=================================
Configuration precedence
=================================

When RouterGen resolves configuration, values follow this precedence:

CLI override
    >
interactive answer
    >
saved host/router profile
    >
topology JSON default
    >
RouterGen default


Topology JSON therefore supplies portable intent and defaults, while detected hardware constrains what can actually be configured.

A configured host interface that does not exist must not be silently replaced with another interface.

=================================
Installation
=================================

Current status: RouterGen is not yet a production package. The commands below describe the current development workflow.

Clone the repository:

git clone <repository-url>
cd wsl2-router-netgen


Create a dedicated Python virtual environment:

python3 -m venv .venv
source .venv/bin/activate


Upgrade the Python packaging tools:

python -m pip install --upgrade pip setuptools wheel


Install RouterGen in editable/development mode:

pip install -e .


The RouterGen virtual environment should remain separate from other networking projects such as OSPF Alt.

Verify the environment:

which python
python --version
pip show wsl2-router-netgen


The Python executable should resolve to the RouterGen repository's .venv.

=================================
Running RouterGen
=================================

RouterGen is currently being developed using a read-only-first workflow.

The intended workflow is:

Topology
   ↓
Validate
   ↓
Discover host
   ↓
Resolve
   ↓
Plan
   ↓
Review
   ↓
Apply
   ↓
Validate


During the current development phase, stop at the Plan stage.

Conceptually:

routergen validate topology.json
routergen discover
routergen resolve topology.json
routergen plan topology.json


The exact CLI commands should be updated in this README as the v0.2 CLI implementation is completed. Do not document apply as usable until its safety gates and post-validation are implemented and verified.

A future operational workflow is expected to look approximately like:

routergen apply topology.json


but only after:

JSON Schema validation passes.
semantic validation passes.
required host interfaces exist.
router/interface mappings are fully resolved.
the deterministic plan passes validation.
the user explicitly authorizes the change.

=================================
Safety model
=================================

RouterGen treats host networking changes as potentially disruptive.

Its design therefore follows several safety rules:

Never silently substitute a missing host interface.
Validate before modifying networking.
Separate read-only planning from application.
Produce a deterministic plan before application.
Reconcile only the selected router's changed resources.
Preserve unchanged router interfaces.
Keep independent Layer-2 segments on independent bridges.
Keep router-interface addressing independent from host-SVI addressing.
Validate the resulting network after changes.
Do not start or modify FRR until the network underlay passes validation.

The long-term goal is a workflow similar to:

  discover → resolve → validate → plan → approve → apply → validate

rather than executing networking commands directly from an unvalidated topology definition.

=================================
Documentation
=================================

Detailed documentation should live under:

docs/


The recommended repository layout is:

README.md
PROJECT_STATUS.md
CHANGELOG.md
LICENSE


docs/
├── architecture/
├── data-model/
├── schema/
├── semantic-validation/
├── host-discovery/
├── resolution/
├── planning/
├── safety/
├── frr/
└── examples/

schemas/
examples/
src/
tests/


Use the files for different purposes:

README.md - The entry point for new users:

what RouterGen is
why it exists
supported platforms
quick architecture overview
installation
basic usage
current stability


PROJECT_STATUS.md - The authoritative engineering checkpoint:

current version/stage
completed milestones
verified tests
current hard gate
known limitations
next implementation step


docs/

Detailed technical design and operational documentation.


CHANGELOG.md

User-visible changes between RouterGen versions/releases.

=================================
Current stability
=================================

RouterGen should currently be considered:

Early development / pre-alpha

The project is not yet a production network provisioning system.

=================================
Stable / frozen design
=================================

The following architectural decisions are currently established for v0.2:

topology-driven configuration
host-interface discovery
router namespaces
router-interface-to-bridge attachments
one dedicated bridge per logical Layer-2 segment
independently configurable router-interface addressing
independently configurable bridge host-SVI addressing
none, static, and DHCP addressing modes
local transport
VLAN transport
host-routed transport
external-bridge transport
staged transport
host-role-to-device resolution
deterministic configuration precedence
explicit failure when configured host interfaces are unavailable
non-destructive reconciliation model
optional per-router FRR intent
independent FRR pathspace per router
network-underlay validation before FRR lifecycle operations
semantic validation outside JSON Schema

=================================
Verified baseline
=================================

The original RouterGen baseline has passed:

12 / 12 tests


including the existing validation/read-only planning baseline.

=================================
Current development gate
=================================

The current work is v0.2-A: read-only architecture:

A1  Project/bootstrap
A2  Topology/schema + semantic validation
A3  Host discovery using structured `ip -j` data
A4  Profiles, prompts, precedence and role resolution
A5  Deterministic read-only planning


The hard gate before moving to the apply phase is:

Logical topology
       +
Actual host discovery
       +
Optional saved profile
       +
User choices
       ↓
Fully resolved router
       ↓
Semantic validation PASS
       ↓
Deterministic plan
       ↓
ZERO network changes


Only after that gate passes should RouterGen proceed to network configuration/application.

=================================
Project status
=================================

The next implementation milestone is:

v0.2-A1: Project/bootstrap

This includes:

Python package skeleton
RouterGen CLI entry point
dedicated .venv bootstrap
command/environment prerequisite checks
preservation of the existing 12/12 test baseline

See PROJECT_STATUS.md for the exact current engineering checkpoint and docs/ for detailed architecture and design documentation.

and positioned PROJECT_STATUS.md as the detailed source of truth for development progress rather than allowing the README to become a development log.

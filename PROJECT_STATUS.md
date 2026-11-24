
# RouterGen Project Status

> Project stage: Pre-alpha  
> Current development phase: v0.2-A, Read-Only Architecture  
> Current milestone: v0.2-A1, Project and Bootstrap  
> Last updated: 2026-11-24  
> Network changes permitted in the current phase: No

---

## 1. Status Summary

RouterGen is a safety-first topology compiler for creating reproducible
Linux and WSL2 router environments from declarative topology definitions.

The project is currently implementing the v0.2 read-only architecture.

The immediate objective is to transform:

- a logical topology;
- actual host-interface discovery;
- an optional saved host/router profile;
- command-line overrides; and
- interactive user choices

into:

- a fully resolved router definition;
- a semantic validation result; and
- a deterministic network plan.

The current phase must make zero network changes.

RouterGen is not yet ready for production use. Network application,
reconciliation, rollback, post-apply validation, and FRRouting lifecycle
management remain later phases.

---

## 2. Current State at a Glance

| Area | Status | Notes |
|---|---|---|
| Project purpose | Stable | Safety-first topology-driven Linux router configuration |
| v0.2 data model | Frozen for v0.2-A | Covers host, router, interface, bridge, SVI, transport, and optional FRR intent |
| JSON Schema direction | Defined | Structural validation belongs in JSON Schema |
| Semantic validation rules | Defined | Cross-object and host-dependent checks are performed outside JSON Schema |
| Host discovery design | Defined | Uses structured `ip -j` output |
| Configuration precedence | Frozen | CLI > prompt > profile > topology default > generator default |
| Read-only planning architecture | Defined | Must be deterministic and make zero changes |
| Existing baseline tests | Passing | 12/12 tests passed |
| v0.2-A implementation | In progress | Begins with A1 project/bootstrap |
| Network apply | Not implemented | Must not be presented as available |
| Reconciliation | Designed, not implemented | Changes only selected router resources |
| Post-apply validation | Planned | Required before declaring an apply successful |
| FRR lifecycle | Designed, not implemented | Runs only after the network underlay passes |
| Native Linux qualification | Not yet complete | Architecture target, not a verified platform claim |
| Production readiness | No | Project remains pre-alpha |

---

## 3. Verified Baseline

The existing RouterGen baseline has been validated with:

```text
12 PASS
0 FAIL


The verified baseline covers the existing validation and read-only planning foundation.

This result must be preserved while implementing v0.2-A.

Baseline preservation rule

No v0.2 change may silently remove, weaken, or bypass the existing baseline tests.

Before a v0.2 milestone is accepted:

all existing baseline tests must pass;
the milestone-specific tests must pass;
no network changes may occur during read-only commands;
the result must clearly distinguish warnings from failures; and
the generated output must remain deterministic.
4. Current Development Phase

The current phase is:

v0.2-A: Read-Only Architecture


Its purpose is to prove that RouterGen can reliably convert topology intent and actual host state into a complete, validated, deterministic plan without changing the host.

v0.2-A milestones
Milestone	Description	StatusA1	Project/bootstrap	Next
A2	Topology, schema, and semantic-validation framework	Planned
A3	Structured host discovery	Planned
A4	Resolution, profiles, prompts, and precedence	Planned
A5	Deterministic read-only planning	Planned
5. Current Milestone: v0.2-A1
Objective

Establish a clean, reproducible RouterGen development and execution environment without changing network configuration.

A1 scope

v0.2-A1 includes:

Python package skeleton;
source package layout;
RouterGen CLI entry point;
dedicated Python virtual-environment bootstrap;
Python version checks;
operating-system checks;
required-command checks;
privilege-awareness checks;
read-only environment reporting;
test framework integration; and
preservation of the existing 12/12 baseline.
Expected repository foundation
wsl2-router-netgen/
├── README.md
├── PROJECT_STATUS.md
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
├── schemas/
├── examples/
├── docs/
├── scripts/
├── src/
│   └── routergen/
│       ├── __init__.py
│       ├── cli.py
│       ├── errors.py
│       ├── models/
│       ├── validation/
│       ├── discovery/
│       ├── resolution/
│       ├── planning/
│       └── reporting/
└── tests/


The exact internal module names may be adjusted during implementation, but the separation between validation, discovery, resolution, planning, and reporting must be preserved.

A1 prerequisite checks

The bootstrap and diagnostic commands should check for at least:

supported Python version;
Linux execution environment;
WSL detection where applicable;
ip;
support for structured ip -j output;
bridge;
sysctl;
ss;
package installation state;
active virtual environment;
whether the active environment belongs to RouterGen; and
whether elevated privileges would be required by a future operation.

A1 checks must not create namespaces, bridges, veth pairs, VLAN interfaces, routes, addresses, or FRR processes.

A1 acceptance criteria

v0.2-A1 is complete only when:

 RouterGen installs into its own .venv.
 The .venv is separate from the OSPF Alt project environment.
 The package can be installed in editable mode.
 The RouterGen CLI starts successfully.
 The CLI provides usable --help output.
 The environment diagnostic is read-only.
 Required external commands are detected.
 Missing optional and required commands are reported distinctly.
 Unsupported conditions produce actionable errors.
 Tests run from a clean checkout.
 The original 12/12 baseline remains passing.
 No command in A1 modifies network state.
 Generated diagnostic output is suitable for saving in a result file.
6. v0.2 Architecture Decisions

The following decisions are frozen for the v0.2-A implementation unless a formal design change is recorded.

6.1 Router interface mapping

The fundamental mapping is:

Router interface
    -> dedicated host bridge
    -> transport
    -> detected host device


Each selected router namespace interface has:

independent router addressing;
optional routing policy; and
one attachment.

Each attachment uses a dedicated Linux bridge representing one logical Layer-2 segment.

6.2 Dedicated bridge rule

Separate logical Layer-2 segments must use separate bridges.

For example:

r1:eth1 -> br-r1-101 -> VLAN 101 -> host interface
r1:eth2 -> br-r1-102 -> VLAN 102 -> host interface


Even if both VLANs use the same physical host interface, br-r1-101 and br-r1-102 remain different Layer-2 domains.

RouterGen must never merge separate point-to-point VLANs onto one bridge merely because they share a host parent interface.

6.3 Addressing independence

Router namespace interface addressing and bridge host-SVI addressing are independent.

Each independently supports:

none;
static; or
dhcp.

A router interface does not require the host bridge to have an IP address.

Likewise, assigning a host SVI does not implicitly assign the router namespace interface.

6.4 Generic bridge model

br0 is not a special management-only object.

It uses the same generic bridge abstraction as every other RouterGen bridge and may represent:

a dedicated management segment;
a production segment;
in-band management;
combined management and production connectivity; or
another explicitly defined logical Layer-2 segment.

Its purpose is determined by topology intent rather than its name.

6.5 Transport types

The initial transport model supports:

local;
vlan;
host-routed;
external-bridge; and
staged.

A VLAN transport resolves its parent_role to a detected host device.

A staged transport permits the logical attachment to exist in the topology without requiring immediate external connectivity.

6.6 Host-interface roles

Topology files refer to logical host-interface roles rather than assuming that every host has the same interface names.

Examples may include:

management
production
uplink_primary
uplink_secondary


A role must resolve to a device that was actually detected on the current host.

If a configured device is missing, RouterGen must report the condition and stop resolution. It must not silently substitute another device.

6.7 Configuration precedence

Resolved values follow this precedence:

CLI override
    >
interactive answer
    >
saved host/router profile
    >
topology JSON default
    >
RouterGen default


The resolution report must identify the source of each resolved value.

For example:

production parent interface: eth1
source: saved host profile

6.8 Reconciliation boundary

Future reconciliation operates on the selected router and its owned resources.

It must:

add newly selected router interfaces;
modify changed router interfaces;
remove deselected router interfaces when explicitly authorized; and
preserve interfaces and resources whose resolved configuration has not changed.

RouterGen must not rebuild every router merely because one router changed.

6.9 FRR lifecycle separation

FRRouting is a later lifecycle layer and must not be coupled to initial network-interface application.

The required sequence is:

Resolve topology
    -> validate semantics
    -> generate network plan
    -> apply network underlay
    -> validate network underlay
    -> generate FRR configuration
    -> validate FRR configuration
    -> start or reconcile FRR
    -> validate routing state


FRR configuration or startup must not proceed when underlay validation fails.

6.10 FRR pathspace isolation

Each logical router uses its own FRR pathspace, normally matching the router identity.

Example:

Router: r1
FRR pathspace: r1

Router: r2
FRR pathspace: r2


This is required so multiple routers can coexist on one Linux or WSL2 host with isolated:

configuration;
PID state;
runtime files;
VTY sockets;
Zebra state; and
routing protocol processes.
7. Validation Model

RouterGen divides validation into separate layers.

7.1 JSON Schema validation

JSON Schema validates structural properties, including:

required objects;
required fields;
field types;
enumerated values;
address and prefix formats where expressible;
identifier syntax;
permitted transport properties;
permitted addressing modes; and
basic object shape.

Schema success means the topology is structurally valid. It does not prove that the topology is semantically or operationally valid.

7.2 Semantic validation

Semantic checks are performed outside JSON Schema.

These checks include, but are not limited to:

unique router identities;
unique namespace names;
unique FRR pathspaces;
unique interface names within each router;
valid object references;
valid attachment and bridge references;
valid host-role references;
address and prefix compatibility;
address uniqueness where required;
VLAN ID validity;
compatible transport properties;
bridge ownership consistency;
router-interface and attachment cardinality;
collisions between generated names;
duplicate or conflicting transport definitions;
required fields for the selected addressing mode;
required fields for the selected transport type;
host-interface availability after discovery; and
prevention of unintended Layer-2 segment merging.
7.3 Operational validation

Operational validation belongs to later apply phases.

It will verify conditions such as:

namespace existence;
link creation;
link state;
bridge membership;
VLAN attachment;
address assignment;
route installation;
DHCP outcome;
expected connectivity; and
FRR daemon and routing-protocol state.

Operational validation is not part of the current v0.2-A implementation except where read-only host facts are required for planning.

8. Read-Only Hard Gate

RouterGen must not proceed to an apply implementation until the following pipeline is proven:

Logical topology
       +
Actual host discovery
       +
Optional saved profile
       +
CLI overrides and user choices
       |
       v
Fully resolved router definition
       |
       v
Schema validation PASS
       |
       v
Semantic validation PASS
       |
       v
Deterministic plan
       |
       v
ZERO network changes

Hard-gate requirements
 The topology is structurally valid.
 The topology is semantically valid.
 Required host devices were actually detected.
 Every required host role is resolved.
 Every selected router interface is fully resolved.
 Every attachment has one dedicated bridge.
 Every non-staged transport is fully resolved.
 Addressing intent is unambiguous.
 The source of each resolved value is recorded.
 The same inputs produce the same normalized plan.
 Plan ordering is deterministic.
 No namespace, link, address, route, bridge, VLAN, rule, or daemon is changed.
 Validation and planning results can be written to one result file.

Passing this gate unlocks planning for the v0.2-B apply lifecycle. It does not automatically make network application safe or production-ready.

9. Planned v0.2-A Work
A1: Project and bootstrap

Deliver:

package skeleton;
CLI foundation;
dedicated .venv workflow;
environment checks;
command checks; and
preserved baseline tests.
A2: Topology and validation foundation

Deliver:

v0.2 topology model;
v0.2 JSON Schema;
topology loader;
normalized internal representation;
schema-validation reporting;
semantic-validation framework; and
initial semantic rule set.
A3: Host discovery

Deliver structured, read-only discovery using commands such as:

ip -j link show
ip -j addr show
ip -j route show
ip -j rule show
bridge -j link show
bridge -j vlan show


Discovery should identify:

available interfaces;
interface type;
administrative and operational state;
addresses;
MTU;
MAC address;
master relationships;
VLAN relationships;
bridge membership;
existing routes; and
information needed to prevent naming or addressing collisions.
A4: Resolution

Deliver:

saved host profile loading;
saved router profile loading;
interactive selection framework;
non-interactive mode;
CLI overrides;
precedence processing;
role-to-device resolution;
provenance for resolved values;
unresolved-value reporting; and
a fully resolved router representation.
A5: Deterministic planning

Deliver a plan that describes proposed operations without executing them.

The plan should identify actions such as:

CREATE namespace r1
CREATE bridge br-r1-mgmt
CREATE veth pair
MOVE router peer into namespace r1
ATTACH host peer to bridge br-r1-mgmt
CREATE VLAN transport on resolved parent device
ASSIGN router address
LEAVE bridge SVI unnumbered


During v0.2-A, these are plan records only. They must not execute system commands that change network state.

10. Out of Scope for the Current Phase

The following items are explicitly outside v0.2-A:

applying network changes;
creating or deleting namespaces;
creating or deleting bridges;
creating veth pairs;
creating VLAN interfaces;
assigning or removing addresses;
changing routes or policy rules;
enabling IP forwarding;
modifying firewall or nftables state;
configuring persistence across reboot;
FRR configuration generation;
FRR startup or shutdown;
OSPF or BGP configuration;
rollback execution;
destructive reconciliation;
multi-host orchestration;
remote deployment;
production appliance packaging; and
production support guarantees.

These items may appear in architecture documents, but they must be labelled as planned or future work.

11. Known Limitations

Current known limitations include:

RouterGen is pre-alpha.
The v0.2 read-only implementation is not complete.
The current actual WSL2 host has only the detected eth0 interface.
The current host does not have eth1, br0, pre-created VLANs, or RouterGen network namespaces.
Example topologies requiring those resources must not be applied to the current host without valid resolution and a future approved apply phase.
Native Linux portability is an architectural objective but is not yet a completed qualification result.
DHCP behavior has not yet been implemented or operationally validated.
External-bridge ownership and lifecycle rules still require apply-phase implementation.
Host-routed transport has not yet been operationally implemented.
FRR intent is represented architecturally but FRR lifecycle management is not implemented.
Multi-host transport orchestration is not part of the current milestone.
Rollback and recovery behavior has not yet been implemented.
Persistence across WSL shutdown or host reboot is not yet implemented.
No production security or privilege-separation review has been completed.
12. Safety Rules

The following rules apply throughout development:

Never silently replace a missing configured interface.
Never treat an example topology as approved for the current host.
Never run apply behavior from a read-only command.
Never merge independent Layer-2 segments onto one bridge.
Never assume bridge addressing from router-interface addressing.
Never assume router-interface addressing from bridge addressing.
Never start FRR before the network underlay passes validation.
Never reuse an FRR pathspace between logical routers.
Never delete unrelated host or router resources.
Never claim a feature is stable solely because its design is documented.
Never claim a live operation passed without a recorded result.
Never weaken an existing test merely to allow a new implementation to pass.
Never execute a plan merely because planning succeeded.
Never use the current WSL2 eth0 as a substitute for a missing topology interface unless it is explicitly selected through the resolution model.
13. Definition of Stability

RouterGen uses the following stability labels.

Design defined

The intended architecture and behavior are documented, but implementation may not exist.

Implemented

The capability exists in code but may not yet have complete test coverage.

Deterministically tested

Automated tests demonstrate repeatable behavior without live network changes.

Lab verified

The capability has been exercised against a controlled Linux or WSL2 network environment and produced an auditable passing result.

Stable

The capability has:

documented behavior;
defined error handling;
deterministic automated tests;
controlled live verification where applicable;
regression coverage;
upgrade or migration consideration; and
no known critical safety defect.
Production ready

The capability additionally has:

security review;
privilege and ownership controls;
failure recovery;
rollback behavior;
operational documentation;
supported installation and upgrade procedures;
production monitoring guidance; and
an explicit support policy.

No RouterGen capability should currently be described as production ready.

14. Evidence and Result Files

Milestone verification should produce an auditable result file.

The preferred workflow is:

one wrapper
    -> prerequisite checks
    -> milestone tests
    -> safety checks
    -> consolidated result file


A result should include:

RouterGen version;
Git commit identifier;
topology hash where applicable;
schema version;
host/platform details;
Python version;
command versions;
test totals;
PASS/FAIL status;
failed stage;
safety-gate result;
whether network changes were permitted;
whether network changes were detected; and
final result marker.

Example final markers:

FINAL_RESULT=PASS
FAILURE_STAGE=NONE
NETWORK_CHANGES_PERMITTED=NO
NETWORK_CHANGES_DETECTED=NO


A milestone is not considered verified until its result has been reviewed and recorded.

15. Branch and Change Discipline

Recommended branch naming:

main
feature/v0.2-a1-bootstrap
feature/v0.2-a2-schema
feature/v0.2-a3-discovery
feature/v0.2-a4-resolution
feature/v0.2-a5-planning


Recommended commit convention:

feat: add RouterGen environment diagnostic
fix: reject unresolved host interface role
test: add deterministic plan ordering coverage
docs: record v0.2 bridge ownership rule
refactor: separate schema and semantic validation


Before merging into main:

 Existing tests pass.
 New milestone tests pass.
 Read-only safety checks pass.
 Documentation reflects actual behavior.
 Planned behavior is not described as implemented.
 PROJECT_STATUS.md is updated.
 CHANGELOG.md is updated when the change is user-visible.
16. Decision Log

Significant architectural changes should be recorded here or in a dedicated Architecture Decision Record under docs/architecture/decisions/.

Decision	Status	RationaleUse declarative topology JSON	Accepted	Separates portable intent from host implementation
Discover the host before resolution	Accepted	Prevents hard-coded interface assumptions
Use one bridge per logical L2 segment	Accepted	Preserves Layer-2 isolation
Keep router and host-SVI addressing independent	Accepted	Supports routed, bridged, numbered, and unnumbered host designs
Use explicit resolution precedence	Accepted	Makes configuration sources predictable
Reject missing configured devices	Accepted	Prevents unsafe silent substitution
Separate read-only planning from apply	Accepted	Provides a safety and review boundary
Reconcile only selected router changes	Accepted	Avoids unnecessary rebuilds and disruption
Add FRR after underlay validation	Accepted	Prevents routing daemons from starting on an invalid network
Use one FRR pathspace per router	Accepted	Isolates multiple FRR routers on one host
Keep semantic checks outside JSON Schema	Accepted	Supports cross-reference and host-dependent validation
17. Next Action

The next action is to implement:

v0.2-A1: Project and Bootstrap


The implementation must begin with:

the package skeleton;
the CLI entry point;
dedicated .venv bootstrap support;
read-only command and environment checks;
test integration; and
verification that the existing 12/12 baseline still passes.

No bridge, namespace, VLAN, veth, address, route, rule, or FRR change is authorized during this milestone.

18. Completion Record

Update this section whenever a milestone is completed.

v0.1 baseline
Status: VERIFIED
Tests: 12 PASS / 0 FAIL
Scope: Existing validation and read-only planning baseline
Network changes: None

v0.2-A1
Status: NOT STARTED
Result file: Not available
Tests: Not available
Network changes permitted: No

v0.2-A2
Status: PLANNED
Result file: Not available
Tests: Not available
Network changes permitted: No

v0.2-A3
Status: PLANNED
Result file: Not available
Tests: Not available
Network changes permitted: No

v0.2-A4
Status: PLANNED
Result file: Not available
Tests: Not available
Network changes permitted: No

v0.2-A5
Status: PLANNED
Result file: Not available
Tests: Not available



Network changes permitted: No


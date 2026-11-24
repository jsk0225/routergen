# RouterGen Architecture

> **Architecture version:** v0.2  
> **Project:** RouterGen  
> **Status:** Architecture baseline for v0.2 development  
> **Last updated:** 2026-11-24

---

## 1. Purpose

RouterGen is a safety-first topology compiler for creating reproducible Linux
router environments from declarative topology definitions.

Its purpose is to separate:

1. the logical router topology that the user wants;
2. the physical interfaces and networking resources actually available on
   the host; and
3. the Linux operations required to construct the desired router.

RouterGen does not assume that two hosts have identical interface names or
network layouts.

Instead, it discovers the host, resolves logical interface roles to actual
devices, validates the resulting configuration, generates a deterministic
plan, and only in a later lifecycle phase applies that plan.

The fundamental workflow is:


Intent
  |
  v
Discovery
  |
  v
Resolution
  |
  v
Validation
  |
  v
Planning
  |
  v
Approval
  |
  v
Apply
  |
  v
Post-Apply Validation
  |
  v
FRR Lifecycle


The current v0.2-A development phase ends at deterministic read-only planning.

2. Design Goals

RouterGen is designed around the following goals.

2.1 Portability

A topology should describe logical intent rather than depend on host-specific names such as:

eth0
eth1
ens192
enp3s0


Logical host roles are resolved against interfaces discovered on the actual host.

2.2 Repeatability

The same:

topology;
detected host state;
profile;
CLI overrides; and
user choices

must produce the same normalized configuration and deterministic plan.

2.3 Safety

RouterGen must understand the difference between:

desired state;
discovered state;
resolved state;
planned changes; and
applied state.

A successful plan is not authorization to perform the plan.

2.4 Isolation

Each router runs inside its own Linux network namespace.

Independent Layer-2 segments remain isolated.

Multiple FRRouting instances use independent FRR pathspaces.

2.5 Explicit configuration

RouterGen must not silently substitute resources.

For example, if the topology expects a host interface role that cannot be resolved, RouterGen must fail resolution rather than silently use another interface.

2.6 Declarative intent

Topology configuration describes the desired architecture rather than a sequence of shell commands.

RouterGen determines the operations necessary to achieve that architecture.

2.7 Lifecycle separation

Network-interface provisioning and routing-daemon provisioning are separate lifecycle layers.

The Linux network underlay must be valid before FRR configuration or startup can occur.

3. High-Level Architecture

RouterGen consists of the following logical stages:

                 +----------------------+
                 | Logical Topology JSON|
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Schema Validation    |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Semantic Validation  |
                 +----------+-----------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
   +--------------------+        +--------------------+
   | Host Discovery     |        | Profiles / Inputs  |
   +---------+----------+        +----------+---------+
             |                              |
             +--------------+---------------+
                            |
                            v
                 +----------------------+
                 | Resolution Engine    |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Resolved Topology    |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Semantic Validation  |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Planning Engine      |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Deterministic Plan   |
                 +----------+-----------+
                            |
                  v0.2-A HARD GATE
                  ZERO NETWORK CHANGES
                            |
               ------------+------------
                    Future lifecycle
                            |
                            v
                 +----------------------+
                 | Apply Engine         |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Network Validation   |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | FRR Lifecycle        |
                 +----------------------+

4. Core Architecture Model

The central RouterGen networking relationship is:

ROUTER
  |
  v
ROUTER INTERFACE
  |
  v
ATTACHMENT
  |
  v
DEDICATED BRIDGE
  |
  v
TRANSPORT
  |
  v
DETECTED HOST DEVICE


For example:

r1
 |
 +-- eth1
      |
      +-- attachment
           |
           +-- br-r1-101
                 |
                 +-- VLAN 101
                        |
                        +-- host production interface


The logical topology describes this relationship.

Host discovery determines which physical device satisfies the required host role.

5. Host Model

The host represents the Linux environment containing RouterGen-managed routers.

The host may be:

WSL2;
a native Linux machine;
a virtual machine; or
another supported Linux environment.

Initial development and validation target WSL2 with Ubuntu 24.04.

The host contains discovered networking resources such as:

HOST
 |
 +-- network interfaces
 |
 +-- addresses
 |
 +-- routes
 |
 +-- bridges
 |
 +-- VLAN interfaces
 |
 +-- policy rules
 |
 +-- existing namespaces
 |
 +-- existing RouterGen resources
 |
 +-- system capabilities


Host discovery is read-only.

RouterGen should primarily consume structured command output where available, for example:

ip -j link show
ip -j addr show
ip -j route show
ip -j rule show
bridge -j link show
bridge -j vlan show


Parsing human-formatted command output should be avoided when a structured representation is available.

6. Router Model

A RouterGen router represents one logical router instance.

The router has an identity such as:

r1
r2
r3


A router contains:

ROUTER
 |
 +-- identity
 |
 +-- namespace
 |
 +-- interfaces
 |
 +-- optional routing policy
 |
 +-- optional FRR intent


Normally, one router maps to one Linux network namespace.

For example:

Router identity: r1
Namespace:       r1
FRR pathspace:   r1


These names may be configurable, but their ownership and uniqueness must remain explicit.

7. Router Interface Model

Each router contains one or more interfaces.

A router interface has its own addressing intent.

Supported addressing modes are:

none
static
dhcp


Conceptually:

ROUTER_INTERFACE
 |
 +-- name
 |
 +-- router_addressing
 |    |
 |    +-- none
 |    +-- static
 |    +-- dhcp
 |
 +-- optional routing_policy
 |
 +-- attachment


The router interface belongs to the router namespace rather than the host network namespace.

8. Attachment Model

Every selected router interface connects to an attachment.

The attachment represents the Layer-2 relationship between the router and the host.

Conceptually:

ROUTER INTERFACE
       |
       v
   ATTACHMENT
       |
       v
     BRIDGE
       |
       v
   TRANSPORT


An attachment owns one dedicated bridge representing one logical Layer-2 segment.

This mapping is fundamental to the v0.2 architecture.

9. Bridge Model

A RouterGen bridge represents one logical Layer-2 segment.

A bridge is not merely an implementation convenience.

It is an isolation boundary.

For example:

r1:eth1 -> br-r1-101 -> VLAN 101
r1:eth2 -> br-r1-102 -> VLAN 102


These represent two different Layer-2 segments.

Even if VLAN 101 and VLAN 102 eventually traverse the same host device:

                   eth0
                    |
             +------+------+
             |             |
          VLAN 101       VLAN 102
             |             |
         br-r1-101     br-r1-102
             |             |
          r1:eth1        r1:eth2


the bridges must remain separate.

RouterGen must never collapse independent Layer-2 segments into one bridge simply because their transports share a physical parent.

10. Host SVI Model

A RouterGen bridge may optionally have Layer-3 addressing on the host.

This is referred to as the host SVI.

Host SVI addressing is independent from router-interface addressing.

Supported modes are:

none
static
dhcp


For example:

Router side:

r1:eth1
192.0.2.2/30

        |
        |
     bridge

        |
        |
Host SVI
192.0.2.1/30


is valid.

However:

Router side:

r1:eth1
192.0.2.2/30

        |
        |
     bridge

Host SVI:
none


is also valid.

RouterGen must therefore never infer:

router address -> host SVI address


or:

host SVI address -> router address


unless an explicit future feature defines such behavior.

11. Generic Bridge Principle

Bridge names do not define their purpose.

For example, br0 is not inherently a management bridge.

The same generic bridge abstraction can support:

management;
production;
in-band management;
service networks;
point-to-point connectivity; or
other topology-defined purposes.

Purpose comes from topology intent, not naming convention.

12. Transport Model

Transport describes how a RouterGen bridge connects beyond the local logical router.

The initial architecture supports:

local
vlan
host-routed
external-bridge
staged

12.1 Local Transport

Local transport represents networking that remains entirely within the current host.

It does not require an external physical interface.

Example:

r1
 |
 br-r1-r2
 |
 r2


The exact implementation may depend on the final topology model, but no external host interface is required.

12.2 VLAN Transport

VLAN transport connects the logical Layer-2 segment through a VLAN on a resolved host interface.

For example:

r1:eth1
   |
br-r1-101
   |
 VLAN 101
   |
production
   |
resolved host device
   |
 eth0


The logical topology may specify:

parent_role: production
vlan_id: 101


rather than:

parent_device: eth0


Host discovery and resolution determine that:

production -> eth0


on the current host.

12.3 Host-Routed Transport

Host-routed transport represents connectivity where the host performs Layer-3 routing rather than extending a Layer-2 VLAN.

Its detailed apply implementation belongs to a later RouterGen phase.

The v0.2 data model reserves this transport type so it can be represented without changing the fundamental attachment architecture.

12.4 External-Bridge Transport

External-bridge transport connects a RouterGen attachment to an existing bridge that RouterGen may not own.

This distinction is important because externally owned resources must not be deleted merely because a RouterGen router is removed.

Future reconciliation must distinguish:

RouterGen-owned resource


from:

externally managed resource

12.5 Staged Transport

A staged transport allows a router interface and its logical Layer-2 segment to exist in the desired topology before external connectivity is assigned.

This is useful during staged deployment and topology development.

A staged interface must not be silently connected to another detected interface.

13. Host Interface Roles

Topology definitions should avoid depending directly on host-specific interface names wherever practical.

Instead, they may define roles such as:

management
production
uplink_primary
uplink_secondary


The resolver maps:

logical role
    |
    v
detected host device


For example:

production -> eth0


on one host and:

production -> enp3s0


on another.

The logical topology can therefore remain unchanged.

14. Missing Interface Rule

Missing configured host interfaces must not be silently substituted.

For example, suppose the saved host profile contains:

production -> eth1


but discovery finds only:

eth0


RouterGen must report the unresolved configuration.

It must not automatically decide:

production -> eth0


This is a safety boundary.

15. Configuration Sources

RouterGen can obtain configuration values from several sources.

The v0.2 precedence order is:

CLI override
      >
interactive answer
      >
saved host/router profile
      >
topology JSON default
      >
RouterGen default


The resolver must preserve the provenance of resolved values.

For example:

Field:  parent_device
Value:  eth0
Source: saved_host_profile


This makes configuration decisions auditable.

16. Resolution Engine

The resolution engine combines:

logical topology
+
host discovery
+
optional profiles
+
interactive answers
+
CLI overrides
+
RouterGen defaults


to create:

FULLY RESOLVED TOPOLOGY


Resolution is separate from application.

Resolving:

production -> eth0


must not configure eth0.

A fully resolved topology must contain enough information for the planning engine to determine precisely what would need to change.

17. Validation Architecture

RouterGen separates validation into several layers.

17.1 Schema Validation

JSON Schema verifies structural correctness.

Examples include:

required properties;
field types;
allowed enumeration values;
identifier formatting;
valid addressing modes;
supported transport types;
basic value ranges.

Schema validation does not prove that the topology is operationally valid.

17.2 Semantic Validation

Semantic validation handles relationships that JSON Schema alone cannot adequately express.

Examples include:

unique router identities;
unique namespace names;
unique FRR pathspaces;
valid object references;
valid router-interface relationships;
valid attachment relationships;
valid bridge ownership;
unique interface names;
VLAN constraints;
addressing conflicts;
duplicate resource names;
host-role resolution;
transport-specific requirements;
prevention of unintended Layer-2 merging.

Semantic validation operates both before and after host-dependent resolution where appropriate.

17.3 Operational Validation

Operational validation verifies the real system after eventual application.

This includes:

namespace existence;
interface existence;
bridge membership;
administrative link state;
VLAN configuration;
IP addressing;
routes;
policy rules;
connectivity;
FRR daemon state; and
routing protocol state.

Operational validation belongs primarily to later lifecycle phases.

18. Planning Architecture

The planner converts a fully resolved topology into deterministic proposed operations.

For example:

CREATE namespace r1

CREATE bridge br-r1-101

CREATE veth
    host peer:   v-r1-101-h
    router peer: v-r1-101-r

MOVE v-r1-101-r
    namespace: r1

ATTACH v-r1-101-h
    bridge: br-r1-101

CREATE VLAN
    VLAN: 101
    parent: eth0

ASSIGN router address
    interface: r1:eth1
    address: 192.0.2.2/30


During v0.2-A these represent plan records only.

The planning engine must not implement plan generation by immediately executing the corresponding Linux commands.

19. Deterministic Planning

For identical normalized input, the plan must be identical.

This includes deterministic:

object naming;
operation ordering;
interface ordering;
bridge ordering;
output formatting where practical;
dependency ordering; and
validation results.

This property makes plans suitable for:

testing;
Git-based review;
auditing;
comparison;
troubleshooting; and
future reconciliation.
20. Read-Only Boundary

v0.2-A has a strict safety boundary:

Topology
   |
   v
Discovery
   |
   v
Resolution
   |
   v
Validation
   |
   v
Planning
   |
   v
STOP


No operation before this boundary may intentionally:

create a namespace;
remove a namespace;
create a veth;
delete an interface;
create a bridge;
change bridge membership;
create a VLAN;
change an address;
change a route;
change a policy rule;
modify forwarding;
change firewall state; or
start or stop FRR.

The hard gate before v0.2-B is:

fully resolved topology
+
semantic PASS
+
deterministic plan
+
zero network changes

21. Future Apply Engine

The apply engine will consume a previously validated plan.

Its eventual responsibilities include:

preflight
   |
   v
plan verification
   |
   v
authorization
   |
   v
dependency-ordered execution
   |
   v
post-apply validation
   |
   +---- PASS ---> commit operational state
   |
   +---- FAIL ---> recovery / rollback policy


Apply functionality is outside the current v0.2-A phase.

Architecture documentation must not imply that application is currently available.

22. Reconciliation Model

RouterGen is intended to reconcile desired state rather than blindly rebuild a host.

For a selected router:

Desired State
     |
     +------ compare ------+
                          |
                   Existing State
                          |
                          v
                    Difference
                          |
               +----------+----------+
               |          |          |
              ADD       CHANGE      REMOVE


Resources that are unchanged must remain unchanged.

A change to r1 must not automatically rebuild r2.

Future reconciliation should therefore operate on explicit:

resource ownership;
router ownership;
normalized identities; and
desired versus discovered state.
23. Resource Ownership

Future apply and reconciliation logic must distinguish between:

RouterGen-owned


and:

external


resources.

RouterGen may safely reconcile resources it owns according to its lifecycle rules.

It must not assume ownership of an existing host resource merely because that resource is referenced by the topology.

This is particularly important for:

physical interfaces;
externally created bridges;
existing routes;
host management interfaces; and
infrastructure created by other software.
24. FRRouting Architecture

FRRouting is deliberately separated from network-underlay provisioning.

The required lifecycle is:

Topology
   |
   v
Network resolution
   |
   v
Network plan
   |
   v
Network apply
   |
   v
Underlay validation
   |
   +--- FAIL ---> STOP
   |
   +--- PASS
          |
          v
    FRR configuration
          |
          v
    FRR validation
          |
          v
      FRR startup
          |
          v
 Routing validation


RouterGen must not use FRR startup as a way to determine whether the underlay was configured correctly.

The underlay must independently pass validation first.

25. FRR Pathspaces

Each RouterGen router must use an independent FRR pathspace.

Normally:

Router r1 -> FRR pathspace r1
Router r2 -> FRR pathspace r2
Router r3 -> FRR pathspace r3


Conceptually:

Linux host
 |
 +-- namespace r1
 |      |
 |      +-- FRR pathspace r1
 |
 +-- namespace r2
 |      |
 |      +-- FRR pathspace r2
 |
 +-- namespace r3
        |
        +-- FRR pathspace r3


Pathspace isolation prevents routers from unintentionally sharing:

configuration;
PID files;
Zebra state;
VTY state;
runtime files; or
routing protocol daemon state.

FRR intent belongs in the logical RouterGen topology, but FRR execution belongs to a later lifecycle layer.

26. Example Multi-Host Architecture

One of RouterGen's longer-term use cases is running separate router instances on separate machines.

For example:

Host A                                    Host B

Router r1                                Router r2
namespace r1                             namespace r2
    |                                        |
 r1:eth1                                  r2:eth1
    |                                        |
 br-r1-101                               br-r2-101
    |                                        |
 VLAN 101                                 VLAN 101
    |                                        |
 host interface                          host interface
    |                                        |
    +---------- external network ------------+


The logical topology describes the relationship.

Each host independently:

discovers its local devices;
selects the router assigned to that host;
resolves the logical host roles;
validates the local portion of the topology;
generates its local deterministic plan; and
eventually applies only its owned portion.

This keeps the logical topology portable across heterogeneous hosts.

27. Example Single-Interface VLAN Architecture

Multiple Layer-2 transports may share one physical host device while remaining isolated.

For example:

                      eth0
                       |
             +---------+---------+
             |                   |
          VLAN 101            VLAN 102
             |                   |
         br-r1-101           br-r1-102
             |                   |
          r1:eth1              r1:eth2


The shared physical device does not imply a shared bridge.

This is an important RouterGen architecture rule.

28. Example Multi-Interface Architecture

Transports may also use different physical interfaces:

r1:eth1                  r1:eth2
   |                        |
br-r1-101               br-r1-201
   |                        |
VLAN 101                 VLAN 201
   |                        |
production               secondary
   |                        |
 eth0                     eth1


The same topology model supports both cases.

Only role resolution differs.

29. Failure Philosophy

RouterGen should prefer a safe explicit failure over an unsafe implicit decision.

Examples:

Configured host role cannot be resolved
    -> FAIL

Duplicate bridge identity
    -> FAIL

Conflicting addressing
    -> FAIL

Invalid VLAN
    -> FAIL

Ambiguous resource ownership
    -> FAIL

FRR requested before underlay validation
    -> FAIL


An error should explain:

what failed
why it failed
which topology object caused it
which source supplied the value
what the user can do to correct it

30. Reporting

RouterGen should generate machine-readable internal results and human-readable reports.

A report should identify:

topology source;
schema version;
host identity;
selected router;
discovery result;
resolved interfaces;
value provenance;
validation result;
semantic errors;
warnings;
proposed plan;
whether changes are authorized;
whether changes occurred; and
final result.

The development workflow should favor:

one wrapper
    |
    v
one consolidated result file


where practical.

31. Package Architecture

The intended Python package separation is:

src/routergen/
 |
 +-- cli
 |
 +-- models
 |
 +-- validation
 |
 +-- discovery
 |
 +-- resolution
 |
 +-- planning
 |
 +-- reporting
 |
 +-- errors


Future lifecycle stages may add modules such as:

apply
reconciliation
state
recovery
frr


The important architectural property is that read-only modules must not acquire hidden write behavior simply for implementation convenience.

In particular:

discovery != apply
resolution != apply
validation != apply
planning != apply

32. Architecture Invariants

The following rules are architecture invariants for v0.2.

Logical topology is separate from detected host state.
Host discovery occurs before host-dependent resolution.
Missing configured host interfaces are never silently substituted.
Each attachment represents one logical Layer-2 segment.
Each logical Layer-2 attachment receives a dedicated bridge.
Independent point-to-point VLANs must not be merged through a common bridge.
Router-interface addressing and host-SVI addressing are independent.
Both router-interface and host-SVI addressing support none, static, and dhcp.
Transport is separate from bridge and attachment identity.
VLAN parent roles resolve to detected host devices.
Configuration precedence is deterministic.
Resolved values retain provenance.
Read-only planning is separate from apply.
Identical normalized inputs produce deterministic plans.
Reconciliation changes only resources that need changing.
Unchanged router resources are preserved.
RouterGen does not assume ownership of externally managed resources.
FRR is a later lifecycle layer.
Network underlay validation must pass before FRR configuration or startup.
Each logical router uses an independent FRR pathspace.

Changes to these rules constitute an architecture change and should be reviewed explicitly.

33. Current Implementation Boundary

The architecture described in this document extends beyond the currently implemented RouterGen functionality.

The current development scope is:

v0.2-A


which covers:

A1  Project / bootstrap

A2  Topology schema and
    semantic validation framework

A3  Structured host discovery

A4  Profiles, prompts, precedence,
    role-to-device mapping and resolution

A5  Deterministic read-only planning


The hard gate before v0.2-B is:

Logical topology
       +
Actual host discovery
       +
Optional profile
       +
User / CLI choices
       |
       v
Fully resolved router
       |
       v
Semantic validation PASS
       |
       v
Deterministic plan
       |
       v
ZERO NETWORK CHANGES


See the repository PROJECT_STATUS.md for the current implementation and verification status.

34. Architecture Change Control

Architecture decisions should not be changed silently during implementation.

A proposed change to an architecture invariant should include:

the current behavior;
the proposed behavior;
the reason for the change;
backward-compatibility impact;
topology-schema impact;
safety impact;
migration requirements; and
required test changes.

Significant decisions should eventually be stored as Architecture Decision Records under:

docs/architecture/decisions/


For example:

docs/architecture/decisions/
├── ADR-0001-dedicated-bridge-per-l2-segment.md
├── ADR-0002-interface-role-resolution.md
├── ADR-0003-read-only-plan-before-apply.md
└── ADR-0004-frr-pathspace-per-router.md

35. Relationship to Other Documentation

This document answers:

How is RouterGen designed?

Other repository documents have different responsibilities.

README.md
    What is RouterGen and how do I get started?

PROJECT_STATUS.md
    What is implemented, tested, stable, and next?

docs/architecture/architecture.md
    How is RouterGen designed?

docs/data-model/
    What objects and relationships exist?

docs/schema/
    How is topology JSON structurally defined?

docs/semantic-validation/
    Which relationships and constraints are validated?

docs/host-discovery/
    How does RouterGen understand the current host?

docs/resolution/
    How does intent become fully resolved configuration?

docs/planning/
    How is a deterministic execution plan produced?

docs/safety/
    What prevents unsafe host changes?

docs/frr/
    How does routing-daemon lifecycle management work?

docs/examples/
    What do valid RouterGen topologies look like?

36. Summary

RouterGen follows this fundamental model:

DECLARE
    what router topology is wanted

DISCOVER
    what the host actually provides

RESOLVE
    logical intent against actual resources

VALIDATE
    that the result is safe and internally consistent

PLAN
    exactly what would need to change

APPROVE
    before changing the host

APPLY
    only validated, explicitly authorized changes

VERIFY
    the resulting network state

CONFIGURE FRR
    only after the network underlay passes





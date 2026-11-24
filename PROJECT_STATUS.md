# RouterGen Project Status

> **Project stage:** Pre-alpha
> **Development line:** v0.2
> **Current phase:** v0.2-A, Read-Only Architecture
> **Current milestone:** v0.2-A1, Project and Bootstrap
> **Milestone state:** Implemented and WSL2-lab verified, pending merge to `main`
> **Last updated:** 2026-11-25
> **Network changes permitted in v0.2-A:** No

---

## 1. Status Summary

RouterGen is a safety-first topology compiler for creating reproducible Linux
and WSL2 router environments from declarative topology definitions.

The v0.2 development line is currently in **v0.2-A**, which establishes the
complete read-only pipeline before any network mutation functionality is
allowed.

The v0.2-A pipeline is:

```text
Topology
   |
   v
Schema Validation
   |
   v
Host Discovery
   |
   v
Resolution
   |
   v
Semantic Validation
   |
   v
Deterministic Planning
   |
   v
STOP
```

The entire v0.2-A phase must make **zero network configuration changes**.

### Current position

v0.2-A1 has now been:

- implemented on `feature/v0.2-a1-bootstrap`;
- tested in GitHub Codespaces;
- tested on the WSL2 test laptop;
- verified with 7/7 automated tests;
- verified with read-only environment diagnostics; and
- confirmed to make no network changes.

A1 has **not yet been merged into `main`**.

The next repository action is to record the A1 evidence, review the feature
branch through a Pull Request, and merge it into `main`.

---

## 2. Current State at a Glance

| Area | Status | Notes |
|---|---|---|
| Project purpose | Defined | Safety-first topology compiler for Linux router environments |
| v0.2 data model | Frozen for v0.2-A | Host, router, interface, bridge, SVI, transport, and optional FRR intent |
| JSON Schema architecture | Defined | Structural validation belongs in JSON Schema |
| Semantic-validation architecture | Defined | Cross-object and host-dependent validation remains outside JSON Schema |
| Host-discovery architecture | Defined | Structured `ip -j` / `bridge -j` data is the preferred interface |
| Configuration precedence | Frozen | CLI > prompt > profile > topology default > RouterGen default |
| Read-only planning architecture | Defined | Plans must be deterministic and non-mutating |
| A1 implementation | WSL2-lab verified | 7/7 tests PASS on Codespace and WSL2 |
| A2 implementation | Not started | Next development milestone after A1 merge |
| Network apply | Not implemented | Explicitly outside v0.2-A |
| Reconciliation | Design defined | Not implemented |
| Post-apply validation | Planned | Later lifecycle |
| FRR lifecycle | Design defined | Must follow successful network-underlay validation |
| Production readiness | No | Project remains pre-alpha |

---

## 3. Historical Prototype Baseline

Before the current GitHub-based RouterGen implementation, the earlier
`wsl2-router-netgen` prototype achieved:

```text
12 PASS
0 FAIL
```

That result is retained as **historical prototype evidence**.

It must not be described as the current GitHub RouterGen test suite.

The current GitHub RouterGen implementation has its own automated test
baseline, established during v0.2-A1.

Where earlier prototype behavior is carried into the current codebase, it
should be represented by current RouterGen tests rather than relying solely
on the historical 12/12 result.

---

## 4. Current GitHub Test Baseline

Current RouterGen feature branch:

```text
feature/v0.2-a1-bootstrap
```

Verified implementation commits:

```text
a9a3204  feat: add RouterGen v0.2-A1 bootstrap foundation
f5972dc  build: add reproducible development bootstrap
```

Current automated test result:

```text
7 PASS
0 FAIL
```

The current test suite covers:

- package version;
- CLI parser construction;
- CLI baseline execution;
- successful environment-diagnostic evaluation;
- missing-required-command failure;
- non-Linux failure;
- read-only safety reporting.

This becomes the current RouterGen test baseline for the A1 implementation.

---

## 5. v0.2-A Milestones

| Milestone | Description | Status |
|---|---|---|
| A1 | Project/bootstrap | **WSL2-lab verified, pending merge** |
| A2 | Topology/schema + semantic-validation framework | Not started |
| A3 | Structured host discovery | Planned |
| A4 | Resolution, profiles, prompts, and precedence | Planned |
| A5 | Deterministic read-only planning | Planned |

---

# 6. Current Milestone: v0.2-A1

## 6.1 Objective

Establish a clean, reproducible RouterGen development and execution
environment without modifying host networking.

## 6.2 Implemented

The A1 implementation currently provides:

- Python package structure under `src/routergen`;
- `pyproject.toml` packaging;
- editable development installation;
- RouterGen CLI entry point;
- `routergen --help`;
- `routergen --version`;
- `routergen diagnose`;
- Linux platform detection;
- WSL detection;
- virtual-environment reporting;
- required external-command discovery;
- command checks for:
  - `ip`;
  - `bridge`;
  - `sysctl`; and
  - `ss`;
- dedicated RouterGen `.venv`;
- automated pytest framework;
- development dependency definition;
- reproducible development bootstrap;
- fresh `.venv` bootstrap;
- repeat/idempotent bootstrap behavior; and
- explicit read-only safety reporting.

The diagnostic reports:

```text
FINAL_RESULT=PASS|FAIL
NETWORK_CHANGES_PERMITTED=NO
```

A1 does not contain network apply functionality.

---

## 6.3 Reproducible Bootstrap

The development bootstrap is:

```text
scripts/bootstrap-dev.sh
```

Its workflow is:

```text
Check Python >= 3.10
        |
        v
Create/reuse .venv
        |
        v
Install RouterGen + development dependencies
        |
        v
Run automated tests
        |
        v
Run read-only environment diagnostics
```

It can be run with:

```bash
./scripts/bootstrap-dev.sh
```

The script is designed to work without requiring the caller's shell to have
the RouterGen virtual environment activated.

---

## 6.4 Codespace Verification

Environment:

```text
Platform: GitHub Codespaces / Linux
Python: 3.14.2
RouterGen: 0.2.0.dev0
Virtual environment: /workspaces/routergen/.venv
WSL: no
```

Required commands:

```text
ip      PASS
bridge  PASS
sysctl  PASS
ss      PASS
```

Automated tests:

```text
7 PASS
0 FAIL
```

Diagnostic:

```text
FINAL_RESULT=PASS
NETWORK_CHANGES_PERMITTED=NO
```

Fresh virtual-environment creation was tested successfully.

A subsequent bootstrap against the already-created environment also passed,
demonstrating repeatable/idempotent bootstrap behavior.

Generated `.venv`, Python-cache, pytest-cache, and package-build artifacts
remain excluded from Git.

---

## 6.5 WSL2 Test-Laptop Verification

A1 was independently verified on the project's WSL2 test laptop.

Checkout:

```text
/mnt/c/Project/routergen
```

Verified branch:

```text
feature/v0.2-a1-bootstrap
```

Verified commit:

```text
f5972dc
```

Environment:

```text
Platform: Linux / WSL2
Python: 3.12.3
RouterGen: 0.2.0.dev0
Virtual environment: /mnt/c/Project/routergen/.venv
WSL: yes
```

WSL kernel reported:

```text
6.18.58.1-microsoft-standard-WSL2
```

Required commands:

```text
ip      PASS
bridge  PASS
sysctl  PASS
ss      PASS
```

Automated tests:

```text
7 PASS
0 FAIL
```

Diagnostic:

```text
FINAL_RESULT=PASS
NETWORK_CHANGES_PERMITTED=NO
```

The RouterGen environment is separate from the existing OSPF Alt project
environment.

No OSPF Alt namespace, FRR pathspace, route, bridge, VLAN, interface, or
other network configuration was intentionally modified by A1 verification.

---

## 6.6 A1 Acceptance Criteria

- [x] RouterGen installs into its own `.venv`.
- [x] The RouterGen `.venv` is separate from the OSPF Alt environment.
- [x] RouterGen installs in editable mode.
- [x] The CLI starts successfully.
- [x] `routergen --help` works.
- [x] `routergen --version` works.
- [x] `routergen diagnose` works.
- [x] Linux is detected.
- [x] WSL is detected when applicable.
- [x] Required external commands are detected.
- [x] Missing required-command behavior is covered by automated tests.
- [x] Non-Linux diagnostic failure is covered by automated tests.
- [x] Fresh `.venv` bootstrap has been verified.
- [x] Repeated bootstrap has been verified.
- [x] Automated tests pass in Codespaces.
- [x] Automated tests pass on the WSL2 test laptop.
- [x] A1 diagnostic output states that network changes are not permitted.
- [x] A1 performs no intentional network configuration changes.
- [ ] A1 verification evidence is committed to `PROJECT_STATUS.md`.
- [ ] A1 Pull Request is reviewed.
- [ ] A1 feature branch is merged into `main`.
- [ ] Codespace `main` is synchronized after the merge.
- [ ] WSL2 test checkout is synchronized with merged `main`.

A1 will be marked **COMPLETE** after the remaining GitHub merge and
post-merge synchronization steps pass.

---

# 7. v0.2 Architecture Invariants

Detailed architecture is maintained in:

```text
docs/architecture/architecture.md
```

`PROJECT_STATUS.md` records implementation status rather than duplicating the
entire architecture specification.

The key v0.2 invariants are:

1. Logical topology is separate from discovered host state.
2. Host discovery occurs before host-dependent resolution.
3. Missing configured host interfaces are never silently substituted.
4. Each attachment represents one logical Layer-2 segment.
5. Each logical Layer-2 attachment uses a dedicated bridge.
6. Separate point-to-point VLANs must not be merged through a shared bridge.
7. Router-interface addressing and host-SVI addressing are independent.
8. Each independently supports `none`, `static`, or `dhcp`.
9. VLAN `parent_role` resolves to an actually detected host device.
10. Configuration-source precedence is deterministic.
11. Resolved values retain provenance.
12. Read-only planning is separate from apply.
13. Identical normalized inputs must produce deterministic plans.
14. Reconciliation must preserve unchanged resources.
15. RouterGen must distinguish owned from externally managed resources.
16. Network-underlay validation must pass before FRR lifecycle operations.
17. Each logical router must use an independent FRR pathspace.

Any change to these invariants requires an explicit architecture decision.

---

# 8. Configuration Precedence

The frozen v0.2 precedence is:

```text
CLI override
    >
interactive answer
    >
saved host/router profile
    >
topology JSON default
    >
RouterGen default
```

The future resolver must retain the provenance of each resolved value.

---

# 9. Validation Model

RouterGen separates validation into three layers.

## 9.1 Schema Validation

JSON Schema handles structural constraints such as:

- required objects and fields;
- types;
- enumerations;
- permitted addressing modes;
- permitted transport types;
- identifier formatting; and
- value ranges expressible in JSON Schema.

## 9.2 Semantic Validation

Semantic validation handles relationships and constraints such as:

- router identity uniqueness;
- namespace uniqueness;
- FRR pathspace uniqueness;
- valid object references;
- interface uniqueness;
- bridge ownership;
- VLAN consistency;
- addressing conflicts;
- transport-specific rules;
- host-role resolution;
- generated-name collisions; and
- prevention of unintended Layer-2 merging.

## 9.3 Operational Validation

Operational validation belongs primarily to later lifecycle stages and will
cover real system state such as:

- namespace existence;
- interface creation;
- link state;
- bridge membership;
- VLAN state;
- addressing;
- routes;
- policy rules;
- connectivity; and
- FRR/routing-protocol state.

---

# 10. v0.2-A Hard Gate

RouterGen must not begin the v0.2-B apply lifecycle until this pipeline is
proven:

```text
Logical topology
       +
Actual host discovery
       +
Optional saved profile
       +
CLI overrides / user selections
       |
       v
Fully resolved router
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
ZERO NETWORK CHANGES
```

The hard gate requires:

- [ ] topology structurally valid;
- [ ] topology semantically valid;
- [ ] required host devices actually detected;
- [ ] every required host role resolved;
- [ ] every selected router interface fully resolved;
- [ ] every attachment mapped to the correct dedicated Layer-2 bridge;
- [ ] every non-staged transport fully resolved;
- [ ] addressing intent unambiguous;
- [ ] provenance of resolved values retained;
- [ ] identical normalized inputs produce the same plan;
- [ ] plan ordering deterministic;
- [ ] no network or routing state changed; and
- [ ] consolidated verification evidence produced.

Passing this gate allows work on v0.2-B to begin. It does not make RouterGen
production ready.

---

# 11. Remaining v0.2-A Work

## A2: Topology/schema + semantic validation

Planned deliverables:

- v0.2 topology model;
- JSON Schema;
- topology loader;
- normalized internal representation;
- schema-validation reporting;
- semantic-validation framework; and
- initial semantic rule set.

## A3: Structured Host Discovery

Planned discovery sources include:

```bash
ip -j link show
ip -j addr show
ip -j route show
ip -j rule show
bridge -j link show
bridge -j vlan show
```

Discovery remains read-only.

## A4: Resolution

Planned deliverables:

- saved host profile loading;
- saved router profile loading;
- interactive selection;
- non-interactive operation;
- CLI overrides;
- precedence processing;
- role-to-device mapping;
- value provenance;
- unresolved-value reporting; and
- fully resolved router representation.

## A5: Deterministic Planning

The planning layer will describe proposed changes without executing them.

Example plan records may eventually include:

```text
CREATE namespace r1
CREATE bridge br-r1-mgmt
CREATE veth pair
MOVE router peer into namespace r1
ATTACH host peer to bridge br-r1-mgmt
CREATE VLAN transport
ASSIGN router address
LEAVE bridge SVI unnumbered
```

During v0.2-A, these remain data describing intended operations. They are not
authorization to execute Linux networking commands.

---

# 12. Out of Scope for v0.2-A

The following remain explicitly outside the current phase:

- network apply;
- namespace creation/deletion;
- bridge creation/deletion;
- veth creation;
- VLAN creation;
- address modification;
- route modification;
- policy-rule modification;
- forwarding changes;
- firewall/nftables changes;
- persistence configuration;
- FRR configuration generation;
- FRR startup/shutdown;
- OSPF configuration;
- BGP configuration;
- destructive reconciliation;
- rollback execution;
- multi-host orchestration;
- remote deployment; and
- production appliance packaging.

Architecture documentation may discuss these capabilities, but they must not
be presented as currently implemented.

---

# 13. Known Limitations

1. RouterGen remains pre-alpha.
2. Only A1 of v0.2-A has been implemented.
3. A1 has not yet been merged into `main`.
4. The current automated GitHub RouterGen suite contains seven tests.
5. A2 topology/schema implementation has not started.
6. Structured A3 host discovery has not been implemented.
7. A4 resolution has not been implemented.
8. A5 deterministic planning has not been implemented.
9. Network apply is intentionally unavailable.
10. DHCP behavior has not been implemented or operationally validated.
11. Host-routed transport has not been operationally implemented.
12. External-bridge lifecycle/ownership handling has not been implemented.
13. FRR intent is part of the architecture, but FRR lifecycle management is
    not implemented.
14. Multi-host deployment/orchestration has not been implemented.
15. Rollback/recovery behavior has not been implemented.
16. Persistence across restart has not been implemented.
17. Production security and privilege-separation review has not been
    completed.

Host-interface observations from a particular machine must be treated as
discovered host state rather than permanent RouterGen project limitations.

---

# 14. Safety Rules

1. Never silently replace a missing configured interface.
2. Never treat an example topology as approved for the current host.
3. Never execute apply behavior from a read-only command.
4. Never merge independent Layer-2 segments merely because they share a
   transport device.
5. Never infer host-SVI addressing from router-interface addressing.
6. Never infer router-interface addressing from host-SVI addressing.
7. Never begin FRR lifecycle operations before successful underlay
   validation.
8. Never reuse an FRR pathspace between different logical routers.
9. Never delete resources that RouterGen does not own.
10. Never describe a design-defined capability as implemented.
11. Never describe an implemented capability as lab-verified without
    evidence.
12. Never weaken tests merely to make new implementation work.
13. Never execute a plan merely because planning succeeded.
14. Never substitute a detected interface for a missing configured device
    unless explicit resolution selects it.
15. Never perform network mutation during v0.2-A.

---

# 15. Stability Definitions

## Design Defined

The architecture and intended behavior are documented.

## Implemented

The capability exists in code.

## Deterministically Tested

Automated tests demonstrate repeatable behavior without live network changes.

## Lab Verified

The capability has been exercised in the intended controlled environment and
has recorded passing evidence.

## Stable

A capability should only be called stable when it additionally has:

- documented behavior;
- documented failure behavior;
- regression coverage;
- appropriate integration or lab verification;
- lifecycle consideration; and
- no known critical safety defect.

## Production Ready

Production readiness additionally requires areas such as:

- security review;
- privilege and ownership controls;
- recovery behavior;
- rollback;
- supported installation/upgrade procedures;
- operational documentation;
- monitoring guidance; and
- an explicit support policy.

No RouterGen capability is currently production ready.

---

# 16. Evidence Policy

Milestone verification should produce enough evidence to establish:

- RouterGen version;
- Git commit;
- topology/schema version where applicable;
- test environment;
- Python version;
- test result;
- safety result;
- failure stage where applicable;
- whether mutation was permitted; and
- whether mutation occurred.

Preferred final markers for consolidated milestone results are:

```text
FINAL_RESULT=PASS
FAILURE_STAGE=NONE
NETWORK_CHANGES_PERMITTED=NO
NETWORK_CHANGES_DETECTED=NO
```

A future verification wrapper should consolidate milestone evidence into one
result file where practical.

---

# 17. Branch and Change Discipline

Current development model:

```text
main
  |
  +-- feature/v0.2-a1-bootstrap
  +-- feature/v0.2-a2-schema
  +-- feature/v0.2-a3-discovery
  +-- feature/v0.2-a4-resolution
  +-- feature/v0.2-a5-planning
```

Recommended commit prefixes include:

```text
feat:
fix:
test:
docs:
build:
refactor:
```

Before merging a milestone into `main`:

- [ ] current tests pass;
- [ ] milestone-specific tests pass;
- [ ] applicable safety gates pass;
- [ ] lab verification is completed where required;
- [ ] documentation describes actual behavior;
- [ ] planned capabilities are not presented as implemented;
- [ ] `PROJECT_STATUS.md` is updated; and
- [ ] the Pull Request is reviewed.

---

# 18. Decision Summary

| Decision | Status | Rationale |
|---|---|---|
| Declarative topology JSON | Accepted | Separates portable intent from host implementation |
| Discover host before resolution | Accepted | Prevents hard-coded interface assumptions |
| Dedicated bridge per logical L2 segment | Accepted | Preserves Layer-2 isolation |
| Router and host-SVI addressing remain independent | Accepted | Supports multiple numbered and unnumbered designs |
| Explicit configuration precedence | Accepted | Makes resolution predictable |
| Missing configured devices are rejected | Accepted | Prevents unsafe silent substitution |
| Plan before apply | Accepted | Creates a safety/review boundary |
| Reconcile only relevant changed resources | Accepted | Avoids unnecessary disruption |
| FRR lifecycle follows underlay validation | Accepted | Prevents routing daemons starting on invalid networking |
| One FRR pathspace per router | Accepted | Isolates multiple logical routers |
| Semantic validation outside JSON Schema | Accepted | Supports cross-object and host-dependent rules |

Detailed architecture decisions belong in `docs/architecture/` and may later
be promoted to individual ADR files.

---

# 19. Next Action

The immediate next action is **not A2 yet**.

A1 must first be integrated into the authoritative branch.

Next steps:

1. Commit this A1 verification/status update to
   `feature/v0.2-a1-bootstrap`.
2. Rerun the seven automated tests.
3. Push the feature branch.
4. Create the project's first GitHub Pull Request:
   `feature/v0.2-a1-bootstrap` -> `main`.
5. Review the Pull Request.
6. Merge A1 into `main`.
7. Synchronize the Codespace checkout with merged `main`.
8. Synchronize the WSL2 test-laptop checkout with merged `main`.
9. Verify both environments reference the authoritative merged A1 commit.
10. Mark v0.2-A1 **COMPLETE**.
11. Begin v0.2-A2.

---

# 20. Completion Record

## Historical `wsl2-router-netgen` baseline

```text
Status: VERIFIED HISTORICAL PROTOTYPE
Tests: 12 PASS / 0 FAIL
Scope: Earlier validation/read-only planning prototype
Relationship to current suite: Historical evidence, not current GitHub tests
```

## v0.2-A1

```text
Status: WSL2-LAB VERIFIED / PENDING MERGE

Feature branch:
feature/v0.2-a1-bootstrap

Implementation commits:
a9a3204
f5972dc

Codespace:
Python: 3.14.2
Tests: 7 PASS / 0 FAIL
Diagnostic: PASS
WSL: no

WSL2 test laptop:
Checkout: /mnt/c/Project/routergen
Python: 3.12.3
Tests: 7 PASS / 0 FAIL
Diagnostic: PASS
WSL: yes

NETWORK_CHANGES_PERMITTED=NO
```

## v0.2-A2

```text
Status: NOT STARTED
Network changes permitted: No
```

## v0.2-A3

```text
Status: PLANNED
Network changes permitted: No
```

## v0.2-A4

```text
Status: PLANNED
Network changes permitted: No
```

## v0.2-A5

```text
Status: PLANNED
Network changes permitted: No
```

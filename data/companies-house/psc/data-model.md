# Corporate PSC ownership data model

## Purpose

This model represents corporate-only Companies House PSC notifications and uses
RDFox rules to derive current direct and transitive corporate-group membership.
The initial root is Carillion plc, company number `03782379`.

The model excludes individual PSCs, directors, dates of birth, addresses, and
other personal data.

## Namespaces

| Prefix | Namespace | Purpose |
|---|---|---|
| `psc:` | `https://w3id.org/rdfox-project-x-demo/ontology/psc#` | Classes and properties |
| `company:` | `https://w3id.org/rdfox-project-x-demo/resource/company/` | Company resources |
| `notification:` | `https://w3id.org/rdfox-project-x-demo/resource/psc-notification/` | PSC notification resources |
| `group:` | `https://w3id.org/rdfox-project-x-demo/resource/group/` | Configured corporate groups |
| `noc:` | `https://w3id.org/rdfox-project-x-demo/vocab/nature-of-control/` | SKOS concepts |

The `w3id.org` base separates persistent public identifiers from physical
hosting. These IRIs are valid identifiers immediately, but they will not
dereference until redirects are registered with the w3id.org project.

## Core pattern

```text
CorporateEntityPSCNotification
├── controllerCompany ──→ Company
├── controlledCompany ──→ Company
├── hasNatureOfControl ─→ skos:Concept
├── notifiedOn ─────────→ xsd:date
├── ceasedOn ───────────→ xsd:date, optional
├── ceased ─────────────→ xsd:boolean
└── prov:wasDerivedFrom → Companies House notification IRI
```

`controllerCompany` and `controlledCompany` are roles in a notification. Both
resources are instances of `psc:Company`; separate controller and controlled
company classes are not used because an intermediate company can occupy both
roles.

## Decisions

### One resource per PSC notification

The CSV repeats a notification once for each nature-of-control code. Conversion
groups rows by `source_url`, producing one notification resource with multiple
`psc:hasNatureOfControl` values.

### Company identity

Companies are identified by normalized company number:

```text
https://w3id.org/rdfox-project-x-demo/resource/company/03782379
```

Company numbers remain strings because leading zeroes and alphabetic prefixes
are significant.

### Source-reported attributes

The CSV's controller name, legal form, legal authority, country, and place of
registration originate in a PSC notification. They are represented on the
notification using `reportedController...` properties.

They are not asserted as canonical company attributes because the snapshot
contains historical variants, inconsistent capitalization, and source errors.
Canonical company name, type, status, and incorporation data can later be
loaded from the Companies House company-profile API.

### Provenance

The Companies House notification URL is an IRI linked with
`prov:wasDerivedFrom`, not an `xsd:anyURI` literal. The source ETag is retained
as `psc:sourceETag`.

### Nature of control

Nature-of-control source codes are SKOS concepts rather than strings. The exact
Companies House code is retained as `skos:notation`, and broader concepts group
share ownership, voting rights, appointment rights, surplus-asset rights, and
significant influence or control.

The vocabulary contains the 15 codes observed in
`carillion-psc-ownership.csv`; it is not claimed to be the complete Companies
House enumeration.

### Current versus historical control

All 263 notifications remain explicit historical source facts. RDFox derives
current direct control only from notifications where `psc:ceased false`.

`psc:ceasedOn` is optional. Retaining both the Boolean and date supports quality
checks for incomplete or contradictory source data.

### Group membership

A group links to a root company using `psc:hasGroupRoot`. RDFox rules infer:

- `psc:directlyControls`;
- `psc:directlyControlledBy`;
- transitive `psc:controls`;
- `psc:ultimatelyControlledBy`, relating each descendant to the configured
  group root; and
- `psc:memberOfGroup`.

The direct and recursive rules avoid deriving self-control. Cycles should still
be investigated as possible source-data or modeling issues.

### PSC control is not identical to ownership

The generic relation is named `controls`, not `owns`. A PSC can arise from share
ownership, voting rights, appointment rights, surplus-asset rights, or
significant influence. Share-ownership queries must restrict
`psc:hasNatureOfControl` to the relevant SKOS concepts.

## Source-to-RDF mapping

| CSV column | RDF representation |
|---|---|
| `controlled_company_number` | Controlled `psc:Company` IRI and `psc:companyNumber` |
| `controller_company_number` | Controller `psc:Company` IRI and `psc:companyNumber` |
| `controller_name` | `psc:reportedControllerName` on notification |
| `notified_on` | `psc:notifiedOn` as `xsd:date` |
| `ceased_on` | Optional `psc:ceasedOn` as `xsd:date` |
| `ceased` | `psc:ceased` as `xsd:boolean` |
| `nature_of_control` | `psc:hasNatureOfControl` to a `noc:` concept |
| `legal_form` | `psc:reportedControllerLegalForm` |
| `legal_authority` | `psc:reportedControllerLegalAuthority` |
| `country_registered` | `psc:reportedControllerCountryRegistered` |
| `place_registered` | `psc:reportedControllerPlaceRegistered` |
| `source_url` | `prov:wasDerivedFrom` |
| `etag` | `psc:sourceETag` |
| `depth_from_root` | Not imported; it is extraction metadata |

## Files

| File | Role |
|---|---|
| `carillion-psc-ownership.csv` | Corporate-only source extract |
| `carillion-psc-ownership.ttl` | Generated notification and company facts |
| `psc-ontology.ttl` | OWL vocabulary |
| `nature-of-control-vocab.ttl` | SKOS concept scheme |
| `carillion-group-root.ttl` | Carillion group configuration |
| `corporate-group-rules.dlog` | RDFox inference rules |
| `carillion-group.rq` | Group inspection query |

## RDFox loading

From the project directory, run this in the RDFox shell:

```text
exec "load-carillion-group.rdfox"
```

The expected current inference is 142 group companies including Carillion plc,
based on 213 active direct-control notifications in this extract.

## Known limitations

- PSC data represents registrable control, not a complete legal group register.
- The graph is a descendant traversal from one configured root.
- Canonical controlled-company names and statuses are not yet loaded.
- Current control uses the snapshot's `ceased` flag, not an arbitrary historical
  assessment date.
- The `w3id.org` namespace requires redirect registration before it becomes
  dereferenceable.

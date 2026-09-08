# Gazette insolvency data

## Files

| File | Purpose |
|---|---|
| `insolvency.owl` | Gazette insolvency ontology downloaded from `https://www.thegazette.co.uk/def/insolvency.owl` |
| `gazette-link-ontology.ttl` | Local vocabulary for linking companies to Gazette resources and notices |
| `company-notice-rules.dlog` | RDFox rules deriving company links and notice relationships |
| `company-notices.rq` | Query for inspecting the derived company-to-notice relationships |
| `../suppliers/gazette-carillion-group-insolvency.ttl` | Downloaded Gazette result graph |

## Rule behavior

The first rule reads the local PSC company number:

```text
local company
  psc:companyNumber
    "08747138"
```

It constructs the corresponding Gazette company IRI and requires that resource
to occur as the company in an imported insolvency notice. It then derives:

```turtle
<https://w3id.org/rdfox-project-x-demo/resource/company/08747138>
    gazlink:gazetteCompanyResource
        <http://business.data.gov.uk/id/company/08747138> .
```

Constructing the IRI preserves leading zeroes and avoids depending on
inconsistent `gazorg:companyNumber` literals found in some Gazette notices.

The second rule follows the Gazette notice structure:

```text
notice
  gaz:isAbout
    notifiable thing
      insolvency:hasCompany
        Gazette company resource
```

It then derives:

```turtle
<https://w3id.org/rdfox-project-x-demo/resource/company/08747138>
    gazlink:hasInsolvencyNotice
        <https://www.thegazette.co.uk/id/notice/4237126> .
```

The notice IRI is retained as the object, so its Gazette notice ID remains
explicit and dereferenceable.

## RDFox import order

Import these files into the same datastore:

1. `data/companies-house/psc/psc-ontology.ttl`
2. `data/companies-house/psc/carillion-psc-ownership.ttl`
3. `data/gazette/insolvency.owl`
4. `data/gazette/gazette-link-ontology.ttl`
5. `data/suppliers/gazette-carillion-group-insolvency.ttl`
6. `data/gazette/company-notice-rules.dlog`

Import the Datalog rules last so RDFox materializes the company and notice
links from the loaded facts.

Run `company-notices.rq` to list the resulting relationships.

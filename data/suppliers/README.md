# Synthetic supplier dataset

## Purpose

This dataset models a fictional company's supplier list for demonstrating how
supplier data can be joined to the Companies House corporate PSC graph in
RDFox.

The customer and all supplier relationships are synthetic. The four supplier
companies and their Companies House numbers are real.

## Companies

The fictional customer is:

| Company name | Company number |
|---|---|
| Northbridge Infrastructure Services Limited | `SYN90001` |

`SYN90001` is an intentionally synthetic identifier and is not a Companies
House company number.

The supplier list is:

| Supplier company name | Company number | Carillion-linked in the PSC graph |
|---|---|---|
| Carillion Construction Limited | `00594581` | Yes |
| Carillion JM Limited | `00077628` | Yes |
| Balfour Beatty plc | `00395826` | No |
| Travis Perkins plc | `00824821` | No |

Carillion Construction Limited and Carillion JM Limited use exactly the same
company IRIs as the corporate PSC graph. This allows supplier relationships to
join directly to Carillion group membership inferred by the RDFox Datalog
rules.

The synthetic dataset does not assert that Balfour Beatty plc or Travis Perkins
plc belong to the Carillion group. They provide control records for comparison
when testing group-risk queries.

## Files

| File | Purpose |
|---|---|
| `fictional-company-suppliers.csv` | Synthetic source supplier list |
| `fictional-company-suppliers.ttl` | RDF transformation of the CSV |
| `supplier-ontology.ttl` | Classes and properties used by the supplier graph |
| `gazette-supplier-insolvency.rq` | Gazette query for supplier companies only |
| `gazette-supplier-and-parent-insolvency.rq` | Gazette query for suppliers and their PSC-recorded parents |
| `gazette-carillion-group-insolvency.rq` | Gazette query for all 142 current Carillion group companies |
| `gazette-carillion-group-insolvency.ttl` | Gazette result subgraph downloaded on 2026-09-07 |
| `../../convert-supplier-csv-to-ttl.py` | Reproducible CSV-to-Turtle converter |

## CSV fields

| Column | Meaning |
|---|---|
| `relationship_id` | Stable identifier for the synthetic supplier relationship |
| `customer_company_name` | Customer name recorded by the supplier system |
| `customer_company_number` | Customer identifier; synthetic in this dataset |
| `supplier_company_name` | Supplier company name |
| `supplier_company_number` | Real Companies House company number |
| `supplier_reference_type` | Identifies the supplier number as a Companies House number |
| `supply_category` | Type of goods or services supplied |
| `relationship_status` | Current or historical relationship status |
| `valid_from` | Start date of the supplier relationship |
| `valid_to` | Optional end date |
| `synthetic` | Confirms that the relationship record is synthetic |

Company numbers are strings. Leading zeroes must be retained.

## Namespaces

| Prefix | Namespace |
|---|---|
| `psc:` | `https://w3id.org/rdfox-project-x-demo/ontology/psc#` |
| `supply:` | `https://w3id.org/rdfox-project-x-demo/ontology/supply#` |
| Company resources | `https://w3id.org/rdfox-project-x-demo/resource/company/` |
| Supplier relationships | `https://w3id.org/rdfox-project-x-demo/resource/supplier-relationship/` |

For example, Carillion Construction Limited is represented by:

```text
https://w3id.org/rdfox-project-x-demo/resource/company/00594581
```

This is the same resource used when the company appears as a controller or
controlled company in a PSC notification.

## Regenerating the Turtle

From the project directory:

```bash
python3 convert-supplier-csv-to-ttl.py \
  data/suppliers/fictional-company-suppliers.csv \
  data/suppliers/fictional-company-suppliers.ttl
```

## Loading into RDFox

Import the following into the same datastore as the Carillion PSC graph:

1. `data/suppliers/supplier-ontology.ttl`
2. `data/suppliers/fictional-company-suppliers.ttl`

The PSC ontology, PSC ownership data, Carillion group root, and corporate-group
Datalog rules must also be present for inferred group membership.

## Finding suppliers linked to the Carillion group

```sparql
PREFIX company:
  <https://w3id.org/rdfox-project-x-demo/resource/company/>
PREFIX group:
  <https://w3id.org/rdfox-project-x-demo/resource/group/>
PREFIX psc:
  <https://w3id.org/rdfox-project-x-demo/ontology/psc#>
PREFIX supply:
  <https://w3id.org/rdfox-project-x-demo/ontology/supply#>

SELECT DISTINCT
  ?customerName
  ?supplierName
  ?supplierNumber
WHERE {
  ?relationship
    a supply:SupplierRelationship ;
    supply:customer ?customer ;
    supply:supplier ?supplier .

  ?customer supply:companyName ?customerName .

  ?supplier
    supply:companyName ?supplierName ;
    psc:companyNumber ?supplierNumber ;
    psc:memberOfGroup group:carillion .
}
ORDER BY ?supplierNumber
```

With the current PSC data and rules, the expected matches are Carillion JM
Limited (`00077628`) and Carillion Construction Limited (`00594581`).

## Querying The Gazette directly

Run either Gazette query directly against:

```text
https://www.thegazette.co.uk/sparql
```

`gazette-supplier-insolvency.rq` passes only the four supplier company numbers
to The Gazette. `gazette-supplier-and-parent-insolvency.rq` uses one flat list
containing those supplier numbers plus the distinct parent company numbers
recorded by the Companies House PSC data.

Both queries follow the Gazette graph path:

```text
gaz:Notice
  └── gaz:isAbout
        └── insolvency:hasCompany
              └── gazorg:companyNumber
```

The supplier-only query currently returns:

| Supplier | Company number | Gazette notice | Notice type |
|---|---|---|---|
| Carillion JM Limited | `00077628` | `https://www.thegazette.co.uk/id/notice/2974387` | Winding-up order |
| Carillion Construction Limited | `00594581` | `https://www.thegazette.co.uk/id/notice/2948342` | Winding-up order |

Both are notice code `2452`. Balfour Beatty plc and Travis Perkins plc do not
produce matches for this query at the time of testing.

`gazette-carillion-group-insolvency.rq` extends the same approach to the 142
companies in the current Carillion group inferred from active corporate PSC
notifications. Its static `VALUES` list includes the root company and all
current descendants identified from the 2026-09-07 PSC snapshot. It constructs
The Gazette's company IRI from each number so the endpoint can use direct graph
lookups instead of scanning and filtering every insolvency notice. A second
`VALUES` block restricts results to the corporate insolvency notice codes
defined at <https://www.thegazette.co.uk/noticecodes>: general corporate
insolvency, administration, receivership, voluntary winding-up, and court
winding-up notices. Personal insolvency codes are excluded.

The downloaded Turtle contains the minimal importable Gazette subgraph needed
to preserve the query results:

- 1,209 triples;
- 159 unique Gazette notices;
- 174 notice-to-company relationships;
- 99 distinct company-number values; and
- 15 notice codes represented in the results.

The result graph has fewer unique notices than the SPARQL `SELECT` has rows
because a notice can produce multiple combinations of notice type, company, or
other matching bindings. RDF serialization stores each resulting triple only
once.

`gazorg:companyNumber` is compared through `STR()` because The Gazette returns
company numbers as `xsd:string`, while plain literals in the `VALUES` block may
otherwise be treated as different RDF terms.

## Data interpretation

- The supplier list is fictional and must not be treated as evidence of actual
  commercial relationships.
- The two Carillion links are derived by joining real company identifiers to
  the corporate PSC graph.
- PSC control can arise through shares, voting rights, appointment rights, or
  significant influence; it should not automatically be described as share
  ownership.
- The current group rules derive control only from PSC notifications whose
  `psc:ceased` value is `false`.

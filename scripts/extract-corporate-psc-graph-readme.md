
Script features:

- start from Carillion plc, company `03782379`;
- scan the 12 GB PSC snapshot using constant memory;
- retain only `corporate-entity-person-with-significant-control`;
- exclude people, directors, addresses, statements and exemptions;
- build a reusable SQLite reverse-ownership index;
- recursively discover companies controlled by Carillion entities;
- write a normalized CSV for later knowledge-graph conversion.


The SQLite database indexes **all corporate PSC relationships in the snapshot**, not only Carillion. Carillion is merely the root supplied for that particular extraction.


Run the script again with the same database and a different root:


Bash






```
python3 extract-corporate-psc-graph.py \
  data/companies-house/psc/bulk-download/persons-with-significant-control-snapshot-2026-09-07.txt \
  --root 12345678 \
  --database data/companies-house/psc/bulk-download/corporate-psc-index.sqlite \
  --output data/companies-house/psc/company-12345678-ownership.csv

```







The script should report:


Plain text






```
Reusing index .../corporate-psc-index.sqlite

```







It will then finish in seconds because it does not rescan the 12 GB snapshot.


You can also extract several root groups into one CSV:


Bash






```
python3 extract-corporate-psc-graph.py \
  data/companies-house/psc/bulk-download/persons-with-significant-control-snapshot-2026-09-07.txt \
  --root 03782379 \
  --root 12345678 \
  --root 87654321 \
  --database data/companies-house/psc/bulk-download/corporate-psc-index.sqlite \
  --output data/companies-house/psc/selected-corporate-groups.csv

```







The reusable database contains:



- `relationships` — one row per corporate PSC notification;

- `control_natures` — one or more control types for each relationship;

- indexes on both controller and controlled company numbers;

- source URLs, notification dates, cessation dates and ETags.


### Traversal limitation

The current script traverses **downward**:


```
root controller
→ directly controlled companies
→ companies controlled by those companies
→ further descendants

```

Therefore, supply the highest known parent as `--root`.

If you start with a subsidiary, the current extraction will find its own subsidiaries but will not automatically walk upward to its parent and then sideways to sibling companies. The SQLite index contains the data needed for upward and bidirectional traversal, but the current CSV extraction intentionally follows descendants only.

The database is snapshot-specific. When you replace the source with a newer PSC snapshot, the script detects the changed file metadata and rebuilds the index. Keep the snapshot date in downstream graph provenance because the index represents Companies House data observed on that date.
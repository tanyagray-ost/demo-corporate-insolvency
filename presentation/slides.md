---
theme: default
layout: cover
class: rdfox-cover
title: "Corporate Insolvency: Hidden Signals of Exposure"
info: |
  A case study showing why a subcontractor's ordinary KYC can miss insolvency
  exposure elsewhere in a customer's corporate group, and how RDFox connects it.
drawings:
  persist: false
transition: slide-left
mdc: true
---

<img class="rdfox-logo" src="/rdfox-logo.svg" alt="RDFox by Oxford Semantic Technologies">

<div class="chapter-kicker">Know Your Customer (KYC) case study</div>

# Surfacing indirect financial risk

### The Carillion corporate insolvency

How RDFox, open public data, and datalog rules can reason across a knowledge graph to reveal indirect financial risk

<div class="cover-meta">Companies House + The Gazette + RDFox</div>


---
layout: full
class: group-overview
---

<div class="group-overview-copy">
  <span class="group-kicker">Carillion Group · at a glance</span>
  <h1>A strategic supplier woven into <span>UK public life</span></h1>
  <br/>
  <p class="group-intro">Created from Tarmac's construction and professional-services businesses, Carillion grew into a multinational construction and facilities-management group.</p>

  <div class="group-metrics">
    <div><span>Established</span><strong>1999</strong><p>Demerger from Tarmac</p></div>
    <div><span>Workforce</span><strong>c.43k</strong><p>globally · c.19k in the UK</p></div>
    <div><span>Public footprint</span><strong>420–450</strong><p>UK public-sector / government contracts</p></div>
    <div><span>Liquidation estate</span><strong>84</strong><p>UK group companies now in liquidation</p></div>
  </div>

  <div class="group-sectors">
    <span>Construction</span>
    <span>Civil engineering</span>
    <span>Facilities management</span>
    <span>Road & rail</span>
  </div>

  <div class="group-collapse">
    <div class="collapse-date"><small>Compulsory liquidation</small><strong>15 JAN 2018</strong></div>
    <div>
      <p>Winding-up orders placed Carillion plc and associated companies under the Official Receiver.</p>
      <strong>Its collapse became the UK's largest-ever trading liquidation.</strong>
    </div>
  </div>

  <div class="group-impact">
    <span>Why it mattered</span>
    <p>Hospitals, schools, prisons, defence accommodation and transport depended on its services. The failure affected public-service continuity, 30,000 suppliers and subcontractors, and 27,000 pension-scheme members.</p>
  </div>
</div>

<div class="group-image-grid">
  <figure class="group-image gchq">
    <img src="/images/gchq-aerial.jpg" alt="Aerial view of GCHQ in Cheltenham">
    <figcaption><span>Public infrastructure</span><strong>GCHQ · Cheltenham</strong></figcaption>
  </figure>
  <figure class="group-image rail">
    <img src="/images/carillion-rail.jpg" alt="Carillion rail maintenance train at Banbury station">
    <figcaption><span>Transport</span><strong>Rail maintenance</strong></figcaption>
  </figure>
  <figure class="group-image identity">
    <img src="/images/carillion-van.jpg" alt="A Carillion-branded service van">
    <figcaption><span>National footprint</span><strong>Field services</strong></figcaption>
  </figure>
</div>

<div class="source-note">Sources: UK Parliament [5], NAO [6], Insolvency Service [4] · Images: Wikimedia Commons [7]</div>

---
layout: full
class: timeline-summary
---

<div class="timeline-heading">
  <div>
    <span class="timeline-kicker">Corporate case history</span>
    <h1>Carillion PLC <span>timeline</span></h1>
  </div>
  <div class="timeline-entity-chip">
    <svg viewBox="0 0 32 32" aria-hidden="true">
      <path d="M7 27V9l9-4 9 4v18M12 12h2m4 0h2m-8 5h2m4 0h2m-8 5h2m4 0h2M4 27h24"/>
    </svg>
    <span><small>Corporate entity</small>CARILLION PLC</span>
  </div>
</div>

<div class="timeline-layout">
  <aside class="timeline-profile">
    <div class="timeline-corporate-mark">
      <svg viewBox="0 0 180 150" aria-hidden="true">
        <path class="mark-links" d="M21 34 57 57m102-31-36 31M27 123l35-24m92 30-35-30"/>
        <circle class="mark-node" cx="18" cy="31" r="6"/>
        <circle class="mark-node" cx="162" cy="23" r="6"/>
        <circle class="mark-node" cx="23" cy="126" r="6"/>
        <circle class="mark-node" cx="157" cy="132" r="6"/>
        <path class="mark-building" d="M55 126V53l35-17 35 17v73M45 126h90M69 65h13m16 0h13M69 82h13m16 0h13M69 99h13m16 0h13M82 126v-12h16v12"/>
      </svg>
    </div>
    <span class="timeline-profile-label">Corporate lifecycle</span>
    <strong>Creation → growth → distress → liquidation</strong>
    <p>Public signals converge into a single, connected sequence.</p>
    <div class="timeline-range">
      <span>1999</span>
      <i></i>
      <span>2018</span>
    </div>
  </aside>

  <div class="timeline-sequence">
    <div class="timeline-axis" aria-hidden="true">
      <span class="axis-start">Start</span>
      <div class="axis-track">
        <i><b>1999</b></i>
        <i><b>2002–11</b></i>
        <i><b>2015</b></i>
        <i><b>Jul ’17</b></i>
        <i><b>Nov ’17</b></i>
        <i><b>Jan ’18</b></i>
        <i><b>Aug ’18</b></i>
      </div>
      <span class="axis-end">End</span>
    </div>
    <div class="timeline-overview">
      <div class="timeline-event" data-step="01">
        <span class="timeline-year">1999</span>
        <strong>Created</strong>
        <p>Construction and professional-services operations demerged from Tarmac.</p>
      </div>
      <div class="timeline-event" data-step="02">
        <span class="timeline-year">2002–11</span>
        <strong>Expanded</strong>
        <p>Acquisitions broadened construction, support and energy services.</p>
      </div>
      <div class="timeline-event warning" data-step="03">
        <span class="timeline-year">2015</span>
        <strong>Signals emerged</strong>
        <p>Debt, supplier-payment terms and financing practices drew scrutiny.</p>
      </div>
      <div class="timeline-event danger" data-step="04">
        <span class="timeline-year">Jul 2017</span>
        <strong>£845m impairment</strong>
        <p>Loss-making contracts forced a major construction-services write-down.</p>
      </div>
      <div class="timeline-event danger" data-step="05">
        <span class="timeline-year">Sep–Nov 2017</span>
        <strong>Crisis accelerated</strong>
        <p>Losses reached £1.15bn; covenant breach and debt of up to £925m forecast.</p>
      </div>
      <div class="timeline-event terminal" data-step="06">
        <span class="timeline-year">15 Jan 2018</span>
        <strong>Liquidated</strong>
        <p>The High Court made a winding-up order. The Official Receiver took control.</p>
      </div>
      <div class="timeline-event final" data-step="07">
        <span class="timeline-year">6 Aug 2018</span>
        <strong>Trading ended</strong>
        <p>The last of 278 contracts had arrangements for transfer.</p>
      </div>
    </div>
  </div>
</div>

<div class="source-note">Summary: Wikipedia synthesis [1], The Gazette [3], Insolvency Service [4]</div>

---

# Timeline 1 · Signals accumulate before insolvency

<div class="crisis-cards four">
  <div class="crisis-card">
    <span class="crisis-date">March 2015</span>
    <h3>Debt concerns</h3>
    <p>External scrutiny focused on leverage, extended supplier-payment terms and financing practices.</p>
  </div>
  <div class="crisis-card">
    <span class="crisis-date">10 July 2017</span>
    <strong>£845m</strong>
    <h3>Impairment charge</h3>
    <p>Loss-making construction projects drove a major write-down.</p>
  </div>
  <div class="crisis-card">
    <span class="crisis-date">29 September 2017</span>
    <strong>£1.15bn</strong>
    <h3>Six-month loss</h3>
    <p>A further support-services write-down deepened the reported loss.</p>
  </div>
  <div class="crisis-card terminal">
    <span class="crisis-date">17 November 2017</span>
    <strong>£925m</strong>
    <h3>Forecast debt</h3>
    <p>A covenant breach was expected and survival depended on recapitalisation.</p>
  </div>
</div>

<div class="investigation-callout">
  <strong>KYC relevance</strong>
  <span>No single event proves future insolvency. Together they show why a later formal group event should trigger an immediate customer-credit review for a subcontractor.</span>
</div>

<div class="source-note">Source: financial-difficulties chronology summarised from Wikipedia [1]</div>

---

# Timeline 2 · The formal group signal arrives

<div class="countdown five">
  <div>
    <span>3 Jan 2018</span>
    <strong>Regulatory investigation reported</strong>
    <p>Public scrutiny focused on earlier financial announcements.</p>
  </div>
  <div>
    <span>13 Jan</span>
    <strong>Collapse described as days away</strong>
    <p>Emergency discussions covered debt, pensions and public contracts.</p>
  </div>
  <div>
    <span>13–14 Jan</span>
    <strong>No rescue agreement</strong>
    <p>Weekend discussions ended without sufficient new funding.</p>
  </div>
  <div class="terminal">
    <span>15 Jan</span>
    <strong>Winding-up order</strong>
    <p>Compulsory liquidation began and the Official Receiver took control.</p>
  </div>
  <div>
    <span>6 Aug</span>
    <strong>Trading phase ended</strong>
    <p>Arrangements had been made to transfer the last of 278 contracts.</p>
  </div>
</div>

<div class="formal-event compact">
  <div><span>Company</span><strong>Carillion plc</strong></div>
  <div><span>Company number</span><strong>03782379</strong></div>
  <div><span>Gazette notice</span><strong>2948343</strong></div>
  <div><span>Notice code</span><strong>2452</strong></div>
</div>

<div class="source-note">Sources: The Gazette [3]; UK Government and Insolvency Service [4]</div>

---
layout: section
---

<div class="chapter-kicker">Subcontractor perspective · baseline run</div>

# Why ordinary customer KYC alerts too late

---

# A subcontractor's customer accounts

<div class="customer-account-list">
  <div class="customer-account-list-head">
    <span>Customer</span><span>Company number</span><span>Relationship</span>
  </div>
  <div>
    <strong>Carillion Construction Limited</strong><code>00594581</code><span>Customer</span>
  </div>
  <div>
    <strong>Carillion JM Limited</strong><code>00077628</code><span>Customer</span>
  </div>
  <div>
    <strong>Balfour Beatty plc</strong><code>00395826</code><span>Customer</span>
  </div>
  <div>
    <strong>Travis Perkins plc</strong><code>00824821</code><span>Customer</span>
  </div>
</div>

<div class="subcontractor-banner">
  <span>Our fictional subcontractor</span>
  <strong>Northbridge Infrastructure Services Limited</strong>
  <code>SYN90001</code>
</div>

<div class="source-note">Customer relationships are synthetic; counterparty company identities are real public records.</div>

---

# Entity-by-entity customer KYC misses the hidden signal

<div class="evidence-grid three">
  <div class="evidence-card">
    <span class="card-number">01</span>
    <h3>Does our customer exist?</h3>
    <p>Northbridge confirms its company number, name, status and registered particulars.</p>
  </div>
  <div class="evidence-card">
    <span class="card-number">02</span>
    <h3>Is our customer insolvent?</h3>
    <p>Northbridge searches for a direct insolvency status or notice against that legal entity.</p>
  </div>
  <div class="evidence-card">
    <span class="card-number">03</span>
    <h3>Should we extend credit?</h3>
    <p>Northbridge reviews filings, accounts and other standard onboarding evidence.</p>
  </div>
</div>

<div class="investigation-callout risk">
  <strong>The KYC blind spot</strong>
  <span>A direct Carillion customer can still look acceptable while a formal risk event is attached to its parent or another company in the same inferred group.</span>
</div>

---

# The signal is hidden in the corporate graph

<div class="group-event">
  <div class="group-root">
    <span>Ultimate parent</span>
    <strong>Carillion plc</strong>
    <code>03782379</code>
  </div>
  <div class="group-companies">
    <div><strong>Carillion Construction Ltd</strong><code>00594581</code></div>
    <div><strong>Carillion JM Ltd</strong><code>00077628</code></div>
    <div><strong>Carillion Services Ltd</strong><code>02684154</code></div>
    <div><strong>Planned Maintenance Engineering Ltd</strong><code>00737307</code></div>
    <div><strong>Carillion Integrated Services Ltd</strong><code>03679838</code></div>
    <div><strong>Carillion Services 2006 Ltd</strong><code>03011791</code></div>
  </div>
</div>

<div class="investigation-callout">
  <strong>What ordinary KYC cannot infer</strong>
  <span>Northbridge's customer is ultimately controlled by Carillion plc, so a Gazette event against the parent changes the subcontractor's credit exposure before its direct customer has a notice.</span>
</div>

---

# Waiting for a direct customer notice is operationally late

<div class="evidence-grid three">
  <div class="evidence-card">
    <span class="card-number">01</span>
    <h3>Control changes</h3>
    <p>The liquidator assumes control while directors' management powers normally cease.</p>
  </div>
  <div class="evidence-card">
    <span class="card-number">02</span>
    <h3>Contracts are assessed</h3>
    <p>Services may continue, transfer, terminate or be disclaimed if they are onerous.</p>
  </div>
  <div class="evidence-card">
    <span class="card-number">03</span>
    <h3>Northbridge becomes a creditor</h3>
    <p>As an unpaid subcontractor, it must establish claims against the assets available in liquidation.</p>
  </div>
</div>

<div class="metric-strip">
  <div><strong>30,000</strong><span>subcontractors and suppliers reportedly affected immediately</span></div>
  <div><strong>£6.9bn</strong><span>estimated liabilities across 27 liquidated UK companies in April 2018</span></div>
  <div><strong>91</strong><span>Carillion companies reported liquidated by the end of 2018</span></div>
</div>

<div class="source-note">Sources: Wikipedia impact and liquidation synthesis [1]; UK Government [4]</div>

---
layout: section
---

<div class="chapter-kicker">RDFox rerun</div>

# Datalog rules surface the hidden signal

---

# RDFox connects three partial views

<div class="evidence-chain three-source">
  <div>
    <span class="chain-step">1</span>
    <strong>Customer ledger</strong>
    <p>Which companies Northbridge supplies and invoices, identified by company number.</p>
  </div>
  <div>
    <span class="chain-step">2</span>
    <strong>Companies House PSC</strong>
    <p>Which corporate entities control other companies in the group.</p>
  </div>
  <div>
    <span class="chain-step">3</span>
    <strong>The Gazette</strong>
    <p>Which companies have dated, typed public insolvency notices.</p>
  </div>
</div>

<div class="join-key">
  <span>Shared key</span>
  <strong>Company number</strong>
  <code>00594581 → 03782379 → notice 2948343</code>
</div>

---

# Datalog materialises the missing relationships

<div class="rule-stack">
  <div>
    <span>Rule 1</span>
    <strong>Current direct control</strong>
    <code>corporate PSC + not ceased<br>→ directlyControls</code>
  </div>
  <div>
    <span>Rule 2</span>
    <strong>Transitive control</strong>
    <code>direct control path<br>→ controls</code>
  </div>
  <div>
    <span>Rule 3</span>
    <strong>Group membership</strong>
    <code>group root + controls<br>→ memberOfGroup</code>
  </div>
  <div>
    <span>Rule 4</span>
    <strong>Gazette evidence</strong>
    <code>company number + notice<br>→ hasInsolvencyNotice</code>
  </div>
</div>

<div class="datalog-inference">
  <span>Alert inference</span>
  <code>hasCustomer(S,C) ∧ memberOfGroup(C,G) ∧ memberOfGroup(E,G) ∧ hasInsolvencyNotice(E,N)<br>→ groupInsolvencyExposure(S,C,N)</code>
</div>

---

# The inferred path explains the KYC alert


```text
Northbridge Infrastructure Services
  └─ supplies / invoices ────────► Customer 00594581
                                      │
                                      ├─ ultimately controlled by
                                      ▼
                                  Company 03782379
                                      │
                                      ├─ has insolvency notice
                                      ▼
                                  Gazette notice 2948343
                                  Winding-up order · 15 Jan 2018
```

<div class="investigation-callout">
  <strong>Hidden signal surfaced</strong>
  <span>The alert does not rely on name similarity. Every step is derived through shared company identifiers, control rules and the imported Gazette notice.</span>
</div>

---

# What “early alert” means in this demo

<div class="alert-window">
  <div>
    <span>1 · Baseline</span>
    <strong>Direct customer check</strong>
    <p>No insolvency notice is found against Northbridge's contracted customer.</p>
  </div>
  <div>
    <span>2 · Public event</span>
    <strong>Group company notice</strong>
    <p>A Gazette event is published against the parent or another group company.</p>
  </div>
  <div class="active">
    <span>3 · RDFox</span>
    <strong>Rule materialisation</strong>
    <p>The event is immediately connected to Northbridge's customers in the same inferred group.</p>
  </div>
  <div>
    <span>4 · KYC action</span>
    <strong>Explainable alert</strong>
    <p>The subcontractor reviews credit exposure instead of waiting for its direct customer to fail.</p>
  </div>
</div>

<div class="investigation-callout risk">
  <strong>Evidence boundary</strong>
  <span>“Early” means earlier in the subcontractor's response window—not prediction before public evidence exists.</span>
</div>

---

# RDFox produces an explainable KYC alert

<div class="alert-panel">
  <div class="alert-status">Corporate insolvency exposure</div>
  <h2>Customer 00594581 is linked to a liquidated group</h2>
  <div class="alert-evidence">
    <div><span>Customer</span><strong>Carillion Construction Limited</strong></div>
    <div><span>Ultimate parent</span><strong>Carillion plc · 03782379</strong></div>
    <div><span>Evidence</span><strong>Gazette notice 2948343</strong></div>
    <div><span>Event</span><strong>Winding-up order · code 2452</strong></div>
  </div>
</div>

<div class="investigation-callout risk">
  <strong>Suggested subcontractor action</strong>
  <span>Review unpaid invoices, pause further unsecured work, protect contractual rights, assess cash-flow impact and diversify away from other customers in the group.</span>
</div>

---

# Same public evidence, different KYC visibility

<div class="comparison-table">
  <div class="comparison-head">
    <span>Question</span><span>Ordinary KYC</span><span>Connected RDFox view</span>
  </div>
  <div>
    <span>Is the direct customer identifiable?</span>
    <strong>Yes</strong>
    <strong class="positive">Yes</strong>
  </div>
  <div>
    <span>Which company ultimately controls it?</span>
    <strong class="negative">Not necessarily checked</strong>
    <strong class="positive">Derived</strong>
  </div>
  <div>
    <span>Does an event elsewhere in the group affect our customer exposure?</span>
    <strong class="negative">Usually hidden</strong>
    <strong class="positive">Connected</strong>
  </div>
  <div>
    <span>Can the alert show its evidence path?</span>
    <strong class="negative">Fragmented</strong>
    <strong class="positive">Explainable</strong>
  </div>
</div>

---

# The RDFox KYC proposition

<div class="conclusion-grid four">
  <div>
    <span>01</span>
    <strong>Signals are distributed</strong>
    <p>Customer-ledger, control and insolvency facts sit in separate records and datasets.</p>
  </div>
  <div>
    <span>02</span>
    <strong>KYC needs the group view</strong>
    <p>A subcontractor's direct customer can inherit credit risk from an event against another group entity.</p>
  </div>
  <div>
    <span>03</span>
    <strong>Datalog surfaces the signal</strong>
    <p>Rules materialise control, group membership, notice links and customer exposure.</p>
  </div>
  <div>
    <span>04</span>
    <strong>Alerts remain explainable</strong>
    <p>RDFox retains the evidence path from KYC record to public event.</p>
  </div>
</div>

---

# Sources and privacy boundary

<div class="sources-list">
  <div><span>[1]</span><p><strong>Wikipedia, “Carillion”</strong> — secondary orientation and chronology, accessed 8 September 2026.</p></div>
  <div><span>[2]</span><p><strong>Companies House</strong> — Carillion plc company and insolvency records, company number 03782379, plus corporate PSC snapshot data.</p></div>
  <div><span>[3]</span><p><strong>The Gazette</strong> — notice 2948343, winding-up order, notice code 2452, published 19 January 2018.</p></div>
  <div><span>[4]</span><p><strong>UK Government and Insolvency Service</strong> — “Carillion declares insolvency: information for employees, creditors and suppliers”, 15 January 2018.</p></div>
  <div><span>[5]</span><p><strong>House of Commons joint committee report</strong> — Carillion, HC 769, published 16 May 2018.</p></div>
  <div><span>[6]</span><p><strong>National Audit Office</strong> — “Investigation into the government's handling of the collapse of Carillion”, published 7 June 2018.</p></div>
  <div><span>[7]</span><p><strong>Wikimedia Commons imagery</strong> — Graham Richardson, <a href="https://commons.wikimedia.org/wiki/File:Carillion_Ford_Transit_350_LWB_Panel_Van.jpg">Carillion van</a> (<a href="https://creativecommons.org/licenses/by/2.0/">CC BY 2.0</a>); Snow storm in Eastern Asia, <a href="https://commons.wikimedia.org/wiki/File:Banbury_Carrilion_train_1.png">Carillion rail train</a> (public domain); Ministry of Defence, <a href="https://commons.wikimedia.org/wiki/File:GCHQ-aerial.jpg">GCHQ aerial</a> (<a href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/1/">OGL v1.0</a>). Images cropped.</p></div>
</div>

<div class="method-note">
  <strong>Privacy boundary:</strong> this presentation uses corporate names,
  company numbers, contracts, financial figures and public insolvency events.
  It intentionally excludes names and other personal data about individuals.
</div>

---
layout: center
class: rdfox-closing text-center
---

<img class="rdfox-logo closing-logo" src="/rdfox-logo.svg" alt="RDFox by Oxford Semantic Technologies">

# Connect the evidence.<br>Alert KYC earlier.

Datalog reasoning in RDFox

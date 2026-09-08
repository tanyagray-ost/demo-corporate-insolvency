# Introduction

Companies House is the United Kingdom's registrar of companies and maintains a comprehensive database of corporate information, including company ownership and financial status. The Gazette publishes notices, on authority, of corporate insolvency and other events. Notices published from 2015 are represented in an RDF format in addition to HTML.

This document provides an overview of a use case for RDFox with a knowledge graph that combines corporate insolvency data, as reported in The Gazette with Companies House data relating to corporate group ownership.

The uses cases will demonstrate the features of RDFox including:

- **Fast materialisation:** new notices can trigger inferred risks across customers, suppliers, contracts and corporate groups.

- **Multi-hop reasoning:** it can traverse parent, subsidiary and dependency relationships that are not stated in one source.

- **Temporal precision:** events are matched against the relationships and contracts active at the relevant time.

- **Explainability:** an alert can retain links to the notice, corporate relationship, contract and rule that produced it.

- **Incremental updating:** new appointments, dismissals, dissolutions or ownership changes can update affected conclusions.

- **Consistent policy:** the same rules can assess every counterparty and group rather than relying on manual interpretation.


# Data sources 

Companies House API 
https://developer.company-information.service.gov.uk/ 





# Use Cases


## Identifying Indirect Insolvency Risk  - current Suppliers
Identify insolvency risk for a company in its list of suppliers, not immediately apparent, through indirect exposure of a parent company or company in the same corporate group.

A company monitors **corporate insolvency notices about current suppliers** primarily to protect operational continuity, money already paid, access to critical goods or services, and contractual rights.

### Principal supplier risks

| Risk | Why the notice matters |
|---|---|
| **Supply interruption** | Production, delivery or support may stop with little warning. |
| **Advance-payment loss** | Deposits and prepaid amounts may become unsecured claims in the insolvency. |
| **Unfulfilled orders** | The supplier may lack cash, staff or materials to complete work already ordered. |
| **Quality deterioration** | Financial pressure can lead to reduced staffing, maintenance, testing or quality control. |
| **Warranty failure** | Repairs, replacements, refunds and long-term support may no longer be available. |
| **Loss of critical services** | Software, hosting, maintenance, logistics or outsourced operations may be suspended. |
| **Ownership disputes** | Goods, tooling, data or materials held at the supplier’s premises may become difficult to recover. |
| **Contract uncertainty** | An administrator or liquidator may continue, sell, renegotiate or terminate arrangements. |
| **Successor-company confusion** | A new entity with similar branding may not assume the old supplier’s contracts or liabilities. |
| **Regulatory exposure** | The supplier may lose licences, insurance, certifications or qualified staff required for compliant delivery. |
| **Concentration risk** | Failure of a sole or strategically important supplier may affect the company’s own customers and revenue. |

### Immediate actions

1. **Identify dependencies:** determine which products, sites, systems and customer commitments rely on the supplier.
2. **Check open exposure:** list deposits, prepayments, undelivered orders, warranty claims and credits.
3. **Confirm trading status:** contact the supplier or appointed insolvency practitioner before placing further orders or payments.
4. **Review contracts:** examine termination, insolvency, continuity, escrow, step-in, intellectual-property and data-return provisions.
5. **Secure company property:** identify tooling, stock, equipment, documents or data held by the supplier and establish ownership.
6. **Activate alternatives:** qualify replacement suppliers, reserve capacity and increase safety stock where appropriate.
7. **Protect critical technology:** exercise source-code escrow, backup, data-export or transition-assistance rights.
8. **Validate any successor:** treat a similarly named replacement company as a new counterparty until its identity, assets, obligations and financial capacity are confirmed.
9. **Prepare a creditor claim:** document sums owed if deposits, rebates, claims or property cannot be recovered.
10. **Notify stakeholders:** inform procurement, operations, finance, legal, information security and affected customers as necessary.

Different notices imply different urgency. A **winding-up petition** is an early but serious warning; **administration** may allow continued trading or a sale; **liquidation** commonly indicates that normal supply will cease; and a **prohibited-name reuse notice** may indicate continuity of the business but not necessarily continuity of contracts, warranties or liabilities.

For supplier monitoring, an insolvency notice is therefore an authoritative **business-continuity trigger**. It should prompt contingency action before the supplier’s financial distress becomes disruption to your own operations.

## Know Your Customer (KYC) 
Identify insolvency risk for a company that is evaluating potential customers, through indirect exposure of a parent company or company in the same corporate group.

A company monitors **corporate insolvency notices about potential or existing customers** because those notices can indicate that the customer may be unable to pay, may cease trading, or may continue through a different legal entity.

### For an existing customer

The notice can trigger immediate credit-control action:

- **Outstanding invoices:** identify unpaid amounts and stop the exposure increasing.
- **Future deliveries:** decide whether to suspend orders, require payment in advance or reduce the credit limit.
- **Proof of debt:** establish whether and how to submit a creditor claim.
- **Retention of title:** determine whether supplied goods can be identified and recovered under the contract.
- **Set-off rights:** check whether amounts owed between the parties can be set off.
- **Contract status:** understand whether an administrator, liquidator or successor company will continue or terminate the contract.
- **Entity changes:** avoid accidentally transferring the old company’s credit terms to a new company with a similar name.
- **Payment verification:** confirm new bank details and instructions independently, particularly during a restructuring.

Speed matters because continuing to supply after a formal insolvency event can substantially increase an unsecured loss.

### For a potential customer

The notice informs the onboarding and credit decision:

- whether the applicant or its directors are connected to a failed company;
- whether it is a newly formed successor with limited financial history;
- whether it acquired the old company’s business and assets but not its liabilities;
- whether similar operating or management risks remain;
- whether normal unsecured credit terms are appropriate; and
- whether guarantees, deposits, insurance or advance payment should be required.

### What different notices can reveal

| Notice or event | Potential customer-risk implication |
|---|---|
| Administration | Serious financial distress, but the business may continue or be sold |
| Creditors’ voluntary liquidation | The company is insolvent and being wound up |
| Compulsory winding-up petition/order | A creditor or public authority is seeking, or has obtained, liquidation |
| Appointment of liquidator | Control has moved from directors to an insolvency practitioner |
| Company voluntary arrangement | Debts may be repaid under modified terms over time |
| Moratorium | Temporary protection from creditor enforcement while rescue is explored |
| Re-use of prohibited name | Related management may continue the business through another entity |
| Final account/dissolution | The insolvency process is approaching completion and recovery prospects may be finalised |

A notice should therefore feed into:

1. **credit limits and payment terms;**
2. **order-release decisions;**
3. **debt-recovery and creditor-claim workflows;**
4. **contract and supply-continuity planning;**
5. **customer identity and bank-detail checks;**
6. **portfolio and concentration-risk reporting.**

The notice is not, by itself, a complete credit assessment. It is an authoritative, time-sensitive signal that should be combined with accounts, payment history, Companies House records, credit data and direct engagement with the customer or appointed insolvency practitioner.


## Know Your Supplier - insolvency in supplier's parent company or sibling company 

The insolvency of a supplier’s **parent or sibling company** does not automatically make the supplier insolvent: each group company is normally a separate legal entity. However, it can create significant **contagion risk** because group companies often share funding, assets, services and contractual obligations.

### Main contagion routes

| Exposure | Potential effect on the supplier |
|---|---|
| **Parent funding** | The supplier may depend on loans, capital injections or payment support from the parent. That support may stop immediately. |
| **Cash pooling** | Supplier cash may be held centrally, swept to the parent, frozen or difficult to recover from the insolvent entity. |
| **Guarantees and security** | The supplier may have guaranteed group debt or granted security over its assets. A parent default could expose those assets. |
| **Cross-default clauses** | The insolvency of one group member may trigger defaults under the supplier’s loans, leases or major contracts. |
| **Intercompany balances** | The supplier may be owed substantial sums by the insolvent parent or sibling and have to recognise a loss. |
| **Shared services** | Payroll, IT, cybersecurity, finance, HR, logistics or procurement provided by the affected company may stop. |
| **Shared assets and premises** | The supplier may use property, equipment, licences, vehicles or inventory legally owned by the insolvent group member. |
| **Intellectual property** | Brands, software, patents or licences essential to supply may belong to the parent and could be sold or access withdrawn. |
| **Common supply chain** | A failed sibling may provide components, manufacturing, warehousing or distribution to the supplier. |
| **Group purchasing** | Loss of group purchasing arrangements may increase costs or remove access to materials and credit. |
| **Reputational contagion** | Banks, insurers and trade suppliers may reduce facilities or tighten terms across the whole group. |
| **Management disruption** | Shared directors and senior staff may be diverted into restructuring or replaced by insolvency practitioners. |
| **Group sale or breakup** | The supplier may be sold, separated from essential operations or closed despite remaining solvent on a standalone basis. |

### Parent versus sibling failure

A **parent-company insolvency** is usually more significant because the parent may control the supplier, own its shares and provide finance, guarantees, strategy and shared infrastructure. An insolvency practitioner may sell the supplier, withdraw support or restructure the group.

A **sibling-company insolvency** is generally less direct, but may still be serious where the companies share customers, facilities, systems, employees, contracts or financing. It can also reveal a broader group-wide problem rather than an isolated failure.

### What the customer should investigate

1. Map the supplier’s ownership and identify all operationally important group companies.
2. Ask whether the supplier is profitable and cash-generative on a standalone basis.
3. Review parent guarantees, cross-guarantees, security and cross-default arrangements.
4. Establish where the supplier’s cash is held and whether it participates in group cash pooling.
5. Identify who owns critical IP, inventory, premises, systems and production equipment.
6. Determine which services and components come from the affected group company.
7. Check whether the supplier has contingency funding and replacement-service arrangements.
8. Confirm whether a sale or restructuring could affect contracts, warranties or data access.
9. Increase monitoring of payment behaviour, staff departures, delivery performance and credit-insurance limits.
10. Prepare alternative suppliers, safety stock and transition plans for critical dependencies.

The key assessment is not merely **“Is the contracted supplier itself insolvent?”** It is:

> **Can the supplier continue performing independently if financial and operational support from the affected group company disappears?**

A related-company insolvency should therefore trigger enhanced due diligence and continuity planning, but not an automatic conclusion that the supplier will fail.



## Know Your Customer (KYC)  - Gazette notice - use of prohibited name 

example https://www.thegazette.co.uk/notice/5203489 

A **re-use of a prohibited name notice** indicates that substantially the same business may continue under similar branding after the previous company entered insolvent liquidation. For a supplier or customer, that creates an important distinction between **business continuity** and **legal-entity continuity**.

The shopfront, staff and trading name may look unchanged, while the entity responsible for debts, contracts and warranties has changed.

| Risk area | Why it matters |
|---|---|
| **Credit risk** | The former company failed while under related management. The successor may have limited capital, little trading history and similar commercial weaknesses. |
| **Old debts** | Amounts owed by the insolvent company generally do not automatically become debts of the successor. Suppliers may lose old receivables while being asked to continue supplying. |
| **Contract continuity** | Existing contracts, purchase orders, guarantees, service agreements and credit limits may not have transferred to the new entity. |
| **Warranty and support** | A customer may discover that the new company does not accept responsibility for deposits, warranties, refunds or unfinished work owed by the old company. |
| **Management continuity** | The same director’s involvement may mean that governance, financial controls and business practices have not materially changed. |
| **Asset continuity** | The successor may have purchased the brand and operating assets but not all employees, licences, systems, insurance or contractual rights needed to perform. |
| **Identity confusion** | Similar names can cause invoices, payments and legal notices to be assigned to the wrong company. |
| **Reputational risk** | Repeated insolvency and continuation under a similar name may concern customers, lenders, insurers and procurement teams. |
| **Supply disruption** | If the underlying financial or operational problems persist, the successor could fail or interrupt delivery. |
| **Legal compliance** | The notice supports one statutory exception, but publication alone does not prove that every condition of rule 22.4 has been met. |

For a **supplier**, the immediate concern is whether to extend credit. Appropriate controls might include shorter payment terms, deposits, credit insurance, guarantees, lower credit limits or payment before delivery.

For a **customer**, the main concerns are delivery, warranty and recoverability of advance payments. Controls might include milestone payments, escrow, performance security, confirmation of insurance and explicit contractual responsibility for continuing services.

The notice is a **risk indicator, not evidence of misconduct**. Publishing it can be a positive sign of transparency and an attempt to comply with insolvency law. It should nevertheless trigger enhanced due diligence:

1. Confirm the exact legal entity, company number, directors and bank-account holder.
2. Determine what business and assets were acquired and from whom.
3. Verify whether your contract or debt belongs to the old or new company.
4. Obtain current accounts, funding information, credit reports and trade references.
5. Check insurance, licences, accreditations and operational capacity.
6. Ask whether warranties, deposits, service obligations and outstanding orders are being honoured.
7. Review related insolvency notices and the liquidator’s reports when available.
8. Set exposure limits appropriate to a newly established or recently restructured counterparty.

In practical risk scoring, code **2403** is therefore best treated as an **insolvency-linked continuity event involving related management**, rather than automatically as a negative legal finding.



## Research and economic indicators

Measure time from incorporation to insolvency, procedure duration and sector-level failure rates using public company facts. 


## Entity resolution

Use company numbers and historical names to join notices published under old trading or registered names to the correct company. 


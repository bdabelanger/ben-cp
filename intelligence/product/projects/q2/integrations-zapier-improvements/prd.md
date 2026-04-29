---
title: Integrations - Zapier improvements
type: prd
domain: product/projects/q2
status: active
taxonomy: Integrations
---

# PRD: Integrations - Zapier improvements

<table data-layout="default">
 <tbody>
  <tr>
   <th>
    <p>
     <strong>
      Status
     </strong>
    </p>
   </th>
   <th>
    <p>
     Discovery
    </p>
   </th>
  </tr>
  <tr>
   <td>
    <p>
     <strong>
      Epic
     </strong>
    </p>
   </td>
   <td>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     <strong>
      Product Manager
     </strong>
    </p>
   </td>
   <td>
    <p>
     @Ben Belanger
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     <strong>
      Designer
     </strong>
    </p>
   </td>
   <td>
    <p>
     @Pierre Klein
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     <strong>
      Engineers
     </strong>
    </p>
   </td>
   <td>
    <p>
     Flow Digital - Eric
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     <strong>
      QA Engineers
     </strong>
    </p>
   </td>
   <td>
    <p>
     @Yi Liu
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     <strong>
      Google Drive File Location
     </strong>
    </p>
   </td>
   <td>
    <p>
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h1>
 Problem Definition
</h1>
<h2>
 Context
</h2>
<p>
 <a href="https://docs.google.com/presentation/d/1ef7I2wDFuX7fwVRILPJbgSPiA_jUX8j26HMIAS_Vsac/edit?slide=id.p39#slide=id.p39">
  https://docs.google.com/presentation/d/1ef7I2wDFuX7fwVRILPJbgSPiA_jUX8j26HMIAS_Vsac/edit?slide=id.p39#slide=id.p39
 </a>
</p>
<p>
 Casebook has deployed a native Zapier application that allows organizations to push data from external systems into Casebook without writing code. Zapier serves as Casebook's primary system-to-system integration channel, enabling customers to connect tools like Jotform, Google Forms, Salesforce, and other platforms to Casebook through automated workflows ("Zaps").
</p>
<table data-layout="default">
 <tbody>
  <tr>
   <th>
    <p>
     <strong>
      Persona(s) Engaged
     </strong>
    </p>
   </th>
   <th>
    <p>
     <strong>
      Job(s) to be Done
     </strong>
    </p>
   </th>
  </tr>
  <tr>
   <td>
    <p>
     Agency Administrator / IT Lead
    </p>
   </td>
   <td>
    <p>
     Configure automated data pipelines between external systems (Jotform, Google Forms, referral platforms, EHRs) and Casebook without requiring developer resources or direct API work.
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     Frontline Worker / Case Manager
    </p>
   </td>
   <td>
    <p>
     Receive complete, well-structured records in Casebook from external form submissions and system events, without having to manually re-enter data that was already captured elsewhere.
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     Supervisor / Program Manager
    </p>
   </td>
   <td>
    <p>
     Trust that data flowing into Casebook from external systems is complete and accurate, including custom fields and sub-resources, so that reporting and compliance requirements are met without manual reconciliation.
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h2>
 How Zapier integrations work today
</h2>
<h3>
 Three basic write actions
</h3>
<p>
 Casebook's current Zapier application supports three write actions: Create a Person, Create an Intake Report, and Create a Case. These cover the most common top-level objects but expose only a fixed set of default fields. Sub-resources are excluded entirely.
</p>
<h3>
 No support for custom fields or dynamic configuration
</h3>
<p>
 Casebook tenants are highly configurable - administrators can add custom fields, rename defaults, change field types, and configure select options. None of this configuration is reflected in the Zapier application. Custom data captured in external forms has no path into Casebook through Zapier, leaving records incomplete.
</p>
<h3>
 No line item support
</h3>
<p>
 Many Casebook objects include one-to-many sub-resources (a Person can have multiple addresses, an Intake Report can have multiple allegations). Zapier supports this pattern through Line Item Groups, but Casebook's app does not implement them.
</p>
<h3>
 No triggers
</h3>
<p>
 The Zapier application offers zero triggers. Customers who want Casebook events to kick off downstream actions must use Zapier's premium Webhooks connector and parse raw payloads manually - a fragile, technical workaround that most customers cannot maintain.
</p>
<h3>
 No search actions
</h3>
<p>
 Without search actions, customers cannot look up existing records before creating new ones. This leads to duplicate records and prevents standard "find or create" Zap patterns.
</p>
<h2>
 Problems &amp; Impact
</h2>
<h3>
 Write actions do not reflect the full Casebook data model
</h3>
<p>
 The three existing write actions only expose a fixed set of default fields. They do not support custom fields, line item groups, or sub-resource creation. Data captured in external forms - even when it maps directly to Casebook fields - has no path into the system through Zapier. Staff must open each record, compare it to the source submission, and manually enter the remaining data. This is the most common source of frustration among customers using Zapier today.
</p>
<h3>
 Casebook events cannot trigger downstream workflows
</h3>
<p>
 Customers who want to react to Casebook events in downstream systems - billing platforms, notification tools, reporting dashboards - have no out-of-the-box option. The only workaround requires technical expertise, is fragile to maintain, and is not viable for most of Casebook's customer base. The absence of triggers also limits Casebook's positioning as a connected system of record.
</p>
<h3>
 No search actions to prevent duplicates or enable conditional logic
</h3>
<p>
 Zapier best practices rely heavily on search actions to implement "find or create" flows. Without them, customers have no way to avoid duplicate records when the same person submits a form twice or when data arrives from multiple systems. Conditional workflows - check if a person has an open case, route an intake differently by program - are also impossible without search.
</p>
<h3>
 Customer Problem Statement(s)
</h3>
<table data-layout="default">
 <tbody>
  <tr>
   <th>
    <p>
     <strong>
      ID
     </strong>
    </p>
   </th>
   <th>
    <p>
     <strong>
      Customer Problem Statement(s)
     </strong>
    </p>
   </th>
  </tr>
  <tr>
   <td>
    <p>
     1
    </p>
   </td>
   <td>
    <p>
     As an Administrator, I need external data submitted through Zapier-connected forms to write directly into Casebook person, intake, and case records — including custom fields — in order to eliminate manual re-entry and ensure complete records from the moment they are created.
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     2
    </p>
   </td>
   <td>
    <p>
     As a Frontline Worker, I need Casebook to automatically receive and structure data from external systems when a new referral, intake, or case event occurs in order to reduce the time between a client submitting information and a worker being ready to act on it.
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h1>
 Solution Concept
</h1>
<h2>
 Overview
</h2>
<p>
 This initiative enhances Casebook's native Zapier application by delivering three fully-featured write actions:
 <strong>
  Create/Update a Person
 </strong>
 ,
 <strong>
  Create/Update an Intake Report
 </strong>
 , and
 <strong>
  Create/Update a Case
 </strong>
 . Each action is designed to support the full Casebook data model for its resource type - including custom fields, line item groups, and upsert logic - and to compose cleanly with the others in multi-step Zaps.
</p>
<p>
 Detailed solution concepts, implementation specifications, and open items for each action are documented in the sub-pages below. Flow Digital should treat each sub-page as the primary technical reference for its respective action.
</p>
<table data-layout="default">
 <tbody>
  <tr>
   <th>
    <p>
     <strong>
      Action
     </strong>
    </p>
   </th>
   <th>
    <p>
     <strong>
      Sub-page
     </strong>
    </p>
   </th>
   <th>
    <p>
     <strong>
      Priority
     </strong>
    </p>
   </th>
   <th>
    <p>
     <strong>
      v1 Scope (25 hrs)
     </strong>
    </p>
   </th>
  </tr>
  <tr>
   <td>
    <p>
     Create/Update a Person
    </p>
   </td>
   <td>
    <p>
     <ac:link>
      <ri:page ri:content-title="Create/Update a Person Write Action" ri:version-at-save="8">
      </ri:page>
      <ac:link-body>
       Create/Update a Person Write Action
      </ac:link-body>
     </ac:link>
    </p>
   </td>
   <td>
    <p>
     P1
    </p>
   </td>
   <td>
    <p>
     In scope
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     Create/Update an Intake Report
    </p>
   </td>
   <td>
    <p>
     Coming soon
    </p>
   </td>
   <td>
    <p>
     P1
    </p>
   </td>
   <td>
    <p>
     In scope
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     Create/Update a Case
    </p>
   </td>
   <td>
    <p>
     Coming soon
    </p>
   </td>
   <td>
    <p>
     P2
    </p>
   </td>
   <td>
    <p>
     Stretch / future
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h2>
 v1 Delivery Scope (25-Hour Budget)
</h2>
<p>
 Flow Digital (Eric) is working within a
 <strong>
  25-hour total budget for v1
 </strong>
 . This budget covers both P1 actions:
</p>
<ul>
 <li>
  <p>
   <strong>
    Create/Update a Person
   </strong>
   — full field set, custom fields (see terminology note below), and key Contact line item groups (addresses, phones, emails)
  </p>
 </li>
 <li>
  <p>
   <strong>
    Create/Update an Intake Report
   </strong>
   — custom fields and association of N People to an Intake Report (minimum: from the Intake action side; bidirectional linking is a stretch goal)
  </p>
 </li>
</ul>
<p>
 Both actions will be delivered as
 <strong>
  new, fresh Zapier actions
 </strong>
 . Manual migration is required from legacy actions. Legacy actions remain functional, clearly labeled as legacy, with no forced migration and no sunset date.
</p>
<h3>
 Terminology: Dynamic Pages = custom fields
</h3>
<p>
 Casebook refers to administrator-configured custom fields as
 <strong>
  Dynamic Pages
 </strong>
 . Zapier's implementation pattern for exposing them at Zap build time uses
 <code>
  dynamicFields
 </code>
 (Zapier SDK terminology). These two terms refer to the same concept from different vantage points.
</p>
<table data-layout="default">
 <tbody>
  <tr>
   <th>
    <p>
     Term
    </p>
   </th>
   <th>
    <p>
     Context
    </p>
   </th>
  </tr>
  <tr>
   <td>
    <p>
     Dynamic Pages
    </p>
   </td>
   <td>
    <p>
     Casebook admin UI and internal documentation
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     <code>
      dynamicFields
     </code>
     /
     <code>
      altersDynamicFields
     </code>
    </p>
   </td>
   <td>
    <p>
     Zapier SDK implementation pattern
    </p>
   </td>
  </tr>
 </tbody>
</table>
<p>
 When this document or its sub-pages refer to "custom field support," they mean Dynamic Pages support, implemented via Zapier's
 <code>
  dynamicFields
 </code>
 pattern.
</p>
<h3>
 Stretch goals (not in 25-hour scope)
</h3>
<p>
 The following are explicitly
 <strong>
  not
 </strong>
 targeted within the 25-hour v1 budget. They are candidates for a follow-on engagement.
</p>
<table data-layout="default">
 <tbody>
  <tr>
   <th>
    <p>
     Stretch Goal
    </p>
   </th>
   <th>
    <p>
     Notes
    </p>
   </th>
  </tr>
  <tr>
   <td>
    <p>
     Custom field (Dynamic Pages) support in the Case action
    </p>
   </td>
   <td>
    <p>
     P2 action, not in v1
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     People-Case linking from the Case action side
    </p>
   </td>
   <td>
    <p>
     Similar pattern to People-Intake. Bidirectional is ideal. MVP would be from the Case action side.
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h3>
 Out of scope — HIPAA-protected fields
</h3>
<p>
 Zapier has not signed a Business Associate Agreement (BAA) with Casebook or its customers. As a result, the following fields are excluded from
 <strong>
  all
 </strong>
 Zapier write actions and must not be exposed:
</p>
<p>
 SSN, allergies, medical conditions, prescriptions, healthcare providers, insurances
</p>
<blockquote>
 <p>
  <strong>
   Note for future integrations:
  </strong>
  Platforms that do have BAA coverage (e.g., Microsoft Power Automate, Google Cloud Workflows) may be able to expose these fields in future integration work. This is a platform-level decision. The exclusion is a Zapier-specific constraint, not a Casebook data model constraint.
 </p>
</blockquote>
<h2>
 Scope
</h2>
<h3>
 What's In
</h3>
<table data-layout="default">
 <tbody>
  <tr>
   <th>
    <p>
     <strong>
      Capability
     </strong>
    </p>
   </th>
   <th>
    <p>
     <strong>
      Actions Affected
     </strong>
    </p>
   </th>
  </tr>
  <tr>
   <td>
    <p>
     Cover full field sets
    </p>
   </td>
   <td>
    <p>
     Person, Intake Report, Case
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     Include custom fields via
     <code>
      dynamicFields
     </code>
    </p>
   </td>
   <td>
    <p>
     Person, Intake Report, Case
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     Support line item group support for sub-resources
    </p>
   </td>
   <td>
    <p>
     Person (addresses, phones, emails, occupations, incomes, educations, relationships), Intake Report (TBD), Case (TBD)
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     Output
     <code>
      person_id
     </code>
     for multi-step Zaps
    </p>
   </td>
   <td>
    <p>
     Person to Intake, Person to Case
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     Match before creating (upsert)
    </p>
   </td>
   <td>
    <p>
     Person
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     Removal of Person fields
    </p>
   </td>
   <td>
    <p>
     Intake
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h3>
 What's Out
</h3>
<table data-layout="default">
 <tbody>
  <tr>
   <th>
    <p>
     <strong>
      Capability
     </strong>
    </p>
   </th>
   <th>
    <p>
     <strong>
      Reason
     </strong>
    </p>
   </th>
  </tr>
  <tr>
   <td>
    <p>
     Zapier triggers
    </p>
   </td>
   <td>
    <p>
     Separate initiative - not in scope for this delivery
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     Zapier search actions
    </p>
   </td>
   <td>
    <p>
     Separate initiative - not in scope for this delivery
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     Zapier write actions for sub-resources (Notes, Attachments, Service Enrollments, Service Interactions, Providers)
    </p>
   </td>
   <td>
    <p>
     Separate initiative - not in scope for this delivery
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     Sub-resource append/replace/upsert control
    </p>
   </td>
   <td>
    <p>
     Separate initiative - MVP assumes append
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     External reference ID / system identifier line items (Person, Intake, Case)
    </p>
   </td>
   <td>
    <p>
     Separate initiative - Needs discovery
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     Upsert for Cases or Intake reports
    </p>
   </td>
   <td>
    <p>
     Separate initiative - Needs discovery
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     SSN, allergies, medical conditions, prescriptions, healthcare providers, insurances (all actions)
    </p>
   </td>
   <td>
    <p>
     Out of scope - Zapier has not signed a BAA with Casebook or its customers. These fields are excluded from all Zapier write actions. See the v1 Delivery Scope section above.
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h2>
 Non-Functional Requirements
</h2>
<table data-layout="default">
 <tbody>
  <tr>
   <th>
    <p>
     <strong>
      ID
     </strong>
    </p>
   </th>
   <th>
    <p>
     <strong>
      Short Title
     </strong>
    </p>
   </th>
   <th>
    <p>
     <strong>
      Requirement
     </strong>
    </p>
   </th>
   <th>
    <p>
     <strong>
      JIRA Link
     </strong>
    </p>
   </th>
  </tr>
  <tr>
   <td>
    <p>
     NF.1
    </p>
   </td>
   <td>
    <p>
     Events - reporting
    </p>
   </td>
   <td>
    <p>
     No events - creator should accurately be listed as the application
    </p>
   </td>
   <td>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     NF.2
    </p>
   </td>
   <td>
    <p>
     Events - audit log
    </p>
   </td>
   <td>
    <p>
     No events - creator should accurately be listed as the application
    </p>
   </td>
   <td>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     NF.3
    </p>
   </td>
   <td>
    <p>
     Events - documentation
    </p>
   </td>
   <td>
    <p>
     Any updates to events should be documented in our Confluence repo illustrating our list/explanation of supported events.
    </p>
   </td>
   <td>
    <p>
    </p>
   </td>
  </tr>
  <tr>
   <td>
    <p>
     NF.4
    </p>
   </td>
   <td>
    <p>
     Performance
    </p>
   </td>
   <td>
    <p>
     Generally responses should be returned within 5 seconds and without timeouts
    </p>
   </td>
   <td>
    <p>
    </p>
   </td>
  </tr>
 </tbody>
</table>

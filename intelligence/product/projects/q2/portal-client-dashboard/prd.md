---
title: Portal - Client Dashboard
type: prd
domain: product/projects/q2
status: active
---

# PRD: Portal - Client Dashboard

<table ac:local-id="e0cf9caaf767" data-layout="default" data-table-width="760">
 <tbody>
  <tr ac:local-id="4c39fb0eb8f8">
   <th ac:local-id="0282311c30e9">
    <p local-id="ef5349a9410b">
     <strong>
      Status
     </strong>
    </p>
   </th>
   <th ac:local-id="7e68d64aa587">
    <p local-id="f18edfd32d12">
     Discovery
    </p>
   </th>
  </tr>
  <tr ac:local-id="d90a5b6b6f36">
   <td ac:local-id="b932b7c32781">
    <p local-id="2932826323a7">
     <strong>
      Epic
     </strong>
    </p>
   </td>
   <td ac:local-id="7c0da9cfe982">
    <p local-id="42910f0be1e5">
    </p>
   </td>
  </tr>
  <tr ac:local-id="3e2bd8ff5765">
   <td ac:local-id="6a3bd4c20b17">
    <p local-id="de65ec3ca39e">
     <strong>
      Product Manager
     </strong>
    </p>
   </td>
   <td ac:local-id="bd56351dcfe3">
    <p local-id="5369166cc5f9">
    </p>
   </td>
  </tr>
  <tr ac:local-id="73694ac369fd">
   <td ac:local-id="3aff64a6b9fc">
    <p local-id="7a9e2d603acc">
     <strong>
      Designer
     </strong>
    </p>
   </td>
   <td ac:local-id="9b588e25da82">
    <p local-id="e1bb04618c7e">
     @Pierre Klein
    </p>
   </td>
  </tr>
  <tr ac:local-id="01246c1b4c52">
   <td ac:local-id="b0fcbc3c77e5">
    <p local-id="1d5ad6056dfd">
     <strong>
      Engineers
     </strong>
    </p>
   </td>
   <td ac:local-id="1b87a26d94c0">
    <p local-id="707848181ba1">
    </p>
   </td>
  </tr>
  <tr ac:local-id="f334b7c1e582">
   <td ac:local-id="6c5bc46ad9b0">
    <p local-id="8c57df1bac3f">
     <strong>
      QA Engineers
     </strong>
    </p>
   </td>
   <td ac:local-id="cd9cc8942991">
    <p local-id="978741b49dc0">
    </p>
   </td>
  </tr>
  <tr ac:local-id="63e38e50ad9c">
   <td ac:local-id="08dd81e92ee8">
    <p local-id="6e9072fdfadf">
     <strong>
      Google Drive File Location
     </strong>
    </p>
   </td>
   <td ac:local-id="e9c219c17862">
    <p local-id="dbe62360b85d">
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h1 local-id="d26ea10724ec">
 Problem Definition
</h1>
<h2 local-id="bb21d263fa5a">
 Context
</h2>
<a data-card-appearance="embed" data-layout="center" data-width="100.00" href="https://docs.google.com/presentation/d/1fCDIBZk_vj7MAM5Tt49DhsT9MAqQGpmczzF879z9Z78/edit?slide=id.g39bcce1743b_0_428#slide=id.g39bcce1743b_0_428" local-id="a569c855ac07">
 https://docs.google.com/presentation/d/1fCDIBZk_vj7MAM5Tt49DhsT9MAqQGpmczzF879z9Z78/edit?slide=id.g39bcce1743b_0_428#slide=id.g39bcce1743b_0_428
</a>
<p local-id="9fe58f996068">
 A critical part of human services work involves collecting information from external parties - the clients, families, foster parents, survivors, and other individuals whom our customers serve.
</p>
<p local-id="7e8b0d52ac06">
 While populating an Intake report or Case in Casebook, Frontline Workers must guide clients through populating a "virtual clipboard" of forms often including a demographic Person profile detailing their personal history and emergency contact information, and likely also a packet of forms requiring signatures such as privacy practices and consent forms.
</p>
<p local-id="311c05b5abdd">
 After an Intake report is screened in for services and converts to a Case, documentation does not end. Personal information must stay up-to-date and signatures/forms/attachments may be required regularly to keep everything moving forward and compliant.
</p>
<p local-id="3cc6b8639558">
 Today, external data collection in Casebook is fragmented across several mechanisms, each with meaningful limitations.
</p>
<h2 local-id="065e2701f011">
 How external data collection works today
</h2>
<table ac:local-id="4ad70931bd8c" data-layout="default" data-table-width="760">
 <tbody>
  <tr ac:local-id="2997884170b1">
   <th ac:local-id="a46cfa4b1476">
    <p local-id="ab9a7d7fdf5e">
     <strong>
      Persona(s) Engaged
     </strong>
    </p>
   </th>
   <th ac:local-id="218c677d69db">
    <p local-id="64b2f2cc2bca">
     <strong>
      Job(s) to be Done
     </strong>
    </p>
   </th>
  </tr>
  <tr ac:local-id="aeba9b2284b1">
   <td ac:local-id="838a61b54998">
    <p local-id="39b053747280">
     Frontline Worker / Case Manager
    </p>
   </td>
   <td ac:local-id="4a1b4da4c730">
    <p local-id="274573022015">
     Collect information from clients (demographics, documents, signed forms) without requiring in-person visits or paper-based workflows. Ensure that collected data flows into the Casebook record without redundant manual entry.
    </p>
   </td>
  </tr>
  <tr ac:local-id="61b6c60e0abb">
   <td ac:local-id="6dc05f25cc5f">
    <p local-id="d04e6cdcd14a">
     Supervisor / Program Manager
    </p>
   </td>
   <td ac:local-id="5eb54a0173d5">
    <p local-id="610101378723">
     Oversee the status of outstanding requests sent to clients. Ensure compliance with data collection requirements across active caseloads.
    </p>
   </td>
  </tr>
  <tr ac:local-id="d798af007d16">
   <td ac:local-id="4eb130cb1504">
    <p local-id="fede0b490854">
     External Client / Service Recipient
    </p>
   </td>
   <td ac:local-id="f049006ecd1d">
    <p local-id="6a242503d391">
     Receive, review, and complete forms or upload documents requested by the organization - on their own time, from any device, without needing specialized software or a full Casebook account.
    </p>
   </td>
  </tr>
  <tr ac:local-id="80e2085cce67">
   <td ac:local-id="2b8d5c6dfb6b">
    <p local-id="1e709e6eccdb">
     Administrator
    </p>
   </td>
   <td ac:local-id="ec8b40eb0e9d">
    <p local-id="8af3bb1f0b6a">
     Configure what information is collected from external clients, manage access controls, and ensure data security and compliance (e.g., HIPAA).
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h3 local-id="ec965735db44">
 <strong>
  External Tasks
 </strong>
</h3>
<p local-id="e918ea5eb795">
 Casebook supports a transactional workflow where staff can send a task to an external person (who does not have a Casebook account) via email. The recipient receives a verification code, clicks a link, and can either complete a
 <a href="http://Form.io">
  Form.io
 </a>
 form or upload an attachment. The completed form or file is saved back to the associated intake report or case.
</p>
<p local-id="39f44da6df5f">
 This flow was designed to be lightweight (no account creation, no persistent login) and it works well for one-off interactions. However, it is limited to a single task per email, offers no dashboard or history for the external user, and depends on
 <a href="http://Form.io">
  Form.io
 </a>
 for the form experience (with the data isolation issues that entails).
</p>
<h3 local-id="c2506311d504">
 <strong>
  Access (Provider Portal)
 </strong>
</h3>
<p local-id="0d13f773f5f2">
 Casebook also has an existing portal module, "Access", which invites external users to set up a persistent user account. Notably, Access was purpose-built for a narrow use case: foster care and adoption provider licensing applications.
</p>
<p local-id="c3c20569f976">
 Users with Access portal accounts can sign in with email and password, enabling richer interactions than the External Task flow. Data entered into Access flows into Track (Providers) upon approval by Staff users.
</p>
<p local-id="bc0a430f8ce2">
 Invited users who have set up Access portal accounts can sign in to a personal dashboard.
</p>
<h3 local-id="fe8e0857e336">
 <strong>
  Third-Party Forms via Zapier
 </strong>
</h3>
<p local-id="162fc1014fa4">
 Many customers have adopted a workaround pattern: they build external-facing forms in tools like Jotform or Google Forms, then use Zapier to pipe submission data into Casebook. This approach gives organizations full control over form design and distribution, but introduces its own challenges.
</p>
<p local-id="4e24bb27554b">
 Casebook's Zapier integration currently supports only three basic write actions (Create Person, Create Intake Report, Create Case) with no support for custom fields, line item groups, or sub-resources. Customers are left with incomplete records that require manual data entry to finish.
</p>
<p local-id="1cd65f63efad">
 See
 <ac:link>
  <ri:page ri:content-title="Integrations - Zapier improvements" ri:version-at-save="6">
  </ri:page>
  <ac:link-body>
   Integrations - Zapier improvements (Flow Digital)
  </ac:link-body>
 </ac:link>
 for more information.
</p>
<h3 local-id="6cba5b1ca3de">
 <a href="http://Form.io">
  <strong>
   Form.io
  </strong>
 </a>
 <strong>
  Integration
 </strong>
</h3>
<p local-id="9a93c0f0c58c">
 Casebook's integrated form engine is powered by
 <a href="http://Form.io">
  Form.io
 </a>
 , a third-party form builder.
 <a href="http://Form.io">
  Form.io
 </a>
 offers a feature-rich editor with support for custom field types, digital signatures, version control, and conditional logic.
</p>
<p local-id="117ff4b7e105">
 However,
 <a href="http://Form.io">
  Form.io
 </a>
 forms store their data in isolated JSON submissions that are not interoperable with Casebook's native database fields. This means that when a client fills out a
 <a href="http://Form.io">
  Form.io
 </a>
 form (whether through an External Task or otherwise) the data exists in a silo. Staff must manually transcribe information from
 <a href="http://Form.io">
  Form.io
 </a>
 submissions into the corresponding Casebook fields on a person, intake report, or case. This is one of the most persistent sources of frustration across the customer base.
</p>
<h1 local-id="9c5612b26a5a">
 Problems &amp; Impact
</h1>
<table ac:local-id="987962787ee3" data-layout="default" data-table-width="760">
 <colgroup>
  <col style="width: 49.0px;"/>
  <col style="width: 711.0px;"/>
 </colgroup>
 <tbody>
  <tr ac:local-id="d380bc89-8a65-46a5-b55c-b83a72bc638b">
   <th ac:local-id="85f86b7d-b15a-45b4-9e4b-dd545d26f394">
    <p local-id="9703b732ce44">
     <strong>
      ID
     </strong>
    </p>
   </th>
   <th ac:local-id="d3953a89-7b1b-4faa-9f2a-87411e9f514e">
    <p local-id="f9c24c38836b">
     <strong>
      Customer Problem Statement(s)
     </strong>
    </p>
   </th>
  </tr>
  <tr ac:local-id="1c5e1a9e-c3a5-4a24-b0b2-75dbf3d36487">
   <td ac:local-id="a51a3c0a-81c9-420a-9bce-22affd6bc792">
    <p local-id="6809769e16e3">
     1
    </p>
   </td>
   <td ac:local-id="be13f51a-d7d6-4a75-92fb-7cc505078611">
    <p local-id="d3e76d6c9b4b">
     As a Frontline Worker, I need to send multiple forms and document requests to a client at once so they can complete everything on their own time without managing separate emails and verification codes per task.
    </p>
   </td>
  </tr>
  <tr ac:local-id="7ae1e987-5b1b-453e-bf22-85885db054b0">
   <td ac:local-id="a91d171b-21e7-435e-8b82-8f427266a451">
    <p local-id="8c245f61f907">
     2
    </p>
   </td>
   <td ac:local-id="fb6dbc94-c8e9-44b9-bd80-47ba1fdc14f8">
    <p local-id="d06159a9e59a">
     As an External Client, I need a single place to see and complete everything my organization has asked of me so I don't lose track of tasks scattered across individual emails.
    </p>
   </td>
  </tr>
  <tr ac:local-id="9806a584-ba4e-48ef-a0fb-b4e736b01dbe">
   <td ac:local-id="bec899af-ceb1-4f97-9993-1d42bc1f612a">
    <p local-id="c9e1f6daaeb9">
     3
    </p>
   </td>
   <td ac:local-id="2b0ee248-c506-4642-bb95-b013423eecda">
    <p local-id="690f38ea5b17">
     As an Administrator, I need to invite any Person in Casebook to a persistent portal account so that recurring clients can access their work history and new tasks without re-verifying their identity each time.
    </p>
   </td>
  </tr>
  <tr ac:local-id="95ee0e3b-0c8f-4ac3-88c3-916d5ac8acc2">
   <td ac:local-id="87d1ae43-3625-4fd4-910e-d4b9b9470865">
    <p local-id="88610d3c7940">
     4
    </p>
   </td>
   <td ac:local-id="11effadf-1945-4dc0-9517-b6784bbae134">
    <p local-id="ad3b0f1b4cd1">
     As a Supervisor, I need visibility into which clients have outstanding tasks so I can ensure compliance without fielding individual status inquiries from staff.
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h2 local-id="6ac4e4386a9b">
 External tasks come up short for collaborative data collection
</h2>
<p local-id="5f026cbb40df">
 Today, Casebook offers External Tasks to facilitate most collaborative data collection interactions. External Tasks are an excellent fit for sporadic or one-time requests in situations where a persistent user account is not required.
</p>
<p local-id="94c22c1e39c7">
 However no accounts = no client view or self-service collaboration. For organizations managing hundreds of active clients, this lack of visibility compounds significantly.
</p>
<p local-id="e6dad55c04c3">
 <strong>
  Key challenges
 </strong>
</p>
<ul local-id="11f3af99d446">
 <li local-id="a86d05b373ab">
  <p local-id="e37318474c38">
   When a staff member sends multiple tasks to the same client (a form to fill out, a document to upload, and another form next week) each arrives as a separate email with a separate verification code
  </p>
 </li>
 <li local-id="0d93f891cbcb">
  <p local-id="2a65ee45c6d1">
   Clients have no dashboard, no history, and no way to see what they've already completed or what's still pending - just the emailed magic links
  </p>
 </li>
 <li local-id="f96b059fc018">
  <p local-id="92d10fc1c7bd">
   This flow is prone to confusion and could increase the support burden on staff who must field status inquiries
  </p>
 </li>
</ul>
<h2 local-id="f8f14c18690f">
 Data entered via external form tasks exists in a silo
</h2>
<p local-id="93bcf0c00699">
 Data isolation in Casebook Forms is a significant driver of customer requests for bidirectional data syncing in Casebook, which contributes to the motivation for the Casebook Form Engine initiative. See
 <ac:link>
  <ri:page ri:content-title="Forms 2.0 - High-Level PRD" ri:version-at-save="2">
  </ri:page>
  <ac:link-body>
   Forms 2.0 PRD
  </ac:link-body>
 </ac:link>
 for more information.
</p>
<p local-id="866fe2a0df1f">
 In the meantime, customers currently must live with the reality that external "Form tasks" do not flow into Casebook records and that this sometimes requires double data entry
</p>
<p local-id="0c045da3a367">
 <strong>
  Key challenges:
 </strong>
</p>
<ul local-id="29d5a6ba5348">
 <li local-id="db1bf1a6ce82">
  <p local-id="b5f66894e5a3">
   Siloed Forms data works fine for compliance but is limited in many of the same ways as paper records
  </p>
 </li>
 <li local-id="9509f1c4f31a">
  <p local-id="286d33c83ee0">
   Data can be been collected, organized into a record, and used in Reporting but submissions do not update any corresponding person, case, or intake report fields in Casebook
  </p>
 </li>
 <li local-id="d88cf87573e8">
  <p local-id="482c7607cd93">
   In those situations where information gathered should update corresponding person, case, or intake report fields, Staff must visually compare form submissions to Casebook records and manually re-enter dat
  </p>
 </li>
</ul>
<h2 local-id="d803f3fddca8">
 Delegated access shouldn’t require workarounds
</h2>
<p local-id="84028c131986">
 Parents and guardians need to be able to work on behalf of the people they are responsible for. A head of household managing a case involving their children, for example, needs to see and act on tasks, forms, and documents assigned to those dependents, not just their own.
</p>
<p local-id="1255957a0113">
 While a true hierarchical delegated access solution with full permission controls is a longer-term vision, even an MVP Client Portal must account for this reality. Without delegated access, organizations will be forced to either create workaround accounts or revert to staff-mediated workflows for multi-person households, undermining the self-service value of the portal.
</p>
<h2 local-id="9ca605bf95f0">
 Casebook Access is too narrow to serve as a general-purpose Client Portal
</h2>
<p local-id="f259d37e6266">
 Although Access allows potential foster parents to submit their own person profile data, and submit tasks, it's a completely unique "Provider Portal" use case from the "People Portal" discussed here.
</p>
<p local-id="4603e36e33a1">
 Access demonstrated the viability of giving external users a persistent, login-based experience with Casebook - but its architecture is deeply tied to provider licensing workflows (specifically foster care and adoption applications), making it impractical to extend to the broader set of client-facing use cases that customers need.
</p>
<h2 local-id="c87422275652">
 Zapier helps but doesn't serve as a Portal
</h2>
<p local-id="53c06bac581c">
 Casebook is simultaneously investing in improving its Zapier integration (expanded write actions, custom field support, line item groups). There is meaningful overlap in the outcome these two initiatives serve (getting external data into Casebook) even though the actors and channels differ (Zapier: system-to-system; Portal: person-to-system).
</p>
<h1 local-id="8cf6e38830bc">
 Solution Concept
</h1>
<h2 local-id="2322469b7701">
 Vision statement
</h2>
<p local-id="7f990667ce2f">
 <strong>
  Self-service portal
 </strong>
</p>
<p local-id="36277b8205d5">
 Client Portal should serve as a hub for ongoing client engagement through intake and service delivery. Clients should be able to populate their profile(s), easily submit requested forms/upload requested attachments, and access their submission history with the organization. Self-service person profiles is a major step towards a more native and less siloed Forms experience, which should result in more complete person profiles populated in Casebook directly without extra work for Staff users.
</p>
<p local-id="735690d988f7">
 In the long term, prospective clients should be able to self-refer and submit eligibility information without staff first creating a record in Casebook. This vision lowers the barrier to entry for reaching out for support and may reduce time-to-first-contact.
</p>
<h2 local-id="0bc5981b07ec">
 MVP
</h2>
<h3 local-id="8fd2c7c3da5e">
 <strong>
  Staff can invite any Person to set up an account with email/password
 </strong>
</h3>
<p local-id="ef244ae0f262">
 Persistent accounts won't just be for Provider People anymore - any Person in Casebook Engage, Intake, People, or Track can be invited to create an account using email and password.
</p>
<h3 local-id="eb543155fd1b">
 <strong>
  Clients can sign in to a "Client" Dashboard for all People in their family or care
 </strong>
</h3>
<p local-id="13986d28975a">
 This MVP introduces a lightweight, "Home"-based dashboard where external clients can sign in to view and complete form tasks and document uploads assigned to them. Clients can also view completed submissions (forms they've submitted, files they've uploaded).
</p>
<p local-id="80ef70daec22">
 Parents, guardians, or any user with delegated access to multiple People will see a unified dashboard of work across all delegated profiles. Staff can easily delegate access to a Person via the Casebook Relationships module.
</p>
<h3 local-id="8fe0f4ac5f0f">
 <strong>
  Introducing self-service person profiles
 </strong>
</h3>
<p local-id="91641b27c03c">
 Clients can help populate richer person profiles to speed up intake. When the client completes new information, the submission writes directly to native Casebook fields on the person record via Dynamic Pages. This self-service person profile flow will be the second form that bypasses the
 <a href="http://Form.io">
  Form.io
 </a>
 data silo directly to the Casebook database, only behind Access's provider application flow.
</p>
<h3 local-id="6c06a4869fe3">
 <strong>
  Only auth changes for External
 </strong>
 <a href="http://Form.io">
  <strong>
   Form.io
  </strong>
 </a>
 <strong>
  and attachment upload tasks
 </strong>
</h3>
<p local-id="db01abc14353">
 No change to the workflow for external tasks - just sign in with your email/password instead of providing a code.
</p>
<p local-id="b5986e95dc58">
 From a Case or Intake Report, a staff member still creates a form task the same way by selecting a Person. Custom
 <a href="http://Form.io">
  Form.io
 </a>
 forms continue to work as they do today with External Tasks. Submissions are stored as JSON. The data isolation tradeoff is accepted for MVP.
</p>
<p local-id="46cafa9d981d">
 Clients can upload files directly from the dashboard. Uploads attach to the relevant intake report, case, or person record in Casebook.
</p>
<h2 local-id="c4f298ccdb0a">
 In scope
</h2>
<ul local-id="653fefd4ab66">
 <li local-id="9d3a29775102">
  <p local-id="269c1f996b4c">
   Invite to Portal action for People surfaces in Engage, Intake, People, and Track
  </p>
 </li>
 <li local-id="3fb8f4bec7e2">
  <p local-id="7418bc18256d">
   Persistent auth for any portal account
  </p>
 </li>
 <li local-id="673f05318d2c">
  <p local-id="1518bfa7e5ee">
   Delegated access via Relationships module in Engage, Intake, and People
  </p>
 </li>
 <li local-id="b3edb98bc695">
  <p local-id="c1069811da85">
   Dashboard showing pending tasks and submission history (forms submitted, attachments uploaded) across all delegated person records
  </p>
 </li>
 <li local-id="923396b3b656">
  <p local-id="82d0016290ac">
   Admin-configurable self-service person profiles via Dynamic Pages
  </p>
 </li>
 <li local-id="c64a91dd6d37">
  <p local-id="daff184141cc">
   Self-service person profiles remain editable across all delegated person records
  </p>
 </li>
 <li local-id="661bcb69ce50">
  <p local-id="95484b4c9972">
   Maintain existing
   <a href="http://Form.io">
    Form.io
   </a>
   and attachment upload tasks
  </p>
 </li>
 <li local-id="3a3ec4121d62">
  <p local-id="9b6bd2a7ac9d">
   English (US and CA) and Spanish (US) localization
  </p>
 </li>
 <li local-id="f6433cd41249">
  <p local-id="e0020f180af6">
   Screen reader accessibility (WCAG 2.1 AA)
  </p>
 </li>
 <li local-id="fedc81a61006">
  <p local-id="4a582328ac07">
   Portal access gated by subscription entitlement; invite action surfaces only for tenants with the portal entitlement active
  </p>
 </li>
</ul>
<h2 local-id="2b56d3b75655">
 Post-MVP
</h2>
<ul local-id="2d4fbb4dc2da">
 <li local-id="9283409fe6bf">
  <p local-id="ecab961bf6c1">
   <strong>
    Tenant branding
   </strong>
   - MVP ships with Casebook branding. Logo, color scheme, and display name customization come in a subsequent release.
  </p>
 </li>
 <li local-id="6f5b0d4bcff6">
  <p local-id="225c9e39785c">
   <strong>
    Household/delegated access
   </strong>
   - MVP uses contact info matching to surface tasks across person records. Explicit guardian delegation controls and per-dependent permissions are post-MVP.
  </p>
 </li>
 <li local-id="0526c322c8ad">
  <p local-id="ad1b66e8ff57">
   <strong>
    Anonymous intake / self-referral
   </strong>
   - Public-facing embeddable forms with QR codes for prospective clients who don't yet exist in Casebook.
  </p>
 </li>
 <li local-id="19cdec1c8aa4">
  <p local-id="33641e2aa7d5">
   <strong>
    Profile change review workflow
   </strong>
   - Staff approval step for client-initiated profile edits.
  </p>
 </li>
 <li local-id="f325de815ece">
  <p local-id="f69f65c47ccc">
   <strong>
    Intake packets
   </strong>
   - Bundled sets of forms triggered by workflow rules (e.g., new intake report triggers 14 forms at once). This belongs to Casebook Workflows, not this project.
  </p>
 </li>
 <li local-id="eb53800d95c8">
  <p local-id="0bd03e468a81">
   <strong>
    Scheduling and calendar integration
   </strong>
   - Underlying calendar infrastructure needs further investment first.
  </p>
 </li>
 <li local-id="4341c4e20677">
  <p local-id="014479b59c7d">
   <strong>
    Communication / messaging
   </strong>
   - On-ramp to SMS and email syncing features, both of which need additional work before they're portal-ready.
  </p>
 </li>
 <li local-id="0042b01601df">
  <p local-id="67ba0c92a65d">
   <strong>
    Provider portal
   </strong>
   - Access (provider licensing) is a separate domain, out of scope.
  </p>
 </li>
 <li local-id="084bb4a15280">
  <p local-id="2e617b0bfdc7">
   <strong>
    Additional Dynamic Pages forms
   </strong>
   - Only personDetails is exposed externally at launch.
  </p>
 </li>
 <li local-id="01fb39d9db85">
  <p local-id="1d57855fd6dc">
   <strong>
    Custom subdomains and email template customization
   </strong>
  </p>
 </li>
 <li local-id="f2c7e1ea0ad1">
  <p local-id="a76676eb3cdb">
   <strong>
    Native Casebook Form Engine migration
   </strong>
   -
   <a href="http://Form.io">
    Form.io
   </a>
   forms migrate to Dynamic Pages as the Form Engine matures.
  </p>
 </li>
 <li local-id="fce1cd774967">
  <p local-id="1a188c84492d">
   <strong>
    2FA cleanup for External Tasks
   </strong>
   - the verification code currently arrives in the same email as the magic link, providing no meaningful second-factor protection. Fix: decouple them so the code is sent as a separate follow-up after the user clicks through. Stretch: SMS delivery of External Task invitations and magic links.
  </p>
 </li>
 <li local-id="f29c565a79e5">
  <p local-id="2a2688247412">
   <strong>
    Portal admin controls
   </strong>
   - self-service admin UI for managing portal invitations and entitlements per tenant. Backend entitlement enforcement is in scope for MVP; the admin management experience is post-MVP.
  </p>
 </li>
</ul>
<h1 local-id="e3c0cab29fbe">
 Implementation Details
</h1>
<h2 local-id="3a51743a7c54">
 Authentication
</h2>
<p local-id="87c2c88bf849">
 The Client Portal builds on Casebook's existing two-track external access model. Both tracks coexist at different subscription tiers.
</p>
<h3 local-id="11db0debe32c">
 <strong>
  Track 1: External Tasks (non-persistent)
 </strong>
</h3>
<p local-id="0a6ffcdf7986">
 A Person receives an email with a magic link to a single task, gated by a verification code as a second factor. After completing the task, the session ends. No dashboard, no history. Available at all subscription tiers.
</p>
<h3 local-id="3aa7bf8785ba">
 <strong>
  Track 2: Portal Users (persistent)
 </strong>
</h3>
<p local-id="14759273fab1">
 An entitlement available at qualifying subscription tiers. Staff can invite any Person in Casebook to set up a portal account with email and password. Once established, the portal provides a persistent session with a full task dashboard, submission history, and self-service person profile. Uses the same AWS Cognito user pool as existing Provider portal users and internal staff, with persona attributes determining which dashboard is rendered.
</p>
<h2 local-id="b214d412fadc">
 <strong>
  Notification routing
 </strong>
</h2>
<p local-id="f0d265582a17">
 When a task is assigned to a Person, delivery is determined by their auth status:
</p>
<ul local-id="fe50b70e4a71">
 <li local-id="62048d7f29f0">
  <p local-id="15149162b5d6">
   Person has a portal account - notification directs them to sign in to their dashboard. No per-task verification code.
  </p>
 </li>
 <li local-id="d262662ac892">
  <p local-id="45ebbfd26e60">
   Person does not have a portal account - existing External Tasks flow (magic link + separate verification code).
  </p>
 </li>
</ul>
<p local-id="dfeaae4f23c3">
 Staff do not need to manage this routing. The task assignment workflow is identical regardless of which track the recipient is on.
</p>
<h2 local-id="ffec69eaf2b2">
 <strong>
  Dashboard architecture
 </strong>
</h2>
<p local-id="ccf15b883ce6">
 New Client dashboard coexists with Staff dashboard within
 <code>
  cbp-home-web
 </code>
 :
</p>
<ul local-id="9fe340a1ec03">
 <li local-id="05e8c339a912">
  <p local-id="6fac5f21a6f1">
   Casebook User - staff (unchanged)
  </p>
 </li>
 <li local-id="c56f8edcf2e8">
  <p local-id="5285dc2cb77e">
   Casebook Person - Client - new view for non-Provider People with portal access
  </p>
 </li>
</ul>
<p local-id="c73d4fee627d">
 Existing Provider dashboard continues to live within
 <code>
  cbp-access-web
 </code>
 :
</p>
<ul local-id="d7ef3973bb08">
 <li local-id="3ae7cb231758">
  <p local-id="4b4f970e1c77">
   Casebook Person - Provider - existing provider portal, quarantined during this initiative to prevent regression
  </p>
 </li>
</ul>
<h2 local-id="6b8d104ef09d">
 <strong>
  Hypothesis(es) &amp; Outcomes
 </strong>
</h2>
<h3 local-id="38005831332a">
 Hypotheses
</h3>
<p local-id="1aa6c0618eef">
 <em>
  To be completed.
 </em>
</p>
<h3 local-id="7c974e13e98a">
 Outcomes
</h3>
<table ac:local-id="95176b2e740c" data-layout="default" data-table-width="760">
 <tbody>
  <tr ac:local-id="3620258ba6f4">
   <th ac:local-id="103bfcd03608">
    <p local-id="5c7641711e55">
     <strong>
      Company OKR
     </strong>
    </p>
   </th>
   <th ac:local-id="f5737e282c18">
    <p local-id="0106fa8f8219">
     <strong>
      Yearly OKR
     </strong>
    </p>
   </th>
   <th ac:local-id="3eb9343f9b13">
    <p local-id="bce9e94a1e18">
     <strong>
      Quarterly OKR
     </strong>
    </p>
   </th>
   <th ac:local-id="c7bd4cafb277">
    <p local-id="e80eab23f617">
     <strong>
      Linkage Logic
     </strong>
    </p>
   </th>
  </tr>
  <tr ac:local-id="602d8c744289">
   <td ac:local-id="3a5bfb9adc23">
    <p local-id="fcae4f143dd4">
     Objective:
    </p>
   </td>
   <td ac:local-id="c0e1730758f6">
    <p local-id="acccb8799748">
     Objective:
    </p>
   </td>
   <td ac:local-id="88683f52dcc1">
    <p local-id="a7f0f024f800">
     Objective:
    </p>
   </td>
   <td ac:local-id="6cbe818a2605">
    <p local-id="8a9d0bcab4c7">
    </p>
   </td>
  </tr>
  <tr ac:local-id="70b301fa3d7d">
   <td ac:local-id="e794daaa82ba">
    <p local-id="5eed95bca467">
     Key Result:
    </p>
   </td>
   <td ac:local-id="5568a676c591">
    <p local-id="bbbbf59d4219">
     Key Result:
    </p>
   </td>
   <td ac:local-id="59ac97d2c9c2">
    <p local-id="91a3377e7cfa">
     Key Result:
    </p>
   </td>
   <td ac:local-id="343c57dc87a6">
    <p local-id="8e2189655301">
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h2 local-id="b99c2e94707e">
 <strong>
  Customer Value Proposition
 </strong>
</h2>
<p local-id="cd081d4fb321">
 <em>
  To be completed in partnership with Product Marketing.
 </em>
</p>
<h2 local-id="bd2b449447cd">
 <strong>
  Scope &amp; Preliminary Estimate
 </strong>
</h2>
<table ac:local-id="3140d27a18cb" data-layout="default" data-table-width="760">
 <tbody>
  <tr ac:local-id="f7ca4c0b7f26">
   <th ac:local-id="41836d589b5a">
    <p local-id="035621f89c06">
     <strong>
      What's In?
     </strong>
    </p>
   </th>
   <th ac:local-id="b289829c62d8">
    <p local-id="88c8e858b426">
     <strong>
      Design Estimate
     </strong>
    </p>
   </th>
   <th ac:local-id="b725777dd8ee">
    <p local-id="9f8c61253149">
     <strong>
      Dev Estimate
     </strong>
    </p>
   </th>
   <th ac:local-id="48dcc5b1fb39">
    <p local-id="b590bb20723a">
     <strong>
      QA Estimate
     </strong>
    </p>
   </th>
  </tr>
  <tr ac:local-id="bf4850021c5e">
   <td ac:local-id="db805263ff43">
    <p local-id="515ee103a3a6">
    </p>
   </td>
   <td ac:local-id="eb80e0936afe">
    <p local-id="364c78010b41">
    </p>
   </td>
   <td ac:local-id="3fd099384f8c">
    <p local-id="713a40f7d031">
    </p>
   </td>
   <td ac:local-id="7ee32a518b9e">
    <p local-id="01dea72f3654">
    </p>
   </td>
  </tr>
 </tbody>
</table>
<table ac:local-id="7048da312191" data-layout="default" data-table-width="760">
 <tbody>
  <tr ac:local-id="ab0ff91a7d29">
   <th ac:local-id="dea496397d2b">
    <p local-id="30581804f36e">
     <strong>
      What's Out?
     </strong>
    </p>
   </th>
   <th ac:local-id="25fdc670c159">
    <p local-id="51a9a146474a">
     <strong>
      Why?
     </strong>
    </p>
   </th>
  </tr>
  <tr ac:local-id="a20c95f10069">
   <td ac:local-id="f192ef6bb8f3">
    <p local-id="9ab962e87470">
    </p>
   </td>
   <td ac:local-id="ec066430d094">
    <p local-id="8d0b9e3e93b1">
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h2 local-id="0fb87a3a82ee">
 <strong>
  Dependencies
 </strong>
</h2>
<table ac:local-id="2f05c42bdf50" data-layout="default" data-table-width="760">
 <tbody>
  <tr ac:local-id="33d8b46a80bc">
   <th ac:local-id="a35c873517b6">
    <p local-id="85eec2916f9b">
     <strong>
      Team
     </strong>
    </p>
   </th>
   <th ac:local-id="de1fe24fc9a3">
    <p local-id="cf83f647e948">
     <strong>
      What's Need From Them?
     </strong>
    </p>
   </th>
  </tr>
  <tr ac:local-id="ef4e11f589e4">
   <td ac:local-id="371ea33e809a">
    <p local-id="eaa1ac255f24">
    </p>
   </td>
   <td ac:local-id="e180e9fdb1c5">
    <p local-id="d6df65759a55">
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h2 local-id="2a53c0234119">
 <strong>
  Risk(s) &amp; Mitigation Plan(s)
 </strong>
</h2>
<table ac:local-id="4791336f6826" data-layout="default" data-table-width="760">
 <tbody>
  <tr ac:local-id="1275778f08c9">
   <th ac:local-id="c56e3e65e824">
    <p local-id="52ebc676fdb1">
     <strong>
      Risk
     </strong>
    </p>
   </th>
   <th ac:local-id="794b5c7a9671">
    <p local-id="b1d7deca52c3">
     <strong>
      Mitigation / Contingency Plan
     </strong>
    </p>
   </th>
  </tr>
  <tr ac:local-id="4ba583953de4">
   <td ac:local-id="2825ac2d5415">
    <p local-id="085a94f0f3d0">
    </p>
   </td>
   <td ac:local-id="4ce5a991610f">
    <p local-id="41569115736e">
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h1 local-id="80456f28f07a">
 Market Analysis
</h1>
<h2 local-id="01ac33a27f1a">
 Competitive Intelligence
</h2>
<h3 local-id="b4000ca9c49e">
 ClientTrack by CaseWorthy
</h3>
<p local-id="606fff7fa8bd">
 The one to watch. CaseWorthy acquired Eccovia (Feb 2025) and unified both products into a single platform. Portal supports self-registration, screening, configurable forms via apBuilder, scheduling, and service enrollment. Portal data writes directly to native records. Opportunities: unclear reporting, weak API connectivity, and active platform consolidation may create instability.
</p>
<h3 local-id="7cb0c8ea1382">
 Bonterra Connect (Apricot) and ClientConnect
</h3>
<p local-id="594300d7be24">
 Two disparate portals under one parent company. Connect is web-based for intake forms, appointment scheduling, and submission history. Also a hub for SMS blasts and reminders. ClientConnect is mobile-first for documentation, appointments, and payments. Opportunities: neither supports document uploads, no household access, email required for registration, and Connect is gated behind "contact for pricing" Pro tier.
</p>
<p local-id="ef880b38e37f">
 <strong>
  Prospect signal:
 </strong>
 One prospect currently using Bonterra shared:
 <em>
  "We have started to use some of our current system's features to allow the participants that we work with to complete intake on their own. [Bonterra] has something called Connect, a participant portal, trying to reduce some of the intake burden on staff... I just think our organization is trying to just go more digital when it comes to file management, and not sure that our current system is the most modern way to do that."
 </em>
</p>
<h3 local-id="573d6df9becf">
 CareDirector
</h3>
<p local-id="5d132eeea770">
 Provider portal with document uploads, authorization views, and agency communication. Updates trigger workflows that route review tasks to record owners. Configurable role-based access controls what providers can view or edit. Opportunities: provider-focused (not client/participant-facing), no public self-referral pathway, and limited presence in the US nonprofit market.
</p>
<h3 local-id="d150e4c89d58">
 Social Solutions ETO
</h3>
<p local-id="ddce62e66ca2">
 Public-facing portal (web + mobile) for applying to services, updating personal info, reviewing past participation, and receiving agency updates. Supports e-signatures and configurable alerts. Opportunities: acquired by Bonterra and being consolidated, aging UX, and historically complex implementation and training requirements.
</p>
<h2 local-id="e8814ab4253e">
 Cost vs. ROI Analysis
</h2>
<p local-id="e3505bf2656e">
 <em>
  To be completed.
 </em>
</p>
<h1 local-id="175b86a1c41e">
 Requirements
</h1>
<h2 local-id="4273f2a03476">
 User Stories/Acceptance Criteria
</h2>
<table ac:local-id="809ba9ce86ff" data-layout="default" data-table-width="760">
 <tbody>
  <tr ac:local-id="6aabaf9b329e">
   <th ac:local-id="950d3db532d8">
    <p local-id="f19041de5c44">
     <strong>
      ID
     </strong>
    </p>
   </th>
   <th ac:local-id="ab33d1740dcf">
    <p local-id="4aef16765338">
     <strong>
      Short Title
     </strong>
    </p>
   </th>
   <th ac:local-id="fa4e6b26c26f">
    <p local-id="0cb000dfcefb">
     <strong>
      Story
     </strong>
    </p>
   </th>
   <th ac:local-id="e49e2c85a5b0">
    <p local-id="e167c7dba978">
     <strong>
      Acceptance Criteria
     </strong>
    </p>
   </th>
   <th ac:local-id="5a76d8867c9c">
    <p local-id="b514ed29b9a2">
     <strong>
      JIRA Link
     </strong>
    </p>
   </th>
  </tr>
  <tr ac:local-id="526885317b6c">
   <td ac:local-id="4f55dbe4c4f1">
    <p local-id="8991910c1b12">
    </p>
   </td>
   <td ac:local-id="4927326d2488">
    <p local-id="6ac7a83d42a5">
    </p>
   </td>
   <td ac:local-id="ba5013ad9f15">
    <p local-id="4bbed1dec4eb">
    </p>
   </td>
   <td ac:local-id="f9d528a63764">
    <p local-id="994f72a45b07">
    </p>
   </td>
   <td ac:local-id="5a94c2002e1a">
    <p local-id="4c2854f36155">
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h2 local-id="b192a45dd166">
 Non-Functional Requirements
</h2>
<table ac:local-id="4e0ec6d44156" data-layout="default" data-table-width="760">
 <tbody>
  <tr ac:local-id="ed7c0aded70e">
   <th ac:local-id="4450a74ac0f6">
    <p local-id="e9b6045d2f74">
     <strong>
      ID
     </strong>
    </p>
   </th>
   <th ac:local-id="88cda807eb08">
    <p local-id="e4eff7804d3a">
     <strong>
      Short Title
     </strong>
    </p>
   </th>
   <th ac:local-id="7cf09b7b4847">
    <p local-id="d9114618d1fc">
     <strong>
      Requirement
     </strong>
    </p>
   </th>
   <th ac:local-id="96f7a39b7b71">
    <p local-id="79e1282c3375">
     <strong>
      JIRA Link
     </strong>
    </p>
   </th>
  </tr>
  <tr ac:local-id="5867a3f67631">
   <td ac:local-id="889ac4100653">
    <p local-id="966c2b0e8ac0">
     NF.1
    </p>
   </td>
   <td ac:local-id="eaee500f05c0">
    <p local-id="ef77f53f4c5d">
     Events - reporting
    </p>
   </td>
   <td ac:local-id="ae0b954f8699">
    <p local-id="831fc3b50957">
     The following events should be recorded and logged for reporting purposes:
    </p>
   </td>
   <td ac:local-id="f72d7214fd56">
    <p local-id="557bf7934182">
    </p>
   </td>
  </tr>
  <tr ac:local-id="00d4c75189f9">
   <td ac:local-id="0e08b81b9c45">
    <p local-id="200b82de9961">
     NF.2
    </p>
   </td>
   <td ac:local-id="addce3a0da49">
    <p local-id="4374130db142">
     Events - audit log
    </p>
   </td>
   <td ac:local-id="071ba9f6f8cf">
    <p local-id="fef67c795204">
     The following events should be recorded so they appear in audit log reporting:
    </p>
   </td>
   <td ac:local-id="b3aa87c1072e">
    <p local-id="52b083df5ad6">
    </p>
   </td>
  </tr>
  <tr ac:local-id="11e316b928eb">
   <td ac:local-id="d1da47a994d9">
    <p local-id="a88406bc3554">
     NF.3
    </p>
   </td>
   <td ac:local-id="5739b7c926bc">
    <p local-id="727e31b01f57">
     Events - documentation
    </p>
   </td>
   <td ac:local-id="ba81d825c31a">
    <p local-id="678a51379ec1">
     Any updates to events should be documented in our Confluence repo illustrating our list/explanation of supported events.
    </p>
   </td>
   <td ac:local-id="337f9189216e">
    <p local-id="7a8b5f56cf63">
    </p>
   </td>
  </tr>
  <tr ac:local-id="096781945c5a">
   <td ac:local-id="65bb6ef2bf16">
    <p local-id="6310a202a8a3">
     NF.4
    </p>
   </td>
   <td ac:local-id="96fa2fd171b4">
    <p local-id="2769600e69c8">
     Performance
    </p>
   </td>
   <td ac:local-id="bbc5fde53ebf">
    <p local-id="86000ce6ddb6">
    </p>
   </td>
   <td ac:local-id="87885de50cfe">
    <p local-id="945f8a8906d6">
    </p>
   </td>
  </tr>
  <tr ac:local-id="5d32ac9414d2">
   <td ac:local-id="ad6269a7020f">
    <p local-id="98cd6f6c33fd">
     NF.5
    </p>
   </td>
   <td ac:local-id="18f598598824">
    <p local-id="996f48983ad9">
     Migration Script Runtime
    </p>
   </td>
   <td ac:local-id="e021c5e984d8">
    <p local-id="ef66a43c3785">
     Need a requirement around max length run-time for any work that requires migration scripts to run.
    </p>
   </td>
   <td ac:local-id="20d1bfa59f27">
    <p local-id="34e6f0edb5ff">
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h2 local-id="3d2deb0a91ed">
 Special UI Requirements
</h2>
<table ac:local-id="a0ddc207b337" data-layout="default" data-table-width="760">
 <tbody>
  <tr ac:local-id="f2c3f1aa4019">
   <th ac:local-id="efa4906d24de">
    <p local-id="f8c119dcb995">
     <strong>
      ID
     </strong>
    </p>
   </th>
   <th ac:local-id="528c8294684e">
    <p local-id="6cc737111c2f">
     <strong>
      Short Title
     </strong>
    </p>
   </th>
   <th ac:local-id="20ad56ce43fc">
    <p local-id="fe3efe2f2fff">
     <strong>
      Condition
     </strong>
    </p>
   </th>
   <th ac:local-id="e290b3124492">
    <p local-id="f21b8add7cb3">
     <strong>
      UI Details - Text Message, Banners, etc.
     </strong>
    </p>
   </th>
   <th ac:local-id="7216079c8ea1">
    <p local-id="362e8bf94026">
     <strong>
      JIRA Link
     </strong>
    </p>
   </th>
  </tr>
  <tr ac:local-id="0067c30ba28a">
   <td ac:local-id="0513df21928b">
    <p local-id="a5545359755f">
    </p>
   </td>
   <td ac:local-id="c72e319a69ef">
    <p local-id="ee1fcd7356e7">
    </p>
   </td>
   <td ac:local-id="5cc832d14d12">
    <p local-id="bba5adaeefb0">
    </p>
   </td>
   <td ac:local-id="0ceefa3bef90">
    <p local-id="0fae9fe2958a">
    </p>
   </td>
   <td ac:local-id="aab6a2341343">
    <p local-id="b517a96097f2">
    </p>
   </td>
  </tr>
 </tbody>
</table>
<h1 local-id="b51094730774">
 Design
</h1>
<h2 local-id="1ef25d1cbe1d">
 User Research &amp; Usability Test Insights
</h2>
<p local-id="9122d7099cdd">
 <em>
  To be completed.
 </em>
</p>
<h2 local-id="a52c81e61f4f">
 User Flow Diagrams &amp; Mock-ups
</h2>
<p local-id="a0126f1f4588">
 <em>
  To be completed.
 </em>
</p>

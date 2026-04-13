# Nylas Upgrade - UX Improvements

- **GID:** 1208822133040792
- **Permalink:** https://app.asana.com/1/1123317448830974/project/1208822133040792
- **Team:** N/A
- **Stage:** Study
- **Status:** on_hold
- **Jira Link:** N/A

## Current Status Update
**Title:** Reviewed v3 diff - no low-hanging fruit, but a few new interesting features to consider
**Text:**
Completed a review of v3 diff and existing Nylas features that we have not leveraged

https://developer.nylas.com/docs/v2/upgrade-to-v3/diff-view/#terminology-changes-in-v3

A few interesting new features which would require additional dev:

Email
    New webhook event for emails message.opened could be used to indicate that an internal user had seen a message

Calendars
    Check a calendar for free/busy status
    Each grant can now have up to 10 virtual calendars + Added the option to specify a primary calendar
    ”You can now send drafts” - save?
    You can schedule a send time for a message, and edit or delete scheduled send times. - The new message.send_success and message.send_failed notifications allow you to track the results of a scheduled send
    The new message.bounce_detected notification is available to check for message bounces from Google, Microsoft Graph, iCloud, and Yahoo.
    You can now soft-delete messages and threads

Also discussed Nylas’ scheduling tools which could address some user requests - after chatting with @Jordan Jan and Allie, it seems that this integration would be a heavy lift and wouldn’t qualify for low-hanging fruit
    https://developer.nylas.com/docs/v3/calendar/group-booking/


## Custom Fields
- **Priority:** null
- **Team:** Platform
- **Stage:** Study
- **Discovery Start:** 2024-11-18T00:00:00.000Z
- **Release Quarter:** N/A
- **Type:** Strategic


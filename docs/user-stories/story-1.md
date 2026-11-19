User story: A shared view of existing inbound items
===================================================

**As a** council officer (request handler), **I want** to see every inbound item that has arrived in one shared list, **so that** I can spot possible FOI requests the same day they arrive, across multiple platforms: email, phone, portal, web form, etc.

Acceptance criteria:
--------------------

**Single list:** GIVEN I'm signed in, WHEN I open the inbound page, THEN I see all items from the loaded data in one list. The 8 sample items all appear, including bin queries, invoices and the phone note.

**Row content:** GIVEN I'm viewing the list, WHEN I look at any row, THEN I see its reference, received date, channel, sender, subject and a short message preview.

**Messy dates:** GIVEN items were received with different date formats, WHEN I view the list, THEN every parseable date is shown in one consistent format.

**Unparseable dates:** GIVEN an item has a received date that can't be parsed (e.g.  `22/9 `, which has no year), WHEN I view the list, THEN the row shows "Date unknown" with an urgent marker, and the system does not guess a date.

**Shared view:** GIVEN two different officers are signed in, WHEN each opens the inbound page, THEN both see the same items, with no per-user inboxes and no admin/non-admin difference.

**Empty state:** GIVEN there are no items in the database, WHEN I open the inbound page, THEN the page tells me there are no items.

**Error state:** GIVEN the list fails to load, WHEN I open the inbound page, THEN I see an error message and not an empty list that looks like nothing has arrived.

**Missing fields:** GIVEN an item has a blank sender or subject (e.g. PH-0093, WF-1187), WHEN it appears in the list, THEN the blank field shows "-" and the row displays normally.
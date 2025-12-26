# ChangeGuard User Flows (v1)

This document describes the main user flows in ChangeGuard v1.

---

## 1. Register & Login

1. User visits the app and clicks “Register” or “Login”.
2. Enters email, password, and name (register only).
3. On success, user is redirected to the dashboard.

---

## 2. Creating a Schema Change

1. Click “New Schema Change”.
2. Fill in name, description, change type, affected services.
3. Submit → backend validates and creates record.
4. Notification(s) sent to affected users.
5. Schema change appears in dashboard.

---

## 3. Commenting on a Schema Change

1. Open schema change detail page.
2. Type comment in input box.
3. Submit → backend stores comment.
4. Notifications sent to relevant users.
5. Comment added to thread in real-time.

---

## 4. Viewing & Resolving Schema Changes

1. Open dashboard → see list of schema changes.
2. Filter by status or service.
3. Click schema change → view details.
4. If issue resolved, click “Mark Resolved” → backend updates status.
5. Notifications sent to all stakeholders.

---

## 5. Notifications Flow

1. User receives notification for a new breaking change or comment.
2. Click notification → navigate to relevant schema change.
3. Mark notification as read → backend updates read status.
4. UI reflects read/unread state.

---

## 6. Search & Filter Flow

1. Use search bar or filter dropdowns on dashboard.
2. Filter results update in real-time.
3. Click on a schema change to view details.

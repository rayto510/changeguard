# ChangeGuard v1 Features

This document outlines the key features of ChangeGuard v1, focusing on tracking schema/API breaking changes.

---

## 1. Schema Change Tracking

- **Create Schema Change Records**
  - Record any schema/API change with name, description, change type (breaking/non-breaking), affected services.
- **Update and Resolve**
  - Change status to open or resolved.
  - Add notes for mitigation.
- **Audit Trail**
  - All changes are timestamped and logged for future reference.

---

## 2. Comments & Collaboration

- **Comment Threads**
  - Discuss each schema change with team members.
  - Add context, mitigation steps, or impact analysis.
- **Mentions**
  - Notify specific users by mentioning them in comments.
  
---

## 3. Notifications

- **Real-time Alerts**
  - Notify affected users of new breaking changes or comments.
- **Mark as Read**
  - Users can mark notifications as read.
- **Notification Types**
  - Breaking change alerts
  - Comment notifications

---

## 4. Search & Filter

- **Search schema changes**
  - By name, description, or affected service.
- **Filter**
  - By status (`open` / `resolved`)
  - By change type (`breaking` / `non-breaking`)
  - By affected service

---

## 5. User Management

- **User Profiles**
  - Name, email, role
- **Role-based Access**
  - Regular users vs. admins
- **Authentication**
  - JWT-based login and registration

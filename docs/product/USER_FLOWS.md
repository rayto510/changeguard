# User Flows

Core user journeys and workflows through ChangeGuard platform.

## Flow 1: New User Onboarding

```
User lands on homepage
  ↓
[Not logged in?]
  ├─ Sign up (email, password)
  │   ↓
  │   Email verification (click link)
  │   ↓
  │   Set profile (name, title, avatar)
  │   ↓
  │   Join or create organization
  │   ↓
  │   Join default team
  │   ↓
  │   See empty dashboard
  │
  └─ Log in (email, password)
      ↓
      [Forgot password?]
      ├─ Reset link sent to email
      │   ↓
      │   Set new password
      │   ↓
      │   Log in
      │
      └─ Successful → Dashboard
```

---

## Flow 2: Creating a Schema Change

```
User navigates to "New Change"
  ↓
Form: Basic Information
  - Change name (required)
  - Description (required)
  - Change type selector (breaking/non-breaking/deprecation)
  ↓
Form: Impact Information
  - Select affected services (multi-select)
  - Add migration notes
  - Set deadline
  - Add rollback procedure
  ↓
Form: Review & Publish
  - Preview change
  - Select assignee/reviewer
  - [Advanced] Set approval requirements
  ↓
Publish change → Send notifications to affected teams
  ↓
Change appears in:
  - Creator's "My Changes" list
  - Affected service team dashboards
  - Organizational change feed
  - Relevant team notifications
```

---

## Flow 3: Reviewing a Schema Change

```
User sees notification: "New breaking change: User API v2.0"
  ↓
Click notification → Open change details
  ↓
View: Change Information
  - Change name and description
  - Affected services
  - Created by / Created date
  - Deadline
  ↓
Scan: Comment Thread
  - View existing comments
  - See team discussions
  - Find key decisions
  ↓
Decision Point:
  ├─ Add my comment → Type and submit
  │   ↓
  │   Mentions @other-engineer
  │   ↓
  │   They receive notification
  │
  ├─ Acknowledge → "I've seen this"
  │   ↓
  │   Notification marked read
  │
  └─ Escalate → Alert my manager
      ↓
      Leave comment mentioning @manager
      ↓
      Request approval
```

---

## Flow 4: Approving a Change

```
Platform architect gets notification: "Change awaiting approval"
  ↓
Review pending changes dashboard
  ↓
Open change: "Deprecate legacy auth endpoint"
  ↓
Read and evaluate:
  - Change details
  - Migration path
  - Team comments
  - Affected services list
  ↓
Decision Point:
  ├─ Approve
  │   ├─ Add approval comment: "Approved - 3 month deadline"
  │   ├─ Submit approval
  │   ↓
  │   Status: Open → Approved
  │   ↓
  │   Notifications sent to creator and affected teams
  │
  ├─ Request changes
  │   ├─ Add comment: "Need larger migration window"
  │   ├─ Change status: In Review → Changes Requested
  │   ↓
  │   Creator notified, update required
  │
  └─ Reject
      ├─ Add comment with rejection reason
      ├─ Change status: In Review → Rejected
      ↓
      Creator decides: Revise or archive change
```

---

## Flow 5: Tracking Change Status

```
Creator wants to see approval progress
  ↓
Click on created change
  ↓
View status timeline:
  - Created (Dec 25, 2025)
  - In Review (Dec 26, 2025)
  - Approved (Dec 27, 2025 by @alice)
  - In Progress (Jan 5, 2026)
  - Resolved (Jan 15, 2026)
  ↓
View comments:
  - @bob: "What about GraphQL schema?"
  - @alice: "Covered in migration guide"
  - @carlos: "Approved as of Jan 2"
  ↓
View notifications history:
  - Who was notified and when
  - Who has seen the change
  - Open discussions
  ↓
Actions:
  - Update status manually
  - Add new comment
  - Archive when done
```

---

## Flow 6: Searching for Changes

```
User navigates to search page
  ↓
Option A: Basic Search
  - Type in search box: "user service"
  - Results show all changes mentioning "user service"
  - Sort by relevance or date
  ↓
Option B: Advanced Filtering
  - Status: "Open" + "Breaking"
  - Service: Select "User API" and "Auth Service"
  - Date range: Last 7 days
  - Priority: "High"
  ↓
Results display:
  - "User API breaking change: Remove deprecated field"
  - "Auth Service: New 2FA requirement"
  - "User API: Rate limit changes"
  ↓
Click result → Opens change detail
```

---

## Flow 7: Team Collaboration on Change

```
Team lead creates change: "Database schema migration"
  ↓
Comments section activity:
  - @data-engineer-1: "What's the rollback procedure?"
  - Team Lead: "@data-engineer-1 See updated migration guide"
  - @data-engineer-2: "How long will the table be locked?"
  - Team Lead: "~2 hours, run during maintenance window"
  - @dba: "Approved, ready to deploy"
  ↓
Notification feed:
  - DBA gets mention notification
  - Engineers get new comment notifications
  - All see discussion in one thread
  ↓
Status updates:
  - Initially: Open
  - After discussion: Approved
  - Execution day: In Progress
  - After success: Resolved
```

---

## Flow 8: Managing Notifications

```
User sees notification badge: "3 new"
  ↓
Click notification icon → Open notification center
  ↓
View notifications:
  - "New breaking change: User API" (unread)
  - "Alice approved your change" (unread)
  - "You were mentioned in Auth Service change" (read)
  ↓
Actions:
  - Click to view change
  - Mark as read
  - Archive notification
  - Mark all as read (bulk action)
  ↓
Notification preferences (settings page):
  - Email notifications: ON/OFF
  - Slack notifications: ON/OFF
  - Which notifications to receive:
    ✓ Breaking changes affecting my services
    ✓ Someone mentions me
    ✓ Changes I created get approved
    ✓ Status changes on watched changes
```

---

## Flow 9: User Profile & Settings

```
User clicks profile icon (top right)
  ↓
Menu options:
  - View Profile
  - Settings
  - Organization Settings (if admin)
  - Logout
  ↓
Settings page tabs:
  ├─ Profile
  │   - Name, email, title, avatar
  │   - Bio / department
  │
  ├─ Account Security
  │   - Change password
  │   - Enable 2FA (v1.0)
  │   - Manage sessions
  │   - Login history
  │
  ├─ Notifications
  │   - Email preferences
  │   - Slack/Teams settings
  │   - Notification types and frequency
  │
  └─ Privacy
      - Visibility (public/private profile)
      - Who can mention me
      - Data deletion
```

---

## Flow 10: Admin Organization Management

```
Admin accesses Organization Settings
  ↓
Dashboard tabs:
  ├─ Overview
  │   - Organization name and settings
  │   - Number of users, teams, changes
  │   - Billing information
  │
  ├─ Team Management
  │   - Create new team
  │   - Add/remove members
  │   - Assign teams to services
  │
  ├─ User Management
  │   - List all users
  │   - Change user roles
  │   - Invite new users
  │   - Revoke access
  │
  ├─ Integrations
  │   - Connect GitHub/GitLab
  │   - Slack notifications settings
  │   - Webhook configuration
  │
  ├─ Policies
  │   - Set approval requirements
  │   - Change notification rules
  │   - Set escalation policies
  │
  └─ Audit Logs
      - View all organization changes
      - Export logs for compliance
      - Track user actions
```

---

## Critical Decision Points

| Decision | Primary Outcome | Alternate Path |
|----------|-----------------|-----------------|
| Create breaking change | Send notifications to teams | Save as draft |
| Approve change | Lock status, notify creator | Request changes |
| Search changes | View results | Save search |
| Join team | Access team changes | Decline invitation |
| Mention user | Send notification | Leave comment |

---

## Time Estimates

- User onboarding: 2-3 minutes
- Create schema change: 5-10 minutes
- Review change (simple): 2-3 minutes
- Review change (complex): 10-15 minutes
- Approve change: 2-5 minutes
- Search and filter: 1-2 minutes
- Modify profile settings: 3-5 minutes

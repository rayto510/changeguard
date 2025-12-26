# ChangeGuard UI Guidelines (v1)

This document describes the UI design principles for ChangeGuard v1.

---

## 1. Design Principles

- **Clarity**
  - Schema changes, comments, and notifications must be immediately visible.
- **Simplicity**
  - Minimalist interface — focus on key data.
- **Consistency**
  - Use consistent colors, typography, and layouts across pages.
- **Responsiveness**
  - Works on desktop and tablet (mobile optional for v1).

---

## 2. Color Palette

- **Primary:** #1F2937 (Dark Gray)
- **Accent / Alerts:** #EF4444 (Red for breaking changes)
- **Secondary:** #3B82F6 (Blue for non-breaking changes)
- **Background:** #F9FAFB (Light Gray)
- **Text:** #111827 (Primary), #6B7280 (Secondary)

---

## 3. Typography

- **Headings:** Inter, Bold
- **Body:** Inter, Regular
- **Font Sizes:**
  - H1: 32px
  - H2: 24px
  - H3: 18px
  - Body: 14px

---

## 4. Component Guidelines

- **Schema Change Card**
  - Shows name, change type, status, affected services, timestamp.
- **Comment Thread**
  - Inline comments with timestamps and author names.
- **Notification List**
  - Shows unread notifications at top, clear type indicators.

---

## 5. Interaction Guidelines

- Buttons and links must have clear states (hover, active, disabled).  
- Breaking changes highlighted in red; non-breaking in blue.  
- Use modals sparingly — only for critical actions (like deleting a schema change).  
- Provide inline feedback on actions (e.g., “Comment added successfully”).

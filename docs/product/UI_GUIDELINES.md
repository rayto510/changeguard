# UI Guidelines & Design System

Design system, component library, and styling guidelines for ChangeGuard.

## Design Principles

### 1. Clarity First
Users must understand what they're looking at and what action to take. Every interface should have a single clear purpose.

### 2. Minimal Friction
Reduce clicks, typing, and cognitive load. Sensible defaults over configuration. Progressive disclosure.

### 3. Consistency
Reusable components and patterns build familiarity. Consistent terminology and behavior across the app.

### 4. Accessible by Default
WCAG 2.1 AA compliance. Keyboard navigation. High contrast. Screen reader support.

### 5. Developer-Friendly
API-first mindset. Transparency over obscurity. Clear error messages and logs.

---

## Color Palette

### Primary Colors
- **Primary Blue**: `#0066CC` - Buttons, links, primary actions
- **Primary Dark**: `#004A99` - Hover state on primary
- **Primary Light**: `#E6F2FF` - Backgrounds, hover states

### Status Colors
- **Success Green**: `#10B981` - Approved, resolved, available
- **Warning Orange**: `#F59E0B` - In review, pending, caution
- **Error Red**: `#EF4444` - Breaking, error, attention required
- **Info Blue**: `#3B82F6` - Notifications, information
- **Neutral Gray**: `#6B7280` - Secondary, disabled

### Semantic Meanings
- **Green (#10B981)**: Change approved, all good
- **Red (#EF4444)**: Breaking change, action required
- **Orange (#F59E0B)**: In review, waiting
- **Gray (#6B7280)**: Archived, resolved

### Accessibility
- Minimum contrast ratio: 4.5:1 for normal text
- 3:1 for large text and icons
- No color alone conveys meaning (always include icon/text)

---

## Typography

### Font Family
- **Primary**: Inter, system-ui, -apple-system, sans-serif
- **Monospace**: 'SF Mono', Monaco, Menlo, Consolas, monospace
- **Fallback**: Helvetica Neue, Arial

### Font Scale
```
Display (48px, 600 weight)    - Page titles
Heading 1 (32px, 600 weight)  - Section headers
Heading 2 (24px, 600 weight)  - Subsection headers
Heading 3 (18px, 600 weight)  - Card titles
Body Large (16px, 400 weight) - Primary text
Body (14px, 400 weight)       - Standard text
Body Small (12px, 400 weight) - Secondary text, labels
Caption (11px, 400 weight)    - Timestamps, hints
Mono (14px, 400 weight)       - Code blocks
```

### Line Heights
- Display/Headings: 1.2
- Body: 1.5
- Mono: 1.4

---

## Spacing System

Consistent 4px base unit for rhythm and alignment:

```
xs: 4px
sm: 8px
md: 16px
lg: 24px
xl: 32px
2xl: 48px
3xl: 64px
```

### Common Patterns
- Padding inside cards: `md` (16px)
- Margin between sections: `lg` (24px)
- Gap in lists/grids: `sm` (8px) to `md` (16px)
- Top/bottom padding on pages: `xl` (32px)

---

## Buttons

### Button Types

**Primary Button**
- Background: Primary Blue (#0066CC)
- Text: White
- Padding: 10px 16px
- Border radius: 6px
- Usage: Main call-to-action (Create, Save, Approve)

**Secondary Button**
- Background: Light Gray (#F3F4F6)
- Text: Dark Gray (#374151)
- Border: 1px solid #E5E7EB
- Padding: 10px 16px
- Usage: Secondary actions (Cancel, Delete)

**Ghost Button**
- Background: Transparent
- Text: Primary Blue (#0066CC)
- Border: None
- Padding: 10px 16px
- Usage: Tertiary actions (Help, View More)

**Destructive Button**
- Background: Error Red (#EF4444)
- Text: White
- Padding: 10px 16px
- Usage: Irreversible actions (Delete change, Remove user)

### Button States
- **Default**: Full color
- **Hover**: 10% darker shade
- **Active**: 20% darker shade
- **Disabled**: 50% opacity, no cursor change
- **Loading**: Spinner inside, disabled state

---

## Cards & Containers

**Change Card** (Listing page)
```
┌─────────────────────────────────┐
│ Change Title                    │
│ Status badge  Date             │
├─────────────────────────────────┤
│ Description preview...          │
│ Affected: Service A, Service B  │
├─────────────────────────────────┤
│ Created by @user · 3 comments   │
│ [View] [Archive]               │
└─────────────────────────────────┘
```

- Padding: 16px
- Border: 1px #E5E7EB
- Border-radius: 8px
- Hover: Background #F9FAFB
- Shadow: 0 1px 3px rgba(0,0,0,0.1)

---

## Status Badges

### Breaking Change
- **Background**: #FEE2E2 (light red)
- **Text**: #DC2626 (dark red)
- **Icon**: ⚠️ or 🚨
- **Label**: "BREAKING"

### Non-Breaking
- **Background**: #DCFCE7 (light green)
- **Text**: #15803D (dark green)
- **Icon**: ✓
- **Label**: "NON-BREAKING"

### Deprecation
- **Background**: #FEF3C7 (light yellow)
- **Text**: #B45309 (dark orange)
- **Icon**: ⏳
- **Label**: "DEPRECATED"

---

## Status States

**Open** (Waiting for action)
- Badge color: Primary Blue
- Icon: Open circle ◯

**In Review** (Under consideration)
- Badge color: Warning Orange
- Icon: Clock ⏱️

**Approved** (Ready/Decision made)
- Badge color: Success Green
- Icon: Check ✓

**Resolved** (Complete)
- Badge color: Gray
- Icon: Archive 📦

**Archived** (Closed)
- Badge color: Light Gray
- Text: Muted gray
- Style: Strikethrough option

---

## Forms

### Form Layout
- **Label**: 12px, 600 weight, `margin-bottom: 8px`
- **Input**: 14px monospace, padding 10px 12px, border-radius 6px
- **Helper text**: 12px, gray, `margin-top: 4px`
- **Error message**: 12px, red, `margin-top: 4px`
- **Input border**: 1px #E5E7EB
- **Input focus**: Border primary blue, outline none, shadow 0 0 0 3px rgba(0,102,204,0.1)

### Input Types
- **Text inputs**: Standard with placeholder
- **Textareas**: Min height 120px, resizable
- **Select dropdowns**: Custom styled with chevron icon
- **Checkboxes**: 16x16px, with label to the right
- **Radio buttons**: 16x16px, with label to the right
- **Date pickers**: Calendar widget on focus

### Form Validation
- **On blur**: Validate field, show error if invalid
- **On submit**: Validate all fields, show errors
- **Success state**: Green border, checkmark icon
- **Error state**: Red border, error message below

---

## Navigation

### Main Navigation (Top Bar)
- Height: 56px
- Background: White
- Border-bottom: 1px #E5E7EB
- Logo: Left side, 32x32px
- Menu items: Center-aligned
- User menu: Right side (avatar + dropdown)

### Sidebar (Future v1.0)
- Width: 256px
- Background: White
- Active state: Blue background, blue left border

### Breadcrumbs
- Format: Home > Dashboard > Changes > Create
- Separator: Forward slash (/)
- Last item: Current page (not linked)

---

## Comment Thread

**Comment Item**
```
┌─────────────────────────────────┐
│ @username · 2 days ago          │
├─────────────────────────────────┤
│ Comment text with markdown      │
│ support and @mentions           │
├─────────────────────────────────┤
│ [Like] [Reply] [Edit] [Delete] │
└─────────────────────────────────┘
  └─ Nested reply (indented)
```

- Avatar: 32x32px, top-left
- Timestamp: 12px gray, clickable (permalink)
- Comment text: 14px, line-height 1.5
- Actions: Secondary buttons (ghost style)
- Nesting: 16px left padding per level
- Max nesting depth: 3 levels (v0.1)

---

## Notification Center

**Notification Item**
```
┌─────────────────────────────────┐
│ ● New breaking change: User API │
│   "Your service is affected"    │
│   @alice · 5 minutes ago        │
└─────────────────────────────────┘
```

- Unread dot: 8px, primary blue, left side
- Click to navigate to change
- Hover: Background #F9FAFB
- Archive on hover: Remove option appears

---

## Loading & Empty States

### Loading Skeleton
```
┌──────────────────────┐
│ ░░░░░░░░░░ (pulse)  │
│ ░░░░░░░              │
│ ░░░░░░░░░░░░░        │
└──────────────────────┘
```
- Gray #E5E7EB background
- Pulse animation (subtle breathing effect)
- Match layout dimensions

### Empty State
- Icon: Large (64x64px), primary blue
- Heading: "No changes yet"
- Description: "Get started by creating your first change"
- CTA: Primary button "Create Change"

---

## Responsive Breakpoints

```
Mobile:     < 640px
Tablet:     640px - 1024px
Desktop:    > 1024px
```

### Responsive Patterns
- **Mobile**: Single column, full-width inputs, bottom navigation
- **Tablet**: Two columns, adjusted spacing
- **Desktop**: Multi-column layouts, sidebar navigation

---

## Accessibility Checklist

- [ ] Keyboard navigation (Tab, Enter, Escape)
- [ ] Focus indicators visible (2px outline)
- [ ] Color contrast 4.5:1 minimum
- [ ] Labels for all form inputs
- [ ] Error messages linked to inputs (aria-describedby)
- [ ] Images have alt text
- [ ] Icons have aria-label if not accompanied by text
- [ ] Modals have focus trap
- [ ] Headings in proper order (h1 → h2 → h3)
- [ ] Screen reader testing done
- [ ] Motion respects prefers-reduced-motion

---

## Dark Mode (v0.2)

When dark mode enabled:
- Background: #111827 (near black)
- Cards: #1F2937 (dark gray)
- Text: #F3F4F6 (light gray)
- Borders: #374151 (medium gray)
- Hover states: +1 shade lighter
- Colors slightly desaturated for comfort

---

## Code Examples

### Tailwind CSS Classes

**Change card**:
```
class="rounded-lg border border-gray-200 bg-white p-4 hover:bg-gray-50 shadow-sm"
```

**Primary button**:
```
class="rounded-md bg-blue-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-blue-700 active:bg-blue-800 disabled:opacity-50"
```

**Status badge**:
```
class="inline-flex items-center rounded-full bg-red-100 px-3 py-1 text-xs font-medium text-red-800"
```

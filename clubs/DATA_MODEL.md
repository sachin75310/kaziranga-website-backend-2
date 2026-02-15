# Data Model Relationships

## Entity Relationship Diagram

```
┌─────────────────────────┐
│      Community          │
├─────────────────────────┤
│ id (PK)                 │
│ name                    │
│ head                    │
│ member_count            │
│ description (Rich Text) │
│ join_form_link          │
│ logo                    │
│ status (ACTIVE/ARCHIVED)│
│ theme                   │
│ created_on              │
│ updated_on              │
└───────────┬─────────────┘
            │
            │ 1
            │
            │
            │ N (one-to-many)
            │
            ▼
┌─────────────────────────┐
│        Event            │
├─────────────────────────┤
│ id (PK)                 │
│ name                    │
│ description             │
│ start_date              │
│ end_date                │
│ event_status            │
│ event_location          │
│ cover_img               │
│ community (FK) ◄────────┼─── Links to Community
│ ...                     │
└─────────────────────────┘
```

## Relationship Details

### Community → Events
- **Type**: One-to-Many
- **Foreign Key**: `Event.community` references `Community.id`
- **Related Name**: `events` (access via `community.events.all()`)
- **On Delete**: `SET_NULL` (preserves events if community is deleted)
- **Nullable**: Yes (events don't require a community)

### Example Usage

```python
# Get all events for a community
chess_community = Community.objects.get(name="Chess Community")
chess_events = chess_community.events.all()

# Get the community for an event
event = Event.objects.get(id=1)
organizing_community = event.community

# Filter events by community
programming_events = Event.objects.filter(community__theme='PROGRAMMING')
```

## API Response Structure

```json
{
  "id": 1,
  "name": "Chess Community",
  "events": [
    {
      "id": 1,
      "name": "Weekly Blitz Tournament",
      "start_date": "2025-01-12T16:00:00Z",
      "...": "..."
    },
    {
      "id": 2,
      "name": "Championship Finals",
      "start_date": "2025-02-01T14:00:00Z",
      "...": "..."
    }
  ]
}
```

## Database Indexes

The following fields are indexed for optimal query performance:
- `Community.name` (unique)
- `Community.status`
- `Community.theme`
- `Event.community` (foreign key)

## Field Choices

### Community.status
- `ACTIVE` - Currently active community
- `ARCHIVED` - Archived/inactive community

### Community.theme
- `CHESS`
- `PROGRAMMING`
- `SPIRITUALITY`
- `POETRY`
- `MUSIC`
- `SPORTS`
- `ARTS`
- `DEBATE`
- `OTHER`

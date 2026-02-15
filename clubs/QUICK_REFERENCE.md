# Communities API Quick Reference

## Base URL
```
/api/communities/
```

## Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/communities/` | List all communities | No |
| GET | `/api/communities/?status=active` | Filter active communities | No |
| GET | `/api/communities/?status=archived` | Filter archived communities | No |
| GET | `/api/communities/{id}/` | Get community details | No |
| POST | `/api/communities/create/` | Create community | Yes (Admin) |
| PUT/PATCH | `/api/communities/{id}/update/` | Update community | Yes (Admin) |
| DELETE | `/api/communities/{id}/delete/` | Delete community | Yes (Admin) |

## List Response Fields
```json
{
  "id": 1,
  "name": "Community Name",
  "logo": "https://...",
  "member_count": 42,
  "theme": "PROGRAMMING",
  "status": "ACTIVE"
}
```

## Detail Response (includes events)
```json
{
  "id": 1,
  "name": "Community Name",
  "head": "Leader Name",
  "member_count": 42,
  "description": "<p>Rich text content</p>",
  "join_form_link": "https://...",
  "logo": "https://...",
  "status": "ACTIVE",
  "theme": "PROGRAMMING",
  "events": [
    {
      "id": 1,
      "name": "Event Name",
      "start_date": "2025-01-12T16:00:00Z",
      "end_date": "2025-01-12T18:00:00Z",
      "event_status": "UPCOMING",
      "event_location": "ONLINE"
    }
  ],
  "created_on": "2024-11-01T10:30:00Z",
  "updated_on": "2024-11-28T15:45:00Z"
}
```

## Query Parameters

| Parameter | Type | Options | Example |
|-----------|------|---------|---------|
| status | String | `active`, `archived` | `?status=active` |
| page | Integer | Any positive integer | `?page=2` |
| page_size | Integer | 1-100 | `?page_size=20` |

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | Deleted |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 503 | Service Unavailable |

## Theme Options
- `CHESS`
- `PROGRAMMING`
- `SPIRITUALITY`
- `POETRY`
- `MUSIC`
- `SPORTS`
- `ARTS`
- `DEBATE`
- `OTHER`

## Status Options
- `ACTIVE`
- `ARCHIVED`

## Quick cURL Examples

### Get active communities
```bash
curl http://localhost:8000/api/communities/?status=active
```

### Get community with ID 1
```bash
curl http://localhost:8000/api/communities/1/
```

### Create community (requires auth token)
```bash
curl -X POST http://localhost:8000/api/communities/create/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Community",
    "head": "Leader Name",
    "description": "<p>Description here</p>",
    "join_form_link": "https://forms.example.com/join",
    "logo": "https://example.com/logo.png",
    "theme": "PROGRAMMING"
  }'
```

### Update member count
```bash
curl -X PATCH http://localhost:8000/api/communities/1/update/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"member_count": 50}'
```

## Frontend Integration Tips

1. **Rich Text**: The `description` field contains HTML - render it safely with a sanitizer
2. **Pagination**: Use `next` and `previous` URLs from response for navigation
3. **Filtering**: Use `?status=active` to show only active communities
4. **Events**: Events are nested in detail view - no separate API call needed
5. **Images**: `logo` field contains full URL - use directly in `<img>` tags

## Django Admin

Access at: `http://localhost:8000/admin/clubs/community/`

Features:
- Filter by status, theme, creation date
- Search by name, head, description
- Bulk actions available
- Sortable columns

## Related Models

The `Event` model now has a `community` field:
```python
event.community  # Returns Community object or None
community.events.all()  # Returns QuerySet of Event objects
```

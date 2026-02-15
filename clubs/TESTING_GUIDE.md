# Testing Guide for Communities API

## Prerequisites
1. Django development server running: `python manage.py runserver`
2. Database migrations applied
3. (Optional) Admin user created for testing protected endpoints

## Test Plan

### ✅ Test 1: List All Communities
**Endpoint**: `GET /api/communities/`

```bash
# Using cURL
curl http://localhost:8000/api/communities/

# Using httpie (if installed)
http GET http://localhost:8000/api/communities/

# Using browser
# Just navigate to: http://localhost:8000/api/communities/
```

**Expected Result**:
- Status: 200 OK
- Paginated response with `count`, `next`, `previous`, `results`
- Each community shows: `id`, `name`, `logo`, `member_count`, `theme`, `status`

---

### ✅ Test 2: Filter Active Communities
**Endpoint**: `GET /api/communities/?status=active`

```bash
curl "http://localhost:8000/api/communities/?status=active"
```

**Expected Result**:
- Status: 200 OK
- Only communities with `status: "ACTIVE"`

---

### ✅ Test 3: Filter Archived Communities
**Endpoint**: `GET /api/communities/?status=archived`

```bash
curl "http://localhost:8000/api/communities/?status=archived"
```

**Expected Result**:
- Status: 200 OK
- Only communities with `status: "ARCHIVED"`

---

### ✅ Test 4: Invalid Status Filter
**Endpoint**: `GET /api/communities/?status=invalid`

```bash
curl "http://localhost:8000/api/communities/?status=invalid"
```

**Expected Result**:
- Status: 400 Bad Request
- Error message: "Invalid status. Use 'active' or 'archived'."

---

### ✅ Test 5: Get Community Details (Valid ID)
**Endpoint**: `GET /api/communities/{id}/`

```bash
# Replace 1 with an actual community ID
curl http://localhost:8000/api/communities/1/
```

**Expected Result**:
- Status: 200 OK
- Full community object with all fields
- `events` array included (may be empty)
- Rich text preserved in `description`

---

### ✅ Test 6: Get Community Details (Invalid ID)
**Endpoint**: `GET /api/communities/99999/`

```bash
curl http://localhost:8000/api/communities/99999/
```

**Expected Result**:
- Status: 404 Not Found
- Error message: "Community not found."

---

### ✅ Test 7: Pagination
**Endpoint**: `GET /api/communities/?page=1&page_size=5`

```bash
curl "http://localhost:8000/api/communities/?page=1&page_size=5"
```

**Expected Result**:
- Status: 200 OK
- Maximum 5 results per page
- `next` and `previous` URLs for navigation

---

### ✅ Test 8: Create Community (Without Auth) ❌
**Endpoint**: `POST /api/communities/create/`

```bash
curl -X POST http://localhost:8000/api/communities/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Community",
    "head": "Test Leader",
    "description": "Test Description",
    "join_form_link": "https://test.com",
    "logo": "https://test.com/logo.png"
  }'
```

**Expected Result**:
- Status: 401 Unauthorized
- Error: "Authentication credentials were not provided."

---

### ✅ Test 9: Create Community (With Auth) ✅

**Step 1**: Get JWT Token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_admin_username",
    "password": "your_admin_password"
  }'
```

**Step 2**: Create Community
```bash
# Replace YOUR_ACCESS_TOKEN with the token from step 1
curl -X POST http://localhost:8000/api/communities/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Test Community",
    "head": "John Doe",
    "member_count": 10,
    "description": "<p>This is a <b>test</b> community with <em>rich text</em></p>",
    "join_form_link": "https://forms.example.com/join",
    "logo": "https://example.com/logo.png",
    "status": "ACTIVE",
    "theme": "PROGRAMMING"
  }'
```

**Expected Result**:
- Status: 201 Created
- Full community object returned with generated ID

---

### ✅ Test 10: Create Community (Missing Required Fields)

```bash
curl -X POST http://localhost:8000/api/communities/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Incomplete Community"
  }'
```

**Expected Result**:
- Status: 400 Bad Request
- Error listing missing fields

---

### ✅ Test 11: Update Community (PATCH)

```bash
curl -X PATCH http://localhost:8000/api/communities/1/update/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "member_count": 100,
    "status": "ARCHIVED"
  }'
```

**Expected Result**:
- Status: 200 OK
- Updated community object returned
- Only specified fields updated

---

### ✅ Test 12: Delete Community

```bash
curl -X DELETE http://localhost:8000/api/communities/1/delete/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Expected Result**:
- Status: 204 No Content
- Success message: "Community deleted successfully."

---

### ✅ Test 13: Rich Text Preservation

Create a community with complex HTML:

```bash
curl -X POST http://localhost:8000/api/communities/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rich Text Test",
    "head": "Test",
    "description": "<h2>Welcome</h2><p>This community has:</p><ul><li>Bullet points</li><li><b>Bold text</b></li><li><em>Italic text</em></li><li><a href=\"https://test.com\">Links</a></li></ul>",
    "join_form_link": "https://test.com",
    "logo": "https://test.com/logo.png"
  }'
```

Then retrieve it and verify HTML is preserved:
```bash
curl http://localhost:8000/api/communities/{created_id}/
```

**Expected Result**:
- HTML formatting fully preserved in response
- No stripping of tags

---

### ✅ Test 14: Community with Events

**Prerequisites**: Create an event linked to a community

1. Create a community (note the ID)
2. In Django admin, create an event and set `community` to the created community
3. Retrieve the community:

```bash
curl http://localhost:8000/api/communities/{community_id}/
```

**Expected Result**:
- `events` array populated with event objects
- Each event includes: id, name, start_date, end_date, event_status, event_location

---

## Using Django Admin for Testing

1. Navigate to: `http://localhost:8000/admin/`
2. Login with superuser credentials
3. Go to `Clubs > Communities`
4. Create test communities with various:
   - Status values (ACTIVE, ARCHIVED)
   - Theme values
   - Rich text descriptions
5. Test the API endpoints with these created communities

---

## Browser Testing

For GET endpoints, you can use your browser:

1. `http://localhost:8000/api/communities/`
2. `http://localhost:8000/api/communities/?status=active`
3. `http://localhost:8000/api/communities/1/`

Django REST Framework provides a browsable API interface!

---

## Postman Collection (Optional)

Create a Postman collection with these requests:

1. **Get Token** - POST `/api/token/`
2. **List Communities** - GET `/api/communities/`
3. **Filter Active** - GET `/api/communities/?status=active`
4. **Get Community** - GET `/api/communities/{id}/`
5. **Create Community** - POST `/api/communities/create/`
6. **Update Community** - PATCH `/api/communities/{id}/update/`
7. **Delete Community** - DELETE `/api/communities/{id}/delete/`

---

## Test Checklist

- [ ] List all communities returns 200
- [ ] Filter by status=active works
- [ ] Filter by status=archived works
- [ ] Invalid status returns 400
- [ ] Get valid community ID returns 200 with full data
- [ ] Get invalid community ID returns 404
- [ ] Pagination works correctly
- [ ] Create without auth returns 401
- [ ] Create with auth but missing fields returns 400
- [ ] Create with valid data returns 201
- [ ] Update community works (200)
- [ ] Delete community works (204)
- [ ] Rich text is preserved in description
- [ ] Events are included in community details
- [ ] Related events show correct community in Event API

---

## Automated Testing (Future)

Consider writing Django test cases:

```python
# clubs/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Community

class CommunityAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.community = Community.objects.create(
            name="Test Community",
            head="Test Head",
            # ... other fields
        )
    
    def test_list_communities(self):
        response = self.client.get('/api/communities/')
        self.assertEqual(response.status_code, 200)
    
    def test_filter_active_communities(self):
        response = self.client.get('/api/communities/?status=active')
        self.assertEqual(response.status_code, 200)
    
    # Add more test methods...
```

Run tests with:
```bash
python manage.py test clubs
```

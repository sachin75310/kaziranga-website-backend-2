# Kaziranga Website Backend – API Reference

## Overview
This backend provides RESTful APIs for managing announcements, events, student profiles, hall of fame achievements, and internal communities (clubs). All APIs return JSON responses and follow REST standards.

---


## Authentication

### Obtain Token
- **POST** `/api/token/`
- **Request Attributes:**
  | Field     | Type   | Required | Description         |
  |-----------|--------|----------|---------------------|
  | username  | string | Yes      | User's username     |
  | password  | string | Yes      | User's password     |
- **Request Example:**
  ```json
  { "username": "your_username", "password": "your_password" }
  ```
- **Success Response:**
  ```json
  { "refresh": "<refresh_token>", "access": "<access_token>" }
  ```
- **Error Response:**
  ```json
  { "detail": "No active account found with the given credentials" }
  ```

### Refresh Token
- **POST** `/api/token/refresh/`
- **Request Attributes:**
  | Field    | Type   | Required | Description         |
  |----------|--------|----------|---------------------|
  | refresh  | string | Yes      | Refresh token value |
- **Request Example:**
  ```json
  { "refresh": "<refresh_token>" }
  ```
- **Success Response:**
  ```json
  { "access": "<new_access_token>" }
  ```
- **Error Response:**
  ```json
  { "detail": "Token is invalid or expired" }
  ```

---


## Announcements

### List Announcements
- **GET** `/api/announcements/get-announcements/`
- **Success Response:**
  ```json
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "Welcome",
        "message": "Welcome to Kaziranga!",
        "author": {"id": 1, "name": "Admin"},
        "posted": "2025-12-11T10:00:00Z"
      }
    ]
  }
  ```
- **Error Response:**
  ```json
  { "error": "Some error occured, Announcements could not be found" }
  ```

### Get Announcement Details
- **GET** `/api/announcements/announcement/{id}/`
- **Success Response:**
  ```json
  {
    "id": 1,
    "title": "Welcome",
    "message": "Welcome to Kaziranga!",
    "author": {"id": 1, "name": "Admin"},
    "posted": "2025-12-11T10:00:00Z"
  }
  ```
- **Error Response (Not Found):**
  ```json
  { "error": "Announcement Not Found" }
  ```

### Create Announcement
- **POST** `/api/announcements/create/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Request Attributes:**
  | Field            | Type    | Required | Description                                                                 |
  |------------------|---------|----------|-----------------------------------------------------------------------------|
  | title            | string  | Yes      | Title of the announcement (unique)                                          |
  | help_format      | int     | Yes      | 1 (On) or 0 (Off)                                                           |
  | intro            | string  | Cond.    | Required if help_format=1                                                   |
  | category         | string  | Cond.    | Required if help_format=1. Enum: E, M, C, MI, Ev                            |
  | target_audience  | string  | Cond.    | Required if help_format=1. Enum: FL, DP, DS, BSC, BS, All                   |
  | use_case         | string  | Cond.    | Required if help_format=1                                                   |
  | summary          | string  | Cond.    | Required if help_format=1                                                   |
  | message          | string  | Cond.    | Required if help_format=0                                                   |
- **Request Example (help_format=1):**
  ```json
  {
    "title": "Exam Help",
    "help_format": 1,
    "intro": "Need help for exams",
    "category": "E",
    "target_audience": "BSC",
    "use_case": "Exam preparation",
    "summary": "Summary here"
  }
  ```
- **Request Example (help_format=0):**
  ```json
  {
    "title": "General Notice",
    "help_format": 0,
    "message": "This is a general announcement."
  }
  ```
- **Success Response:**
  ```json
  { "message": "Announcement created successfully" }
  ```
- **Error Response (Missing Fields):**
  ```json
  { "message": "Missing fields: [message]" }
  ```
- **Error Response (Unauthorized):**
  ```json
  { "detail": "Authentication credentials were not provided." }
  ```

---


## Events

### List Events
- **GET** `/api/events/get-events/`
- **Query Parameters:**
  - `event-status`, `event-tag`, `open-to-choice`, `event-location`
- **Success Response:**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Hackathon 2025",
        "description": "Annual hackathon event.",
        "start_date": "2025-12-20T09:00:00Z",
        "end_date": "2025-12-20T18:00:00Z",
        "event_status": "UPCOMING"
      }
    ]
  }
  ```
- **Error Response (Invalid Filter):**
  ```json
  { "message": "Incorrect event status" }
  ```

### Get Event Details
- **GET** `/api/events/get-event/{id}/`
- **Success Response:**
  ```json
  {
    "id": 1,
    "name": "Hackathon 2025",
    "description": "Annual hackathon event.",
    "start_date": "2025-12-20T09:00:00Z",
    "end_date": "2025-12-20T18:00:00Z",
    "event_status": "UPCOMING"
  }
  ```
- **Error Response (Not Found):**
  ```json
  { "message": "Event Not Found" }
  ```

### Create Event
- **POST** `/api/events/create/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Request Attributes:**
  | Field            | Type    | Required | Description                                                      |
  |------------------|---------|----------|------------------------------------------------------------------|
  | name             | string  | Yes      | Event name (unique)                                              |
  | description      | string  | Yes      | Event description                                                |
  | rules            | list    | Yes      | List of rules (strings)                                          |
  | cover_img        | string  | Yes      | URL to cover image                                               |
  | start_date       | string  | Yes      | Start datetime (ISO format)                                      |
  | end_date         | string  | Yes      | End datetime (ISO format)                                        |
  | prizes           | list    | Yes      | List of prizes (strings)                                         |
  | organizers       | list    | Yes      | List of Student IDs (integers)                                   |
  | event_status     | string  | Yes      | Enum: LIVE, UPCOMING, ENDED                                      |
  | event_tags       | string  | Yes      | Enum: HACKATHON, DSA, UI/UX, IDEATION                            |
  | open_to_choices  | string  | Yes      | Enum: OPEN, KAZIRANGA, BS, ALL                                   |
  | event_location   | string  | Yes      | Enum: ONLINE, OFFLINE, HYBRID                                    |
  | community        | int     | No       | Community ID (optional, nullable)                                |
- **Request Example:**
  ```json
  {
    "name": "Hackathon 2025",
    "description": "Annual hackathon event.",
    "rules": ["Rule 1", "Rule 2"],
    "cover_img": "https://example.com/img.png",
    "start_date": "2025-12-20T09:00:00Z",
    "end_date": "2025-12-20T18:00:00Z",
    "prizes": ["Prize 1"],
    "organizers": [1],
    "event_status": "UPCOMING",
    "event_tags": "HACKATHON",
    "open_to_choices": "OPEN",
    "event_location": "ONLINE",
    "community": 1
  }
  ```
- **Success Response:**
  ```json
  { "message": "Event successfully created", "data": { "id": 2, ... } }
  ```
- **Error Response (Missing Fields):**
  ```json
  { "message": "Missing fields: [name, ...]" }
  ```
- **Error Response (Unauthorized):**
  ```json
  { "detail": "Authentication credentials were not provided." }
  ```

---


## Student Profile

### Get Profile
- **GET** `/api/profile/get-profile/{profile_id}/`
- **Success Response:**
  ```json
  {
    "id": 1,
    "name": "Student Name",
    "email": "student@example.com",
    ...
  }
  ```
- **Error Response (Not Found):**
  ```json
  { "message": "Profile Not Found" }
  ```

### Edit Profile
- **PUT** `/api/profile/edit-profile/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Request:**
  ```json
  { "name": "New Name", ... }
  ```
- **Success Response:**
  ```json
  { "message": "Profile Updated" }
  ```
- **Error Response (Validation):**
  ```json
  { "error": { "name": ["This field may not be blank."] } }
  ```
- **Error Response (Unauthorized):**
  ```json
  { "error": "An error occured, couldn't edit profile" }
  ```

---


## Hall of Fame

### List Achievements
- **GET** `/api/hall-of-fame/get-achievements/`
- **Success Response:**
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "Best Coder",
        "achiever": {"id": 1, "name": "Student"},
        "date": "2025-12-01"
      }
    ]
  }
  ```
- **Error Response:**
  ```json
  { "error": "An error occured, couldn't get achievement list" }
  ```

### Get Achievement Details
- **GET** `/api/hall-of-fame/get-detailed-achievement/{achievement_id}/`
- **Success Response:**
  ```json
  { "message": { "id": 1, "title": "Best Coder", ... } }
  ```
- **Error Response (Not Found):**
  ```json
  { "message": "Achievement Not Found" }
  ```

### Submit Achievement
- **POST** `/api/hall-of-fame/submit-my-achievement/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Request Attributes:**
  | Field           | Type    | Required | Description                                 |
  |-----------------|---------|----------|---------------------------------------------|
  | cover_img       | string  | Yes      | URL to cover image                          |
  | headline        | string  | Yes      | Headline                                    |
  | article         | string  | Yes      | Article text                                |
  | achievement     | string  | Yes      | Achievement name                            |
  | achievement_tag | string  | Yes      | Enum: Study, DSA, Development, Hackathon... |
- **Request Example:**
  ```json
  {
    "cover_img": "https://example.com/cover.png",
    "headline": "Best Coder",
    "article": "Won the national coding contest.",
    "achievement": "National Coding Champion",
    "achievement_tag": "Hackathon"
  }
  ```
- **Success Response:**
  ```json
  { "message": "Achievement submitted successfully." }
  ```
- **Error Response (Validation):**
  ```json
  { "field": ["This field is required."] }
  ```
- **Error Response (Unauthorized):**
  ```json
  { "error": "Student profile not found for this user." }
  ```

---


## Communities (Clubs)

### List Communities
- **GET** `/api/communities/`
- **Query Parameters:**
  - `status` (`active` or `archived`)
- **Success Response:**
  ```json
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Chess Club",
        "logo": "https://...",
        "member_count": 42,
        "theme": "CHESS",
        "status": "ACTIVE"
      }
    ]
  }
  ```
- **Error Response (Invalid Filter):**
  ```json
  { "error": "Invalid status. Use 'active' or 'archived'." }
  ```

### Get Community Details
- **GET** `/api/communities/{id}/`
- **Success Response:**
  ```json
  {
    "id": 1,
    "name": "Chess Club",
    "head": "Alex",
    "member_count": 42,
    "description": "<p>Plays <b>competitive chess</b> weekly</p>",
    "join_form_link": "https://...",
    "logo": "https://...",
    "status": "ACTIVE",
    "theme": "CHESS",
    "events": [
      {
        "id": 1,
        "name": "Weekly Blitz",
        "start_date": "2025-01-12T16:00:00Z",
        "end_date": "2025-01-12T18:00:00Z",
        "event_status": "UPCOMING",
        "event_location": "ONLINE"
      }
    ],
    "created_on": "2025-12-01T10:00:00Z",
    "updated_on": "2025-12-10T12:00:00Z"
  }
  ```
- **Error Response (Not Found):**
  ```json
  { "error": "Community not found." }
  ```

### Create Community
- **POST** `/api/communities/create/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Request Attributes:**
  | Field           | Type    | Required | Description                                         |
  |-----------------|---------|----------|-----------------------------------------------------|
  | name            | string  | Yes      | Name of the community (unique)                      |
  | head            | string  | Yes      | Community lead                                      |
  | member_count    | int     | No       | Number of members (default: 0)                      |
  | description     | string  | Yes      | Rich text (HTML/Markdown)                           |
  | join_form_link  | string  | Yes      | URL to join form                                    |
  | logo            | string  | Yes      | URL to logo image                                   |
  | status          | string  | No       | Enum: ACTIVE, ARCHIVED (default: ACTIVE)            |
  | theme           | string  | No       | Enum: CHESS, PROGRAMMING, ... (default: OTHER)      |
- **Request Example:**
  ```json
  {
    "name": "Poetry Society",
    "head": "Maria Garcia",
    "member_count": 25,
    "description": "<p>A community for poetry lovers.</p>",
    "join_form_link": "https://forms.example.com/poetry-join",
    "logo": "https://example.com/poetry-logo.png",
    "status": "ACTIVE",
    "theme": "POETRY"
  }
  ```
- **Success Response:**
  ```json
  {
    "id": 3,
    "name": "Poetry Society",
    "head": "Maria Garcia",
    "member_count": 25,
    "description": "<p>A community for poetry lovers.</p>",
    "join_form_link": "https://forms.example.com/poetry-join",
    "logo": "https://example.com/poetry-logo.png",
    "status": "ACTIVE",
    "theme": "POETRY",
    "events": [],
    "created_on": "2025-12-11T12:00:00Z",
    "updated_on": "2025-12-11T12:00:00Z"
  }
  ```
- **Error Response (Missing Fields):**
  ```json
  { "error": "Missing required fields: name, description, logo" }
  ```
- **Error Response (Unauthorized):**
  ```json
  { "detail": "Authentication credentials were not provided." }
  ```

### Update Community
- **PUT/PATCH** `/api/communities/{id}/update/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Request:**
  ```json
  { "member_count": 45, "status": "ARCHIVED" }
  ```
- **Success Response:**
  ```json
  {
    "id": 1,
    "name": "Chess Club",
    "head": "Alex",
    "member_count": 45,
    "description": "<p>Plays <b>competitive chess</b> weekly</p>",
    "join_form_link": "https://...",
    "logo": "https://...",
    "status": "ARCHIVED",
    "theme": "CHESS",
    "events": [...],
    "created_on": "2025-12-01T10:00:00Z",
    "updated_on": "2025-12-11T12:30:00Z"
  }
  ```
- **Error Response (Not Found):**
  ```json
  { "error": "Community not found." }
  ```
- **Error Response (Unauthorized):**
  ```json
  { "detail": "Authentication credentials were not provided." }
  ```

### Delete Community
- **DELETE** `/api/communities/{id}/delete/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Success Response:**
  ```json
  { "message": "Community deleted successfully." }
  ```
- **Error Response (Not Found):**
  ```json
  { "error": "Community not found." }
  ```
- **Error Response (Unauthorized):**
  ```json
  { "detail": "Authentication credentials were not provided." }
  ```

---

## Common Features

- **Pagination:** All list endpoints are paginated. Use `page` and `page_size` query parameters.
- **Filtering:** Supported on events and communities.
- **Error Handling:** Standard HTTP status codes and error messages.
- **Authentication:** JWT required for all modifying endpoints (create, update, delete).

---

## Example Error Responses

```json
{ "error": "Authentication credentials were not provided." }
{ "error": "Invalid status. Use 'active' or 'archived'." }
{ "error": "Profile Not Found" }
{ "error": "An error occured, couldn't get profile" }
```

---

## Status Codes

- `200 OK` – Success
- `201 Created` – Resource created
- `204 No Content` – Resource deleted
- `400 Bad Request` – Invalid input
- `401 Unauthorized` – Not authenticated
- `403 Forbidden` – Not authorized
- `404 Not Found` – Resource not found
- `503 Service Unavailable` – Server error

---

## Quick Start

1. Obtain a JWT token via `/api/token/`.
2. Use the token in the `Authorization: Bearer <token>` header for protected endpoints.
3. Use GET endpoints to fetch data, and POST/PUT/PATCH/DELETE for modifications as per above.

---

For detailed request/response examples and model schemas, see the in-app documentation files or contact the backend team.

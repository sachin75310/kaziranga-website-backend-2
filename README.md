Backend repo for Kaziranga House's Website.

## Tech Stack
- **Backend**: Django & Django REST Framework
- **DBMS**: PostgreSQL (Production) / SQLite (Development)
- **Authentication**: JWT (Simple JWT)

## API Endpoints

### 🔐 Authentication
- `POST /api/token/` - Obtain JWT token pair
- `POST /api/token/refresh/` - Refresh access token

### 📢 Announcements
- `GET /api/announcements/get-announcements/` - List announcements
- `GET /api/announcements/announcement/{id}/` - Get announcement details
- `POST /api/announcements/create/` - Create announcement (Admin)

### 🎯 Events
- `GET /api/events/` - List events
- `GET /api/events/{id}/` - Get event details

### 👥 Student Profile
- `GET /api/profile/` - Get profile information

### 🏆 Hall of Fame
- `GET /api/hall-of-fame/` - List hall of fame entries

### 🎭 **Communities (NEW)**
- `GET /api/communities/` - List all communities
- `GET /api/communities/?status=active` - Filter active communities
- `GET /api/communities/?status=archived` - Filter archived communities
- `GET /api/communities/{id}/` - Get community details with events
- `POST /api/communities/create/` - Create community (Admin)
- `PUT/PATCH /api/communities/{id}/update/` - Update community (Admin)
- `DELETE /api/communities/{id}/delete/` - Delete community (Admin)

📖 **See [clubs/API_DOCUMENTATION.md](clubs/API_DOCUMENTATION.md) for detailed Communities API documentation**

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kaziranga-Website-Backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - API: http://localhost:8000/api/
   - Admin Panel: http://localhost:8000/admin/

## Project Structure

```
kaziranga-Website-Backend/
├── announcements/          # Announcements app
├── events/                 # Events management
├── clubs/                  # Communities/Clubs (Internal Communities)
│   ├── api/               # API endpoints
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── models.py          # Community data model
│   └── API_DOCUMENTATION.md
├── student_profile/        # Student profiles
├── hall_of_fame/          # Hall of fame entries
├── kaziranga_backend/     # Main project settings
└── manage.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

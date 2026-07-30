# TruthLens AI

An AI-powered fake news detection platform that uses machine learning to analyze news articles and provide credibility assessments with confidence scores and detailed indicators.

## Features

- **AI-Powered Analysis**: Advanced ML models analyze text patterns, sources, and linguistic markers
- **Real-Time Detection**: Instant credibility scores and detailed breakdowns
- **Detailed Reports**: Comprehensive analysis with confidence scores and key indicators
- **History Tracking**: Searchable history with trend visualization
- **File Upload Support**: Analyze TXT, PDF, and DOCX files
- **User Authentication**: Secure JWT-based authentication
- **Admin Dashboard**: User management and platform analytics
- **Responsive Design**: Beautiful UI built with React, TypeScript, and Tailwind CSS

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **ML Model**: Linear SVM with TF-IDF vectorization
- **File Processing**: PyPDF2, python-docx for document parsing
- **Email**: SMTP integration for password reset

### Frontend
- **Framework**: React 18 with TypeScript
- **UI Library**: Shadcn/ui components
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Notifications**: Sonner (toast)
- **Icons**: Lucide React

## Project Structure

```
TruthLens-AI/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configuration, security, logging
│   │   ├── database/     # Database models and base
│   │   ├── ml/           # ML predictor and models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic layer
│   │   └── utils/        # Utility functions
│   ├── alembic/          # Database migrations
│   ├── tests/            # Backend tests
│   ├── main.py           # FastAPI application entry
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Backend Docker configuration
├── frontend/
│   ├── src/
│   │   ├── app/          # App configuration (router, providers)
│   │   ├── components/   # React components
│   │   ├── context/      # React contexts
│   │   ├── hooks/        # Custom React hooks
│   │   ├── layouts/      # Page layouts
│   │   ├── lib/          # Utilities and constants
│   │   ├── pages/        # Page components
│   │   ├── services/     # API service layer
│   │   └── types/        # TypeScript types
│   ├── public/           # Static assets
│   ├── package.json      # Node dependencies
│   ├── vite.config.ts    # Vite configuration
│   └── Dockerfile        # Frontend Docker configuration
├── docker-compose.yml    # Docker Compose configuration
└── render.yaml           # Render deployment configuration
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TruthLens-AI
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   alembic upgrade head
   uvicorn main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   # Edit .env with your API URL
   npm run dev
   ```

### Using Docker Compose

```bash
docker-compose up -d
```

This will start:
- Backend API on http://localhost:8000
- Frontend on http://localhost:3000
- PostgreSQL database

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/truttlens
SECRET_KEY=your-secret-key
FRONTEND_URL=http://localhost:3000
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-email-password
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=TruthLens AI
VITE_APP_VERSION=1.0.0
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Main Endpoints

#### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get tokens
- `POST /api/auth/logout` - Logout (invalidate tokens)
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password

#### Predictions
- `POST /api/predictions/analyze` - Analyze text for fake news
- `POST /api/predictions/upload` - Upload and analyze file

#### Dashboard
- `GET /api/dashboard` - Get dashboard statistics

#### History
- `GET /api/history` - Get user's prediction history
- `DELETE /api/history/{id}` - Delete history item

#### Reports
- `GET /api/reports` - List reports
- `POST /api/reports/{prediction_id}` - Generate report
- `GET /api/reports/{id}` - Get specific report

#### User
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile
- `DELETE /api/users/me` - Delete account

#### Admin
- `GET /api/admin/users` - List all users
- `DELETE /api/admin/users/{id}` - Delete user
- `GET /api/admin/predictions` - List all predictions
- `GET /api/admin/analytics` - Get platform analytics

## Development

### Running Tests

Backend:
```bash
cd backend
pytest
```

Frontend:
```bash
cd frontend
npm test
```

### Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Deployment

### Docker

Build and run with Docker Compose:
```bash
docker-compose up -d --build
```

### Render

The project includes `render.yaml` for easy deployment on Render.com. Simply connect your repository and Render will automatically deploy both frontend and backend services.

### Manual Deployment

1. Deploy backend to a hosting service (Render, Railway, AWS, etc.)
2. Deploy frontend to a static hosting service (Vercel, Netlify, etc.)
3. Update frontend `VITE_API_BASE_URL` to point to backend URL
4. Update backend `FRONTEND_URL` to point to frontend URL

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the GitHub repository.

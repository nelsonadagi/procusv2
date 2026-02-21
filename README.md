# Construction Marketplace MVP

## Phase 1 Deliverable

A monorepo for the Construction Materials Marketplace.

### Structure
*   `frontend/`: Vue 3 + Vite app.
*   `backend/`: Django + DRF API.
*   `infra/`: Infrastructure configs.
*   `docs/`: Project documentation.

### Getting Started

1.  **Start the Stack**:
    ```bash
    docker-compose up --build
    ```

2.  **Access**:
    *   Frontend: http://localhost:5173
    *   Backend API: http://localhost:8000/api/v1/products/
    *   Admin: http://localhost:8000/admin/

### Development

*   **Backend**: `cd backend`
    *   `python manage.py runserver`
*   **Frontend**: `cd frontend`
    *   `npm run dev`

### Credentials

*   **Admin**: admin / adminpass
*   **Vendor**: vendor1 / vendorpass

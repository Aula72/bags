# Ugbags API Documentation

## 🚀 Quick Start

Swagger/OpenAPI documentation has been successfully integrated into the Ugbags API.

## 📚 Accessing the Documentation

### Swagger UI (Interactive Documentation)
Access the interactive API documentation at:
```
http://localhost:8000/swagger/
```
or 
```
http://localhost:8000/
```

**Features:**
- Interactive API explorer
- Try out API endpoints directly in the browser
- View request/response schemas
- Test authentication flows
- See example responses

### ReDoc (Alternative Documentation)
Access the ReDoc documentation at:
```
http://localhost:8000/redoc/
```

**Features:**
- Clean, modern documentation layout
- Better for reading and reference
- Three-panel design
- Search functionality

### OpenAPI Schema (JSON/YAML)
Download the raw OpenAPI schema:
- **JSON:** `http://localhost:8000/swagger.json`
- **YAML:** `http://localhost:8000/swagger.yaml`

Use these files for:
- Code generation
- API testing tools (Postman, Insomnia)
- CI/CD integration

## 📦 Installation

The required packages have been added to `requirements.txt`:
```bash
pip install -r requirements.txt
```

Required packages:
- `drf-yasg==1.21.7` - Swagger/OpenAPI generator
- `inflection==0.5.1` - String transformation (dependency)

## 🔧 Configuration

### Settings (bags/settings.py)
```python
INSTALLED_APPS = [
    ...
    'drf_yasg',  # Swagger/OpenAPI documentation
    ...
]
```

### URLs (bags/urls.py)
Documentation endpoints configured:
- `/swagger/` - Swagger UI
- `/redoc/` - ReDoc UI
- `/swagger.json` - JSON schema
- `/swagger.yaml` - YAML schema

## 📖 API Endpoints

### Main Endpoints:

| Endpoint | Description |
|----------|-------------|
| `/api/v1/` | API root with all endpoints |
| `/api/v1/bags/` | Bag listings |
| `/api/v1/shops/` | Shop management |
| `/api/v1/users/` | User management |
| `/api/v1/profiles/` | User profiles |
| `/api/v1/financial-accounts/` | Financial transactions |
| `/api/v1/login/` | User authentication |
| `/api/v1/logout/` | User logout |
| `/api/v1/register/` | User registration |
| `/api/v1/search/` | Search functionality |
| `/api/v1/contact/` | Contact messages |

## 🔑 Authentication

The API uses **Token Authentication**:

1. **Login** at `/api/v1/login/` with username and password
2. Receive an authentication token in response
3. Include token in subsequent requests:
   ```
   Authorization: Token <your-token-here>
   ```

### Testing Authentication in Swagger:
1. Click the **Authorize** button (lock icon) in Swagger UI
2. Enter: `Token <your-token>`
3. Click **Authorize**
4. Now you can test authenticated endpoints

## 🎯 Features

### API Documentation Includes:
- ✅ Complete endpoint documentation
- ✅ Request/response schemas
- ✅ Authentication requirements
- ✅ HTTP methods and status codes
- ✅ Query parameters and filters
- ✅ Request body examples
- ✅ Response examples
- ✅ Error responses

### View Docstrings:
All API views include detailed docstrings describing:
- Available operations (GET, POST, PUT, DELETE)
- Required permissions
- Request/response formats
- Special parameters

## 🧪 Testing APIs

### Using Swagger UI:
1. Navigate to `http://localhost:8000/swagger/`
2. Expand an endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"
6. View the response

### Using cURL:
```bash
# Get all bags
curl -X GET http://localhost:8000/api/v1/bags/

# Login
curl -X POST http://localhost:8000/api/v1/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'

# Create a bag (authenticated)
curl -X POST http://localhost:8000/api/v1/bags/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{"price":50000,"bag_type":"laptop",...}'
```

## 📝 Development Notes

### Adding Documentation to New Endpoints:
Add docstrings to your APIView classes:

```python
class MyView(APIView):
    """
    Brief description of the endpoint.
    
    get:
    Description of GET operation.
    
    post:
    Description of POST operation.
    """
    def get(self, request):
        # implementation
        pass
```

### Updating Documentation:
The Swagger documentation auto-generates from:
- View docstrings
- Serializer definitions
- URL patterns
- Permission classes

Changes to any of these will automatically reflect in the documentation.

## 🚀 Production Deployment

For production, consider:
1. Restricting documentation access:
   ```python
   permission_classes=(permissions.IsAdminUser,)
   ```

2. Disabling documentation entirely:
   ```python
   # Comment out swagger URLs in production
   ```

3. Using cached schema:
   ```python
   schema_view.with_ui('swagger', cache_timeout=3600)
   ```

## 🔗 Useful Links

- **drf-yasg Documentation:** https://drf-yasg.readthedocs.io/
- **OpenAPI Specification:** https://swagger.io/specification/
- **Django REST Framework:** https://www.django-rest-framework.org/

## 📞 Support

For issues or questions:
- Email: info@ugbags.com
- Check the logs for API errors
- Review the Swagger UI for endpoint details

---

**Last Updated:** April 2026
**API Version:** v1
**Framework:** Django REST Framework with drf-yasg

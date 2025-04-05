from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse

@api_view(['GET'])
@permission_classes([AllowAny])
def landing_page(request):
    html_content = """
    <html>
    <head>
        <title>Task Management API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            code { background: #f4f4f4; padding: 2px 5px; }
            pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>Task Management API</h1>
        <p>This API requires authentication. To use the API, you need to:</p>
        <ol>
            <li>Register a new user at <code>/api/auth/register/</code></li>
            <li>Get a JWT token at <code>/api/auth/login/</code></li>
            <li>Include the token in your requests as <code>Authorization: Bearer &lt;your_token&gt;</code></li>
        </ol>
        <h2>Example with curl:</h2>
        <pre>
# Register
curl -X POST http://localhost:8000/api/auth/register/ \\
  -H "Content-Type: application/json" \\
  -d '{"username":"testuser","password":"strong_password","password2":"strong_password","email":"test@example.com"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \\
  -H "Content-Type: application/json" \\
  -d '{"username":"testuser","password":"strong_password"}'

# Use API with token
curl http://localhost:8000/api/tasks/ \\
  -H "Authorization: Bearer &lt;your_token&gt;"
        </pre>
    </body>
    </html>
    """
    return HttpResponse(html_content)
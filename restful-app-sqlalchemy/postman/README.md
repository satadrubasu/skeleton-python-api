### Usage 

1. Environment variables {{jwt_token}}
   > Header: Authorization JWT {{jwt_token}}
2. Test Javascript to process the JSON response - JWT token.
 ```
// Capture access_token from response and update ENV variable
const responseJson = pm.response.json();
pm.environment.set("jwt_token", responseJson.access_token);
 ```
npx openapi-typescript "http://rest-api:8000/openapi?format=openapi-json" -o ../web-app/merchant/schemas/api-types.ts
npx openapi-typescript "http://rest-api:8000/openapi?format=openapi-json" -o ../web-app/storefront/schemas/api-types.ts
npx openapi-typescript "http://rest-api:8000/openapi?format=openapi-json" -o ../web-app/ops/schemas/api-types.ts
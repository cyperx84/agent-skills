---
name: api-doc-generator
description: >
  Automatically generates API documentation from code annotations, OpenAPI specs, or live endpoints. Creates interactive docs with examples, types, and error codes. Use when user needs API documentation. Triggers: generate API docs, create API documentation, document endpoints, API reference
license: MIT
metadata:
  author: cyperx
  version: "1.0.0"
  openclaw: true
  categories: [dev, dotfiles]
---


# API Doc Generator Skill

## Purpose

The API Doc Generator automates API documentation creation. Manually writing API docs is tedious - documenting every endpoint, parameter, response type, and error code. This skill scans your code, extracts API definitions, generates beautiful documentation, and keeps it synchronized with code changes.

## When to Use This Skill

Activate when the user:
- Needs to document API endpoints
- Wants to generate OpenAPI/Swagger specs
- Is creating API reference docs
- Needs to update outdated documentation
- Mentions keywords like: "API docs", "document endpoints", "generate swagger", "API reference"

## Workflow

### Phase 1: API Discovery

**Scan for API Definitions**:

```bash
# Detect API frameworks
detect_api_framework() {
  grep -q "express" package.json && echo "express"
  grep -q "fastapi" requirements.txt && echo "fastapi"
  grep -q "actix-web" Cargo.toml && echo "actix-web"
  grep -q "gin" go.mod && echo "gin"
}
```

**Extract Endpoints**:

```bash
# Parse routes from code
extract_express_routes() {
  grep -r "app\.\(get\|post\|put\|delete\)" . \
    --include="*.js" --include="*.ts" \
    | sed 's/.*\.\(get\|post\|put\|delete\)(\([^,]*\).*/\U\1\E \2/'
}
```

### Phase 2: Documentation Generation

**Generate OpenAPI Spec**:

```bash
generate_openapi() {
  cat > openapi.yaml << 'EOF'
openapi: 3.0.0
info:
  title: ${API_TITLE}
  version: 1.0.0
paths:
  /api/users:
    get:
      summary: List users
      responses:
        '200':
          description: Success
EOF
}
```

**Create Interactive Docs**:

```bash
# Generate Swagger UI
npm install swagger-ui-express
# Generate Redoc
npm install redoc-cli
```

### Phase 3: Example Generation

**Auto-generate Examples**:

```bash
create_examples() {
  # cURL examples
  echo "curl -X GET https://api.example.com/users"

  # Response examples
  echo '{"users": [{"id": 1, "name": "John"}]}'
}
```

## Guidelines

### DO:
✅ Extract from code comments
✅ Generate request/response examples
✅ Include error codes
✅ Keep docs synchronized with code
✅ Support multiple output formats

### DON'T:
❌ Generate docs without validation
❌ Skip error documentation
❌ Ignore deprecated endpoints

## Success Metrics

- ✅ All endpoints documented
- ✅ Examples included
- ✅ Types/schemas defined
- ✅ Error codes documented
- ✅ < 2 minutes generation time

## Version History

- v1.0.0 (2025-10-30): Initial release

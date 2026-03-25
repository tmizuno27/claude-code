# Database Designer Prompt

## Objective
Design a complete database schema for a SaaS application or data-driven project, including tables, relationships, indexes, and migration scripts.

## Required Context / Inputs
- Application description
- Key entities and relationships
- Database platform (Supabase/PostgreSQL, SQLite, MySQL)

## Prompt

```
Design a complete database schema for [APPLICATION].

**Application:**
- Name: [APP NAME]
- Description: [WHAT DOES IT DO]
- Platform: [Supabase (PostgreSQL) / SQLite / MySQL / Prisma]
- Key entities: [LIST MAIN OBJECTS - users, posts, products, orders, etc.]

**Generate:**

1. **Entity Relationship Diagram** (text-based):
   - All tables with columns, types, and constraints
   - Relationships (1:1, 1:N, N:M)
   - Foreign keys

2. **SQL Schema**:
   - CREATE TABLE statements
   - Indexes for common queries
   - Enum types where applicable
   - Row-level security policies (if Supabase)
   - Timestamps (created_at, updated_at) on all tables

3. **Seed Data**:
   - Sample INSERT statements for testing
   - Realistic example data

4. **Migration Script**:
   - Versioned migration file
   - Rollback script

5. **Query Examples**:
   - 5-10 common queries the app will need
   - Optimized with proper JOINs and indexes

**Output:**
- Save schema to [PROJECT]/database/schema.sql
- Save migrations to [PROJECT]/database/migrations/
- Save seed data to [PROJECT]/database/seed.sql

Application: [YOUR APP]
```

## Expected Output
- `database/schema.sql`, `database/migrations/`, `database/seed.sql`

## Tips
- Always include soft delete (deleted_at) for user-facing data
- Index columns used in WHERE, JOIN, and ORDER BY clauses
- Use UUIDs for public-facing IDs, serial integers for internal references

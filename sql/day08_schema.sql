
-- =====================================================
-- DAY 8: PGVECTOR WITH PERMISSION FILTERS
-- Project: FieldReady
-- PostgreSQL: 18.6
-- pgvector: 0.8.1
-- =====================================================

-- 1. Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create document chunks table
CREATE TABLE IF NOT EXISTS document_chunks (
    id BIGSERIAL PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    allowed_roles TEXT[] NOT NULL,
    source TEXT NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    content TEXT NOT NULL,
    embedding VECTOR(3) NOT NULL
);

-- 3. Insert sample document chunks
INSERT INTO document_chunks
(tenant_id, allowed_roles, source, content, embedding)
VALUES
(
    'tenant_A',
    ARRAY['admin', 'manager'],
    'HR_policy.pdf',
    'Company employee leave policy',
    '[0.1, 0.2, 0.3]'
),
(
    'tenant_A',
    ARRAY['employee'],
    'Employee_guide.pdf',
    'General employee guidelines',
    '[0.2, 0.3, 0.4]'
),
(
    'tenant_B',
    ARRAY['admin'],
    'Finance.pdf',
    'Confidential financial information',
    '[0.3, 0.4, 0.5]'
);

-- 4. Enable Row-Level Security
ALTER TABLE document_chunks
ENABLE ROW LEVEL SECURITY;

-- 5. Create restricted database role
-- Run only if the role does not already exist.
-- CREATE ROLE fieldready_employee LOGIN;

-- 6. Grant permissions
GRANT USAGE ON SCHEMA public TO fieldready_employee;
GRANT SELECT ON document_chunks TO fieldready_employee;

-- 7. Create tenant and role filtering policy
CREATE POLICY document_chunks_access_policy
ON document_chunks
FOR SELECT
TO fieldready_employee
USING (
    tenant_id = current_setting('app.tenant_id', true)
    AND allowed_roles @> ARRAY[
        current_setting('app.user_role', true)
    ]::TEXT[]
);

-- 8. Verify stored records
SELECT id, tenant_id, allowed_roles, source
FROM document_chunks;

-- 9. Verify RLS is enabled
SELECT relrowsecurity
FROM pg_class
WHERE relname = 'document_chunks';

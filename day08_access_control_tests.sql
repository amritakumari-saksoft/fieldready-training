
-- Day 8: pgvector Access Control Tests
-- Database: fieldready_db

-- Test 1: Employee access in tenant_A
SET app.tenant_id = 'tenant_A';
SET app.user_role = 'employee';

SELECT id, tenant_id, allowed_roles, source
FROM document_chunks;

-- Expected: Employee_guide.pdf only


-- Test 2: Manager access in tenant_A
SET app.user_role = 'manager';

SELECT id, tenant_id, source
FROM document_chunks;

-- Expected: HR_policy.pdf only


-- Test 3: Admin access in tenant_B
SET app.tenant_id = 'tenant_B';
SET app.user_role = 'admin';

SELECT id, tenant_id, source
FROM document_chunks;

-- Expected: Finance.pdf only


-- Test 4: Similarity search with RLS
SET app.tenant_id = 'tenant_A';
SET app.user_role = 'employee';

SELECT
    id,
    tenant_id,
    source,
    content,
    embedding <=> '[0.1, 0.2, 0.3]' AS distance
FROM document_chunks
ORDER BY embedding <=> '[0.1, 0.2, 0.3]'
LIMIT 5;


-- Test 5: Cross-tenant visibility check
SELECT COUNT(*)
FROM document_chunks
WHERE tenant_id = 'tenant_B';

-- Expected: 0 for tenant_A employee


-- Security finding:
-- Custom session settings are user-modifiable.
-- Trusted identity enforcement is still required.

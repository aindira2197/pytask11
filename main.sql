CREATE TABLE cache_store (
    id SERIAL PRIMARY KEY,
    function_name VARCHAR(255) NOT NULL,
    input_params JSONB NOT NULL,
    result JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION memoize(func_name text, input_params jsonb)
RETURNS jsonb AS $$
DECLARE
    cached_result jsonb;
BEGIN
    SELECT result INTO cached_result
    FROM cache_store
    WHERE function_name = func_name AND input_params = input_params;
    
    IF cached_result IS NOT NULL THEN
        RETURN cached_result;
    END IF;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION store_result(func_name text, input_params jsonb, result jsonb)
RETURNS VOID AS $$
BEGIN
    INSERT INTO cache_store (function_name, input_params, result)
    VALUES (func_name, input_params, result)
    ON CONFLICT (function_name, input_params) DO UPDATE
    SET result = EXCLUDED.result, updated_at = CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION cached_function(func_name text, input_params jsonb)
RETURNS jsonb AS $$
DECLARE
    cached_result jsonb;
    result jsonb;
BEGIN
    cached_result := memoize(func_name, input_params);
    
    IF cached_result IS NOT NULL THEN
        RETURN cached_result;
    END IF;
    
    result := (SELECT * FROM json_build_object('result', input_params->>'key'));
    
    PERFORM store_result(func_name, input_params, result);
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION example_function(input_params jsonb)
RETURNS jsonb AS $$
BEGIN
    RETURN (SELECT * FROM json_build_object('result', input_params->>'key'));
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION memoized_example_function(input_params jsonb)
RETURNS jsonb AS $$
BEGIN
    RETURN cached_function('example_function', input_params);
END;
$$ LANGUAGE plpgsql;

SELECT memoized_example_function('{"key": "value"}'::jsonb);
SELECT memoized_example_function('{"key": "value"}'::jsonb);
SELECT memoized_example_function('{"key": "new_value"}'::jsonb);

SELECT * FROM cache_store;
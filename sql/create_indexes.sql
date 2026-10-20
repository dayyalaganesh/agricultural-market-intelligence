-- PostgreSQL indexes for agricultural market intelligence.
-- Run this script after the mandi_prices table has been created and loaded.

CREATE INDEX IF NOT EXISTS idx_mandi_prices_market
    ON public.mandi_prices (market);

CREATE INDEX IF NOT EXISTS idx_mandi_prices_state
    ON public.mandi_prices (state);

-- Refresh planner statistics after creating indexes.
ANALYZE public.mandi_prices;

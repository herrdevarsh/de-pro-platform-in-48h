from stream.utils import record_to_df

def test_record_to_df_empty():
    assert record_to_df([]).empty

def test_record_to_df_basic():
    rec = [{"payload":{"after":{"id":1,"updated_at":"2025-01-01T00:00:00Z"}}}]
    df = record_to_df(rec)
    assert not df.empty

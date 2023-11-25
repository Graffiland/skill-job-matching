import extraction 
import transform
import load
import pytest

@pytest.mark.extraction
def test_extraction_data():
    result_s=extraction.extracted_survey()
    assert isinstance(result_s, dict)
    result_c=extraction.extracted_text()
    assert isinstance(result_c, str)
    
@pytest.mark.transform  
def test_transform_data():
    Transformcvobject = transform.Transformcv()
    Transformsurveyobject = transform.Transformsuvery()
    data="is the tranformed data in good format"
    result_tc= Transformcvobject.masking_on_data(data)
    assert isinstance(result_tc, str)
    result_ts=Transformsurveyobject.masking_on_data()
    assert isinstance(result_ts, dict)
    
    
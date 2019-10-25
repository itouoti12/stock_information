# -*- coding: utf-8 -*-

from main.pytest_selenium import target
import pytest
import requests

def test_access_success(requests_mock):

    # GIVEN
    mock_response = {

    }
    requests_mock.get('https://jp.kabumap.com/servlets/kabumap/Action?SRC=basic/top/base&codetext=7203', json=mock_response, status_code = 200)

    expected_response = {

    }

    expected_status = 200

    # WHEN
    executer = target
    actual_response = target()
    actual_status = actual_response.status_code

    # THEN  
    assert actual_status == expected_status
    assert actual_response == expected_response
    

'''Test mp3_to_dropbox.'''

import mock
from nose.tools import eq_

import mp3_to_dropbox as m2d

from datetime import (datetime, timedelta)


@mock.patch('__builtin__.open', new_callable=mock.mock_open)
@mock.patch('requests.get')
def test_download_mp3(m_get, m_open):
    '''Tests download_mp3.
       Mocks file open and request.get'''

    test_url = 'testurl'
    test_path = 'testpath'
    test_content = 'testcontent'

    # Mock content for requests.get()
    m_get.return_value = mock.Mock(content=test_content)
    m_get.content = test_content

    m2d.download_mp3(test_url, test_path)

    m_get.assert_called_with(test_url)
    m_open.assert_called_with(test_path, 'wb')
    m_file = m_open()
    m_file.write.assert_called_with(test_content)


def test_is_old():
    '''Test is_old.'''
    now = datetime.now()
    test_cases = (
        (now - timedelta(days=11), 10, True),
        (now - timedelta(days=2), 1, True),
        (now - timedelta(days=9), 10, False),
        (now - timedelta(days=0), 1, False),
    )
    for date, days, expected in test_cases:
        eq_(m2d.is_old(date, days), expected)

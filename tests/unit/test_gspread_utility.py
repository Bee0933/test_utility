# pylint: disable=import-error
import pytest
import sys
import os
import subprocess
from unittest.mock import patch, Mock
from ..utils.utils import subprocess_run

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXTRACT_SH_PATH = os.path.join(BASE_PATH, os.environ["BASH_SCRIPT_NAME"])
sys.path.insert(0, BASE_PATH)
from main import Workbook



print(BASE_PATH)

def test_bash_arguments() -> None:
    """_summary_
    Tests if bash file exists and is executable
    Tests bash script fails with bad arguments
    """

    # test executable bash script
    assert os.path.isfile(EXTRACT_SH_PATH) and os.access(EXTRACT_SH_PATH, os.X_OK)
    assert os.path.exists(EXTRACT_SH_PATH)

    # test for bad argument
    with pytest.raises(subprocess.CalledProcessError):
        # pylint: disable=implicit-str-concat
        bad_argument = ["2023", "2", "3"]
        result = subprocess_run(bad_argument)

        assert result.returncode == 1


@patch("subprocess.run")
def test_bash_download(mock_run):
    """_summary_
    Mock test that bash download script runs perfectly and retuens download path
    """

    # define mock result
    # pylint: disable=implicit-str-concat
    arguments = ["extract.sh" "2023", "2"]
    # define mock return value
    mock_return_value = subprocess.CompletedProcess(
        args=["bash", EXTRACT_SH_PATH, *arguments],
        returncode=0,
        stdout="./data/ny_taxi_data_2.parquet",
        stderr="",
    )
    mock_run.return_value = mock_return_value

    args = ["2023", "2"]
    result = subprocess_run(args)

    # check if successful run
    assert result.returncode == 0

    # check if standard output contains do download path
    assert "./data/ny_taxi_data_2.parquet" in result.stdout


# pylint: disable=unused-argument
@patch("main.gspread.authorize", return_value=Mock())
def test_class_instance(mock_authorize):
    """_summary_
    - Test data validation
    - Mock test client connection
    """
    # test input data instantiation
    workbook_test = Workbook("test_wb", "test_sh", "bestnyah7@gmail.com", "2023", "2")
    assert workbook_test.email == "bestnyah7@gmail.com"
    assert workbook_test.year == "2023"

    assert workbook_test.client is not None

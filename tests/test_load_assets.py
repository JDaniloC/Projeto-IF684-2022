from utils import direct_edges_from_csv_file, real_edges_from_csv_file
import pytest, csv, os
from faker import Faker

HEADER = ["from", "to", "cost"]
faker = Faker()

@pytest.fixture
def fixture_create_csv_file():
    remove_files = []
    def closure(path_file: str, content: list) -> str:
        """
        This function was created to be possible to call
        the fixture with arguments, and the remove_files
        list is used to remove the files created here.
        """
        with open(path_file, "w", newline = "") as file:
            writer = csv.writer(file)
            for row in content:
                writer.writerow(row)
        remove_files.append(path_file)
        return path_file
    
    yield closure

    remove_path = remove_files[0]
    if os.path.exists(remove_path):
        os.remove(remove_path)

@pytest.fixture
def fixture_receive_fake_edges() -> tuple:
    """
    Returns three fake stations and two fake costs.
    """
    first_station = faker.word()
    second_station = faker.word()
    third_station = faker.word()
    first_cost = faker.pyint(min_value = 0, max_value = 99)
    second_cost = faker.pyint(min_value = 0, max_value = 99)

    return first_station, second_station, third_station, first_cost, second_cost

def test_direct_edges_from_csv_file(fixture_create_csv_file, fixture_receive_fake_edges):
    """
    Tests the direct_edges_from_csv_file function.
    """
    first_station, second_station, third_station, \
    first_cost, second_cost = fixture_receive_fake_edges
    file_path = fixture_create_csv_file("test_direct_edges.csv", 
        [HEADER, [first_station, second_station, first_cost], 
        [second_station, third_station, second_cost]])
    direct_edges = direct_edges_from_csv_file(file_path)
    
    assert direct_edges == { 
        (first_station, second_station): float(first_cost), 
        (second_station, third_station): float(second_cost) 
    }

def test_real_edges_from_csv_file(fixture_create_csv_file, fixture_receive_fake_edges):
    """
    Tests the real_edges_from_csv_file function.
    """
    first_station, second_station, third_station, \
    first_cost, second_cost = fixture_receive_fake_edges

    file_path = fixture_create_csv_file("test_real_edges.csv", 
        [HEADER, [first_station, second_station, first_cost], 
        [second_station, third_station, second_cost]])
    real_edges = real_edges_from_csv_file(file_path)
    assert real_edges == { 
        first_station: [(second_station, float(first_cost))], 
        second_station: [
            (first_station, float(first_cost)), 
            (third_station, float(second_cost))
        ],
        third_station: [(second_station, float(second_cost))]
    }


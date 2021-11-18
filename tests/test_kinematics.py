import sys
sys.path.append("../")
from hexapod.models import VirtualHexapod
from kinematics_cases import case1, case2
from helpers import assert_hexapod_points_equal

CASES = [case1]


def assert_kinematics(case, assume_ground_targets):
    print("in create virturalHexapod")
    hexapod = VirtualHexapod(case.given_dimensions)
    #hexapod.update(case.given_poses, assume_ground_targets)
    # assert_hexapod_points_equal(
    #     hexapod, case.correct_body_points, case.correct_leg_points, case.description
    # )


def test_sample_kinematics():
    for case in CASES:
        assert_kinematics(case, True)
        assert_kinematics(case, False)

for case in CASES:
    assert_kinematics(case, True)
 

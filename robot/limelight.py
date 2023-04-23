"""
This file is open source.
It is a Python version of the limelight lib and
 a copy has been provided to ChiefDelphi and the Limelight team.
"""

import json
from dataclasses import dataclass
from enum import IntEnum
from functools import lru_cache
from typing import Sequence, cast

import ntcore
from wpimath.geometry import (
	Pose2d,
	Pose3d,
	Rotation2d,
	Rotation3d,
	Translation2d,
	Translation3d,
)
# from wpimath.units import degreesToRadians as radians
from math import radians

# The `cast` calls are no-ops at runtime but are a workaround for broken type hints in ntcore


def _ll_to_Pose3d(data: Sequence) -> Pose3d | None:
	if not data:
		return None
	return Pose3d(
		Translation3d(
			data[0],
			data[1],
			data[2],
			),
		Rotation3d(  # type: ignore
			radians(data[3]),
			radians(data[4]),
			radians(data[5]),
			),
	)


def _ll_to_Pose2d(data: Sequence) -> Pose2d | None:
	if not data:
		return None
	return Pose2d(
		Translation2d(
			data[0],
			data[1],
			),
		Rotation2d.fromDegrees(data[5]),
	)


@dataclass(frozen=True)
class LimelightTarget_Retro:
	# points: tuple[tuple[float, float]] # The example json has empty pts so idk what the format is
	ta: float
	tx: float
	ty: float
	txp: float
	typ: float
	camera_pose_in_target_space: Pose3d | None
	robot_pose_in_field_space: Pose3d | None
	robot_pose_in_target_space: Pose3d | None
	target_pose_in_camera_space: Pose3d | None
	target_pose_in_robot_space: Pose3d | None
	camera_pose_in_target_space_2D: Pose2d | None
	robot_pose_in_field_space_2D: Pose2d | None
	robot_pose_in_target_space_2D: Pose2d | None
	target_pose_in_camera_space_2D: Pose2d | None
	target_pose_in_robot_space_2D: Pose2d | None

	@staticmethod
	def from_limelight_json(data: dict) -> "LimelightTarget_Retro":
		return LimelightTarget_Retro(
			ta=data["ta"],
			tx=data["tx"],
			ty=data["ty"],
			txp=data["txp"],
			typ=data["typ"],
			camera_pose_in_target_space=_ll_to_Pose3d(data["t6c_ts"]),
			robot_pose_in_field_space=_ll_to_Pose3d(data["t6r_fs"]),
			robot_pose_in_target_space=_ll_to_Pose3d(data["t6r_ts"]),
			target_pose_in_camera_space=_ll_to_Pose3d(data["t6t_cs"]),
			target_pose_in_robot_space=_ll_to_Pose3d(data["t6t_rs"]),
			camera_pose_in_target_space_2D=_ll_to_Pose2d(data["t6c_ts"]),
			robot_pose_in_field_space_2D=_ll_to_Pose2d(data["t6r_fs"]),
			robot_pose_in_target_space_2D=_ll_to_Pose2d(data["t6r_ts"]),
			target_pose_in_camera_space_2D=_ll_to_Pose2d(data["t6t_cs"]),
			target_pose_in_robot_space_2D=_ll_to_Pose2d(data["t6t_rs"]),
		)


@dataclass(frozen=True)
class LimelightTarget_Fiducial:
	id: int
	family: str
	# points: tuple[tuple[float, float]] # The example json has empty pts so idk what the format is
	ta: float
	tx: float
	ty: float
	txp: float
	typ: float
	camera_pose_in_target_space: Pose3d | None
	robot_pose_in_field_space: Pose3d | None
	robot_pose_in_target_space: Pose3d | None
	target_pose_in_camera_space: Pose3d | None
	target_pose_in_robot_space: Pose3d | None
	camera_pose_in_target_space_2D: Pose2d | None
	robot_pose_in_field_space_2D: Pose2d | None
	robot_pose_in_target_space_2D: Pose2d | None
	target_pose_in_camera_space_2D: Pose2d | None
	target_pose_in_robot_space_2D: Pose2d | None

	@staticmethod
	def from_limelight_json(data: dict) -> "LimelightTarget_Fiducial":
		return LimelightTarget_Fiducial(
			id=data["id"],
			family=data["family"],
			ta=data["ta"],
			tx=data["tx"],
			ty=data["ty"],
			txp=data["txp"],
			typ=data["typ"],
			camera_pose_in_target_space=_ll_to_Pose3d(data["t6c_ts"]),
			robot_pose_in_field_space=_ll_to_Pose3d(data["t6r_fs"]),
			robot_pose_in_target_space=_ll_to_Pose3d(data["t6r_ts"]),
			target_pose_in_camera_space=_ll_to_Pose3d(data["t6t_cs"]),
			target_pose_in_robot_space=_ll_to_Pose3d(data["t6t_rs"]),
			camera_pose_in_target_space_2D=_ll_to_Pose2d(data["t6c_ts"]),
			robot_pose_in_field_space_2D=_ll_to_Pose2d(data["t6r_fs"]),
			robot_pose_in_target_space_2D=_ll_to_Pose2d(data["t6r_ts"]),
			target_pose_in_camera_space_2D=_ll_to_Pose2d(data["t6t_cs"]),
			target_pose_in_robot_space_2D=_ll_to_Pose2d(data["t6t_rs"]),
		)


@dataclass(frozen=True)
class LimelightTarget_Barcode:
	...

	@staticmethod
	def from_limelight_json(data: dict) -> "LimelightTarget_Barcode":
		return LimelightTarget_Barcode()


@dataclass(frozen=True)
class LimelightTarget_Detector:
	class_name: str
	id: int
	confidence: float
	# points: tuple[tuple[float, float]] # The example json has empty pts so idk what the format is
	ta: float
	tx: float
	ty: float
	txp: float
	typ: float

	@staticmethod
	def from_limelight_json(data: dict) -> "LimelightTarget_Detector":
		return LimelightTarget_Detector(
			class_name=data["class"],
			id=data["classID"],
			confidence=data["conf"],
			ta=data["ta"],
			tx=data["tx"],
			ty=data["ty"],
			txp=data["txp"],
			typ=data["typ"],
		)


@dataclass(frozen=True)
class LimelightTarget_Classifier:
	class_name: str
	id: int
	confidence: float

	@staticmethod
	def from_limelight_json(data: dict) -> "LimelightTarget_Classifier":
		return LimelightTarget_Classifier(
			class_name=data["class"],
			id=data["classID"],
			confidence=data["conf"],
		)


milliseconds = float


@dataclass(frozen=True)
class Results:
	pipeline_index: float
	targeting_latency: float
	timestamp: milliseconds
	is_valid: bool

	botpose: Pose3d | None
	botpose_wpired: Pose3d | None
	botpose_wpiblue: Pose3d | None

	botpose_2D: Pose2d | None
	botpose_wpired_2D: Pose2d | None
	botpose_wpiblue_2D: Pose2d | None

	retro_results: list[LimelightTarget_Retro]
	fiducial_results: list[LimelightTarget_Fiducial]
	barcode_results: list[LimelightTarget_Barcode]
	classifier_results: list[LimelightTarget_Classifier]
	detector_results: list[LimelightTarget_Detector]

	@staticmethod
	def from_limelight_json(data: dict) -> "Results":
		return Results(
			pipeline_index=data["pID"],
			targeting_latency=data["tl"],
			timestamp=data["ts"],
			is_valid=data["v"],
			botpose=_ll_to_Pose3d(data["botpose"]),
			botpose_wpired=_ll_to_Pose3d(data["botpose_wpired"]),
			botpose_wpiblue=_ll_to_Pose3d(data["botpose_wpiblue"]),
			botpose_2D=_ll_to_Pose2d(data["botpose"]),
			botpose_wpired_2D=_ll_to_Pose2d(data["botpose_wpired"]),
			botpose_wpiblue_2D=_ll_to_Pose2d(data["botpose_wpiblue"]),
			retro_results=[
				LimelightTarget_Retro.from_limelight_json(x) for x in data["Retro"]
				],
			fiducial_results=[
				LimelightTarget_Fiducial.from_limelight_json(x)
				for x in data["Fiducial"]
				],
			barcode_results=[],  # [LimelightTarget_Barcode.from_limelight_json(x) for x in data['Barcode']],
			classifier_results=[
				LimelightTarget_Classifier.from_limelight_json(x)
				for x in data["Classifier"]
				],
			detector_results=[
				LimelightTarget_Detector.from_limelight_json(x)
				for x in data["Detector"]
				],
		)


class LEDMode(IntEnum):
	PIPELINE_CONTROL = 0
	FORCE_OFF = 1
	FORCE_BLINK = 2
	FORCE_ON = 3


class StreamMode(IntEnum):
	STANDARD = 0
	PIP_MAIN = 1
	PIP_SECONDARY = 2


class Limelight:
	def __init__(self, name: str = "limelight"):
		self.name = name
		self.nt_table = ntcore.NetworkTableInstance.getDefault().getTable(self.name)

	def __repr__(self) -> str:
		return f"Limelight(name={self.name})"

	@property
	def pipeline_index(self) -> float:
		return cast(float, self.nt_table.getEntry("pipeline").getDouble(0))

	@pipeline_index.setter
	def pipeline_index(self, value: float) -> None:
		self.nt_table.getEntry("pipeline").setDouble(value)

	@property
	def led_mode(self) -> LEDMode:
		return LEDMode(self.nt_table.getEntry("ledMode").getDouble(0))

	@led_mode.setter
	def led_mode(self, value: LEDMode) -> None:
		self.nt_table.getEntry("ledMode").setDouble(int(value))

	@property
	def stream_mode(self) -> StreamMode:
		return StreamMode(self.nt_table.getEntry("stream").getDouble(0))

	@stream_mode.setter
	def stream_mode(self, value: StreamMode) -> None:
		self.nt_table.getEntry("stream").setDouble(int(value))

	@property
	def crop_window(self) -> tuple[tuple[float, float], tuple[float, float]]:
		arr = cast(list, self.nt_table.getEntry("crop").getDoubleArray([0, 0, 0, 0]))
		return ((arr[0], arr[1]), (arr[2], arr[3]))

	@crop_window.setter
	def crop_window(self, value: tuple[tuple[float, float], tuple[float, float]]) -> None:
		self.nt_table.getEntry("crop").setDoubleArray(
			[value[0][0], value[0][1], value[1][0], value[1][1]]
		)

	@property
	def json_dump(self) -> str | None:
		return self.nt_table.getEntry("json").getString(None) # type: ignore

	@lru_cache(maxsize=2)
	def _json_to_results(self, json_dump: str) -> Results:
		return Results.from_limelight_json(json.loads(json_dump)["Results"])

	@property
	def latest_results(self) -> Results | None:
		json_dump = self.json_dump
		if json_dump is None:
			return None
		return self._json_to_results(json_dump)

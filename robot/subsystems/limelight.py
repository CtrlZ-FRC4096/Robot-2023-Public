import math
from limelight import Limelight

detector_idx = 3
april_tags_idx = 1
retroreflective_idx = 2

class Limelight_Wrapper(Limelight):
	ll_mount_angle = 11.5
	ll_height = 9.75
	ll_yaw = 3.5
	ll_offset = 0 # not measured
	offset_from_shaft = 3

	def set_to_detector(self):
		self.pipeline_index = detector_idx

	def set_to_april_tags(self):
		self.pipeline_index = april_tags_idx

	def set_to_retroreflective(self):
		self.pipeline_index = retroreflective_idx

	@property
	def horizontal_double_pole_alignment(self) -> float | None:
		results = self.latest_results
		if not results:
			return None
		results = results.retro_results

		if not len(results) == 2:
			return None
		results.sort(key=lambda x: x.ty)
		lowest, highest = results
		return lowest.tx - highest.tx

	@property
	def angle_to_upper_pole(self) -> float | None:
		results = self.latest_results
		if not results:
			return None
		results = results.retro_results

		if not len(results) == 2:
			return None
		results.sort(key=lambda x: x.ty)
		highest = results[1]
		return highest.tx

	@property
	def distance_to_lower_pole(self) -> float | None:
		results = self.latest_results
		if not results:
			return None
		results = results.retro_results
		if not results:
			return None
		results.sort(key=lambda x: x.ta,reverse=True)
		lowest = results[0]
		angle = lowest.ty + self.ll_mount_angle
		angle = math.radians(angle)
		tape_height = 24
		return (tape_height - self.ll_height) / math.tan(angle) - self.offset_from_shaft + 3

	@property
	def lower_pole(self) -> tuple[float, float] | None:
		results = self.latest_results
		if not results:
			return None
		results = results.retro_results
		if not results:
			return None
		results.sort(key=lambda x: x.ta,reverse=True)
		lowest = results[0]
		angle = lowest.ty + self.ll_mount_angle
		angle = math.radians(angle)
		tape_height = 24
		return ((tape_height - self.ll_height) / math.tan(angle) - self.offset_from_shaft + 3, lowest.tx + self.ll_yaw)

	@property
	def distance_to_upper_pole(self) -> float | None:
		results = self.latest_results
		if not results:
			return None
		results = results.retro_results

		if not len(results) == 2:
			return None
		results.sort(key=lambda x: x.ty)
		highest = results[1]
		angle = highest.ty + self.ll_mount_angle
		angle = math.radians(angle)
		tape_height = 44
		return (tape_height - self.ll_height) / math.tan(angle)

	@property
	def angle_to_nearest_cone(self) -> float | None:
		results = self.latest_results
		if not results:
			return None
		results = results.detector_results

		results = [x for x in results if x.class_name == "cone"]
		if not results or not self.pipeline_index == 3:
			return None
		nearest = max(results,key=lambda x: x.ta)
		return nearest.tx

	@property
	def angle_to_nearest_cube(self) -> float | None:
		results = self.latest_results
		if not results:
			return None
		results = results.detector_results

		results = [x for x in results if x.class_name == "cube"]
		if not results or not self.pipeline_index == 3:
			return None
		nearest = max(results,key=lambda x: x.ta)
		return nearest.tx

	@property
	def angle_to_nearest_gamepiece(self) -> float | None:
		results = self.latest_results
		if not results:
			return None
		results = results.detector_results
		if not results or not self.pipeline_index == 3:
			return None
		nearest = max(results,key=lambda x: x.ta)
		return nearest.tx

	@property
	def angle_to_lower_pole(self) -> float | None:
		results = self.latest_results
		if not results:
			return None
		results = results.retro_results
		if not results:
			return None
		results.sort(key=lambda x: x.ta,reverse=True)
		lowest = results[0]
		return lowest.tx


	@property
	def area_of_nearest_cone(self) -> float | None:
		results = self.latest_results
		if not results:
			return None
		results = results.detector_results
		results = [x for x in results if x.class_name == "cone"]
		if not results or not self.pipeline_index == 3:
			return None
		nearest = max(results,key=lambda x: x.ta)
		return nearest.ta
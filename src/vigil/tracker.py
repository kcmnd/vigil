import math
from enum import Enum

from vigil.models import Observation, Vec2

MAX_TENTATIVE_SCANS = 5
MAX_MISSING_SCANS = 5
MAX_DISTANCE = 10  # meters


class TrackStatus(Enum):
    TENTATIVE = "tentative"
    CONFIRMED = "confirmed"
    LOST = "lost"


class Track:
    def __init__(self, first_observation: Observation):
        """initializes a new `Track` object

        Args:
            first_observation (Observation): the first time this object has been detected
        """
        # list of observations associated with this track/object
        self.observations = [first_observation]
        # how many scans it's been since first detection
        self.scans_elapsed = 1
        # the scan this track was last detected on
        self.last_detection_scan = 1
        # the status of this track: TENTATIVE, CONFIRMED, LOST
        self.status = TrackStatus.TENTATIVE

    def increment_scans(self):
        """increments the `scans_elapsed` attribute. call this on all tracks with every scan, and ALWAYS before `detect`"""
        self.scans_elapsed += 1

    def should_delete(self) -> bool:
        """checks if a track should be deleted

        call this method only if there are no observations associated with this track

        Returns:
            True if the track should be deleted, False otherwise
        """
        return (
            self.status == TrackStatus.TENTATIVE
            and self.scans_elapsed >= MAX_TENTATIVE_SCANS
            and len(self.observations) < 2
        )

    def is_lost(self) -> bool:
        """checks if a track is lost

        Returns:
            True if the track has been lost, False otherwise
        """
        if (
            self.status == TrackStatus.CONFIRMED
            and (self.scans_elapsed - self.last_detection_scan) >= MAX_MISSING_SCANS
        ):
            self.status = TrackStatus.LOST

        return self.status == TrackStatus.LOST

    def detect(self, new_observation: Observation):
        """updates list of observations and last_detection_scan

        Args:
            new_observation (observation): the newest observation associated with this track
        """
        self.observations.append(new_observation)
        self.last_detection_scan = self.scans_elapsed

        if self.status == TrackStatus.TENTATIVE and len(self.observations) >= 2:
            self.status = TrackStatus.CONFIRMED


class Tracker:
    def __init__(self):
        self.tracks: dict[str, Track] = {}
        # tracks are numbered 0, 1, 2, ... in the order they're created
        self._next_id = 0

    def update(self, new_observations: list[Observation]):
        if not self.tracks:  # no existing tracks to associate observations with
            for new_obs in new_observations:
                self._add_track(new_obs)
            return

        updated_tracks: dict[str, Observation] = {}
        new_tracks: list[Observation] = []

        for new_observation in new_observations:
            closest_track_id = None
            closest_distance = 0.0

            for track_id, track in self.tracks.items():
                if track_id in updated_tracks:
                    continue

                current_obs = track.observations[-1]
                distance = self._find_difference(current_obs.position, new_observation.position)

                # too far away: don't associate with this track, even if it's the closest
                if distance >= MAX_DISTANCE:
                    continue

                if closest_track_id is None or distance < closest_distance:
                    closest_track_id = track_id
                    closest_distance = distance

            if closest_track_id is not None:
                updated_tracks[closest_track_id] = new_observation
            else:
                new_tracks.append(new_observation)

        expired_tracks = []

        for track_id, track in self.tracks.items():
            track.increment_scans()  # always increment scans

            if track_id in updated_tracks:
                track.detect(updated_tracks[track_id])
                continue

            if track.should_delete():
                expired_tracks.append(track_id)

        for track_id in expired_tracks:
            del self.tracks[track_id]

        if new_tracks:  # some new observations need to start their own track
            for obs in new_tracks:
                self._add_track(obs)

    def _add_track(self, obs: Observation):
        """adds a new track to `self.tracks`"""
        self.tracks[str(self._next_id)] = Track(obs)
        self._next_id += 1

    def _find_difference(self, a: Vec2, b: Vec2) -> float:
        """finds the difference between two positions"""
        d_x = a.x - b.x
        d_y = a.y - b.y
        return math.sqrt((d_x**2) + (d_y**2))

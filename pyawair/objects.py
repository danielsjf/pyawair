
#!/usr/bin/env python3
# coding=utf-8
# author: @netmanchris
# -*- coding: utf-8 -*-

from pyawair.data import get_current_air_data
from pyawair.data import get_all_devices
import datetime

class AwairDev:
    def __init__(self, device_name, auth, cache_time = 15):
        self._auth = auth
        self._cache_time = cache_time
        self._last_update = datetime.datetime.now()  # records the last update

        self._device_name = device_name

        # Get device type and ID from name
        devices = get_all_devices(self._auth)
        self._type = next((item for item in devices if item["name"] == device_name),
                          False)['deviceType']  # get the device type
        self._id = next((item for item in devices if item["name"] == device_name),
                        False)['deviceId']  # get the device ID

        # Initiate data fields
        self._data = {}
        self._last_update = None

        self.refresh()

    def get_state(self, indicator: str) -> float:
        """
        Function to get the state of a specific indicator.

        The values are cached, in accordance with the cache time that is set for the object.

        :param indicator: A string containing one of the values from: score, temp, humid, co2, voc or dust.
        :return: The value of the specific indicator.
        """
        now = datetime.datetime.now()
        delta_min = (now - self._last_update).total_seconds() / 60
        if delta_min > self._cache_time:
            self.refresh()
        return(self._data[indicator])

    def refresh(self) -> object:
        """
        Function to refresh the state of the objects.

        The values are cached internally for the period equal to the cache
        time value. The refresh function refreshed these values, independent of the time that has past since the last
        refresh.

        :return: The object itself.
        """
        current_data: list = get_current_air_data(self._auth, device_id=self._id, device_type=self._type)
        self._data['score'] = current_data[0]['score']
        self._data['temp'] = current_data[0]['sensors'][0]['value']
        self._data['humid'] = current_data[0]['sensors'][1]['value']
        self._data['co2'] = current_data[0]['sensors'][2]['value']
        self._data['voc'] = current_data[0]['sensors'][3]['value']
        self._data['dust'] = current_data[0]['sensors'][4]['value']
        self._last_update = datetime.datetime.now()  # records the time of the last update


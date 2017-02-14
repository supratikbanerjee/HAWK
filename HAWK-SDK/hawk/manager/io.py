# Copyright (C) 2017 HAWK-OS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Supratik Banerjee(drakula941)


import pygame
from pygame.locals import *
from hardware_abstract_layer.pwm import ControlInputToPWM


class InputControlManager:
    def __init__(self):
        self.servo_move = 0
        self.percentage_full_range = 0
        self.percentage_mid_range = 0
        self.pwm = 0
        self.ToPWM = ControlInputToPWM()

    def set_exponential_dual_rate(self, exponential_value, dual_rate_value, percentage, bit_precision):
        """ Defining relationship between expo and dual rates."""
        if bit_precision == 4:  # subtract by mid value of the percentage
            percentage -= 5  # since it oscillates between -1 to 1
            percentage *= 2  # multiply to get percentage change
            percentage /= 10.  # divide to get the percentage for 4-bit
        elif bit_precision == 8:
            percentage -= 50  # the same concept as above implies for 8 bit
            percentage *= 2  # values adjusted for 1-99 range
            percentage /= 100.

        self.servo_move = (((abs(percentage) == percentage) * 2) - 1) * (
            abs(percentage) ** (4 ** (exponential_value / 100))) * (dual_rate_value / 100)
        return self.servo_move

    def input_percentage_full_range(self, device_input, threshold):
        """Movement of servo or motor from 0-100 with 0 as starting point"""
        if device_input < threshold:  # ideally -0.15 or 0.15
            self.percentage_full_range = int((abs(device_input) * 10))
        else:
            self.percentage_full_range = 0
        return self.percentage_full_range

    def input_percentage_mid_range(self, device_input, threshold):
        """Movement of servo or motor from 0-50-100 where 50 (mid) is the starting point."""
        if device_input < -threshold:
            self.percentage_mid_range = 5 - int((abs(device_input) * 9) / 2)
        elif device_input > threshold:
            self.percentage_mid_range = int((abs(device_input) * 9) / 2) + 5
        else:
            self.percentage_mid_range = 5
        return self.percentage_mid_range

    def invert_controller_input(self, device_input):
        return int(10 - device_input)


class InputDeviceManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("H.A.W.K")
        self.clock = pygame.time.Clock()

        self.olx = 0
        self.oly = 0

        self.orx = 0
        self.ory = 0

        self.ort = 0
        self.olt = 0

        self.ot = 0

        self.button_state = 'up'

        self.joysticks = []

        self.event = pygame.event.get()

    # def get_event_type(self, event):
    #     return event.type

    def get_device(self):
        for i in range(0, pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
            # print(joysticks[i])
            self.joysticks[-1].init()  # (to do) initialize the specified joystick
            return str(self.joysticks[-1].get_name())  # (to do) return the specified joystick
            # print("Detected joystick '", joysticks[-1].get_name(), "'")

    def get_event(self):
        self.event = pygame.event.get()
        return self.event

    def get_l_x_axis(self, event):
        x = self.olx
        if event.type == JOYAXISMOTION:
            # print("Joystick '", joysticks[-1].get_name(), "' axis", event.axis, "motion.")
            if event.axis == 0:  # left - right stick 1
                x = event.value
                self.olx = x
        return x

    def get_l_y_axis(self, event):
        y = self.oly
        if event.type == JOYAXISMOTION:
            # print("Joystick '", joysticks[-1].get_name(), "' axis", event.axis, "motion.")
            if event.axis == 1:  # left - right stick 1
                y = event.value
                self.oly = y
        return y

    def get_r_x_axis(self, event):
        x = self.orx
        if event.type == JOYAXISMOTION:
            #  print("Joystick '", joysticks[-1].get_name(), "' axis", event.axis, "motion.")
            if event.axis == 4:  # left - right stick 2
                x = event.value
                self.orx = x
        return x

    def get_r_y_axis(self, event):
        y = self.ory
        if event.type == JOYAXISMOTION:
            # print("Joystick '", joysticks[-1].get_name(), "' axis", event.axis, "motion.")
            if event.axis == 3:  # left - right stick 2
                y = event.value
                self.ory = y
        return y

    def get_r_trigger(self, event):
        rt = self.ort
        if event.type == JOYAXISMOTION:
            # print("Joystick '", joysticks[-1].get_name(), "' axis", event.axis, "motion.")
            if event.axis == 2:
                rt = event.value
                if rt < -0.1:
                    self.ort = rt
                else:
                    rt = self.ort
        return rt

    def get_l_trigger(self, event):
        lt = self.olt
        if event.type == JOYAXISMOTION:
            # print("Joystick '", joysticks[-1].get_name(), "' axis", event.axis, "motion.")
            if event.axis == 2:
                lt = event.value
                if lt > 0.1:
                    self.olt = lt
                else:
                    lt = self.olt
        return lt

    def get_triggers(self, event):
        bt = self.ot
        if event.type == JOYAXISMOTION:
            if event.axis == 2:
                bt = event.value
                self.ot = bt
        return self.ot

    def get_button_state(self, event, button):
        state = self.button_state
        if event.type == JOYBUTTONDOWN:
            if event.button == button:  # checks whether the button used in event is button pressed.
                state = 'down'
                self.button_state = state
        elif event.type == JOYBUTTONUP:
            if event.button == button:
                state = 'up'
                self.button_state = state
        return state

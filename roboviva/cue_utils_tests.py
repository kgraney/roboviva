# Roboviva - Better cue sheets for everyone
# Copyright (C) 2015 Mike Kocurek
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import cue
import cue_utils

def CheckDistances(route):
  for index, entry in enumerate(route.entries[0:-1]):
    next_entry = route.entries[index + 1]
    if (next_entry.absolute_distance != entry.absolute_distance + entry.for_distance):
      print "Error: %s -> %s (%s, %s)" % (entry, next_entry, index, index + 1)
      print route
      return False
  return True

def MakeRoute():
  entries = [ cue.Entry(cue.Instruction.RIGHT, "Start of route", 0.0, for_distance = 1.0),
              cue.Entry(cue.Instruction.RIGHT, "Entry 1", 1.0, for_distance = 0.5),
              cue.Entry(cue.Instruction.RIGHT, "Entry 2", 1.5, for_distance = 2.5),
              cue.Entry(cue.Instruction.RIGHT, "Entry 3", 4.0, for_distance = 1.0),
              cue.Entry(cue.Instruction.RIGHT, "Entry 4", 5.0, for_distance = 3.0),
              cue.Entry(cue.Instruction.RIGHT, "End of route", 8.0)]
  return cue.Route(entries, 8.0, 12345, "Test Route", 1000)

class CueUtilsTestCase(unittest.TestCase):
  '''Tests for the cue_utils library'''

  def test_AdjustStartAndEnd_startOnly(self):
    kStartDescription = "foo"
    kStartIndex = 3
    route = MakeRoute()
    route.entries[kStartIndex].description = kStartDescription
    route.entries[kStartIndex].instruction = 'start'

    cue_utils.AdjustStartAndEnd(route)
    self.assertEqual(5, len(route.entries))
    self.assertEqual(kStartDescription, route.entries[0].description)
    self.assertEqual(0.0, route.entries[0].absolute_distance)
    self.assertEqual(route.entries[1].absolute_distance, route.entries[0].for_distance)
    self.assertEqual(cue.Instruction.NONE, route.entries[0].instruction)
    self.assertTrue(CheckDistances(route))

  def test_AdjustStartAndEnd_endOnly(self):
    kEndDescription = "foo"
    kEndIndex = 3
    route = MakeRoute()
    kRouteLength = route.entries[-1].absolute_distance
    route.entries[kEndIndex].description = kEndDescription
    route.entries[kEndIndex].instruction = 'end'

    cue_utils.AdjustStartAndEnd(route)
    self.assertEqual(5, len(route.entries))
    self.assertEqual(kEndDescription, route.entries[-1].description)
    self.assertTrue(CheckDistances(route))
    self.assertEqual(kRouteLength, route.entries[-1].absolute_distance)
    self.assertEqual(None, route.entries[-1].for_distance)
    self.assertEqual(cue.Instruction.NONE, route.entries[-1].instruction)

if __name__ == '__main__':
  unittest.main()

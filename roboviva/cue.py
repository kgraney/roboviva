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

import csv
import enum

'''The action a particular cue entry represents'''
Instruction = enum.Enum(LEFT        = "L",
                        RIGHT       = "R",
                        STRAIGHT    = "S",
                        PIT         = "PIT",
                        DANGER      = "!",
                        CROSSES     = "X",
                        CAT_HC      = "CHC",
                        CAT_1       = "C1",
                        CAT_2       = "C2",
                        CAT_3       = "C3",
                        CAT_4       = "C4",
                        CAT_5       = "C5",
                        SUMMIT      = "^",
                        FIRST_AID   = "+",
                        NONE        = "")

'''An instruction modifier. Only really makes sense for LEFT and RIGHT, at the moment'''
Modifier = enum.Enum(NONE   = "",
                     SLIGHT = "B",
                     QUICK  = "Q")

'''The background color this cue entry should have'''
Color = enum.Enum(NONE = "None",
                  GRAY = "Gray",
                  YELLOW = "Yellow")

def ColorFromInstruction(instruction):
  '''
  Given a cue.Instruction, return the cue.Color associated with it.
  '''
  if instruction in (Instruction.PIT, Instruction.DANGER):
    return Color.YELLOW
  elif instruction in (Instruction.RIGHT):
    return Color.GRAY
  else:
    return Color.NONE

class Entry(object):
  '''Simple storage class representing a single cue sheet entry. Nothing fancy.'''
  def __init__(self,
              instruction,
              description,
              absolute_distance,
              note         = "",
              modifier     = Modifier.NONE,
              for_distance = None,
              color        = Color.NONE):
    ''' Inits a CueEntry.
        instruction       - The entry's Instruction (see above)
        description       - The entry's 'action' (e.g., 'Turn right on Pine St')
        absolute_distance - How far this entry is from the ride's start (miles)
        note              - Optional. Any additional notes on this entry.
        modifier          - Optional. A Modifier to apply to the Instruction.
        for_distance      - Optional. How long from this entry to the next entry.
        color             - Optional. The color of this cue entry.
    '''
    self.instruction       = instruction
    self.description       = description
    self.absolute_distance = float(absolute_distance)
    self.note              = note
    self.modifier          = modifier
    self.for_distance      = for_distance
    self.color             = color

  def __repr__(self):
    for_str = ""
    if self.for_distance:
      for_str = "%5.2f" % self.for_distance
    else:
      for_str = "     "

    return "Entry[%s%s | %5.2f | %s | %s | %s | %s]" % (self.modifier,
                                                   self.instruction,
                                                   self.absolute_distance,
                                                   for_str,
                                                   self.description,
                                                   self.note,
                                                   self.color)

class Route(object):
  '''Simple storage class representing a route. This is just a list of Entrys,
  plus some metadata (title, route #, etc.)'''
  def __init__(self,
               entries,
               length_mi,
               route_id,
               route_name = None,
               elevation_gain_ft = None):
    '''
      Inits the storage members of the class:

      - entries:      A list of Entry objects
      - length_mi:    The total length of the route, in miles.
      - route_id:     The RWGPS route # for this route
      - route_name:   The name of this route (Optional)
      - elevation_gain_ft : The amount of climb in this route, in ft (Optional)
    '''
    self.name    = route_name
    self.id      = route_id
    self.entries = entries
    self.elevation_gain_ft = elevation_gain_ft
    self.length_mi = length_mi

  def __repr__(self):
    ret = ""
    ret += "Route:\n"
    ret += "  Name:  \"%s\"" % self.name
    ret += "  Id:    %s" % self.id
    ret += "  Climb: %s ft" % self.elevation_gain_ft
    ret += "  Length: %s mi\n" % self.length_mi
    for entry in self.entries:
      ret += "    %s\n" % entry
    return ret

class SettingsItem(object):
    TYPE = str

    def __init__(self, name, short, default, description, advanced=False):
        self.name = name
        self.short = short
        self.default = default
        self.description = description
        self.advanced = advanced

    def to_dict(self):
        return {
            'name': self.name,
            'short': self.short,
            'default': self.default,
            'description': self.description,
            'advanced': self.advanced}


class RangeSettingFloat(SettingsItem):
    TYPE = float

    def __init__(self, name, short, default, description, low, high, step, advanced=False):
        super(RangeSettingFloat, self).__init__(name, short, default, description, advanced)
        self.low = low
        self.high = high
        self.step = step

    def to_dict(self):
        d = super(RangeSettingFloat, self).to_dict()
        d.update({'low': self.low, 'high': self.high, 'step': self.step})
        return d

    @staticmethod
    def convert(val):
        return float(val)


class RangeSettingInt(RangeSettingFloat):
    TYPE = int

    @staticmethod
    def convert(val):
        return int(val)


class BoolSetting(SettingsItem):
    TYPE = bool

    @staticmethod
    def convert(val):
        if isinstance(val, bool):
            return val
        return str(val).upper() in ['TRUE', '1', 'T', 'Y', 'YES']


# All measurements are in mm
def cm(v):
    return v * 10


def um(v):
    return v / 1000.0


DEFAULT_SETTINGS = [
    ('Geometry',
     [
         RangeSettingFloat('scale', 'Scale', 1.0, low=0.1, high=10.0, step=0.1,
                           description='Scaling factor for input geometry'),
         RangeSettingFloat('roundOffError', 'Round-off error', um(20), low=um(1), high=um(100), step=um(1),
                           description='Merging area of vertices', advanced=True),
         # RangeSettingInt('positionMinX', 'Min X', 0, low=0, high=500, step=1,
         # description='Min X position on plate'),
         # RangeSettingInt('positionMinY', 'Min Y', 0, low=0, high=500, step=1, description='Min Y position on plate')
     ]
     ),
    ('Printer',
     [
         RangeSettingInt('printPlateWidth', 'Plate width', 200, low=0, high=500, step=1, description='Plate width'),
         RangeSettingInt('printPlateLength', 'Plate length', 200, low=0, high=500, step=1, description='Plate length'),
         RangeSettingFloat('nozzleDiameter', 'Nozzle diameter', default=0.35, low=0.1, high=1.0, step=0.01,
                           description='Nozzle diameter'),
         RangeSettingFloat('filamentDiameter', 'Filament diameter', default=3.0, low=0.1, high=5.0, step=0.01,
                           description='Filament diameter'),
         RangeSettingInt('nozzleTemperature', 'Nozzle temperature', default=236, low=0, high=300, step=1,
                         description='Nozzle temperature'),
         RangeSettingInt('bedTemperature', 'Bed temperature', 90, low=0, high=150, step=1,
                         description='Bed temperature'),
         RangeSettingFloat('layerHeight', 'Layer height', 0.30, low=0.1, high=1.0, step=0.01,
                           description='Layer height'),
         RangeSettingFloat('extrusionWidth', 'Exstrusion width', 0.35, low=0.1, high=1.0, step=0.01,
                           description='Extrusion width'),
         RangeSettingFloat('correctionZ', 'Z correction', 0, low=0, high=10, step=0.01, description='Z correction'),
     ]
     ),
    ('Infill',
     [
         # includes contour
         RangeSettingInt('offsetsNr', 'Offsets nr', default=3, low=0, high=10, step=1,
                         description='Number of offsets (including perimeter)'),  # infill
         RangeSettingFloat('offsetsDelta', 'Offsets delta', default=0, low=0, high=1.0, step=0.01,
                           description='Empty space between offsets'),  # infill; + extrusionWidth
         # number of offsets that have to be feasible inside of contour so that line infill is performed
         RangeSettingInt('offsetsMinNrForLines', 'Min nr offsets for lines', default=2, low=1, high=10, step=1,
                         description='Minimum amount of offsets that has to fit into the most inner offset to create a line infill inside it',
                         advanced=True),
         # infill

         BoolSetting('linesEnable', 'Enable line infill', default=True, description='Enable lines inner pattern'),
         # infll
         # extra spacing between tvo extrusion lines
         RangeSettingFloat('linesDelta', 'Lines delta', default=0.2, low=0.0, high=5.0, step=0.1,
                           description='Spacing between lines'),  # + extrusionWidth # infll
         # When connecting lines of line infill - how long is max acceptable connection (factor * lineInfillSpacing)
         RangeSettingFloat('linesConnectionDistFactor', 'Lines connection distance factor', default=2.0, low=0.0,
                           high=5.0, step=0.1,
                           description='Factor of line spacing between two consecutive lines are connected with extruded filament'),
         # infll
         # 0 - never rotate, 1 - rotate every layer
         RangeSettingInt('linesNrLayersForRotation', 'Nr layers for lines rotation', default=2, low=0, high=10,
                         step=1,
                         description='How many consecutive layers have the same rotation'),
         # infll
         RangeSettingInt('linesRotationTheta', 'Lines rotation degrees', default=30, low=0, high=180, step=1,
                         description='The degree of rotation'),  # infll
     ]
     ),
    ('Support',
     [
         RangeSettingFloat('skirtsInitialDelta', 'Skirts initial delta', default=7, low=0, high=30, step=0.1,
                           description='Spacing between skirts and AABB of the model'),
         RangeSettingInt('skirtsOffsetsNr', 'Skirts nr of offsets', default=2, low=0, high=5, step=1,
                         description='Number of skirt offsets'),
         RangeSettingInt('skirtsLayers', 'Skirts nr layers', default=1, low=0, high=5, step=1,
                         description='How high should skirts be'),
     ]
     ),
    ('G-Code',
     [
         RangeSettingFloat('extrusionMultiplier', 'Exstrusion multiplier', default=1.0, low=0.1, high=2.0,
                           step=0.01,
                           description='By how much should the calculated extruded filament be multiplied'),
         RangeSettingInt('speedOffsets', 'Speed offsets', default=1260, low=100, high=10000, step=1,
                         description='Speed of printing offsets'),
         RangeSettingInt('speedContours', 'Speed contours', default=1800, low=100, high=10000, step=1,
                         description='Speed of printing contours'),
         RangeSettingInt('speedLines', 'Speed lines', default=3600, low=100, high=10000, step=1,
                         description='Speed of printing lines'),
         RangeSettingInt('speedTravel', 'Speed travel', default=7800, low=100, high=10000, step=1,
                         description='Speed of travel'),
         RangeSettingInt('speedSupports', 'Speed supports', default=3600, low=100, high=10000, step=1,
                         description='Speed of printing supports'),
         RangeSettingFloat('speedModifierLayers', 'Speed modifier layers', default=1.0, low=0.01, high=10.0,
                           step=0.1,
                           description='For how many layers should speed modifier be used'),
         RangeSettingFloat('speedModifier', 'Speed modifier', default=0.70, low=0.1, high=1.0, step=0.1,
                           description='Speed modifier'),

         # 0 - no retracts
         RangeSettingFloat('retractLength', 'Retract length', default=0.2, low=0.0, high=5.0, step=0.1,
                           description='Length of retraction'),
         RangeSettingFloat('spitLength', 'Spit length', default=0.01, low=0.0, high=5.0, step=0.1,
                           description='Length of contra retraction'),

         BoolSetting('retractEachLayer', 'Retract each layer', default=True,
                     description='Should retract on the beggining of each layer'),
         BoolSetting('retractEachPath', 'Retract each path', default=False,
                     description='Should retract for each path'),
         BoolSetting('retractFirstPath', 'Retract first path', default=False,
                     description='Should retract for the first path of pattern'),
         BoolSetting('verbose', 'Verbose', default=True,
                     description='Add comments to commands'),
     ]
     )
]


def settings_iter():
    for group in DEFAULT_SETTINGS:
        for prop in group[1]:
            yield group[0], prop


def create_reverse_map():
    d = {}
    for group_key, prop in settings_iter():
        d[prop.name] = group_key
    return d


def create_settings_dict():
    d = {}
    for group_key, prop in settings_iter():
        d.setdefault(group_key, {})
        d[group_key][prop.name] = prop
    return d


DEFAULT_SETTINGS_GROUPS_REVERSE = create_reverse_map()
DEFAULT_SETTINGS_DICT = create_settings_dict()

DEFAULT_SETTINGS_CONFIG = [(group[0], [prop.to_dict() for prop in group[1]]) for group in DEFAULT_SETTINGS]


class SlicerSettings(object):
    def __init__(self, settings=None):
        self._settings = {}

        for group_key, prop in settings_iter():
            self._settings[prop.name] = prop.convert(prop.default)

        if settings:
            self.load(settings, '{key}')

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        if key in DEFAULT_SETTINGS_GROUPS_REVERSE:
            self[key] = value
        else:
            return object.__setattr__(self, key, value)

    def __getitem__(self, item):
        return self._settings[item]

    def __setitem__(self, key, value):
        prop = DEFAULT_SETTINGS_DICT[DEFAULT_SETTINGS_GROUPS_REVERSE[key]][key]
        self._settings[key] = prop.convert(value)

    def load(self, form, form_key_str='{group}[{key}]'):
        for name, group_key in DEFAULT_SETTINGS_GROUPS_REVERSE.items():
            form_key = form_key_str.format(group=group_key, key=name)
            f_val = form.get(form_key)
            if f_val is not None:
                self[name] = f_val

    def to_dict(self):
        d = {}
        for group_key, prop in settings_iter():
            d.setdefault(group_key, {})
            d[group_key].setdefault(prop.name, {})
            d[group_key][prop.name] = self[prop.name]
        return d

    def __repr__(self):
        return self._settings.__repr__()

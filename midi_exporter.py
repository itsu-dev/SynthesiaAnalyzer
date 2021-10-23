import pretty_midi


class MIDIExporter:
    def __init__(self, filename, tempo):
        self.filename = filename
        self.pm = pretty_midi.PrettyMIDI(resolution=960, initial_tempo=tempo)
        self.instruments = {}

    def create_instrument(self, channel, program=1, name=''):
        if channel not in self.instruments.keys():
            self.instruments[channel] = pretty_midi.Instrument(is_drum=False, program=program, name=name)
            self.pm.instruments.append(self.instruments[channel])

    def append_note(self, channel, velocity, pitch, start, end):
        pitch = pitch.replace('s', '#')
        pitch = pitch[0:len(pitch) - 1] + str(int(pitch[len(pitch) - 1:len(pitch)]) + 1)
        note_number = pretty_midi.note_name_to_number(pitch)
        note = pretty_midi.Note(velocity=velocity, pitch=note_number, start=start, end=end)
        self.instruments[channel].notes.append(note)

    def export(self):
        self.pm.write(self.filename)

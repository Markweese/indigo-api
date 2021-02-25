import json

class logic_editor_module:
    # Init
    def __init__(self):
        print('init segmentation_module')

    # Update logic
    def update_logic(self, segment_obj):
        with open('data/segments.json', 'r', encoding='utf-8') as segments_file:
            print(segments_file.read())
            segments = json.loads(segments_file.read())

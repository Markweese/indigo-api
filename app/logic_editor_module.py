import json
from datetime import datetime

class logic_editor_module:
    # Init
    def __init__(self):
        print('init segmentation_module')

    # Update logic
    def update_logic(self, segment_obj):
        with open('data/segments.json', 'r', encoding='utf-8') as segments_file:
            segments = json.loads(segments_file.read())

        if any(segment_obj['segment'] == s['name'] for s in segments):
            editing = [s for s in segments if s['name'] == segment_obj['segment']]

            if len(editing) > 0:
                editing = editing[0]

                if segment_obj['eventCategory'] == 'pageView':
                    if 'link' in segment_obj:
                        exact = segment_obj['exact'] if 'exact' in segment_obj else False
                        weight = segment_obj['weight'] if 'weight' in segment_obj else 1

                        insert_obj = {
                            'match': segment_obj['link'],
                            'exact': exact,
                            'weight': weight
                        }

                        if 'urls' not in editing:
                            editing['urls'] = []

                        editing['urls'].append(insert_obj)

                        self.write_json(segments)

                    else:
                        return dict(
                            status=422,
                            message='not all neccesary fields were provided'
                        )
                    
                if segment_obj['eventCategory'] == 'cta':
                    if 'origin' in segment_obj and 'target' in segment_obj and 'name' in segment_obj:
                        insert_obj = {
                            'origin': segment_obj['origin'],
                            'target': segment_obj['target'],
                            'name': segment_obj['name']
                        }

                        if 'cta' not in editing:
                            editing['ctas'] = []

                        editing['ctas'].append(insert_obj)

                        self.write_json(segments)

                    else:
                        return dict(
                            status=422,
                            message='not all neccesary fields were provided'
                        )

                if segment_obj['eventCategory'] == 'recipeSearch':
                    if 'searchTerm' in segment_obj:
                        insert_obj = {
                            'searchTerm': segment_obj['searchTerm']
                        }

                        if 'recipeSearches' not in editing:
                            editing['recipeSearches'] = []

                        editing['recipeSearches'].append(insert_obj)

                        self.write_json(segments)

                    else:
                        return dict(
                            status=422,
                            message='not all neccesary fields were provided'
                        )
                
                if segment_obj['eventCategory'] == 'centerSearch':
                    if 'modality' in segment_obj:
                        insert_obj = {
                            'modality': segment_obj['modality']
                        }

                        if 'centerSearches' not in editing:
                            editing['centerSearches'] = []

                        editing['centerSearches'].append(insert_obj)

                        self.write_json(segments)

    # write_json: write new object to json
    # obj: the entire segment object
    def write_json(self, obj):
        self.backup_json()

        with open('data/segments.json', 'w') as segments_file:
            json.dump(obj, segments_file)

    # backup_json: save the old json version before overwriting
    def backup_json(self):
        today = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'segments-{today}.json'

        with open('data/segments.json', 'r') as segments_file:
            backup = json.loads(segments_file.read())
        
        with open(f'data/{filename}', 'w') as backup_file:
            json.dump(backup, backup_file)

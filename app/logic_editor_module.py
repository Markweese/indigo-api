import json
from datetime import datetime, timedelta

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

                        if 'ctas' not in editing:
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

    # delete_logic: delete a logic object from a segment
    def delete_logic(self, obj):
        with open('data/segments.json', 'r') as segments_file:
            segments = json.loads(segments_file.read())
        
        if any(obj['segment'] == s['name'] for s in segments):
            editing = [s for s in segments if s['name'] == obj['segment']]

            if len(editing) > 0:
                editing = editing[0]

                if obj['eventCategory'] == 'pageView' and 'urls' in editing:
                    editing['urls'] = [v for v in editing['urls'] if v['match'] != obj['link']]

                if obj['eventCategory'] == 'cta' and 'ctas' in editing:
                    editing['ctas'] = [c for c in editing['ctas'] if c['name'] != obj['name'] or c['origin'] != obj['origin'] or c['target'] != obj['target']]

                if obj['eventCategory'] == 'recipeSearch' and 'recipeSearches' in editing:
                    editing['recipeSearches'] = [s for s in editing['recipeSearches'] if s['searchTerm'] != obj['searchTerm']]

                if obj['eventCategory'] == 'centerSearch' and 'centerSearches' in editing:
                    editing['centerSearches'] = [s for s in editing['centerSearches'] if s['modality'] != obj['modality']]

                self.write_json(segments)

    # delete_segment: delete a segment object from segments
    def delete_segment(self, obj):
        with open('data/segments.json', 'r') as segments_file:
            segments = json.loads(segments_file.read())
        
        segments = [s for s in segments if s['name'] != obj['segment']]
        self.write_json(segments)

    # create_segment: create a segment object
    def create_segment(self, obj):
        with open('data/segments.json', 'r') as segments_file:
            segments = json.loads(segments_file.read())
        
        if not any([s for s in segments if s['name'] == obj['segment']]):
            new_segment = {
                "name": obj['segment'],
                "urls": [],
                "ctas": [],
                "recipeSearches": [],
                "centerSearches": []
            }

            segments.append(new_segment)
        
        try:
            self.write_json(segments)
            return new_segment
        except Exception as e:
            print(e)


    # write_json: write new object to json
    # obj: the entire segment object
    def write_json(self, obj):
        self.backup_json()

        with open('data/segments.json', 'w') as segments_file:
            json.dump(obj, segments_file)

    # backup_json: save the old json version before overwriting
    def backup_json(self):
        today = datetime.today().strftime('%Y%m%d%H%M%S')
        filename = f'segments-{today}.json'

        with open('data/segments.json', 'r') as segments_file:
            backup = json.loads(segments_file.read())
        
        with open(f'data/{filename}', 'w') as backup_file:
            json.dump(backup, backup_file)

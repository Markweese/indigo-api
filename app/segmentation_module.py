import json
import pandas

df = pandas.read_csv('app/data/userevents.csv')
df.fillna(0, inplace=True)

class segmentation_module:
    # Init
    def __init__(self):
        print('init segmentation_module')

    # derive_segments
    # return the segment scores for a specific user
    def derive_user_segment(self, id):
        top_segments = {}
        output_object = []

        with open('data/segments.json', 'r', encoding='utf-8') as segments_file:
            segments = json.loads(segments_file.read())

        sel = df[df['UserID'] == id]
        ctas = sel[sel['EventCategory'] == 'cta'].to_dict('records')
        page_views = sel[sel['EventCategory'] == 'pageView'].to_dict('records')
        center_searches = sel[sel['EventCategory'] == 'centerSearch'].to_dict('records')
        recipe_searches = sel[sel['EventCategory'] == 'recipeSearch'].to_dict('records')

        # count page views
        try:
            page_views_matches = [self.get_url_score(s, page_views) for s in segments]

            for m in page_views_matches:
                if m['segment'] in top_segments:
                    top_segments[m['segment']] += m['count']
                elif m['count'] > 0:
                    top_segments[m['segment']] = m['count']
        except Exception as e:
            print(e)

        # count ctas
        try:
            ctas_matches = [self.get_cta_score(s, ctas) for s in segments]

            for m in ctas_matches:
                if m['segment'] in top_segments:
                    top_segments[m['segment']] += m['count']
                elif m['count'] > 0:
                    top_segments[m['segment']] = m['count']
        except Exception as e:
            print(e)

        # count recipe searches
        try:
            recipe_searches_matches = [self.get_recipe_score(s, recipe_searches) for s in segments]

            for m in recipe_searches_matches:
                if m['segment'] in top_segments:
                    top_segments[m['segment']] += m['count']
                elif m['count'] > 0:
                    top_segments[m['segment']] = m['count']
        except Exception as e:
            print(e)

        # count center searches
        try:
            center_searches_matches = [self.get_center_score(s, center_searches) for s in segments]

            for m in center_searches_matches:
                if m['segment'] in top_segments:
                    top_segments[m['segment']] += m['count']
                elif m['count'] > 0:
                    top_segments[m['segment']] = m['count']
        except Exception as e:
            print(e)

        try:
            # Full response object
            output_object.append({
                'user': id,
                'topSegments': top_segments,
            })
        except Exception as e:
                print(e)

        return output_object

    # derive_segments
    # return the segment scores for every user/segment
    def derive_segments(self):
        users = df['UserID'].unique()

        with open('data/segments.json', 'r', encoding='utf-8') as segments_file:
            output_object = []
            segments = json.loads(segments_file.read())

        for user in users:
            top_segments = {}
            sel = df[df['UserID'] == user]
            ctas = sel[sel['EventCategory'] == 'cta'].to_dict('records')
            page_views = sel[sel['EventCategory'] == 'pageView'].to_dict('records')
            center_searches = sel[sel['EventCategory'] == 'centerSearch'].to_dict('records')
            recipe_searches = sel[sel['EventCategory'] == 'recipeSearch'].to_dict('records')

            # count page views
            try:
                page_views_matches = [self.get_url_score(s, page_views) for s in segments]

                for m in page_views_matches:
                    if m['segment'] in top_segments:
                        top_segments[m['segment']] += m['count']
                    elif m['count'] > 0:
                        top_segments[m['segment']] = m['count']
            except Exception as e:
                print(e)

            # count ctas
            try:
                ctas_matches = [self.get_cta_score(s, ctas) for s in segments]

                for m in ctas_matches:
                    if m['segment'] in top_segments:
                        top_segments[m['segment']] += m['count']
                    elif m['count'] > 0:
                        top_segments[m['segment']] = m['count']
            except Exception as e:
                print(e)

            # count recipe searches
            try:
                recipe_searches_matches = [self.get_recipe_score(s, recipe_searches) for s in segments]

                for m in recipe_searches_matches:
                    if m['segment'] in top_segments:
                        top_segments[m['segment']] += m['count']
                    elif m['count'] > 0:
                        top_segments[m['segment']] = m['count']
            except Exception as e:
                print(e)

            # count center searches
            try:
                center_searches_matches = [self.get_center_score(s, center_searches) for s in segments]

                for m in center_searches_matches:
                    if m['segment'] in top_segments:
                        top_segments[m['segment']] += m['count']
                    elif m['count'] > 0:
                        top_segments[m['segment']] = m['count']
            except Exception as e:
                print(e)

            try:
                output_object.append({
                    'user': user,
                    'topSegments': top_segments
                })
            except Exception as e:
                print(e)

        return output_object

    # get_user_events
    # return events
    def get_user_events(self, id):
        # get all user events and sort by event type
        sel = df[df['UserID'] == id]
        ctas = sel[sel['EventCategory'] == 'cta'].to_dict('records')
        page_views = sel[sel['EventCategory'] == 'pageView'].to_dict('records')
        center_searches = sel[sel['EventCategory'] == 'centerSearch'].to_dict('records')
        recipe_searches = sel[sel['EventCategory'] == 'recipeSearch'].to_dict('records')

        with open('data/segments.json', 'r', encoding='utf-8') as segments_file:
            segments = json.loads(segments_file.read())

        # modify each event type group to say which segment each event falls into, if any
        try:
            [self.get_cta_events(s, ctas) for s in segments]
            [self.get_url_events(s, page_views) for s in segments]
            [self.get_center_events(s, center_searches) for s in segments]
            [self.get_recipe_events(s, recipe_searches) for s in segments]
        except Exception as e:
            print(e)

        return {
            'ctas': ctas,
            'pageViews': page_views,
            'centerSearches': center_searches,
            'recipeSearches': recipe_searches
        }

    ## Utility Functions ##

    # get_url_score: count all url matches between user data and segment
    # segment: the segment to match against
    # views: the user views to match against
    def get_url_score(self, segment, views):
        matches = []

        for url in segment['urls']:
            if url['exact'] == False:
                try:
                    matches += [v for v in views if url['match'].lower() in v['Link'].lower()]
                except Exception as e:
                    print(e)
            else:
                try:
                    matches += [v for v in views if url['match'] == v['Link']]
                except Exception as e:
                    print(e)

        return {'segment': segment['name'], 'count': len(matches), 'matches': matches}

    # get_cta_score: count all cta matches between user data and segment
    # segment: the segment to match against
    # ctas: the user ctas to match against
    def get_cta_score(self, segment, ctas):
        matches = []

        for cta in segment['ctas']:
            try:
                matches += [c for c in ctas if cta['target'] in c['Target'] and cta['origin'] in c['Origin'] and str(cta['name']).lower() == str(c['Name']).lower()]
            except Exception as e:
                print(e)

        return {'segment': segment['name'], 'count': len(matches), 'matches': matches}

    # get_recipe_score: count all recipe matches between user data and segment
    # segment: the segment to match against
    # recipes: the user recipes to match against
    def get_recipe_score(self, segment, recipes):
        matches = []

        for recipe in segment['recipeSearches']:
            try:
                matches += [r for r in recipes if recipe['searchTerm'].lower() in str(r['SearchTerm']).lower()]
            except Exception as e:
                print(e)

        return {'segment': segment['name'], 'count': len(matches), 'matches': matches}

    # get_center_score: count all center matches between user data and segment
    # segment: the segment to match against
    # centers: the user centers to match against
    def get_center_score(self, segment, centers):
        matches = []

        for center in segment['centerSearches']:
            try:
                matches += [c for c in centers if int(center['modality']) == int(c['Modality'])]
            except Exception as e:
                print(e)

        return {'segment': segment['name'], 'count': len(matches), 'matches': matches}

    # get_url_events: count all url matches between user data and segment
    # segment: the segment to match against
    # views: the user views to match against
    def get_url_events(self, segment, views):
        for url in segment['urls']:
            if url['exact'] == False:
                try:
                    for v in views:
                        if 'segments' not in v:
                            v['segments'] = []

                        if url['match'].lower() in v['Link'].lower():
                            if not any(s['name'] == segment['name'] for s in v['segments']):
                                v['segments'].append({'name': segment['name'], 'weight': url['weight']})
                except Exception as e:
                    print(e)
            else:
                try:
                    for v in views:
                        if 'segments' not in v:
                            v['segments'] = []

                        if url['match'].lower() == v['Link'].lower():
                            if not any(s['name'] == segment['name'] for s in v['segments']):
                                v['segments'].append({'name': segment['name'], 'weight': url['weight']})
                except Exception as e:
                    print(e)

    # get_cta_events: count all cta matches between user data and segment
    # segment: the segment to match against
    # ctas: the user ctas to match against
    def get_cta_events(self, segment, ctas):
        for cta in segment['ctas']:
            try:
                for c in ctas:
                    if 'segments' not in c:
                        c['segments'] = []

                    if cta['target'] in c['Target'] and cta['origin'] in c['Origin'] and str(cta['name']).lower() == str(c['Name']).lower():
                        if not any(s['name'] == segment['name'] for s in c['segments']):
                            c['segments'].append({'name': segment['name']})

            except Exception as e:
                print(e)

    # get_recipe_events: count all recipe matches between user data and segment
    # segment: the segment to match against
    # recipes: the user recipes to match against
    def get_recipe_events(self, segment, recipes):
        for recipe in segment['recipeSearches']:
            try:
                for r in recipes:
                    if 'segments' not in r:
                        r['segments'] = []

                    if recipe['searchTerm'].lower() in str(r['SearchTerm']).lower():
                        if not any(s['name'] == segment['name'] for s in r['segments']):
                            r['segments'].append({'name': segment['name']})
            except Exception as e:
                print(e)

    # get_center_events: count all center matches between user data and segment
    # segment: the segment to match against
    # centers: the user centers to match against
    def get_center_events(self, segment, centers):
        for center in segment['centerSearches']:
            try:
                for c in centers:
                    if 'segments' not in c:
                        c['segments'] = []

                    if int(center['modality']) == int(c['Modality']):
                        if not any(s['name'] == segment['name'] for s in c['segments']):
                            c['segments'].append({'name': segment['name']})


            except Exception as e:
                print(e)

    # get_usernames: get all usernames
    def get_usernames(self):
        try:
            return list(df['UserID'].unique())
        except Exception as e:
            print(e)

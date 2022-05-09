from rest_framework.renderers import JSONRenderer


class myRenderer(JSONRenderer):


    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''
        
        if "results" in data:
            if "schoolName" in data["results"][0]:
                for i in range(len(data["results"])):
                    data["results"][i] = data["results"][i]["schoolName"]
        
        return super().render(data, accepted_media_type, renderer_context)


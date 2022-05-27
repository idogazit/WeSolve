from rest_framework.renderers import JSONRenderer


class examRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''
        
        for i in range(len(data["results"])):
            examTime = (str(data["results"][i]["year"]) + 
                        data["results"][i]["semester"] + 
                        data["results"][i]["examType"])
            data["results"][i] = {
                "examId" : data["results"][i]["examId"],
                "examTime" : examTime
            }

        
        return super().render(data, accepted_media_type, renderer_context)

class crumbsRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''
        examTime = (str(data["year"]) + 
                    data["semester"] + 
                    data["examType"])
        data["examTime"] = examTime
        del data["year"], data["semester"], data["examType"]
        

        
        return super().render(data, accepted_media_type, renderer_context)

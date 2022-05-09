from rest_framework.renderers import JSONRenderer


class facultyRenderer(JSONRenderer):


    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''
        
        if "results" in data:
            if "facultyName" in data["results"][0]:
                for i in range(len(data["results"])):
                    data["results"][i] = data["results"][i]["facultyName"]
        
        return super().render(data, accepted_media_type, renderer_context)

class SchoolRenderer(JSONRenderer):


    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''
        
        if "results" in data:
            if "schoolName" in data["results"][0]:
                for i in range(len(data["results"])):
                    data["results"][i] = data["results"][i]["schoolName"]
        
        return super().render(data, accepted_media_type, renderer_context)


class CourseRenderer(JSONRenderer):


    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''
        
        if "results" in data:
            if "courseName" in data["results"][0]:
                for i in range(len(data["results"])):
                    data["results"][i] = data["results"][i]["courseName"]
        
        return super().render(data, accepted_media_type, renderer_context)

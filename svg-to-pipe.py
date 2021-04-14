import svg.path as sp
import numpy as np
import json
import time
import subprocess

# Copy the "d" attribute of "path" SVG elements here
# A quick-and-dirty way to extract this from an image:
#  1. open the svg in chrome
#  2. F12 to open console
#  3. run this command: $$('path[d]').map(function(e){return e.getAttribute("d")})
#  4. right-click the output -> copy object
#  5. paste it here

# Data below is: https://www.coffeestainstudios.com/assets/images/coffeestain-logo.svg
path_text = [
    "M92.4,345.7c-6.6,0-10.9,5.7-12.2,11.8l0.6,0.2c1.2-1.2,2.8-1.8,4.4-1.7c2.6,0.2,3.6,2.8,3.5,5.4  c-0.3,6.4-8,16.7-17.4,16.5c-12.9-0.2-4.4-19-1.6-24.9c2.6-5.5,8.1-12.5,8.1-18.9c0-4.7-3.2-8.6-8.1-8.5c-8.4,0.2-16.4,7-21.7,12.9  c0.5-4.7-3.4-8.5-7.8-8.5c-4.4-0.1-8.7,2.8-10.2,6.9c1.9,1.1,2.1,4.5,1.4,8.8c-2.6,7.4-10.1,23.8-18.3,24.2c-8.4,0.4,6.7-28,9.3-31  c-1-2.7-4.5-4.3-7.8-4.4c-2,0-4,0.8-5.4,1.8c-5.4,3.8-11.4,18.9-13.2,26c-2.9,6.7-6.3,14.1-10.3,14.2c-1.5,0.1-2.4-1.5-1.5-5.5  c0.8-4,3.7-9.3,3.6-12.6c-0.1-3.1-2.9-4.7-6-4.7c-5.5,0.1-8.4,7.4-10.8,11.4c-3.2,5.5-8.3,12.4-12.4,12c-9.5-0.9,9.5-33.8,21.2-34.1  c3.7-0.1,2.9,1.5,2.4,5.4c-0.6,3.9,10,0.9,9.9-6.8c0-6.3-6.5-9.5-12.1-9.3c-17.8,0.6-34.7,23.4-40.4,42.1c-2.9,3.8-7.4,7.8-10.8,7.9  c-5.1,0.1-2.6-8.2-1.6-10.7c4.2-10.4,11.4-24.7,19.1-37.1c28.6-7,61.1-9.3,89.9-12.1c16-1.6,38.2-3.1,48.4-17.6  c4.3-6.2,4.9-11.9,4.2-19.1c3.9-3.6,1.8-9.1-2.4-11.5c-9.7-5.5-24.4-2.2-32.7,4c-2.6,1.9-2.1,6-0.8,6.2c4.7-1.3,21.4-5.3,23.8,1.3  c0.9,2.5-0.9,5.8-3.7,8.4c-8,7.4-26.6,12.1-39.8,14.6c-14.4,2.7-50,7.4-78.1,12.9c1.5-1.9,2.9-3.7,4.3-5.3c-0.3-3.6-2.4-6.5-6.1-6.4  c-4,0-6.1,3-8.1,6c-1.7,2.5-3.8,5.7-6.3,9.3c-9.3,2.3-16.5,4.7-20,7.1c-2.7,1.9-4.6,4.9-5.4,8.3c-0.5,2.2,0.3,6.1,2.9,6.2  c3.3-2.8,7.8-5.1,12.8-7.1C-82.7,358-95.7,380.2-96.1,392c-0.2,6.3,2.8,11.7,9.7,11.5c8.5-0.2,18.3-9.5,24.5-17.3  c1.2,5,4.6,8.1,10.4,7.9c10.2-0.3,18-9.6,22.9-17.6c0.5,6.6,2.9,12.3,10,12.3c5.7,0,10-4,13.1-9.2c0.9,1.8,3.2,5.3,8.6,5.4  c6.4,0.2,14.6-6.4,18.5-11.4c0.1,3.2,3.6,6.4,6.9,6.5c4.8,0.1,7.1-3.8,8.7-7.6c2.5-5.9,14.6-32.7,21-33.1c4-0.3,1.3,5.7,0.6,7.7  c-3.3,8.8-10.6,17.4-11.4,29c-0.8,11.1,6.8,17,17.3,17.1c17.3,0.1,37.3-18.9,37.3-36.5C101.9,350.4,98.8,345.7,92.4,345.7z",
    "M120.1,235c-4,5.7-13.2,13.5-20.7,13.9c-10.6,0.5-9.8-11.4-4-17.3c1.1,3,4.2,3.5,7,3.4  c11.9-0.6,27.6-12.9,28.1-25.5c0.2-6.7-4-12-12.2-11.8c-16.5,0.3-32,18.1-39,32.6c-6.2,9.7-15.8,19.2-26.7,19.3  c-7.8,0-9.3-7.8-4.8-13.2c0.7,2.9,3.4,3.8,6.1,3.8c12,0,27.6-13.5,28-25.6c0.2-6-4-10.1-10.6-10.4c-18.3-0.7-40.4,26.7-41.4,44.7  c-0.5,9.2,4.3,15.7,13.8,16.3c9.7,0.5,21.8-7.9,28.9-15.7c0.6,9.8,7.5,14.4,16.5,14.5c12.9,0.1,28.3-9.7,34-24.2  C123.8,237.2,122.8,234.7,120.1,235z M117.7,209c8.8,0.4-4.9,15.7-13.7,15.8C95.1,224.9,111.6,208.8,117.7,209z M69.4,214.9  c1.7-0.1,2.5,0.9,2.5,2.4c-0.1,7.7-17.4,15.8-17.6,11.1C54.1,224.9,64.9,215,69.4,214.9z",
    "M55.3,398.5c-2.1-1.1-8.1-2.7-12.9-2.5c-6.8,0.2-8.2,6-3.2,9.8c7-0.6,13.3,0.3,20,1.3  C60,402.7,58.1,400.1,55.3,398.5z",
    "M43.5,277.3c-0.2-2.6-3.9-4.2-6.3-4.2c-9.2,0.2-16.1,10.2-15.9,19c0.2,5.4,3.5,10,10,10.3  c1.5-0.5,1.4-1.9,1.4-1.9c0.7-6.6,5.5-14.6,9.3-19.8C43.7,278.2,43.5,277.3,43.5,277.3z",
    "M-65,300.4c0.2-5.8-2.5-11-10.1-11.2c-18-0.3-26.4,31.6-30.2,45.6c-12.4,7.8-26.4,12.7-38.8,12.4  c-5.3-0.1-10.3-1.4-12.7-4.7c-2-2.8-2.8-6.8,0.1-9.3c-0.5-1-2.2-1.3-3.6-0.9c-13.1,3.6-14.1,35.1,14.2,34.5  c9.8-0.2,23.1-5.9,36.1-14.3c-10,30.4-31.9,71-61.3,71.2c-12.5,0.1-20.8-8.5-20.9-19.6c-0.2-17.1,19.5-33.9,34.5-21.4l0.9-1  c-0.2-10.9-12.9-14.8-21.9-14.8c-23.8,0.2-41.3,22-41.3,44.6c0,24.1,18.5,39,42.1,38.5c51.1-1.1,72.5-65.9,85.2-110.4  C-81.3,329.4-65.5,312.6-65,300.4z M-74.8,298c3.2,0.3-0.1,6-0.9,7.5c-2.9,5.1-6.8,10.2-11.5,14.9C-84.5,311.9-79.5,297.6-74.8,298z  ",
    "M23.5,396.3c-40.4-1.9-111.1,12-143.8,34.3c-5,3.9-7.8,8.5-7.4,14.9c0.3,4.6,3.5,9.3,7.9,10.5  c35-29.3,92.3-48.1,149.6-50C30.1,400.7,29.3,397,23.5,396.3z",
    "M-150.5,324.7c22.5-0.4,49.4-27.4,60.8-49.5c5.7,8.9,18.9,9.1,29-0.4c7.2-6.7,13.4-16.2,17.3-24.2  c7.5-3.1,12.9-8.3,12.9-8.2c-9.2,11.6-26.7,38.1-26.7,52.8c0,6,2.5,9.6,8.8,9.4c21.8-0.4,37.6-44.6,34.7-62.6c0,0,10.5-2.9,20.8-8.1  c-10.9,16.2-29.8,48.6-29.6,62.6c0.3,21.2,38.4,10.5,41.2-42c0.2-3.4,0.2-6.5,0-9.2c2.6-4.7,10.1-6.8,10.1-6.8  c2.6-7.2,6.1-11.3,6.1-11.3c-3.4-0.3-8.3,1.4-11.4,2.7c0.6-1.5,1.2-2.9,1.9-4.3c18.4-10.8,45.8-38.8,46.2-57  c0.1-5.4-2.2-10.5-8.9-10.6c-15.8-0.2-40.8,47.3-47.8,60.8c-6.5,3.8-16.1,8.3-25,8.9c19-16.8,43.6-44.2,43.6-60.7  c0-5-2.2-9.3-8.6-9.2c-18.6,0.2-40.1,48-48.9,69.4c-2,2.3-7.7,8-15.1,10.6c1.7-9.4,0.9-21.5-11.1-21.2c-6.6,0.2-11.3,5.4-14.1,11  c-14.9,1.9-27.3,20.9-28.3,34.6c-11.2,15.7-30.6,38.2-49.2,37.9c-40.8-0.8,19.9-121,58.4-122c20.7-0.5-4.9,51.8-14.8,52.6  c-1.7-0.1-2.4-1.8-2.5-4.3c-0.2-8.5,5.9-18.6,11.5-24.4c0.4-0.4-0.8-1-0.8-1c-16.2-0.9-33.6,24-34.1,39.9  c-0.2,6.1,2.1,13.9,9.6,13.8c21.9-0.2,53.6-49.7,53.5-70.4c-0.1-12.1-7-19.5-19.8-19.4c-46.3,0.6-97.3,82.2-97.9,124.8  C-178.9,308-171.4,325.1-150.5,324.7z M61.1,167.6c4.5-0.1,0.4,7.4-4.3,14.2c-6.9,10-14,18.7-23.5,25.8  C36.9,199.9,56.1,167.7,61.1,167.6z M-3.2,289c-5.2-0.9,7.2-26.3,15.8-41.9C12.8,255.8,3.2,290.2-3.2,289z M23.4,169  C29,170,7.7,198.6-2,208.7C2.7,198.3,17.5,167.9,23.4,169z M-19.7,247.4c0,0.1,0,0.1,0,0.2c-0.8,8.3-13.1,37.6-18.9,37.9  C-42.8,285.7-27,254.1-19.7,247.4z M-48.1,227.4c3.3,0,2.8,5.7,0.3,11.5c-2.4-0.2-4.5-1.2-4.7-4.3C-52.6,232.1-51,227.5-48.1,227.4z   M-67,241.1c0.7,6.7,4.6,11.1,11.5,11.8c-3.8,5.5-8.8,11-14.3,11.1C-79.1,264-76.3,248.7-67,241.1z"
]
paths = [sp.parse_path(t) for t in path_text]


template = """
                {{
                  "properties": [
                    {{
                      "name": "Location",
                      "type": "StructProperty",
                      "index": 0,
                      "value": {{
                        "type": "Vector",
                        "x": {lx},
                        "y": {ly},
                        "z": {lz}
                      }}
                    }},
                    {{
                      "name": "ArriveTangent",
                      "type": "StructProperty",
                      "index": 0,
                      "value": {{
                        "type": "Vector",
                        "x": {atx},
                        "y": {aty},
                        "z": {atz}
                      }}
                    }},
                    {{
                      "name": "LeaveTangent",
                      "type": "StructProperty",
                      "index": 0,
                      "value": {{
                        "type": "Vector",
                        "x": {ltx},
                        "y": {lty},
                        "z": {ltz}
                      }}
                    }}
                  ]
                }}

"""

class Placer:
    template_path = "pipe_template.json"
    id_names = ["circle_top"]
    def __init__(self, id_offset, x, y, z, color=1):
        with open(self.template_path, "r") as t:
            template_s = t.read()
            ids = {}
            buffer_0_id = None
            for i, id_name in enumerate(self.id_names):
                new_id = id_offset + i
                template_s = template_s.replace("{{"+id_name+"}}", str(new_id))
                if id_name == self.id_names[0]:
                    buffer_0_id = new_id
                    
        self.template_json = json.loads(template_s)
        self.actors = []
        self.components = []
        for actor in self.template_json:
            if actor["type"] == 1:
                actor["transform"]["translation"][0] = x
                actor["transform"]["translation"][1] = y
                actor["transform"]["translation"][2] = z
                # Bind the pipe to a color-gun slot
                actor["entity"]["properties"][3]["value"]["value"] = color
                self.actors.append(actor)
            else:
                self.components.append(actor)
                
    def write_shape_points(self, points, arrive_tangents, leave_tangents):
        for actor in self.actors:
            actor["entity"]["properties"][0]["value"]["values"].clear()
            for c,at,lt in zip(points, arrive_tangents, leave_tangents):
                s = json.loads(template.format(lx=c[0], ly=c[1], lz=c[2], atx=at[0], aty=at[1], atz=at[2], ltx=lt[0], lty=lt[1], ltz=lt[2]))
                actor["entity"]["properties"][0]["value"]["values"].append(s)
    
    def write(self, save_json, debug=False):
        #if debug:
        #    print(json.dumps(self.actors, indent=" "))
        save_json["actors"].extend(self.actors)
        save_json["components"].extend(self.components)


def tangents(points):
    diffs = (points[1:] - points[:-1]) / 2
    leave_tangents = np.append(diffs, np.array([0.,0.,0.]))
    arrive_tangents = np.insert(diffs, 0, np.array([0.,0.,0.]))
    return arrive_tangents.reshape((len(points), 3)), leave_tangents.reshape((len(points), 3))
    

def find_item_id_offset(save_json):
    max_id = None
    for actor in save_json["actors"]:
        if actor["className"] == "/Game/FactoryGame/Buildable/Factory/Pipeline/Build_Pipeline.Build_Pipeline_C":
            actor_id = int(actor["pathName"].split("_")[-1])
            if not max_id or actor_id > max_id:
                max_id = actor_id
    return max_id

# your source save file
# convert to json with https://ficsit-felix.netlify.app/#/ or
# https://github.com/ficsit-felix/satisfactory-json
json_save_path = "debug.json"
with open(json_save_path, 'rb') as f:
    save_json = json.load(f)
    
id_offset = find_item_id_offset(save_json) + 1

# where in the game to spawn
# all pipes have this location, SVG path gives the offset relative to this point
# NOTE: I haven't figured out rotation, the resulting pipes will be oriented
#  due East (you'll be looking at it facing due West)
translation = np.array([-186378.09375, -82377.40625, 24282.08203125])
# scale the image up or down, play with this till it looks good
script_scale = 50.
# how many points per line segment
# higher numbers give smoother lines, but too high and you'll get wrinkles
steps_per_path = 100.
# x,y offset in the SVG coordinate space
# if the SVG paths have a transformation in their own coordinate system you can plug that in here
point_translate = (0.,0.)

for path_hm in paths:
    # paths are composed of segments, spawn one pipe per segment
    # NOTE: you can use the same code to instead spawn one pipe per path, ymmv
    for path in path_hm:
        domain_points = np.arange(0.,1.,1./steps_per_path)
        path_coords = np.array([(0., -path.point(dp).real - point_translate[0], -path.point(dp).imag - point_translate[1]) for dp in domain_points])
        path_coords = path_coords * script_scale
        arrive_tangents, leave_tangents = tangents(path_coords)
        placer = Placer(id_offset, translation[0], translation[1], translation[2])
        placer.write_shape_points(path_coords, arrive_tangents, leave_tangents)
        placer.write(save_json)
        id_offset += 1

# output json save file
json_save_out_path = "debug-curve.json"
with open(json_save_out_path, 'w') as f:
    json.dump(obj=save_json, fp=f)

# convert back to a save with
# https://ficsit-felix.netlify.app/#/ or
# https://github.com/ficsit-felix/satisfactory-json
"""
print(subprocess.run(args=[
    "node", "lib\\cli\\json2sav.js", "debug-curve.json", "debug-curve.sav"],
               check=False, capture_output=True))
 """

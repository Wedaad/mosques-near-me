import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.gis.geos import Point, Polygon
from django.http import JsonResponse
from django.shortcuts import redirect

from .models import UserProfile, Mosques
from .forms import RegisterUserForm
from django.shortcuts import render
import overpy


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("mosques_near_me:menu")
            else:
                redirect("mosques_near_me:home")
        else:
            redirect("mosques_near_me:home")
            return render(request=request, template_name="user_registration/login.html", context={"login_form": form})
    else:
        form = AuthenticationForm()
        return render(request=request, template_name="user_registration/login.html", context={"login_form": form})


# Create your views here.
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            username = request.POST.get('username')
            email = request.POST.get('email')
            new_profile = UserProfile(user=new_user, username=username, email=email)
            new_profile.save()
            return redirect("mosques_near_me:success")
        else:
            return redirect("mosques_near_me:home")
    else:
        form = RegisterUserForm()
    return render(request=request, template_name="user_registration/register.html", context={"signup_form": form})


@login_required
def logout_request(request):
    logout(request)
    return redirect("mosques_near_me:home")


@login_required
def update_location(request):
    current_location = request.POST.get("userlocation", None)
    if not current_location:
        return JsonResponse({"message": "No location found."}, status=400)

    try:
        profile = request.user.userprofile

        if not profile:
            raise ValueError("Can't get user profile")

        coordinates = [float(coordinate) for coordinate in current_location.split(',')]
        profile.user_location = Point(coordinates, srid=4326)
        profile.save()

        update_msg = f'Update current location for {request.user.username} to {coordinates}'

        return JsonResponse({"message": update_msg}, status=200)
    except:
        return JsonResponse({"Error: ": "No Location found"}, status=400)

@login_required
def find_mosque(request):
    try:
        api = overpy.Overpass()
        bounding_box = request.POST.get("bbox", None)
        print("BBOX: ", bounding_box)

        # changing the bounding box to have the correct coords in the right place
        if bounding_box:
            bbox = bounding_box.split(",")

            shuffled_bbox = [bbox[1], bbox[0], bbox[3], bbox[2]]
            mod_boundingbox = [float(item) for item in shuffled_bbox]
            bounding_box = mod_boundingbox
        print(bounding_box)

        # query to find all the mosques within the bounding box of the map
        result = api.query(f"""
        [out:json];
        (
            node["amenity"="place_of_worship"]["religion"="muslim"]{tuple(bounding_box)};
            way["amenity"="place_of_worship"]["religion"="muslim"]{tuple(bounding_box)};
            relation["amenity"="place_of_worship"]["religion"="muslim"]{tuple(bounding_box)};
        );
        out body;
        >;
        out skel qt;
        """)

        # if no mosques are returned
        if len(result.nodes) == 0:
            return JsonResponse({"message": "There are no mosques near your location"})

        print("NODES: ", len(result.nodes))

        geojson_result = {

            "type": "FeatureCollection",
            "features": [],
        }

        nodes_in_way = []

        for way in result.ways:
            geojson_feature = {

                "type": "Feature",
                "id": "",
                "geometry": "",
                "properties": {}
            }

            poly = []
            for node in way.nodes:
                nodes_in_way.append(node.id)
                poly.append([float(node.lon), float(node.lat)])

                try:
                    poly = Polygon(poly)
                except:
                    continue

                geojson_feature["id"] = f"way_{way.id}"
                geojson_feature["geometry"] = json.loads(poly.centroid.geojson)
                geojson_feature["properties"] = {}

                for k, v in way.tags.items():
                    geojson_feature["properties"][k] = v
                    # print(geojson_feature)

                geojson_result["features"].append(geojson_feature) # adding all the information of the mosque to the geojson object

                # looping over all the mosques returned in the query
                for node in result.nodes:
                    if node.id in nodes_in_way:
                        continue

                    geojson_feature = {
                        "type": "Feature",
                        "id": "",
                        "geometry": "",
                        "properties": {}
                    }

                    point = Point([float(node.lon), float(node.lat)])
                    geojson_feature["id"] = f"node_{node.id}"
                    geojson_feature["geometry"] = json.loads(point.geojson)
                    geojson_feature["properties"] = {}
                    for k, v in node.tags.items():
                        geojson_feature["properties"][k] = v

                    geojson_result["features"].append(geojson_feature)

        return JsonResponse(geojson_result, status=200)
    except Exception as e:
        return JsonResponse({"message": f"Error: {e}."}, status=400)


@login_required
def addFavouriteMosque(request):

    try:
        mosque_name = request.POST.get("mosqueName", None)
        mosque_address = request.POST.get("mosqueCity", None)
        latitude = request.POST.get("lat", None)
        longitude = request.POST.get("long", None)
        mosque_coords = [float(latitude), float(longitude)]
        print("Mosque: ", mosque_name)
        user = request.user

        favourite_mosque = Mosques(mosque_name=mosque_name, mosque_goer=user, location=mosque_address)
        favourite_mosque.mosque_map_location = Point(mosque_coords, srid=4326)
        favourite_mosque.save()
        update_msg = f'{mosque_name} has been added to your list of favourite mosques'

        return JsonResponse({"message": update_msg}, status=200)

    except Exception as e:
        return JsonResponse({"Error": f"No mosque found near your area {e}"}, status=400)


# View which retrieves the current users list of favourite mosques
@login_required()
def getFavouriteMosque(request):
    if request.method == "GET":
        favourite_mosque = Mosques.objects.filter(mosque_goer=request.user)
        return render(request=request, template_name="user_profile.html", context={"favourite_mosques": favourite_mosque})

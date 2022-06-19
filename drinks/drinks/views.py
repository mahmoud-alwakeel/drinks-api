from django.http import JsonResponse
from.models import Drink
from .serializers import DrinkSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status

# decorator is something you put above your function to describe it's functionality
@api_view(['GET','POST'])
def drink_list(request, format=None):
# get all drinks , serialize them and return json
    if request.method == 'GET':
        drinks =Drink.objects.all()
        serializer  = DrinkSerializer(drinks, many=True)
        return Response(serializer.data)
        # old return method
        #return JsonResponse({"drinks":serializer.data})

    if request.method == 'POST':
        serializer = DrinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
    
@api_view(['GET','PUT','DELETE'])
def drink_detail(request,id,format=None):

    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
       # this response is not json specific and allows us to see new html view to work with our data 
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DrinkSerializer(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

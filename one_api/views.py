from django.core.paginator import Paginator, EmptyPage

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import *
from utils.one_api_endpoints import *
from utils.helper import Helper

MAX_LIMIT = 50


class CharacterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk=None):
        data = request.query_params
        response = OneApi().get_characters(page=data.get('page'), limit=data.get('limit'))
        return Response(data=response['data'], status=Helper.get_status_code(response['status']))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_favorite_character(request, pk=None):
    user, data = request.user, request.data
    if pk == None:
        return Response(data={"message": "Invalid character id passed", "status": False}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if UserFavoriteCharacter.objects.filter(_id=pk, user=user).exists():
        return Response(data={"message": "You have already added this character as a favorite", "status": False}, status=status.HTTP_409_CONFLICT)
    response_data = OneApi().get_single_character(pk)
    if response_data['status'] != 200:
        return Response(data={"message": "Cannot add this favorite character at the moment", "status": False}, status=status.HTTP_400_BAD_REQUEST)
    character_info = response_data['data']['data']['docs'][0]
    serializer = UserFavoriteCharacterSerializer(data=character_info)
    serializer.is_valid(raise_exception=True)
    serializer.validated_data['user'] = user
    serializer.save()
    return Response(data={"message": "Favorite character saved sucessfully", "status": True, "data": serializer.data}, status=status.HTTP_201_CREATED)


class QuoteView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk=None):
        data = request.query_params
        if pk == None:
            return Response(data={"message": "Invalid character id passed", "status": False}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        response = OneApi().get_qoute(
            character_id=pk, page=data.get('page'), limit=data.get('limit'))
        return Response(data=response['data'], status=Helper.get_status_code(response['status']))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_favorite_quote(request, pk, quote_id):
    user = request.user
    if pk == None or quote_id == None:
        return Response(data={"message": "Invalid character id or quote id given", "status": False}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if UserFavouriteQuote.objects.filter(_id=quote_id, user=user).exists():
        return Response(data={"message": "You have already added this quote as a favorite", "status": False}, status=status.HTTP_409_CONFLICT)
    created_new_character = False
    try:
        character = UserFavoriteCharacter.objects.get(_id=pk, user=user)
    except:
        created_new_character = True
        response_data = OneApi().get_single_character(pk)
        if response_data['status'] != 200:
            return Response(data={"message": "Error occured while trying to fetch character, ensure the id is valid", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        character_info = response_data['data']['data']['docs'][0]
        serializer = UserFavoriteCharacterSerializer(data=character_info)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = user
    qoute_response_data = OneApi().get_single_quote(quote_id)
    if qoute_response_data['status'] != 200:
        return Response(data={"message": "Error occured while trying to fetch quote, ensure the id is valid", "status": False}, status=status.HTTP_400_BAD_REQUEST)
    quote_info = qoute_response_data['data']['data']['docs'][0]
    quote_serializer = UserFavoriteQuoteSerializer(data=quote_info)
    quote_serializer.is_valid(raise_exception=True)
    if created_new_character:
        character = serializer.save()
    quote_serializer.validated_data['user'] = user
    quote = quote_serializer.save()
    character.quotes.add(quote)
    character_serializer = UserFavoriteCharacterSerializer(character)
    return Response(data={"message": "Favorite quote saved sucessfully", "status": True, "data": character_serializer.data}, status=status.HTTP_201_CREATED)


class GetFavorites(APIView):
    serializer_class = UserFavoriteCharacterSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user, data = request.user, request.query_params
        favorite_characters = UserFavoriteCharacter.objects.filter(user=user)
        total_result = favorite_characters.count()
        limit, page = data.get('limit'), data.get('page')
        if limit:
            try:
                limit = int(limit)
            except:
                return Response(data={"message": "Invalid limit sent", "status": False}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        paginator = Paginator(
            favorite_characters, limit if limit and limit <= MAX_LIMIT else LIMIT)
        try:
            favorite_characters = paginator.page(int(page) if page else 1)
        except EmptyPage:
            favorite_characters = []
        except:
            return Response(data={"status": 'error', "message": "Invalid page parameter", "status": False}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serializer = self.serializer_class(favorite_characters, many=True)
        return Response(data={"message": "data retrieved successfully", "count": total_result, "status": True, "data": serializer.data}, status=status.HTTP_200_OK)

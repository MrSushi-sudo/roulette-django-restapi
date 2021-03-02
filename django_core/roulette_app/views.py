from rest_framework import generics, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from .utils import get_spin
from django.db.models import Count, QuerySet


class StartRound(generics.CreateAPIView):
    queryset = Round.objects.all()
    serializer_class = RoundCreateSerializer


class SpinTheRoulette(generics.CreateAPIView):
    queryset = Spin.objects.all()
    serializer_class = SpinSerializer

    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)

        # получаем текущий раунд
        request_data["user"] = request_data["user"]

        user_data = request_data["user"][0]

        current_round = Round.objects.filter(user=user_data).reverse().first()

        # проверем, закончился ли этот раунд
        is_round_finished = current_round.spins_count == 11 or current_round.is_finished

        if is_round_finished:
            new_round = Round(user=user_data)
            new_round.save()

            current_round = new_round

        # получаем все спины из этого раунда
        spins = list(current_round.spins.values())

        spins = [Spin.objects.get(pk=spin['id']).result for spin in spins]

        # получаем спин для раунда
        spin = get_spin(spins)

        # если спин равен 11,
        # то игру надо заканчивать
        is_jackpot = spin == 11

        if is_jackpot:
            current_round.is_finished = True
            current_round.is_jackpot = True
            current_round.save()

        # вписываем это в результат
        request_data["result"] = spin

        request_data = self.serializer_class(data=request_data)
        request_data.is_valid(raise_exception=True)
        request_data.save()

        current_round.spins.add(request_data.data["id"])
        current_round.save()

        return Response(data=request_data.data, status=status.HTTP_201_CREATED)


class EndRound(generics.UpdateAPIView):
    queryset = Round.objects.all()
    serializer_class = RoundUpdateSerializer

    def patch(self, request, *args, **kwargs):
        request_data = dict(request.data)

        # получаем текущий раунд
        request_data["user"] = request_data["user"]

        user_data = request_data["user"][0]

        current_round = Round.objects.filter(user=user_data).reverse().first()

        current_round.is_finished = True
        current_round.save()

        response_data = Round.objects.filter(user=user_data).reverse().values().first()

        return Response(data=response_data, status=status.HTTP_200_OK)


class RoundStatistics(generics.ListAPIView):
    queryset = Round.objects.all()
    serializer_class = RoundDetailSerializer

    def get(self, request, *args, **kwargs):

        def sortFunction(value):
            return value["games"]

        results = list(Round.objects.all().values())

        if not results:
            return Response(data={"Error": "No data"}, status=status.HTTP_200_OK)

        spin_dict = {}
        spin_dict['users'] = []

        for result_ in results:

            if len(spin_dict['users']) == 0:
                spin_dict['users'].append(
                    {
                        'user': result_['user'],
                        'games': 1,
                        'spins': result_['spins_count']
                    }
                )

            else:
                isFound = False
                for iter_ in spin_dict['users']:

                    if iter_['user'] == result_['user']:
                        iter_['games'] += 1
                        iter_['spins'] += result_['spins_count']
                        isFound = True

                if not isFound:
                    spin_dict['users'].append(
                        {
                            'user': result_['user'],
                            'games': 1,
                            'spins': result_['spins_count']
                        }
                    )

        spin_dict = {'users': sorted(spin_dict['users'], key=sortFunction, reverse=True)}

        if 'max_active' in request.GET:

            for user_ in spin_dict['users']:
                user_['avg_spins'] = user_['spins'] // user_['games']

            return Response(data=spin_dict, status=status.HTTP_200_OK)

        max_round = spin_dict['users'][0]['games']

        statistics = {}

        for game_ in range(1, max_round + 1):
            user_list = []
            kol = 0
            for user_ in spin_dict['users']:

                if user_['games'] >= game_:
                    user_list += user_['user']
                    kol += 1

            statistics[game_] = kol

        return Response(data=statistics, status=status.HTTP_200_OK)

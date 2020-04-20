from django.core.management.base import BaseCommand
from django.utils import timezone
import pandas as pd, numpy as np
from sklearn.metrics import r2_score
from main.models import *

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        if True :

            for country in Country.objects.all():
                datapoints = country.datapoint_set.all().order_by("date").values("cases")
                values = pd.DataFrame(list(datapoints))[-30:]
                values["_index"] = np.arange(len(values))

                if not datapoints:continue;

                predictor, accuracy = create_model(values)

                country.predicted = predictor(len(values)+5)
                country.accuracy = accuracy
                country.save()

                print(country.name, country.predicted, country.accuracy )

            
        # except TypeError:
        #     pass
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)


def create_model(data):
                    
    model = np.polyfit(data["_index"], data.cases, 4 )
    predict = np.poly1d(model)

    accuracy = r2_score(data.cases, predict(data["_index"]))

    return predict, accuracy
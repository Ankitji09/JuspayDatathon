from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import matplotlib.pyplot as plt

class APIList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        data = pd.read_csv('Transactions datasheet.csv')

        data['hour'] = data.hr.str.slice(11, )
        data_1 = data[['t', 'success', 'mid']]
        data_group_1 = data_1.groupby(['mid']).sum()
        data_group_1['success_rate'] = data_group_1['success'] * 100 / data_group_1['t']
        all_pgs = data['pg'].unique()
        plots_per_row = 2
        i, j = 0, 0
        fig, axs = plt.subplots(10, plots_per_row, figsize=(40, 50))
        for pg in all_pgs:
            filter = data['pg'] == pg
            data_f_pg = data.where(filter)[['t', 'hour', 'success']].dropna()
            data_pg_grouped_hr = data_f_pg.groupby(['hour'], as_index=False).sum()
            data_pg_grouped_hr['success_rate'] = data_pg_grouped_hr['success'] * 100 / data_pg_grouped_hr['t']
            axs[i][j].plot(data_pg_grouped_hr['hour'], data_pg_grouped_hr['success_rate'])
            axs[i][j].set_ylabel('success_rate')
            axs[i][j].set_xlabel('Time')
            axs[i][j].set_title(pg)
            j += 1
            if j % plots_per_row == 0:
                i += 1
                j = 0
        json_response = axs.toJSON()
        return Response(json_response)

# voter_analytics/views.py
# Name: Rahil Shah
# Email: rshah10@bu.edu
# File contains views for voter_analytics app

from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go

# Create your views here.
class VoterListView(ListView):
    """
    View to display a list of Voter objects.
    """
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100  # Number of voters to display per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = range(1900, 2025)  # Example range of years for filtering
        return context

    def get_queryset(self):
        """
        Override the default queryset to order voters by voter_score descending.
        """
        results = super().get_queryset()

        if 'party' in self.request.GET:
            party = self.request.GET.get('party')
            print(party)
            if party:
                results = results.filter(party_affiliation__istartswith=party.strip())
                print(results)
        if 'min_year' in self.request.GET:
            min_year = self.request.GET.get('min_year')
            if min_year:
                results = results.filter(date_of_birth__year__gte=min_year)
        if 'max_year' in self.request.GET:
            max_year = self.request.GET.get('max_year')
            if max_year:
                results = results.filter(date_of_birth__year__lte=max_year)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET.get('voter_score')
            if voter_score:
                results = results.filter(voter_score=voter_score)
        if 'v20state' in self.request.GET:
            v20state = self.request.GET.get('v20state')
            if v20state == 'on':
                results = results.filter(v20state=True)
        if 'v21town' in self.request.GET:
            v21town = self.request.GET.get('v21town')
            if v21town == 'on':
                results = results.filter(v21town=True)
        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET.get('v21primary')
            if v21primary == 'on':
                results = results.filter(v21primary=True)
        if 'v22general' in self.request.GET:
            v22general = self.request.GET.get('v22general')
            if v22general == 'on':
                results = results.filter(v22general=True)
        if 'v23town' in self.request.GET:
            v23town = self.request.GET.get('v23town')
            if v23town == 'on':
                results = results.filter(v23town=True)

        return results.order_by('-voter_score')

class VoterDetailView(DetailView):
    """
    View to display details of a single Voter object.
    """
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class GraphsView(ListView):
    """
    View to display graphs related to Voter data.
    """
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        """
        Override the default queryset to order voters by voter_score descending.
        """
        results = super().get_queryset()

        if 'party' in self.request.GET:
            party = self.request.GET.get('party')
            if party:
                results = results.filter(party_affiliation__istartswith=party.strip())
        if 'min_year' in self.request.GET:
            min_year = self.request.GET.get('min_year')
            if min_year:
                results = results.filter(date_of_birth__year__gte=min_year)
        if 'max_year' in self.request.GET:
            max_year = self.request.GET.get('max_year')
            if max_year:
                results = results.filter(date_of_birth__year__lte=max_year)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET.get('voter_score')
            if voter_score:
                results = results.filter(voter_score=voter_score)
        if 'v20state' in self.request.GET:
            v20state = self.request.GET.get('v20state')
            if v20state == 'on':
                results = results.filter(v20state=True)
        if 'v21town' in self.request.GET:
            v21town = self.request.GET.get('v21town')
            if v21town == 'on':
                results = results.filter(v21town=True)
        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET.get('v21primary')
            if v21primary == 'on':
                results = results.filter(v21primary=True)
        if 'v22general' in self.request.GET:
            v22general = self.request.GET.get('v22general')
            if v22general == 'on':
                results = results.filter(v22general=True)
        if 'v23town' in self.request.GET:
            v23town = self.request.GET.get('v23town')
            if v23town == 'on':
                results = results.filter(v23town=True)

        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        year_counts = {}
        for voter in voters:
            if voter.date_of_birth:
                year = voter.date_of_birth.year
                year_counts[year] = 1 + year_counts.get(year, 0)
        birth_years = sorted(year_counts.keys())
        counts = [year_counts[year] for year in birth_years]
        context['years'] = birth_years
        bar_fig = go.Bar(x=birth_years, y=counts)
        title_text = 'Distribution of Voters By Birth Year'
        graph_div_years = plotly.offline.plot({"data": [bar_fig],
                                                   "layout_title_text": title_text
                                                   },
                                                   auto_open=False,
                                                   output_type="div")
        context['graph_div_years'] = graph_div_years
        
        party_counts = {}
        for voter in voters:
            party = voter.party_affiliation
            if party:
                party_counts[party] = 1 + party_counts.get(party, 0)

        parties = [party for party in party_counts.keys()]
        values = [party_counts[party] for party in parties]

        pie_fig = go.Pie(labels=parties, values=values)
        title_text = "Voter Distribution By Party"
        graph_div_party = plotly.offline.plot({"data": [pie_fig],
                                               "layout_title_text": title_text},
                                               auto_open=False,
                                               output_type="div")

        context['graph_div_party'] = graph_div_party

        election_counts = {
            'v20state': 0,
            'v21town': 0,
            'v21primary': 0,
            'v22general': 0,
            'v23town': 0,
        }
        for voter in voters:
            if voter.v20state == True:
                election_counts['v20state'] += 1
            if voter.v21town == True:
                election_counts['v21town'] += 1
            if voter.v21primary == True:
                election_counts['v21primary'] += 1
            if voter.v22general == True:
                election_counts['v22general'] += 1
            if voter.v23town == True:
                election_counts['v23town'] += 1

        labels = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        values = [count for count in election_counts.values()]
        
        bar_fig = go.Bar(x=labels, y=values)
        title_text = 'Voter Count By Election'
        graph_div_election = plotly.offline.plot({"data": [bar_fig],
                                                   "layout_title_text": title_text
                                                   },
                                                   auto_open=False,
                                                   output_type="div")
        context['graph_div_election'] = graph_div_election

        return context
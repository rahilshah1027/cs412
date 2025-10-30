# voter_analytics/models.py
# Name: Rahil Shah
# Email: rshah10@bu.edu
# File contains models for voter_analytics app

from django.db import models

# Create your models here.
class Voter(models.Model):
    """
    Model representing a voter with various attributes.
    last_name: Voter's last name.
    first_name: Voter's first name.
    address_street_number: Street number of the voter's address.
    address_street_name: Street name of the voter's address.
    address_apt_number: Apartment number of the voter's address.
    address_zip_code: ZIP code of the voter's address.
    date_of_birth: Voter's date of birth.
    date_of_registration: Date when the voter registered.
    party_affiliation: Voter's political party affiliation.
    precinct_number: Precinct number where the voter is registered.
    v20state: Boolean indicating if the voter participated in the 2020 state election.
    v21town: Boolean indicating if the voter participated in the 2021 town election.
    v21primary: Boolean indicating if the voter participated in the 2021 primary election.
    v22general: Boolean indicating if the voter participated in the 2022 general election.
    v23town: Boolean indicating if the voter participated in the 2023 town election.
    voter_score: Interger indicating how many of the past 5 elections the voter participated in.
    """

    # Voter information fields
    last_name = models.CharField()
    first_name = models.CharField()
    address_street_number = models.CharField(blank=True, null=True)
    address_street_name = models.CharField()
    address_apt_number = models.CharField(blank=True, null=True)
    address_zip_code = models.CharField()
    date_of_birth = models.DateField(blank=True, null=True)

    # Voter political information fields
    date_of_registration = models.DateField(blank=True, null=True)
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField()

    # Voter participation fields
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}, Voter Score: {self.voter_score}'
 
def load_data():
    """ 
    Function to load data into the Voter model.
    """

    Voter.objects.all().delete()
    
    filename = '/Users/rahilshah/Desktop/newton_voters.csv'
    f = open(filename, 'r')

    f.readline()  # Skip the header line

    for line in f:
        try:
            fields = line.strip().split(',')

            voter = Voter(last_name = fields[1],
                            first_name = fields[2],
                            address_street_number = fields[3],
                            address_street_name = fields[4],
                            address_apt_number = fields[5],
                            address_zip_code = fields[6],
                            date_of_birth = fields[7],
                            date_of_registration = fields[8],
                            party_affiliation = fields[9],
                            precinct_number = fields[10],
                            v20state = True if fields[11] == "TRUE" else False,
                            v21town = True if fields[12] == "TRUE" else False,
                            v21primary = True if fields[13] == "TRUE" else False,
                            v22general = True if fields[14] == "TRUE" else False,
                            v23town = True if fields[15] == "TRUE" else False,
                            voter_score = fields[16],
                        )
            voter.save()
            # print(f'Created result: {voter}')
        except Exception as e:
            print("Something went wrong!")
            print(f"line={line}")
            print("Error details:", e)

    print(f"Done! Created {len(Voter.objects.all())} voters")
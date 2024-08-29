import pandas as pd
from django.core.management.base import BaseCommand
from store.models import Book
from sqlalchemy import create_engine
from django.conf import settings
from django.db import transaction

class Command(BaseCommand):
    help = "A command to add data from a CSV file to the Book model in the database"

    def handle(self, *args, **options):
        excel_file = 'book.csv'

        try:
            # Start a database transaction
            with transaction.atomic():
                # Read the CSV file into a DataFrame
                df = pd.read_csv(excel_file)

                # Iterate through DataFrame rows and create Book instances
                for _, row in df.iterrows():
                    Book.objects.create(
                        title=row['title'],
                        # Add other fields as needed
                    )

            self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV to the database'))

        except Exception as e:
            # Handle exceptions, e.g., if the CSV file is not found or if there's a problem with the data
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
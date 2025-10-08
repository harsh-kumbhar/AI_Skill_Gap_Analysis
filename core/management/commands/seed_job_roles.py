from django.core.management.base import BaseCommand
import csv, ast
from core.models import DreamRole, Skill
from django.db import transaction

class Command(BaseCommand):
    help = "Seed DreamRole and Skill data from CSV file"

    def handle(self, *args, **kwargs):
        file_path = "core\data\job_roles.csv"

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                with transaction.atomic():
                    for row in reader:
                        role_name = row["job_title"].strip()
                        skill_list = ast.literal_eval(row["job_skill_set"])

                        role, _ = DreamRole.objects.get_or_create(name=role_name)

                        for skill_name in skill_list:
                            skill_name = skill_name.strip()
                            skill_obj, _ = Skill.objects.get_or_create(name=skill_name)
                            role.skills.add(skill_obj)

            self.stdout.write(self.style.SUCCESS("✅ Roles and skills imported successfully!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))

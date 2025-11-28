from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Create sample materials"

    def handle(self, *args, **options):
        try:
            from construction.models import Material
        except Exception as exc:
            self.stderr.write("Could not import Material model: %s" % exc)
            return

        # optional Supplier model
        Supplier = None
        try:
            from construction.models import Supplier
            Supplier = Supplier
        except Exception:
            Supplier = None

        # sample rows
        samples = [
            {"name": "Cement (50kg bag)", "unit_price": "8.50", "stock": 120, "supplier": "Acme Supplies"},
            {"name": "River Sand (m3)", "unit_price": "25.00", "stock": 50, "supplier": "SandCo"},
            {"name": "Steel Rebar (10mm)", "unit_price": "2.30", "stock": 2000, "supplier": "SteelWorks"},
            {"name": "Bricks (per 1000)", "unit_price": "450.00", "stock": 30, "supplier": "BrickMakers"},
            {"name": "Paint (20L)", "unit_price": "75.00", "stock": 40, "supplier": "ColorHub"},
            {"name": "Timber (m3)", "unit_price": "150.00", "stock": 15, "supplier": "ForestPro"},
        ]

        for s in samples:
            # Use 'name' as lookup key, remove it from defaults
            lookup = {'name': s.get('name')}
            defaults = {k: v for k, v in s.items() if k != 'name'}

            # Ensure numeric quantity is never None to avoid NOT NULL DB errors
            if defaults.get('quantity') is None:
                defaults['quantity'] = 0

            # Fill simple sensible defaults for other non-nullable fields when missing.
            # Inspect Material model fields and set basic defaults for common types.
            try:
                from construction.models import Material
                for field in Material._meta.fields:
                    fname = field.name
                    if fname in lookup or fname in defaults or field.auto_created or field.primary_key:
                        continue
                    # Only attempt simple defaults for fields declared not nullable and without a model default
                    if not field.null and not field.has_default():
                        internal = field.get_internal_type()
                        if internal in ("CharField", "TextField"):
                            defaults.setdefault(fname, "")
                        elif internal in ("IntegerField", "BigIntegerField", "SmallIntegerField",
                                          "PositiveIntegerField", "PositiveSmallIntegerField",
                                          "FloatField", "DecimalField"):
                            defaults.setdefault(fname, 0)
                        elif internal == "BooleanField":
                            defaults.setdefault(fname, False)
                        # Skip complex/date/foreign key fields to avoid incorrect values

            except Exception:
                # If introspection fails, still proceed with the required 'quantity' fallback
                pass

            try:
                obj, created_flag = Material.objects.update_or_create(
                    **lookup,
                    defaults=defaults
                )
                action = "Created" if created_flag else "Updated"
                self.stdout.write(f"{action} material: {obj.name}")
            except IntegrityError as e:
                # Log details and continue creating other samples
                logger.error("Failed to create/update material %s: %s\ndefaults=%r", lookup.get('name'), e, defaults)
                self.stderr.write(f"ERROR: Failed to create/update material '{lookup.get('name')}': {e}")
                continue

        self.stdout.write(self.style.SUCCESS(f"Sample materials created/updated: created={created}, updated={updated}"))
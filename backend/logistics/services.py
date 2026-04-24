import abc
import random
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from .models import Carrier, Shipment, TrackingEvent, PricingZone, PricingRule

class CarrierStrategy(abc.ABC):
    @abc.abstractmethod
    def create_shipment(self, shipment: Shipment):
        pass

    @abc.abstractmethod
    def get_tracking_status(self, tracking_number: str):
        pass

    @abc.abstractmethod
    def calculate_rate(self, origin, destination, weight):
        pass

class G4SCarrier(CarrierStrategy):
    def create_shipment(self, shipment: Shipment):
        return {
            "external_id": f"G4S-{shipment.tracking_number}", 
            "status": "ACCEPTED",
            "tracking_url": f"https://g4s-logistics.ke/track/{shipment.tracking_number}"
        }

    def get_tracking_status(self, tracking_number: str):
        # Simulate movement towards Mombasa
        base_lat = -1.2921 # Nairobi
        base_lng = 36.8219
        offset = random.uniform(0.01, 0.05)
        
        return {
            "status": "IN_TRANSIT", 
            "location": "Mombasa Road, Athi River",
            "lat": base_lat - offset,
            "lng": base_lng + offset,
            "timestamp": timezone.now().isoformat()
        }

    def calculate_rate(self, origin, destination, weight):
        return Decimal(500) + (Decimal(weight) * Decimal(50))

class DHLCarrier(CarrierStrategy):
    def create_shipment(self, shipment: Shipment):
        return {
            "external_id": f"DHL-{shipment.tracking_number}", 
            "status": "SCHEDULED",
            "tracking_url": f"https://dhl.com/track/{shipment.tracking_number}"
        }

    def get_tracking_status(self, tracking_number: str):
        return {
            "status": "OUT_FOR_DELIVERY", 
            "location": "Nyali Distribution Center",
            "lat": -4.0435,
            "lng": 39.6682,
            "timestamp": timezone.now().isoformat()
        }

    def calculate_rate(self, origin, destination, weight):
        return Decimal(1200) + (Decimal(weight) * Decimal(150)) # Premium

class SendyCarrier(CarrierStrategy):
    def create_shipment(self, shipment: Shipment):
        return {
            "external_id": f"SENDY-{shipment.tracking_number}", 
            "status": "DISPATCHING",
            "driver_name": "John Doe",
            "driver_phone": "+254700000000"
        }

    def get_tracking_status(self, tracking_number: str):
        return {
            "status": "PICKED_UP", 
            "location": "Industrial Area, Nairobi",
            "lat": -1.3005,
            "lng": 36.8400,
            "timestamp": timezone.now().isoformat()
        }

    def calculate_rate(self, origin, destination, weight):
        return Decimal(300) + (Decimal(weight) * Decimal(20)) # Economy

class LogisticsService:
    _strategies = {
        "G4S": G4SCarrier(),
        "DHL": DHLCarrier(),
        "SENDY": SendyCarrier(),
    }

    @classmethod
    def get_strategy(cls, carrier_code: str) -> CarrierStrategy:
        return cls._strategies.get(carrier_code, G4SCarrier()) # Default to G4S

    @classmethod
    def calculate_cost(cls, zone_id: int, weight: float, volume: float = 0) -> dict:
        try:
            zone = PricingZone.objects.get(id=zone_id)
            
            # Simple fallback calculation based on the first active rule
            rule = zone.rules.filter(is_active=True).first()
            if rule:
                base_cost = rule.base_cost + (rule.per_kg_cost * Decimal(weight))
            else:
                base_cost = Decimal(500) # Fallback if no rules
            
            # Compare Carrier Rates (Mock)
            quotes = []
            for code, strategy in cls._strategies.items():
                rate = strategy.calculate_rate("Nairobi", zone.name, weight)
                quotes.append({
                    "carrier": code,
                    "price": float(base_cost + rate), # Add zone markup
                    "service_level": "Standard" if code != "DHL" else "Express"
                })
                
            return {
                "zone": zone.name,
                "base_cost": float(base_cost),
                "quotes": quotes
            }
        except PricingZone.DoesNotExist:
            return {"error": "Zone not found", "quotes": []}

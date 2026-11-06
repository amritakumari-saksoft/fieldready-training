import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "policies"

documents = {
    "01_delivery_times": (
        "Standard parcels are delivered within 3 to 5 business days. "
        "Express parcels are delivered within 1 to 2 business days."
    ),
    "02_delayed_parcels": (
        "A parcel is considered delayed when its expected delivery date "
        "has passed. Customers should contact support after 2 additional "
        "business days."
    ),
    "03_tracking": (
        "Customers can track parcels using their tracking number. "
        "Tracking information is updated when parcels reach scanning "
        "checkpoints."
    ),
    "04_damaged_parcels": (
        "Customers must report damaged parcels within 48 hours of "
        "delivery and provide photographs of the damaged package."
    ),
    "05_lost_parcels": (
        "A parcel may be declared lost after 10 business days without "
        "tracking updates. Support must investigate before confirming loss."
    ),
    "06_refunds": (
        "Refunds for approved lost or damaged parcel claims are processed within 7 business days."
    ),
    "07_delivery_attempts": (
        "Couriers attempt delivery twice before returning the parcel to the local depot."
    ),
    "08_address_changes": (
        "Delivery addresses may be changed before the parcel is dispatched. "
        "Address changes after dispatch are not guaranteed."
    ),
    "09_cancellations": (
        "Customers may cancel a shipment before dispatch. "
        "Once dispatched, cancellation requests require support review."
    ),
    "10_returns": (
        "Eligible parcels may be returned within 14 days of delivery, "
        "subject to the sender's return policy."
    ),
    "11_proof_of_delivery": (
        "Proof of delivery may include a recipient signature, "
        "delivery photograph, or courier confirmation."
    ),
    "12_customer_complaints": (
        "Customer complaints receive a reference number. "
        "Support aims to provide an initial response within 24 hours."
    ),
    "13_weather_delays": (
        "Severe weather may delay parcel delivery. "
        "Customers should check tracking updates for revised delivery "
        "estimates."
    ),
    "14_international_shipping": (
        "International parcels may be delayed by customs inspection. "
        "Customs clearance times vary by destination."
    ),
    "15_prohibited_items": (
        "Hazardous materials, illegal goods, and other restricted items "
        "cannot be shipped through the parcel service."
    ),
    "16_insurance": (
        "Optional shipment insurance may cover eligible loss or damage "
        "up to the declared insured value."
    ),
    "17_weight_limits": (
        "Standard parcels must not exceed 25 kilograms. "
        "Oversized or overweight shipments require special handling."
    ),
    "18_pickup_requests": (
        "Customers may schedule parcel pickup at least one business day "
        "in advance, subject to availability."
    ),
    "19_failed_delivery": (
        "If delivery fails because the recipient is unavailable, "
        "the courier may leave instructions for redelivery."
    ),
    "20_escalations": (
        "Unresolved delivery complaints may be escalated to a supervisor "
        "after 48 hours without a satisfactory resolution."
    ),
}


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for name, content in documents.items():
        file_path = OUTPUT_DIR / f"{name}.txt"
        file_path.write_text(content, encoding="utf-8")

    logger.info(
        "Created %d synthetic policy documents.",
        len(documents),
    )


if __name__ == "__main__":
    main()

from app.schemas.fruit_reception_schema import FruitReceptionSchema
from app.schemas.in_out_precooling_schema import InOutPrecoolingSchema
from app.schemas.client_schema import ClientSchema
from app.schemas.shipping_manifest_schema import ShippingManifestSchema

# Register schemas to avoid lazy-loading resolution errors
__all__ = [
    "FruitReceptionSchema",
    "InOutPrecoolingSchema",
    "ClientSchema"
]

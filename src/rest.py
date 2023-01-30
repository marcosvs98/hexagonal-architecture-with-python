from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from settings import ACCEPT_PARALLEL_REQUESTS, CACHE_SILENT_MODE
from adapters.middlewares_adapter import PreventDuplicatesMiddleware
from adapters.redis_adapter import RedisAdapter

from exceptions import CommonException
from schemas.order import HealthCheck

from domain.order.controllers.order_controller import OrderController
from domain.order.repository.order_repository import OrderRepository
from domain.order.repository.mongo_order_repository import MongoOrderDatabaseRepository
from domain.order.services.order_service import OrderService

from domain.payment.adapters.paypal_adapter import PayPalPaymentAdapter
from domain.product.adapters.product_adapter import ProductAdapter
from domain.delivery.adapters.cost_calculator_adapter import DeliveryCostCalculatorAdapter
from domain.maps.adapters.google_maps_adapter import GoogleMapsAdapter
from domain.order.adapters.order_event_publisher_adapter import OrderEventPublisher

import event_handler
from settings import MongoDatabaseSettings
from functools import partial


def init_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if not ACCEPT_PARALLEL_REQUESTS:
        app.add_middleware(
            PreventDuplicatesMiddleware,
            cache=RedisAdapter(silent_mode=CACHE_SILENT_MODE)
        )


def init_routes(app: FastAPI):
    @app.get('/', status_code=200, response_model=HealthCheck)
    async def health_check():
        return {'status': 200}

    app.state.event_source_config = MongoDatabaseSettings()
    app.add_event_handler(
        'startup', func=partial(event_handler.startup, app=app)
    )
    app.add_event_handler(
        'shutdown', func=partial(event_handler.shutdown, app=app)
    )

    app.include_router(
        OrderController(
            OrderService(
                repository=MongoOrderDatabaseRepository(),
                payment_service=PayPalPaymentAdapter(),
                product_service=ProductAdapter(),
                delivery_service=DeliveryCostCalculatorAdapter(
                    maps_service=GoogleMapsAdapter()
                ),
                event_publisher=OrderEventPublisher()
            )
        ).router,
        tags=["order"],
        prefix="/api/v1/order"
    )

    @app.exception_handler(CommonException)
    async def service_exception_handler(request: Request, error: CommonException):
        return JSONResponse(error.to_dict(), status_code=error.code)
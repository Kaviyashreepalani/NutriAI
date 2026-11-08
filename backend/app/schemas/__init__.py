from app.schemas.common import APIResponse, PaginatedResponse, SuccessMessage, ErrorEnvelope
from app.schemas.auth import SessionRequest, UserSessionResponse, RegisterProfileRequest, GuardianConsentRequest
from app.schemas.profile import (
    UserProfileUpdate, MeasurementCreate, MeasurementResponse, DietaryPreferenceUpdate,
    AllergyItem, AllergiesUpdate, HealthInfoUpdate, FullProfileResponse
)
from app.schemas.report import (
    ExtractedResultResponse, ExtractedResultCorrection, BatchCorrectionsRequest,
    ReportSummaryResponse, ReportDetailResponse
)
from app.schemas.assessment import AssessmentCreateRequest, AssessmentResponse, FindingItem, SafetyMessage
from app.schemas.formulation import (
    FormulationGenerateRequest, FormulationIngredientItem, WhySelectedReason,
    FormulationResponse, RecommendationDetailResponse, CompareFormulationsResponse
)
from app.schemas.commerce import (
    AddToCartRequest, UpdateCartItemRequest, CartItemResponse, CartResponse,
    ShippingAddress, CheckoutRequest, OrderStatusEventResponse, OrderItemResponse, OrderResponse
)
from app.schemas.progress import (
    PlanCreateRequest, DailyLogCreateRequest, ConsumptionPlanResponse,
    ProgressOverviewResponse, LabComparisonPoint, LabComparisonResponse, ReminderUpdate
)
from app.schemas.chat import (
    ChatSessionCreate, ChatMessageCreate, ChatMessageResponse, ChatSessionResponse,
    STTResponse, TTSRequest
)
from app.schemas.admin import IngredientCreateUpdate, StatisticVerifyRequest, OrderStatusUpdateRequest


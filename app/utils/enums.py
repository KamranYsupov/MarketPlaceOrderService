import enum


class OrderStatus(enum.Enum):
    IN_PROGRESS = 'IN_PROGRESS'
    SENT = 'SENT'
    DELIVERED = 'DELIVERED'
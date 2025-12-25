from dataclasses import dataclass
from typing import Annotated, Literal

import tiktoken
from loguru import logger

type SupportedModels = Annotated[Literal["model1"], "Supported Models"]
type PriceTable = Annotated[
    dict[SupportedModels, float], "Price table fro supported models"
]

price_table: PriceTable = {"anthropic.claude-3-5-sonnet-20241022-v2:0": 0.05}


@dataclass
class Message:
    prompt: str
    response: str | None
    model: SupportedModels


@dataclass
class MessageCostReport:
    req_cost: float
    res_cost: float
    total_cost: float


def count_tokens(text: str | None):
    if text is None:
        logger.warning("Response is None, Assuming 0 tokens used")
        return 0
    encoding_model = tiktoken.encoding_for_model("gpt-4o")
    output = encoding_model.encode(text)
    return len(output)


def calculate_usage_cost(message: Message) -> MessageCostReport:
    if message.model not in price_table:
        raise ValueError(f"cost calculation is not supported by {model} model")
    price = price_table[message.model]
    req_costs = price * count_tokens(message.prompt)
    res_costs = price * count_tokens(message.response)
    total_costs = req_costs + res_costs
    return MessageCostReport(
        req_cost=req_costs, res_cost=res_costs, total_cost=total_costs
    )
